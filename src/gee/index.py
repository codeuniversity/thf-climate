from datetime import datetime
from typing import Union

import ee

from src.gee.auth import authenticate


def get_preprocessed_imagery(
    coordinates: ee.Geometry, start_date: datetime, end_date: datetime
) -> list:
    authenticate()

    aoi = ee.Geometry.Polygon(coordinates)
    # area_m2 = aoi.area().getInfo()

    # Get imagery collection
    image_collection = get_imagery(aoi, start_date, end_date)
    image_list = image_collection.toList(image_collection.size())

    # List to hold masked images
    masked_images = []

    # Loop through the collection in Python
    for i in range(image_list.size().getInfo()):
        image = ee.Image(image_list.get(i))

        # Get cloud and shadow masks
        cloud_mask = get_cloud_vector_mask(image, aoi)
        cloud_shadow_mask = get_cloud_shadow_vector_mask(image, aoi)

        # Combine the cloud and shadow masks using logical OR
        combined_mask = cloud_mask.Or(cloud_shadow_mask)

        # Apply the combined mask to the image to mask out clouds and shadows
        masked_image = image.updateMask(combined_mask.Not())

        # Add the masked image reference to the list
        masked_images.append(masked_image)

    return masked_images


def get_cloud_vector_mask(image: ee.Image, aoi: ee.Geometry.Polygon) -> ee.Image:
    clipped_image = image.clip(aoi)
    scl = clipped_image.select("SCL")
    # Create a mask for classes 10, 9, and 8 (could add 7 as needed)
    cloud_mask = scl.eq(10).Or(scl.eq(9)).Or(scl.eq(8))
    return cloud_mask


def get_cloud_shadow_vector_mask(image: ee.Image, aoi: ee.Geometry.Polygon) -> ee.Image:
    clipped_image = image.clip(aoi)
    scl = clipped_image.select("SCL")
    # Create a mask for cloud shadows (class 3)
    cloud_shadow_mask = scl.eq(3)
    return cloud_shadow_mask


def calculate_masked_area(mask: ee.Image, aoi: ee.Geometry, scale: int = 10) -> float:
    # Calculate the area of masked pixels by multiplying by pixel area
    masked_area = (
        mask.multiply(ee.Image.pixelArea())
        .rename("area")  # Rename the band to "area" for clarity
        .reduceRegion(
            reducer=ee.Reducer.sum(), geometry=aoi, scale=scale, maxPixels=1e8
        )
        .get("area")  # Access the renamed key
        .getInfo()
    )

    return masked_area


def get_imagery(
    aoi: ee.Geometry.Polygon,
    start_date: Union[datetime, str],
    end_date: Union[datetime, str],
) -> ee.ImageCollection:
    # Convert dates to strings for Earth Engine if they are datetime objects
    # TODO: check that timerange is not outside of allowed range for HARMONIZED collection
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    collection = (
        # ee.ImageCollection('COPERNICUS/S2')
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate(start_date_str, end_date_str)
        .filterBounds(aoi)
    )
    return collection
