<script>
  let ph, ec, doVal, temp;

  async function submitLog() {
    await fetch('http://127.0.0.1:5000/logs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ph, ec, do: doVal, temp })
    });
    alert("Log submitted!");
  }
</script>

<h2>Add Pond Reading</h2>
<form on:submit|preventDefault={submitLog}>
  <label>pH: <input type="number" step="0.1" bind:value={ph}></label><br>
  <label>EC: <input type="number" step="0.1" bind:value={ec}></label><br>
  <label>DO: <input type="number" step="0.1" bind:value={doVal}></label><br>
  <label>Temp: <input type="number" step="0.1" bind:value={temp}></label><br>
  <button type="submit">Add Log</button>
</form>