import calendar
import os
import sys

import ee
import pandas as pd
import plotly.express as px

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.gee.auth import authenticate

# Authenticate and initialize Earth Engine
authenticate()

# Define the region of interest (ROI) using coordinates
roi = ee.Geometry.Polygon(
    [
        [
            [13.393926142690503, 52.479459342318194],
            [13.39035120841146, 52.47528176851594],
            [13.390475915421774, 52.47274971256647],
            [13.396461851886613, 52.46831826407774],
            [13.403694858449427, 52.466849456987205],
            [13.412964746171014, 52.46897667893188],
            [13.416622818456005, 52.47090121972539],
            [13.415209472346135, 52.47626923084667],
            [13.410969434016465, 52.47728198970532],
            [13.408101172792328, 52.47869981294684],
            [13.405856446618543, 52.479459342318194],
            [13.399662665136049, 52.479889736475684],
            [13.393926142690503, 52.479459342318194],
        ]
    ]
)

# Define the date range
start_date = "2015-01-01"
end_date = "2023-12-31"

# Load the Landsat 8 image collection, filtering by date and, according to requirement, cloud cover
collection = (
    ee.ImageCollection("LANDSAT/LC08/C02/T1_TOA")
    .filterDate(start_date, end_date)
    .filter(ee.Filter.lt("CLOUD_COVER", 50))
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

# Combine year and month into a single datetime column for easier plotting
df["date"] = pd.to_datetime(
    df["year"].astype(str) + "-" + df["month"].astype(str), format="%Y-%B"
)

# Sort the DataFrame by date
df = df.sort_values(by="date")

# Plot the data using Plotly
fig = px.line(
    df,
    x="date",
    y="ndvi",
    title="Monthly Median NDVI (2015-2023) for Tempelhofer Feld",
    labels={"date": "Date", "ndvi": "NDVI"},
)

fig.show()
