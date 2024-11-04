export async function fetchWeatherData() {
    try {
      const response = await fetch('/api/weather/temperature?startDate=1438689667&endDate=1691150467&location=TEMPELHOFER_FELD&temporalResolution=MONTHLY&aggregation=MEAN');
      if (!response.ok) throw new Error('Failed to fetch');
      const data = await response.json();
      return data;  
    } catch (error) {
      console.error('Error fetching data:', error);
      return [];
    }
  }
  