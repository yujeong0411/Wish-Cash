<template>
  <div class="chart-container">
    <canvas ref="barChart" />
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

export default {
  name: "BarChart",
  props: {
    chartData: {
      type: Object,
      required: true,
    },
    chartOptions: {
      type: Object,
      required: true,
    },
  },
  mounted() {
    this.createChart();
    console.log(this.chartData)
  },
  methods: {
    createChart() {
      new Chart(this.$refs.barChart, {
        type: "bar", // 차트 타입
        data: this.chartData, // 전달받은 데이터
        options: {
          ...this.chartOptions,
          responsive: true, // 반응형 활성화
          maintainAspectRatio: false, // 컨테이너에 맞도록 비율 조정
        },
      });
    },
  },
};
</script>

<style scoped>
.chart-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%; /* 부모 컨테이너의 너비에 맞춤 */
  height: 100%; /* 부모 컨테이너의 높이에 맞춤 */
  max-width: 1200px; /* 컨테이너 최대 너비 */
  max-height: 600px; /* 컨테이너 최대 높이 */
  margin: 0 auto; /* 가운데 정렬 */
  position: relative; /* 차트가 컨테이너에 맞게 렌더링 */
}
canvas {
  display: block;
  width: 100% !important; /* 부모 컨테이너의 너비에 맞춤 */
  height: 100% !important; /* 부모 컨테이너의 높이에 맞춤 */
}
</style>


