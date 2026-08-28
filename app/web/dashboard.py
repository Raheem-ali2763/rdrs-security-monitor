from fastapi.responses import HTMLResponse


def render_dashboard() -> HTMLResponse:
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>RDRS — Security Dashboard</title>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                min-height: 100vh;
                background: #080d19;
                color: #e8edf7;
                font-family:
                    Inter, ui-sans-serif, system-ui, -apple-system,
                    BlinkMacSystemFont, "Segoe UI", sans-serif;
            }

            .app {
                display: flex;
                min-height: 100vh;
            }

            /* Sidebar */
            .sidebar {
                width: 250px;
                padding: 24px 16px;
                border-right: 1px solid #1d2638;
                background: #0b1120;
            }

            .brand {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 8px 12px 30px;
            }

            .brand-icon {
                width: 40px;
                height: 40px;
                display: grid;
                place-items: center;
                border-radius: 12px;
                background: #17233a;
                font-size: 20px;
            }

            .brand-name {
                font-size: 19px;
                font-weight: 700;
            }

            .brand-subtitle {
                margin-top: 3px;
                color: #71809b;
                font-size: 11px;
                letter-spacing: .08em;
            }

            .nav-title {
                padding: 12px;
                color: #56647d;
                font-size: 10px;
                font-weight: 700;
                letter-spacing: .12em;
                text-transform: uppercase;
            }

            .nav-item {
                display: flex;
                align-items: center;
                gap: 12px;
                margin: 4px 0;
                padding: 12px;
                border-radius: 10px;
                color: #8491a8;
                font-size: 14px;
            }

            .nav-item.active {
                background: #16233a;
                color: #f1f5ff;
            }

            .nav-icon {
                width: 20px;
                text-align: center;
            }

            .sidebar-bottom {
                margin-top: 40px;
                padding: 14px;
                border: 1px solid #1d293e;
                border-radius: 12px;
                background: #0e1627;
            }

            .system-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 12px;
                color: #8491a8;
            }

            .online {
                color: #63df9b;
            }

            /* Main */
            .main {
                flex: 1;
                min-width: 0;
                padding: 28px 32px;
            }

            .topbar {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                gap: 20px;
                margin-bottom: 28px;
            }

            .eyebrow {
                color: #6e7d97;
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: .12em;
            }

            h1 {
                margin: 6px 0;
                font-size: 30px;
            }

            .description {
                margin: 0;
                color: #75839c;
                font-size: 14px;
            }

            .status {
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 9px 14px;
                border: 1px solid #194a35;
                border-radius: 999px;
                background: #0d281d;
                color: #67dfa0;
                font-size: 12px;
                font-weight: 600;
            }

            .status-dot {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: #67dfa0;
            }

            /* Metrics */
            .metrics {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 16px;
                margin-bottom: 20px;
            }

            .card {
                border: 1px solid #1d273a;
                border-radius: 15px;
                background: #0e1525;
            }

            .metric {
                padding: 20px;
            }

            .metric-label {
                color: #71809a;
                font-size: 12px;
            }

            .metric-value {
                margin-top: 12px;
                font-size: 30px;
                font-weight: 700;
            }

            .metric-change {
                margin-top: 7px;
                color: #63718a;
                font-size: 11px;
            }

            .metric-change.good {
                color: #58c991;
            }

            .metric-change.warning {
                color: #d6ae61;
            }

            /* Content */
            .grid {
                display: grid;
                grid-template-columns: 1.55fr 1fr;
                gap: 20px;
            }

            .panel {
                overflow: hidden;
            }

            .panel-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 18px 20px;
                border-bottom: 1px solid #1c2638;
            }

            .panel-title {
                font-size: 14px;
                font-weight: 650;
            }

            .panel-action {
                color: #70809b;
                font-size: 11px;
            }

            .activity {
                height: 280px;
                display: flex;
                align-items: flex-end;
                gap: 10px;
                padding: 25px;
            }

            .bar {
                flex: 1;
                min-width: 8px;
                border-radius: 5px 5px 2px 2px;
                background: #304666;
            }

            .bar.high {
                background: #76515d;
            }

            .bar.peak {
                background: #9a5b63;
            }

            .events {
                padding: 6px 0;
            }

            .event {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 14px 20px;
                border-bottom: 1px solid #172133;
            }

            .event:last-child {
                border-bottom: 0;
            }

            .event-icon {
                width: 32px;
                height: 32px;
                display: grid;
                place-items: center;
                border-radius: 9px;
                background: #172237;
            }

            .event-info {
                min-width: 0;
                flex: 1;
            }

            .event-name {
                overflow: hidden;
                color: #dce4f2;
                font-size: 12px;
                text-overflow: ellipsis;
                white-space: nowrap;
            }

            .event-path {
                margin-top: 4px;
                overflow: hidden;
                color: #596983;
                font-size: 10px;
                text-overflow: ellipsis;
                white-space: nowrap;
            }

            .severity {
                padding: 5px 8px;
                border-radius: 6px;
                font-size: 9px;
                font-weight: 700;
                letter-spacing: .05em;
            }

            .severity.normal {
                background: #15291f;
                color: #68ca94;
            }

            .severity.warning {
                background: #302818;
                color: #d8b461;
            }

            .severity.critical {
                background: #351c23;
                color: #e47d8d;
            }

            @media (max-width: 1050px) {
                .metrics {
                    grid-template-columns: repeat(2, 1fr);
                }

                .grid {
                    grid-template-columns: 1fr;
                }
            }

            @media (max-width: 720px) {
                .sidebar {
                    display: none;
                }

                .main {
                    padding: 20px;
                }

                .metrics {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>

    <body>
        <div class="app">

            <aside class="sidebar">
                <div class="brand">
                    <div class="brand-icon">🛡</div>
                    <div>
                        <div class="brand-name">RDRS</div>
                        <div class="brand-subtitle">SECURITY PLATFORM</div>
                    </div>
                </div>

                <div class="nav-title">Monitor</div>

                <div class="nav-item active">
                    <span class="nav-icon">⌂</span>
                    Overview
                </div>

                <div class="nav-item">
                    <span class="nav-icon">◉</span>
                    Events
                </div>

                <div class="nav-item">
                    <span class="nav-icon">⚠</span>
                    Incidents
                </div>

                <div class="nav-item">
                    <span class="nav-icon">◈</span>
                    Evidence
                </div>

                <div class="nav-title">Manage</div>

                <div class="nav-item">
                    <span class="nav-icon">▣</span>
                    Reports
                </div>

                <div class="nav-item">
                    <span class="nav-icon">⚙</span>
                    Settings
                </div>

                <div class="sidebar-bottom">
                    <div class="system-row">
                        <span>Detection engine</span>
                        <span class="online">ONLINE</span>
                    </div>
                    <div style="height:8px"></div>
                    <div class="system-row">
                        <span>Database</span>
                        <span class="online">CONNECTED</span>
                    </div>
                </div>
            </aside>

            <main class="main">

                <header class="topbar">
                    <div>
                        <div class="eyebrow">Security Operations</div>
                        <h1>Dashboard</h1>
                        <p class="description">
                            Real-time ransomware detection and response overview.
                        </p>
                    </div>

                    <div class="status">
                        <span class="status-dot"></span>
                        SYSTEM ONLINE
                    </div>
                </header>

                <section class="metrics">
                    <div class="card metric">
                        <div class="metric-label">THREAT SCORE</div>
                        <div class="metric-value">72</div>
                        <div class="metric-change warning">Elevated activity</div>
                    </div>

                    <div class="card metric">
                        <div class="metric-label">EVENTS TODAY</div>
                        <div class="metric-value">128</div>
                        <div class="metric-change good">Monitoring active</div>
                    </div>

                    <div class="card metric">
                        <div class="metric-label">ACTIVE INCIDENTS</div>
                        <div class="metric-value">3</div>
                        <div class="metric-change warning">Requires review</div>
                    </div>

                    <div class="card metric">
                        <div class="metric-label">FILES MONITORED</div>
                        <div class="metric-value">1,248</div>
                        <div class="metric-change good">Protection active</div>
                    </div>
                </section>

                <section class="grid">

                    <div class="card panel">
                        <div class="panel-header">
                            <span class="panel-title">Threat Activity</span>
                            <span class="panel-action">LAST 24 HOURS</span>
                        </div>

                        <div class="activity">
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
                            <span class="panel-action">VIEW ALL</span>
                        </div>

                        <div class="events">

                            <div class="event">
                                <div class="event-icon">⚠</div>
                                <div class="event-info">
                                    <div class="event-name">Entropy spike detected</div>
                                    <div class="event-path">data/sandbox/sample.bin</div>
                                </div>
                                <span class="severity critical">CRITICAL</span>
                            </div>

                            <div class="event">
                                <div class="event-icon">↻</div>
                                <div class="event-info">
                                    <div class="event-name">Mass file modification</div>
                                    <div class="event-path">data/sandbox/</div>
                                </div>
                                <span class="severity warning">WARNING</span>
                            </div>

                            <div class="event">
                                <div class="event-icon">✓</div>
                                <div class="event-info">
                                    <div class="event-name">File created</div>
                                    <div class="event-path">data/sandbox/report.txt</div>
                                </div>
                                <span class="severity normal">NORMAL</span>
                            </div>

                            <div class="event">
                                <div class="event-icon">✓</div>
                                <div class="event-info">
                                    <div class="event-name">File monitored</div>
                                    <div class="event-path">data/sandbox/</div>
                                </div>
                                <span class="severity normal">NORMAL</span>
                            </div>

                        </div>
                    </div>

                </section>

            </main>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=html)
