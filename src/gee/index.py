from datetime import datetime
from typing import Union

import ee

from src.gee.auth import authenticate


def get_preprocessed_imagery(
    coordinates: ee.Geometry, start_date: datetime, end_date: datetime
) -> ee.ImageCollection:
    authenticate()

    aoi = ee.Geometry.Polygon(coordinates)
    # Get imagery collection
    image_collection = get_imagery(aoi, start_date, end_date)
    print("============= Original Collection =============")
    print_image_collection_info(image_collection)

    # Use the function
    mosaicked_collection = get_mosaicked_by_date_collection(image_collection)
    print("============= Mosaicked Collection =============")
    print_image_collection_info(mosaicked_collection)
    # Apply masking to each image in the collection
    masked_collection = mosaicked_collection.map(lambda image: mask_image(image, aoi))

    return masked_collection


def mask_image(image: ee.Image, aoi: ee.Geometry) -> ee.Image:
    """Applies cloud and shadow masks to a single image."""
    # Get cloud and shadow masks
    cloud_mask = get_cloud_vector_mask(image, aoi)
    cloud_shadow_mask = get_cloud_shadow_vector_mask(image, aoi)

    # Combine the cloud and shadow masks using logical OR
    combined_mask = cloud_mask.Or(cloud_shadow_mask)

    # Apply the combined mask to the image to mask out clouds and shadows
    return image.updateMask(combined_mask.Not())


def get_cloud_vector_mask(image: ee.Image, aoi: ee.Geometry.Polygon) -> ee.Image:
    clipped_image = image.clip(aoi)
    scl = clipped_image.select("SCL")
    # Create a mask for classes 10, 9, and 8 (cloud, cirrus, and high probability cloud)
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
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate(start_date_str, end_date_str)
        .filterBounds(aoi)
        .filter(ee.Filter.contains(".geo", aoi))
        .filter(ee.Filter.lte("CLOUDY_PIXEL_PERCENTAGE", 95))
    )
    print(f"collection size right after creation{collection.size().getInfo()}")
    return collection


# Function to print detailed information of each image in an ImageCollection
def print_image_collection_info(image_collection: ee.ImageCollection):
    # Convert the ImageCollection to a list
    image_list = image_collection.toList(image_collection.size())

    # Get the number of images in the collection
    num_images = image_collection.size().getInfo()

    print(f"Total number of images in collection: {num_images}\n")

    # Loop through the images (limited to the first 10 images for performance reasons)
    for i in range(
        min(num_images, 10)
    ):  # Adjust the limit as needed, 10 is used here for simplicity
        image = ee.Image(image_list.get(i))
        image_info = image.getInfo()

        # Extract and print relevant details
        image_id = image_info.get("id", "N/A")
        acquisition_time = image_info.get("properties", {}).get(
            "system:time_start", "N/A"
        )
        cloud_coverage = image_info.get("properties", {}).get(
            "CLOUDY_PIXEL_PERCENTAGE", "N/A"
        )

        if acquisition_time != "N/A":
            acquisition_time = datetime.utcfromtimestamp(acquisition_time / 1000)

        print(f"Image ID: {image_id}")
        print(f"Acquisition Time (UTC): {acquisition_time}")
        print(f"Cloud Coverage (%): {cloud_coverage}\n")


def get_mosaicked_by_date_collection(image_collection):
    def add_date(image):
        date_str = image.date().format("YYYY-MM-dd")
        return image.set("date", date_str)

    image_collection = image_collection.map(add_date)
    dates = image_collection.aggregate_array("date").distinct()

    def mosaic_by_date(date_str):
        date_str = ee.String(date_str)
        images = image_collection.filter(ee.Filter.eq("date", date_str))
        mosaicked_image = images.mosaic().set(
            "system:time_start", ee.Date(date_str).millis()
        )
        return mosaicked_image.set("date", date_str)

    mosaicked_images = ee.ImageCollection(dates.map(mosaic_by_date))
    return mosaicked_images
