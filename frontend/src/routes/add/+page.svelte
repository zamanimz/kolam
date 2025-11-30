<script lang="ts">
  import { goto } from '$app/navigation';
  
  let ph = '';
  let ec = '';
  let doVal = '';
  let temp = '';
  let submitting = false;
  let message: string | null = null;
  let messageType = '';

  async function submitLog() {
    // Validate inputs
    if (!ph || !ec || !doVal || !temp) {
      message = 'Please fill in all fields';
      messageType = 'error';
      return;
    }
    
    try {
      submitting = true;
      message = null;
      
      const response = await fetch('http://127.0.0.1:5000/logs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          ph: parseFloat(ph), 
          ec: parseFloat(ec), 
          do: parseFloat(doVal), 
          temp: parseFloat(temp) 
        })
      });
      
      if (!response.ok) throw new Error('Failed to submit reading');
      
      message = 'Reading submitted successfully!';
      messageType = 'success';
      
      // Reset form
      ph = '';
      ec = '';
      doVal = '';
      temp = '';
      
      // Redirect to dashboard after 1.5 seconds
      setTimeout(() => {
        goto('/');
      }, 1500);
      
    } catch (err) {
      message = err instanceof Error ? err.message : 'Failed to submit reading';
      messageType = 'error';
    } finally {
      submitting = false;
    }
  }
</script>

<div class="container">
  <div style="max-width: 600px; margin: 0 auto;">
    <h1>Add New Reading</h1>
    
    {#if message}
      <div class="alert alert-{messageType}">
        {message}
      </div>
    {/if}
    
    <div class="card">
      <form on:submit|preventDefault={submitLog}>
        <div class="form-group">
          <label for="ph">🧪 pH Level</label>
          <input 
            id="ph"
            type="number" 
            step="0.01" 
            min="0" 
            max="14" 
            placeholder="Enter pH (0-14)"
            bind:value={ph}
            required
          >
          <small style="color: var(--text-light); display: block; margin-top: 0.25rem;">
            Normal range: 6.5 - 8.5
          </small>
        </div>

        <div class="form-group">
          <label for="ec">⚡ Electrical Conductivity (μS/cm)</label>
          <input 
            id="ec"
            type="number" 
            step="0.1" 
            min="0"
            placeholder="Enter EC value"
            bind:value={ec}
            required
          >
          <small style="color: var(--text-light); display: block; margin-top: 0.25rem;">
            Measures dissolved salts and minerals
          </small>
        </div>

        <div class="form-group">
          <label for="do">💧 Dissolved Oxygen (mg/L)</label>
          <input 
            id="do"
            type="number" 
            step="0.01" 
            min="0"
            placeholder="Enter DO value"
            bind:value={doVal}
            required
          >
          <small style="color: var(--text-light); display: block; margin-top: 0.25rem;">
            Minimum recommended: 5 mg/L for fish
          </small>
        </div>

        <div class="form-group">
          <label for="temp">🌡️ Temperature (°C)</label>
          <input 
            id="temp"
            type="number" 
            step="0.1" 
            placeholder="Enter temperature"
            bind:value={temp}
            required
          >
          <small style="color: var(--text-light); display: block; margin-top: 0.25rem;">
            Optimal range varies by fish species
          </small>
        </div>

        <div style="display: flex; gap: 1rem; margin-top: 2rem;">
          <button 
            type="submit" 
            class="btn btn-primary" 
            disabled={submitting}
            style="flex: 1;"
          >
            {submitting ? 'Submitting...' : '✓ Submit Reading'}
          </button>
          <a 
            href="/" 
            class="btn btn-secondary"
            style="flex: 1; text-align: center; text-decoration: none; display: flex; align-items: center; justify-content: center;"
          >
            ← Back to Dashboard
          </a>
        </div>
      </form>
    </div>
    
    <div class="card" style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border: 2px solid var(--primary);">
      <h3 style="color: var(--primary); margin-bottom: 1rem;">💡 Quick Tips</h3>
      <ul style="color: var(--text-dark); line-height: 1.8; padding-left: 1.5rem;">
        <li>Take readings at the same time each day for consistency</li>
        <li>Wait a few seconds for sensor readings to stabilize</li>
        <li>Clean sensors regularly for accurate measurements</li>
        <li>Monitor trends over time rather than individual readings</li>
      </ul>
    </div>
  </div>
</div>