<script>
  import { onMount } from 'svelte';
  let logs = [];

  onMount(async () => {
    const res = await fetch('http://127.0.0.1:5000/logs');
    logs = await res.json();
  });
</script>

<h1>Pond Logger Dashboard</h1>

<table>
  <tr><th>Time</th><th>pH</th><th>EC</th><th>DO</th><th>Temp</th></tr>
  {#each logs as log}
    <tr>
      <td>{log.timestamp}</td>
      <td>{log.ph}</td>
      <td>{log.ec}</td>
      <td>{log.do}</td>
      <td>{log.temp}</td>
    </tr>
  {/each}
</table>