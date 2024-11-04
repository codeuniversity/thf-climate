import unittest
from unittest.mock import MagicMock, patch

from src.analysis.data_prep import get_monthly_median_ndvi


class TestDataPrep(unittest.TestCase):
    @patch("src.analysis.data_prep.ee.Geometry")
    @patch("src.analysis.data_prep.ee.ImageCollection")
    def test_get_monthly_median_ndvi(self, mock_image_collection, mock_geometry):
        mock_geometry.return_value = MagicMock()

        mock_collection = MagicMock()

        mock_image_collection.return_value = mock_collection
        mock_collection.filterDate.return_value = mock_collection
        mock_collection.select.return_value = mock_collection
        mock_collection.median.return_value = mock_collection

        mock_collection.reduceRegion.return_value = MagicMock(
            get=lambda key: {"NDVI": 0.6}.get(key)
        )

        result = get_monthly_median_ndvi(2020, 5)

        self.assertEqual(result["year"], 2020)
        self.assertEqual(result["month"], "May")
        self.assertEqual(result["ndvi"], 0.6)


if __name__ == "__main__":
    unittest.main()
