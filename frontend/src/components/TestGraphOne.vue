<template>
  <div>
    <h2>Median Monthly Temperature</h2>
    
    <!-- Date Range Input Fields -->
    <div class="date-picker">
      <label>
        Start Date:
        <input type="date" v-model="startDate" @change="updateDateRange" />
      </label>
      <label>
        End Date:
        <input type="date" v-model="endDate" @change="updateDateRange" />
      </label>
    </div>

    <!-- Plotly Chart -->
    <div ref="plotlyChart" style="width: 100%; height: 400px;"></div>
  </div>
</template>

<script>
import Plotly from 'plotly.js-dist-min';

export default {
name: 'MedianTempGraph',
data() {
  return {
    location: 'TEMPELHOFER_FELD',
    temporalResolution: 'MONTHLY',
    aggregation: 'MEDIAN',
    startDate: '2015-01-01',
    endDate: '2023-12-31',
    plotData: [],
  };
},

mounted() {
  this.loadApiData();
},

methods: {
  async loadApiData() {
    const startTimestamp = new Date(this.startDate).getTime() / 1000;
    const endTimestamp = new Date(this.endDate).getTime() / 1000;

    const url = `/api/weather/temperature?startDate=${startTimestamp}&endDate=${endTimestamp}&location=${this.location}&temporalResolution=${this.temporalResolution}&aggregation=${this.aggregation}`;

    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error('Failed to fetch');
      
      const data = await response.json();
      this.processData(data);
      this.renderPlot();
    } catch (error) {
      console.error('Error fetching data', error);
    }
  },
  
  processData(apiResponse) {
    if (!apiResponse.data || !Array.isArray(apiResponse.data)) {
      console.log('Unexpected data format:', apiResponse);
      return;
    }

    const dates = apiResponse.data.map(entry => 
      new Date(entry.timestamp * 1000).toISOString().split('T')[0]
    );
    const temperatures = apiResponse.data.map(entry => entry.value);

    this.plotData = [
      {
        x: dates,
        y: temperatures,
        mode: 'lines',
        name: 'Temperature',
        line: { color: '#FF4136' }
      }
    ];
  },

  renderPlot() {
    const layout = {
      title: 'Median Monthly Temperature for Tempelhofer Feld (2015 - 2023)',
      xaxis: { title: '', type: 'date', rangeslider: { visible: true } },
      yaxis: { title: 'Temperature (°C)' },
      template: 'plotly_white'
    };

    Plotly.newPlot(this.$refs.plotlyChart, this.plotData, layout);
  },
  updateDateRange() {
    if (this.startDate && this.endDate) {
      this.loadApiData();
    }
  }
}
};
</script>

<style scoped>
h2 {
text-align: center;
margin-bottom: 10px;
}
.date-picker {
display: flex;
justify-content: center;
gap: 10px;
margin-bottom: 20px;
}
</style>
