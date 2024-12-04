import ee
from ..constants import IndexType

INDEX_FEATURE_LABEL = "indexing_value"
TIMESTAMP_FEATURE_LABEL = "start_of_day_timestamp"
INDEX_NULL_STRING = "NULL"


def get_index_image_by_index_type(index_type: IndexType, image: ee.Image):
    match index_type:
        case IndexType.NDVI:
            return image.normalizedDifference(["B8", "B4"]).rename("NDVI") # B8 = NIR, B4 = RED
        case IndexType.MSAVI:
            return image.expression(
                expression="((2 * NIR + 1) - ((2 * NIR + 1)**2 - 8 * (NIR - RED))**0.5) / 2",
                opt_map={
                    "NIR": image.select("B8"),
                    "RED": image.select("B4"),
                },
            ).rename("MSAVI")
        case _:
            return None


def calculate_mean_index_GEE_SERVER(image: ee.Image, aoi: ee.Geometry.Polygon, index_type: IndexType):
    index_image = get_index_image_by_index_type(index_type, image)
    mean_index = index_image.reduceRegion(
        reducer=ee.Reducer.mean(), geometry=aoi, scale=10, maxPixels=1e8
    ).get(index_type.value)

    mean_index = ee.Algorithms.If(
        ee.Algorithms.IsEqual(mean_index, None), INDEX_NULL_STRING, mean_index
    )
    return image.set(INDEX_FEATURE_LABEL, mean_index)



def calculate_start_of_day_timestamp_GEE_SERVER(image: ee.Image):
    acquisition_time = image.get("system:time_start")
    start_of_day = (
        ee.Date(acquisition_time)
        .update(hour=0, minute=0, second=0)
        .millis()
        .divide(1000)
    )
    return image.set(TIMESTAMP_FEATURE_LABEL, start_of_day)


def get_sat_index_info(
    image_collection: ee.ImageCollection, coordinates: ee.Geometry.Polygon, index_type: IndexType
):
    aoi = ee.Geometry.Polygon(coordinates)

    # Setting indexing values Server side
    image_collection_with_index = image_collection.map(
        lambda img: calculate_mean_index_GEE_SERVER(img, aoi, index_type)
    )

    # Setting timestamps Server side
    image_collection_with_timestamp_and_index = image_collection_with_index.map(
        lambda img: calculate_start_of_day_timestamp_GEE_SERVER(img)
    )

    #  Getting indexing values to the client side
    index_value_list = image_collection_with_timestamp_and_index.aggregate_array(
        INDEX_FEATURE_LABEL
    ).getInfo()

    # Getting timestamps to the client
    timestamp_list = image_collection_with_timestamp_and_index.aggregate_array(
        TIMESTAMP_FEATURE_LABEL
    ).getInfo()

    if len(timestamp_list) != len(index_value_list):
        raise ValueError(
            "The lists of gee indexing values and timestamps do not have the same size" +
            f"Timestamps: {len(timestamp_list)}, Values: {len(index_value_list)}"

        )

    # Convert the results to a list of dictionaries
    combined_results = [
        {"timestamp": ts, "value": val}
        for ts, val in zip(timestamp_list, index_value_list)
        if val != INDEX_NULL_STRING
    ]

    return combined_results
