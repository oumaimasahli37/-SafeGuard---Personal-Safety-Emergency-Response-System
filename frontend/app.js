const API_BASE = 'http://127.0.0.1:5000'; // backend is running here per your console
const statusEl = document.getElementById('status');
const overviewEl = document.getElementById('overview');
const summaryList = document.getElementById('summary-list');
const rawJson = document.getElementById('raw-json');

async function loadOverview(){
  try{
    statusEl.textContent = 'Requesting analytics overview...';
    const res = await fetch(`${API_BASE}/api/analytics/overview`);
    if(!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    // show summary
    overviewEl.classList.remove('hidden');
    document.getElementById('status').textContent = 'Data loaded successfully';

    summaryList.innerHTML = `
      <li><strong>Total incidents:</strong> ${data.total_incidents ?? 'N/A'}</li>
      <li><strong>Average severity:</strong> ${data.average_severity ?? 'N/A'}</li>
      <li><strong>High risk count:</strong> ${data.high_risk_count ?? 'N/A'}</li>
      <li><strong>Most common type:</strong> ${data.most_common_type ?? 'N/A'}</li>
    `;

    // show raw JSON
    rawJson.textContent = JSON.stringify(data, null, 2);
    document.getElementById('raw').classList.remove('hidden');

  }catch(err){
    statusEl.textContent = 'Error loading data: ' + err.message;
    console.error(err);
  }
}

// load on page open
window.addEventListener('DOMContentLoaded', loadOverview);
