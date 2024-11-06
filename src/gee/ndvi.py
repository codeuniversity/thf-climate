import ee

INDEX_FEATURE_LABEL = "indexing_value"
TIMESTAMP_FEATURE_LABEL = "start_of_day_timestamp"
INDEX_NULL_STRING = "NULL"


def calculate_mean_ndvi_GEE_SERVER(image: ee.Image, aoi: ee.Geometry.Polygon):
    ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")
    mean_ndvi = ndvi.reduceRegion(
        reducer=ee.Reducer.mean(), geometry=aoi, scale=10, maxPixels=1e8
    ).get("NDVI")
    mean_ndvi = ee.Algorithms.If(
        ee.Algorithms.IsEqual(mean_ndvi, None), INDEX_NULL_STRING, mean_ndvi
    )
    return image.set(INDEX_FEATURE_LABEL, mean_ndvi)


def calculate_start_of_day_timestamp_GEE_SERVER(image: ee.Image):
    acquisition_time = image.get("system:time_start")
    start_of_day = (
        ee.Date(acquisition_time)
        .update(hour=0, minute=0, second=0)
        .millis()
        .divide(1000)
    )
    return image.set(TIMESTAMP_FEATURE_LABEL, start_of_day)


def get_ndvi_info(
    image_collection: ee.ImageCollection, coordinates: ee.Geometry.Polygon
):
    aoi = ee.Geometry.Polygon(coordinates)

    # Setting indexing values Server side
    image_collection_with_ndvi = image_collection.map(
        lambda img: calculate_mean_ndvi_GEE_SERVER(img, aoi)
    )

    # Setting timestamps Server side
    image_collection_with_timestamp_and_ndvi = image_collection_with_ndvi.map(
        lambda img: calculate_start_of_day_timestamp_GEE_SERVER(img)
    )

    #  Getting indexing values to the client side
    index_value_list = image_collection_with_timestamp_and_ndvi.aggregate_array(
        INDEX_FEATURE_LABEL
    ).getInfo()

    # Getting timestamps to the client
    timestamp_list = image_collection_with_timestamp_and_ndvi.aggregate_array(
        TIMESTAMP_FEATURE_LABEL
    ).getInfo()

    if len(timestamp_list) != len(index_value_list):
        print(f"Timestamps: {len(timestamp_list)}, Values: {len(index_value_list)}")
        raise ValueError(
            "The lists of gee indexing values and timestamps do not have the same size"
        )

    # Convert the results to a list of dictionaries
    combined_results = [
        {"timestamp": ts, "value": val}
        for ts, val in zip(timestamp_list, index_value_list)
    ]

    return combined_results
