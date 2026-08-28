from fastapi.responses import HTMLResponse


def render_dashboard() -> HTMLResponse:
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>RDRS — Security Dashboard</title>

<style>
*{box-sizing:border-box}
body{margin:0;min-height:100vh;background:#080d19;color:#e8edf7;font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}
.app{display:flex;min-height:100vh}
.sidebar{width:250px;padding:24px 16px;border-right:1px solid #1d2638;background:#0b1120}
.brand{display:flex;align-items:center;gap:12px;padding:8px 12px 30px}
.brand-icon{width:40px;height:40px;display:grid;place-items:center;border-radius:12px;background:#17233a;font-size:20px}
.brand-name{font-size:19px;font-weight:700}
.brand-subtitle{margin-top:3px;color:#71809b;font-size:11px;letter-spacing:.08em}
.nav-title{padding:12px;color:#56647d;font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}
.nav-item{display:flex;align-items:center;gap:12px;margin:4px 0;padding:12px;border-radius:10px;color:#8491a8;font-size:14px}
.nav-item.active{background:#16233a;color:#f1f5ff}
.nav-icon{width:20px;text-align:center}
.sidebar-bottom{margin-top:40px;padding:14px;border:1px solid #1d293e;border-radius:12px;background:#0e1627}
.system-row{display:flex;justify-content:space-between;font-size:12px;color:#8491a8}
.online{color:#63df9b}
.main{flex:1;min-width:0;padding:28px 32px}
.topbar{display:flex;justify-content:space-between;align-items:flex-start;gap:20px;margin-bottom:28px}
.eyebrow{color:#6e7d97;font-size:12px;text-transform:uppercase;letter-spacing:.12em}
h1{margin:6px 0;font-size:30px}
.description{margin:0;color:#75839c;font-size:14px}
.status{display:flex;align-items:center;gap:8px;padding:9px 14px;border:1px solid #194a35;border-radius:999px;background:#0d281d;color:#67dfa0;font-size:12px;font-weight:600}
.status-dot{width:7px;height:7px;border-radius:50%;background:#67dfa0}
.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-bottom:20px}
.card{border:1px solid #1d273a;border-radius:15px;background:#0e1525}
.metric{padding:20px}
.metric-label{color:#71809a;font-size:12px}
.metric-value{margin-top:12px;font-size:30px;font-weight:700}
.metric-change{margin-top:7px;color:#63718a;font-size:11px}
.good{color:#58c991}.warning{color:#d6ae61}
.grid{display:grid;grid-template-columns:1.55fr 1fr;gap:20px}
.panel{overflow:hidden}
.panel-header{display:flex;justify-content:space-between;align-items:center;padding:18px 20px;border-bottom:1px solid #1c2638}
.panel-title{font-size:14px;font-weight:650}
.panel-action{color:#70809b;font-size:11px}
.activity{height:280px;display:flex;align-items:flex-end;gap:10px;padding:25px}
.bar{flex:1;min-width:8px;border-radius:5px 5px 2px 2px;background:#304666;transition:height .4s}
.bar.high{background:#76515d}.bar.peak{background:#9a5b63}
.events{padding:6px 0}
.event{display:flex;align-items:center;gap:12px;padding:14px 20px;border-bottom:1px solid #172133}
.event:last-child{border-bottom:0}
.event-icon{width:32px;height:32px;display:grid;place-items:center;border-radius:9px;background:#172237}
.event-info{min-width:0;flex:1}
.event-name{overflow:hidden;color:#dce4f2;font-size:12px;text-overflow:ellipsis;white-space:nowrap}
.event-path{margin-top:4px;overflow:hidden;color:#596983;font-size:10px;text-overflow:ellipsis;white-space:nowrap}
.severity{padding:5px 8px;border-radius:6px;font-size:9px;font-weight:700;letter-spacing:.05em}
.severity.normal{background:#15291f;color:#68ca94}
.severity.warning{background:#302818;color:#d8b461}
.severity.critical{background:#351c23;color:#e47d8d}
.empty{padding:30px 20px;color:#687791;text-align:center;font-size:12px}
@media(max-width:1050px){.metrics{grid-template-columns:repeat(2,1fr)}.grid{grid-template-columns:1fr}}
@media(max-width:720px){.sidebar{display:none}.main{padding:20px}.metrics{grid-template-columns:1fr}}
</style>
</head>

<body>
<div class="app">

<aside class="sidebar">
<div class="brand">
<div class="brand-icon">🛡</div>
<div><div class="brand-name">RDRS</div><div class="brand-subtitle">SECURITY PLATFORM</div></div>
</div>

<div class="nav-title">Monitor</div>
<div class="nav-item active"><span class="nav-icon">⌂</span>Overview</div>
<div class="nav-item"><span class="nav-icon">◉</span>Events</div>
<div class="nav-item"><span class="nav-icon">⚠</span>Incidents</div>
<div class="nav-item"><span class="nav-icon">◈</span>Evidence</div>

<div class="nav-title">Manage</div>
<div class="nav-item"><span class="nav-icon">▣</span>Reports</div>
<div class="nav-item"><span class="nav-icon">⚙</span>Settings</div>

<div class="sidebar-bottom">
<div class="system-row"><span>Detection engine</span><span class="online">ONLINE</span></div>
<div style="height:8px"></div>
<div class="system-row"><span>Database</span><span class="online">CONNECTED</span></div>
</div>
</aside>

<main class="main">

<header class="topbar">
<div>
<div class="eyebrow">Security Operations</div>
<h1>Dashboard</h1>
<p class="description">Real-time ransomware detection and response overview.</p>
</div>
<div class="status"><span class="status-dot"></span>SYSTEM ONLINE</div>
</header>

<section class="metrics">
<div class="card metric">
<div class="metric-label">THREAT SCORE</div>
<div id="threat-score" class="metric-value">--</div>
<div id="threat-label" class="metric-change warning">Loading...</div>
</div>

<div class="card metric">
<div class="metric-label">EVENTS TODAY</div>
<div id="event-count" class="metric-value">--</div>
<div class="metric-change good">Monitoring active</div>
</div>

<div class="card metric">
<div class="metric-label">SUSPICIOUS EVENTS</div>
<div id="suspicious-count" class="metric-value">--</div>
<div class="metric-change warning">Requires review</div>
</div>

<div class="card metric">
<div class="metric-label">RECENT EVENTS</div>
<div id="recent-count" class="metric-value">--</div>
<div class="metric-change good">Database connected</div>
</div>
</section>

<section class="grid">

<div class="card panel">
<div class="panel-header">
<span class="panel-title">Threat Activity</span>
<span class="panel-action">LIVE DATABASE</span>
</div>
<div id="activity" class="activity">
<div class="bar" style="height:25%"></div>
<div class="bar" style="height:35%"></div>
<div class="bar" style="height:20%"></div>
<div class="bar" style="height:48%"></div>
<div class="bar" style="height:38%"></div>
<div class="bar" style="height:58%"></div>
<div class="bar high" style="height:72%"></div>
<div class="bar" style="height:44%"></div>
<div class="bar" style="height:62%"></div>
<div class="bar peak" style="height:88%"></div>
<div class="bar high" style="height:68%"></div>
<div class="bar" style="height:51%"></div>
</div>
</div>

<div class="card panel">
<div class="panel-header">
<span class="panel-title">Recent Events</span>
<span class="panel-action">LIVE</span>
</div>
<div id="events" class="events">
<div class="empty">Loading events...</div>
</div>
</div>

<div class="card panel" style="margin-top:20px">
<div class="panel-header">
<span class="panel-title">Active Incidents</span>
<span class="panel-action">LIVE</span>
</div>
<div id="incidents" class="events">
<div class="empty">Loading incidents...</div>
</div>
</div>

</section>

<section class="card panel" style="margin-top:20px">
<div class="panel-header">
    <span class="panel-title">System Settings</span>
    <span class="panel-action">CONFIGURATION</span>
</div>
<div id="settings" class="events">
    <div class="empty">Loading settings...</div>
</div>
</section>

<section class="card panel" style="margin-top:20px">
<div class="panel-header">
    <span class="panel-title">Security Report</span>
    <span class="panel-action">LIVE SUMMARY</span>
</div>
<div id="report" class="events">
    <div class="empty">Loading report...</div>
</div>
</section>



<section class="card panel" style="margin-top:20px">
<div class="panel-header">
    <span class="panel-title">System Settings</span>
    <span class="panel-action">CONFIGURATION</span>
</div>
<div id="settings" class="events">
    <div class="empty">Loading settings...</div>
</div>
</section>

<section class="card panel" style="margin-top:20px">
<div class="panel-header">
    <span class="panel-title">Active Incidents</span>
    <span class="panel-action">LIVE</span>
</div>
<div id="incidents" class="events">
    <div class="empty">Loading incidents...</div>
</div>
</section>


</main>
</div>

<script>
async function resolveIncident(id){
    try{
        const response = await fetch(`/api/incidents/${id}`, {
            method: "PATCH",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                status: "resolved"
            })
        });

        if(!response.ok) throw new Error("Unable to resolve incident");

        await loadDashboard();
    }catch(error){
        console.error(error);
    }
}


async function loadReport(){
    try{
        const response = await fetch("/api/reports/summary");

        if(!response.ok) throw new Error("Report unavailable");

        const report = await response.json();

        document.getElementById("report").innerHTML = `
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;padding:18px">
                <div class="card" style="padding:14px">
                    <div class="metric-label">TOTAL EVENTS</div>
                    <div class="metric-value" style="font-size:22px">${report.total_events}</div>
                </div>
                <div class="card" style="padding:14px">
                    <div class="metric-label">SUSPICIOUS</div>
                    <div class="metric-value" style="font-size:22px">${report.suspicious_events}</div>
                </div>
                <div class="card" style="padding:14px">
                    <div class="metric-label">INCIDENTS</div>
                    <div class="metric-value" style="font-size:22px">${report.total_incidents}</div>
                </div>
                <div class="card" style="padding:14px">
                    <div class="metric-label">RESOLVED</div>
                    <div class="metric-value" style="font-size:22px">${report.resolved_incidents}</div>
                </div>
            </div>
        `;
    }catch(error){
        document.getElementById("report").innerHTML =
            '<div class="empty">Unable to load report.</div>';
    }
}


async function loadSettings(){
    try{
        const response = await fetch("/api/settings");

        if(!response.ok) throw new Error("Settings unavailable");

        const settings = await response.json();

        document.getElementById("settings").innerHTML = `
            <div style="padding:18px">
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px">
                    <span class="metric-label">MONITORING ENGINE</span>
                    <button
                        onclick="toggleMonitoring(${!settings.monitoring_enabled})"
                        style="padding:7px 11px;border:1px solid #28553f;border-radius:7px;background:#10261d;color:#69d89c;cursor:pointer;font-size:10px">
                        ${settings.monitoring_enabled ? "ENABLED" : "DISABLED"}
                    </button>
                </div>

                <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
                    <div>
                        <div class="metric-label">MONITORED PATH</div>
                        <div style="margin-top:7px;color:#dce4f2;font-size:13px">
                            ${settings.monitored_path}
                        </div>
                    </div>

                    <div>
                        <div class="metric-label">ENTROPY THRESHOLD</div>
                        <div style="margin-top:7px;color:#dce4f2;font-size:13px">
                            ${settings.entropy_threshold}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }catch(error){
        document.getElementById("settings").innerHTML =
            '<div class="empty">Unable to load settings.</div>';
    }
}

async function toggleMonitoring(enabled){
    await fetch("/api/settings", {
        method: "PATCH",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            monitoring_enabled: enabled
        })
    });

    loadSettings();
}

async function loadDashboard(){
    try{
        const [statsRes, eventsRes, incidentsRes] = await Promise.all([
            fetch("/api/stats"),
            fetch("/api/events?limit=6"),
            fetch("/api/incidents")
        ]);

        if(!statsRes.ok || !eventsRes.ok || !incidentsRes.ok)
            throw new Error("API unavailable");

        const stats = await statsRes.json();
        const events = await eventsRes.json();
        const incidents = await incidentsRes.json();

        const total = stats.total_events || 0;
        const suspicious = stats.suspicious_events || 0;
        const recent = stats.recent_events || 0;
        const openIncidents = incidents.filter(i => i.status === "open").length;

        const openIncidents = incidents.filter(
            incident => incident.status === "open"
        );

        const maxThreatScore = incidents.length
            ? Math.max(...incidents.map(i => Number(i.threat_score) || 0))
            : 0;

        const score = Math.round(
            Math.max(
                maxThreatScore,
                Math.min(100, suspicious * 20 + Math.min(total, 20))
            )
        );

        document.getElementById("threat-score").textContent = score;
        document.getElementById("event-count").textContent = total;
        document.getElementById("suspicious-count").textContent =
            openIncidents.length;

        document.getElementById("recent-count").textContent = recent;
        const incidentCount = document.getElementById("incident-count");
        if (incidentCount) incidentCount.textContent = openIncidents;

        document.getElementById("threat-label").textContent =
            score >= 70 ? "Elevated activity" :
            score >= 40 ? "Moderate activity" : "Low activity";

        const incidentContainer = document.getElementById("incidents");

        if(!incidents.length){
            incidentContainer.innerHTML =
                '<div class="empty">No incidents recorded.</div>';
        }else{
            incidentContainer.innerHTML = incidents
                .filter(i => i.status === "open")
                .map(incident => {
                    const severity =
                        incident.severity === "critical" ? "critical" :
                        incident.severity === "high" ? "critical" :
                        incident.severity === "medium" ? "warning" :
                        "normal";

                    return `
                    <div class="event">
                        <div class="event-icon">⚠</div>
                        <div class="event-info">
                            <div class="event-name">
                                ${incident.incident_id} — ${incident.summary}
                            </div>
                            <div class="event-path">
                                Threat score: ${incident.threat_score}
                            </div>
                        </div>
                        <span class="severity ${severity}">
                            ${incident.severity.toUpperCase()}
                        </span>
                    </div>`;
                }).join("");
        }

        const incidentContainer = document.getElementById("incidents");

        const activeIncidents = incidents.filter(
            incident => incident.status === "open"
        );

        if(!activeIncidents.length){
            incidentContainer.innerHTML =
                '<div class="empty">No active incidents.</div>';
        }else{
            incidentContainer.innerHTML = activeIncidents.slice(0, 6).map(incident => `
                <div class="event">
                    <div class="event-icon">⚠</div>
                    <div class="event-info">
                        <div class="event-name">
                            ${incident.incident_id} — ${incident.summary}
                        </div>
                        <div class="event-path">
                            Threat score: ${incident.threat_score}
                        </div>
                    </div>
                    <span class="severity critical">
                        ${incident.severity.toUpperCase()}
                    </span>
                </div>
            `).join("");
        }

        const container = document.getElementById("events");

        if(!events.length){
            container.innerHTML = '<div class="empty">No events recorded yet.</div>';
        }else{
            container.innerHTML = events.map(event => {
                const severity = event.suspicious ? "critical" :
                    event.event_type === "file_modified" ? "warning" : "normal";

                const label = event.suspicious ? "CRITICAL" :
                    event.event_type === "file_modified" ? "WARNING" : "NORMAL";

                const icon = event.suspicious ? "⚠" :
                    event.event_type === "file_modified" ? "↻" : "✓";

                return `
                <div class="event">
                    <div class="event-icon">${icon}</div>
                    <div class="event-info">
                        <div class="event-name">${event.event_type}</div>
                        <div class="event-path">${event.path}</div>
                    </div>
                    <span class="severity ${severity}">${label}</span>
                </div>`;
            }).join("");
        }

    }catch(error){
        document.getElementById("events").innerHTML =
            '<div class="empty">Unable to load events.</div>';
    }
}

loadDashboard();
loadReport();
loadSettings();

setInterval(loadDashboard, 5000);
setInterval(loadReport, 10000);
</script>

</body>
</html>
"""
    return HTMLResponse(content=html)
