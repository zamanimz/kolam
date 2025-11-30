<script lang="ts">
  import { onMount } from 'svelte';
  let logs: any[] = [];
  let loading = true;
  let error: string | null = null;

  async function fetchLogs() {
    try {
      loading = true;
      error = null;
      const res = await fetch('http://127.0.0.1:5000/logs');
      if (!res.ok) throw new Error('Failed to fetch logs');
      logs = await res.json();
    } catch (err) {
      error = err instanceof Error ? err.message : 'An error occurred';
    } finally {
      loading = false;
    }
  }

  onMount(fetchLogs);
  
  // Calculate latest values for stats
  $: latestLog = logs.length > 0 ? logs[logs.length - 1] : null;
</script>

<div class="container">
  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
    <h1>Dashboard</h1>
    <button class="btn btn-primary" on:click={fetchLogs} disabled={loading}>
      {loading ? '↻ Refreshing...' : '↻ Refresh'}
    </button>
  </div>

  {#if error}
    <div class="alert alert-error">
      <strong>Error:</strong> {error}
    </div>
  {/if}

  {#if latestLog}
    <div class="stats-grid">
      <div class="stat-card" style="background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);">
        <h3>pH Level</h3>
        <div class="value">{latestLog.ph ?? 'N/A'}</div>
      </div>
      <div class="stat-card" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
        <h3>EC (μS/cm)</h3>
        <div class="value">{latestLog.ec ?? 'N/A'}</div>
      </div>
      <div class="stat-card" style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);">
        <h3>DO (mg/L)</h3>
        <div class="value">{latestLog.do ?? 'N/A'}</div>
      </div>
      <div class="stat-card" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);">
        <h3>Temperature (°C)</h3>
        <div class="value">{latestLog.temp ?? 'N/A'}</div>
      </div>
    </div>
  {/if}

  <div class="card">
    <h2 style="margin-bottom: 1.5rem;">Recent Readings</h2>
    
    {#if loading && logs.length === 0}
      <p style="text-align: center; padding: 2rem; color: var(--text-light);">Loading data...</p>
    {:else if logs.length === 0}
      <p style="text-align: center; padding: 2rem; color: var(--text-light);">
        No readings yet. <a href="/add" style="color: var(--primary); text-decoration: underline;">Add your first reading</a>
      </p>
    {:else}
      <div style="overflow-x: auto;">
        <table>
          <thead>
            <tr>
              <th>📅 Timestamp</th>
              <th>🧪 pH</th>
              <th>⚡ EC (μS/cm)</th>
              <th>💧 DO (mg/L)</th>
              <th>🌡️ Temp (°C)</th>
            </tr>
          </thead>
          <tbody>
            {#each logs.slice().reverse() as log}
              <tr>
                <td>{new Date(log.timestamp).toLocaleString()}</td>
                <td>{log.ph ?? 'N/A'}</td>
                <td>{log.ec ?? 'N/A'}</td>
                <td>{log.do ?? 'N/A'}</td>
                <td>{log.temp ?? 'N/A'}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}
  </div>
</div>

<style>
  .stats-grid {
    animation: fadeIn 0.5s ease-in;
  }
  
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>