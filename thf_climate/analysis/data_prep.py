import calendar
import os
import sys

import ee
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from thf_climate.gee.auth import authenticate

# Authenticate and initialize Earth Engine
authenticate()

# Define the region of interest (ROI) using coordinates
roi = ee.Geometry.Polygon(
    [
        [
            [13.402040012795936, 52.47446109087355],
            [13.402040012795936, 52.47345119235675],
            [13.406965596014118, 52.47345119235675],
            [13.406965596014118, 52.47446109087355],
            [13.402040012795936, 52.47446109087355],
        ]
    ]
)

# Define the date range
start_date = "2015-01-01"
end_date = "2023-12-31"

# Load the Landsat 8 image collection, filtering by date and, according to requirement, cloud cover
collection = (
    ee.ImageCollection("LANDSAT/LC08/C02/T1_TOA").filterDate(start_date, end_date)
    # .filter(ee.Filter.lt("CLOUD_COVER", 30))
)


# Calculate NDVI
def add_ndvi(image):
    ndvi = image.normalizedDifference(["B5", "B4"]).rename("NDVI")
    return image.addBands(ndvi)


# Apply the NDVI function to the collection
collection_with_ndvi = collection.map(add_ndvi)


# Function to calculate monthly median NDVI
def get_monthly_median_ndvi(year, month):
    start = ee.Date.fromYMD(year, month, 1)
    end = start.advance(1, "month")

    # Filter the collection for the given month and year
    monthly_collection = collection_with_ndvi.filterDate(start, end)

    # Get the median NDVI for that month
    monthly_median_ndvi = monthly_collection.select("NDVI").median()

    # Reduce the region to get the median NDVI value for the ROI
    stats = monthly_median_ndvi.reduceRegion(
        reducer=ee.Reducer.median(), geometry=roi, scale=30, bestEffort=True
    )

    # Return a dictionary containing year, month, and the NDVI value
    ndvi_value = stats.get("NDVI").getInfo() if stats.get("NDVI") is not None else None
    return {
        "year": year,
        "month": calendar.month_name[month],  # Display month names instead of numbers
        "ndvi": ndvi_value,
    }


# List to hold the results
results = []

# Loop through years 2015 to 2023 and all months of the year
for year in range(2015, 2024):
    for month in range(1, 13):
        result = get_monthly_median_ndvi(year, month)
        results.append(result)

# Convert the results to a pandas DataFrame
df = pd.DataFrame(results)

# Save the results to a CSV file
df.to_csv("monthly_median_ndvi_thf.csv", index=False)

print("CSV file has been saved.")
