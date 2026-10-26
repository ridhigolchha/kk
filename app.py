from flask import Flask, jsonify, render_template_string, request

from leadgen import LeadGenerator

app = Flask(__name__)

generator = LeadGenerator()

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Lead Generation Dashboard</title>
    <style>
      :root {
        --bg: #0f172a;
        --panel: #111827;
        --panel-2: #1f2937;
        --muted: #94a3b8;
        --primary: #38bdf8;
        --accent: #34d399;
        --text: #e5e7eb;
        --warning: #fbbf24;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: Arial, sans-serif;
        background: linear-gradient(135deg, #020817, #111827);
        color: var(--text);
      }
      .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 24px;
      }
      .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
      }
      .topbar h1 {
        margin: 0;
        font-size: 2rem;
      }
      .badge {
        display: inline-block;
        background: rgba(56, 189, 248, 0.18);
        color: var(--primary);
        padding: 8px 12px;
        border-radius: 999px;
        font-weight: bold;
      }
      .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 20px;
        margin-bottom: 24px;
      }
      .card {
        background: rgba(17, 24, 39, 0.88);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
      }
      .card h3 {
        margin-top: 0;
        color: var(--muted);
        font-size: 0.9rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }
      .metric {
        font-size: 2.1rem;
        font-weight: bold;
        margin-top: 14px;
      }
      .controls {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin-bottom: 18px;
      }
      input, button {
        border: none;
        border-radius: 10px;
        padding: 12px 14px;
        font-size: 1rem;
      }
      input {
        background: rgba(31, 41, 55, 0.9);
        color: var(--text);
        min-width: 180px;
      }
      button {
        background: linear-gradient(135deg, var(--primary), var(--accent));
        color: #03121b;
        font-weight: bold;
        cursor: pointer;
      }
      .lead-table {
        width: 100%;
        border-collapse: collapse;
        background: rgba(17, 24, 39, 0.88);
        border-radius: 14px;
        overflow: hidden;
      }
      .lead-table th, .lead-table td {
        padding: 12px 14px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.15);
        text-align: left;
      }
      .lead-table th {
        background: rgba(15, 23, 42, 0.9);
      }
      .score-pill {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 0.8rem;
        background: rgba(52, 211, 153, 0.12);
        color: var(--accent);
        font-weight: bold;
      }
      .muted {
        color: var(--muted);
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="topbar">
        <h1>Lead Generation Dashboard</h1>
        <span class="badge">Pipeline Intelligence</span>
      </div>

      <div class="grid">
        <div class="card">
          <h3>Total Leads</h3>
          <div class="metric" id="totalLeads">0</div>
        </div>
        <div class="card">
          <h3>High Intent</h3>
          <div class="metric" id="highIntent">0</div>
        </div>
        <div class="card">
          <h3>Avg. Score</h3>
          <div class="metric" id="avgScore">0</div>
        </div>
        <div class="card">
          <h3>Top Source</h3>
          <div class="metric" id="topSource">—</div>
        </div>
      </div>

      <div class="controls">
        <input id="leadCount" type="number" min="1" max="25" value="5" aria-label="Lead count">
        <button id="generateBtn">Generate Leads</button>
      </div>

      <div class="card">
        <h3>Qualified Accounts</h3>
        <table class="lead-table">
          <thead>
            <tr>
              <th>Company</th>
              <th>Role</th>
              <th>Industry</th>
              <th>Source</th>
              <th>Budget</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody id="leadRows">
            <tr>
              <td colspan="6" class="muted">No leads generated yet.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <script>
      async function generateLeads() {
        const count = document.getElementById('leadCount').value || 5;
        const response = await fetch('/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ count: Number(count) })
        });
        const data = await response.json();
        renderLeads(data.leads);
      }

      function renderLeads(leads) {
        const tbody = document.getElementById('leadRows');
        tbody.innerHTML = '';

        if (!leads.length) {
          tbody.innerHTML = '<tr><td colspan="6" class="muted">No leads generated yet.</td></tr>';
          return;
        }

        leads.forEach((lead) => {
          const row = document.createElement('tr');
          row.innerHTML = `
            <td>${lead.company}</td>
            <td>${lead.job_title}</td>
            <td>${lead.industry}</td>
            <td>${lead.source}</td>
            <td>$${Number(lead.budget).toLocaleString()}</td>
            <td><span class="score-pill">${lead.score}</span></td>
          `;
          tbody.appendChild(row);
        });

        const highIntent = leads.filter((lead) => lead.score >= 80).length;
        const avgScore = Math.round(leads.reduce((sum, lead) => sum + lead.score, 0) / leads.length);
        const sourceCounts = {};
        leads.forEach((lead) => {
          sourceCounts[lead.source] = (sourceCounts[lead.source] || 0) + 1;
        });
        const topSource = Object.entries(sourceCounts).sort((a, b) => b[1] - a[1])[0];

        document.getElementById('totalLeads').textContent = leads.length;
        document.getElementById('highIntent').textContent = highIntent;
        document.getElementById('avgScore').textContent = `${avgScore}`;
        document.getElementById('topSource').textContent = topSource ? topSource[0] : '—';
      }

      document.getElementById('generateBtn').addEventListener('click', generateLeads);
      generateLeads();
    </script>
  </body>
</html>
"""


@app.route("/")
def dashboard():
    return render_template_string(HTML_TEMPLATE)


@app.route("/generate", methods=["POST"])
def generate_leads():
    payload = request.get_json(silent=True) or {}
    count = int(payload.get("count", 5))
    leads = generator.generate_batch(count)
    return jsonify({"leads": leads})


if __name__ == "__main__":
    app.run(debug=True)
