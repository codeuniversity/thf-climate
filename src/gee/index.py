from datetime import datetime
from typing import Union

import ee

from src.gee.auth import authenticate

DAY_FEATURE_LABEL = "DAY_ONLY"


def get_preprocessed_imagery(
    coordinates: list, start_date: datetime, end_date: datetime
) -> ee.ImageCollection:
    authenticate()

    aoi = ee.Geometry.Polygon(coordinates)

    # Get imagery
    image_collection = get_imagery(aoi, start_date, end_date)

    # Preprocess the imagery
    mosaicked_collection = get_mosaicked_by_date_collection(image_collection)
    clipped_collection = mosaicked_collection.map(lambda img: img.clip(aoi))
    cloud_masked_collection = clipped_collection.map(lambda img: get_cloud_masked(img))

    return cloud_masked_collection


def get_cloud_masked(image: ee.Image) -> ee.Image:
    """Applies cloud and shadow masks to a single image."""
    # Get cloud and shadow masks
    cloud_mask = get_cloud_vector_mask(image)
    cloud_shadow_mask = get_cloud_shadow_vector_mask(image)

    # Combine the cloud and shadow masks using logical OR
    combined_mask = cloud_mask.Or(cloud_shadow_mask)

    # Apply the combined mask to the image to mask out clouds and shadows
    return image.updateMask(combined_mask.Not())


def get_cloud_vector_mask(image: ee.Image) -> ee.Image:
    scl = image.select("SCL")
    # Create a mask for classes 10, 9, and 8 (cloud, cirrus, and high probability cloud)
    cloud_mask = scl.eq(10).Or(scl.eq(9)).Or(scl.eq(8))
    return cloud_mask


def get_cloud_shadow_vector_mask(image: ee.Image) -> ee.Image:
    scl = image.select("SCL")
    # Create a mask for cloud shadows (class 3)
    cloud_shadow_mask = scl.eq(3)
    return cloud_shadow_mask


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
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate(start_date_str, end_date_str)
        .filterBounds(aoi)
        .filter(ee.Filter.contains(".geo", aoi))
        .filter(ee.Filter.lte("CLOUDY_PIXEL_PERCENTAGE", 95))
    )
    return collection


def get_mosaicked_by_date_collection(image_collection):
    # Add date strings as a property on each image
    image_collection = image_collection.map(
        lambda img: img.set(DAY_FEATURE_LABEL, img.date().format("YYYY-MM-dd"))
    )
    # Get unique dates
    dates = image_collection.aggregate_array(DAY_FEATURE_LABEL).distinct()

    # Function to mosaic images by date
    def mosaic_by_date(date_str):
        date_str = ee.String(date_str)
        mosaicked_image = (
            image_collection.filter(ee.Filter.eq(DAY_FEATURE_LABEL, date_str))
            .mosaic()
            .set("system:time_start", ee.Date(date_str).millis())
            .set(DAY_FEATURE_LABEL, date_str)
        )
        return mosaicked_image

    # Apply mosaic by date and create a new collection
    return ee.ImageCollection(dates.map(mosaic_by_date))
