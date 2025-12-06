<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { Chart, registerables } from 'chart.js';
  Chart.register(...registerables);

  export let logs: any[] = [];
  export let maxPoints = 48;

  let canvasEl: HTMLCanvasElement;
  let chart: Chart | null = null;

  function buildData() {
    const slice = logs.slice(-maxPoints);
    const labels = slice.map(l => new Date(l.timestamp).toLocaleString());
    const ph = slice.map(l => (l.ph ?? null));
    const ec = slice.map(l => (l.ec ?? null));
    const doArr = slice.map(l => (l.do ?? null));
    const temp = slice.map(l => (l.temp ?? null));

    return {
      labels,
      datasets: [
        { label: 'pH', data: ph, borderColor: '#06b6d4', backgroundColor: 'rgba(6,182,212,0.08)', tension: 0.25, yAxisID: 'y' },
        { label: 'EC (μS/cm)', data: ec, borderColor: '#059669', backgroundColor: 'rgba(5,150,105,0.06)', tension: 0.25, yAxisID: 'y1' },
        { label: 'DO (mg/L)', data: doArr, borderColor: '#7c3aed', backgroundColor: 'rgba(124,58,237,0.06)', tension: 0.25, yAxisID: 'y' },
        { label: 'Temp (°C)', data: temp, borderColor: '#f59e0b', backgroundColor: 'rgba(245,158,11,0.06)', tension: 0.25, yAxisID: 'y' }
      ]
    };
  }

  function createChart() {
    const cfg = {
      type: 'line' as const,
      data: buildData(),
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        stacked: false,
        scales: {
          x: { display: true, title: { display: false } },
          y: { type: 'linear', display: true, position: 'left' },
          y1: { type: 'linear', display: true, position: 'right', grid: { drawOnChartArea: false } }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: { mode: 'index', intersect: false }
        }
      }
    };

    const ctx = canvasEl.getContext('2d');
    if (!ctx) return;
    chart = new Chart(ctx, cfg as any);
  }

  onMount(() => {
    createChart();
  });

  $: if (chart) {
    chart.data = buildData() as any;
    chart.update();
  }

  onDestroy(() => {
    chart?.destroy();
    chart = null;
  });
</script>

<div class="chart-card">
  {#if logs.length === 0}
    <div class="empty">No data to display</div>
  {:else}
    <div class="chart-wrapper">
      <canvas bind:this={canvasEl}></canvas>
    </div>
  {/if}
</div>

<style>
  .chart-wrapper { height: 320px; }
  .chart-card { margin-bottom: 1.25rem; }
  .empty { padding: 2rem; color: var(--text-light); text-align: center; }
</style>
