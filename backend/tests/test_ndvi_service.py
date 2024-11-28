from unittest.mock import patch
from datetime import datetime
from src.service import ndvi_service
from src.constants import LocationPolygon, TemporalResolution, AggregationMethod

@patch('src.gee.index.get_preprocessed_imagery')
@patch('src.gee.ndvi.get_ndvi_info')
def test_ndvi_service(mock_get_ndvi_info, mock_get_preprocessed_imagery):
    mock_get_preprocessed_imagery.return_value = "mocked_images"
    mock_get_ndvi_info.return_value = [{"timestamp": 1633046400, "value": 0.5}]
    
    start_date = datetime(2021, 10, 1)
    end_date = datetime(2021, 10, 2)
    result = ndvi_service(
        LocationPolygon.TEMPELHOFER_FELD,  # Use the enum member directly
        TemporalResolution.DAILY,
        AggregationMethod.MEAN,
        start_date,
        end_date
    )
    
    assert len(result) > 0
    assert result[0]["value"] == 0.5