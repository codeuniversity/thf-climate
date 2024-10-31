from datetime import datetime

import ee

from src.gee.auth import authenticate
from src.utils.temporal import get_start_of_day


def get_ndvi_info(masked_image_list: list[ee.Image], coordinates: ee.Geometry.Polygon):
    authenticate()
    aoi = ee.Geometry.Polygon(coordinates)
    results = []
    for masked_image in masked_image_list:
        ndvi = masked_image.normalizedDifference(["B8", "B4"]).rename("NDVI")

        # Calculate the mean NDVI within the AOI
        mean_ndvi = (
            ndvi.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=aoi,
                scale=10,  # Adjust scale based on Sentinel-2 resolution (10m)
                maxPixels=1e8,
            )
            .get("NDVI")
            .getInfo()
        )
        acquisition_time = masked_image.get("system:time_start").getInfo()
        acquisition_datetime = datetime.utcfromtimestamp(acquisition_time / 1000)
        acquisition_start_of_day = get_start_of_day(acquisition_datetime)
        results.append({"timestamp": acquisition_start_of_day, "value": mean_ndvi})

    print(f"Result length {len(results)}")
    return results
