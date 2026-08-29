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
.nav-item{display:flex;text-decoration:none;cursor:pointer;align-items:center;gap:12px;margin:4px 0;padding:12px;border-radius:10px;color:#8491a8;font-size:14px}
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

/* =========================================================
   RDRS PREMIUM UI
   Modern SOC / Claude-inspired dark interface
   ========================================================= */

:root{
    --bg:#070b14;
    --bg2:#0a1020;
    --panel:#0d1424;
    --panel2:#10192c;
    --border:#1b2941;
    --border2:#243552;
    --text:#edf3ff;
    --muted:#71809b;
    --muted2:#53627b;
    --blue:#4c8dff;
    --purple:#8b5cf6;
    --cyan:#22d3ee;
    --green:#34d399;
    --yellow:#f59e0b;
    --red:#ef5365;
    --shadow:0 18px 45px rgba(0,0,0,.28);
}

*{
    scrollbar-width:thin;
    scrollbar-color:#263957 #080d19;
}

body{
    background:
        radial-gradient(circle at 75% -10%,rgba(76,141,255,.10),transparent 30%),
        radial-gradient(circle at 20% 20%,rgba(139,92,246,.06),transparent 28%),
        var(--bg);
    color:var(--text);
    letter-spacing:.005em;
}

.app{
    min-height:100vh;
    background:
        linear-gradient(90deg,rgba(255,255,255,.015) 1px,transparent 1px),
        linear-gradient(rgba(255,255,255,.012) 1px,transparent 1px);
    background-size:48px 48px;
}

/* SIDEBAR */

.sidebar{
    width:250px;
    padding:24px 15px;
    background:rgba(8,13,25,.88);
    border-right:1px solid rgba(91,113,150,.18);
    backdrop-filter:blur(18px);
    position:sticky;
    top:0;
    height:100vh;
}

.brand{
    padding:7px 11px 32px;
}

.brand-icon{
    width:42px;
    height:42px;
    border-radius:13px;
    background:
        linear-gradient(145deg,#18264b,#111a31);
    border:1px solid #26385c;
    box-shadow:
        0 0 24px rgba(76,141,255,.12),
        inset 0 1px rgba(255,255,255,.06);
}

.brand-name{
    font-size:18px;
    letter-spacing:.02em;
}

.brand-subtitle{
    color:#62728f;
    font-size:9px;
    letter-spacing:.12em;
}

.nav-title{
    color:#4f607d;
    margin-top:8px;
}

.nav-item{
    position:relative;
    margin:5px 0;
    padding:11px 12px;
    border:1px solid transparent;
    transition:.2s ease;
}

.nav-item:hover{
    color:#dfe8fa;
    background:rgba(76,141,255,.06);
    border-color:rgba(76,141,255,.10);
    transform:translateX(2px);
}

.nav-item.active{
    background:
        linear-gradient(90deg,rgba(76,141,255,.17),rgba(139,92,246,.08));
    border-color:rgba(76,141,255,.16);
    box-shadow:inset 3px 0 var(--blue);
}

.nav-icon{
    color:#7e8da8;
}

/* SIDEBAR STATUS */

.sidebar-bottom{
    margin-top:55px;
    padding:15px;
    border:1px solid #1b2b46;
    border-radius:14px;
    background:
        linear-gradient(145deg,rgba(18,29,51,.85),rgba(10,17,31,.8));
    box-shadow:var(--shadow);
}

.online{
    text-shadow:0 0 12px rgba(52,211,153,.35);
}

/* MAIN */

.main{
    padding:30px 34px 50px;
    max-width:1600px;
    width:100%;
    margin:auto;
}

.topbar{
    margin-bottom:25px;
}

.eyebrow{
    color:#6e8bb8;
    font-size:10px;
    font-weight:700;
    letter-spacing:.16em;
}

h1{
    font-size:31px;
    line-height:1.15;
    letter-spacing:-.035em;
    margin:7px 0;
}

.description{
    color:#697994;
    font-size:13px;
}

.status{
    padding:9px 15px;
    background:rgba(19,83,55,.28);
    border-color:rgba(52,211,153,.25);
    box-shadow:0 0 25px rgba(52,211,153,.06);
}

/* METRICS */

.metrics{
    gap:14px;
    margin-bottom:16px;
}

.card{
    background:
        linear-gradient(145deg,rgba(16,25,44,.94),rgba(10,17,31,.96));
    border:1px solid rgba(73,96,132,.22);
    border-radius:15px;
    box-shadow:
        0 10px 30px rgba(0,0,0,.18),
        inset 0 1px rgba(255,255,255,.025);
    transition:
        transform .2s ease,
        border-color .2s ease,
        box-shadow .2s ease;
}

.card:hover{
    border-color:rgba(91,125,178,.35);
    box-shadow:
        0 14px 38px rgba(0,0,0,.25),
        inset 0 1px rgba(255,255,255,.035);
}

.metric{
    min-height:118px;
    padding:18px 19px;
    position:relative;
    overflow:hidden;
}

.metric:after{
    content:"";
    position:absolute;
    width:90px;
    height:90px;
    right:-35px;
    bottom:-45px;
    border-radius:50%;
    background:rgba(76,141,255,.07);
    filter:blur(8px);
}

.metric-label{
    color:#687895;
    font-size:10px;
    font-weight:700;
    letter-spacing:.08em;
}

.metric-value{
    margin-top:10px;
    font-size:29px;
    letter-spacing:-.04em;
}

.metric-change{
    font-size:10px;
}

.good{
    color:#39d99a;
}

.warning{
    color:#e7b65b;
}

/* PANELS */

.grid{
    gap:16px;
}

.panel{
    border-radius:15px;
}

.panel-header{
    padding:16px 19px;
    background:rgba(255,255,255,.008);
    border-bottom:1px solid rgba(70,91,126,.18);
}

.panel-title{
    color:#e8effc;
    font-size:13px;
    font-weight:650;
    letter-spacing:.01em;
}

.panel-action{
    color:#61718d;
    font-size:9px;
    letter-spacing:.07em;
    text-transform:uppercase;
}

/* THREAT ACTIVITY */

.activity{
    height:280px;
    padding:25px 20px 20px;
    background:
        repeating-linear-gradient(
            to top,
            transparent 0,
            transparent 54px,
            rgba(100,125,165,.055) 55px
        );
}

.bar{
    background:
        linear-gradient(to top,#294b78,#4d78b5);
    border-radius:5px 5px 2px 2px;
    box-shadow:0 -4px 18px rgba(76,141,255,.08);
}

.bar.high{
    background:linear-gradient(to top,#70445d,#a15d71);
}

.bar.peak{
    background:linear-gradient(to top,#873f54,#d65d72);
    box-shadow:0 0 18px rgba(239,83,101,.18);
}


/* ===== PREMIUM RECENT EVENTS ===== */

#events-section{
    position:relative;
    overflow:hidden;
}

#events-section::before{
    content:"";
    position:absolute;
    inset:0;
    pointer-events:none;
    background:
        radial-gradient(
            circle at 90% 10%,
            rgba(77,126,255,.10),
            transparent 34%
        ),
        linear-gradient(
            120deg,
            transparent 0%,
            rgba(255,255,255,.018) 50%,
            transparent 100%
        );
}

#events{
    position:relative;
    max-height:280px;
    overflow:auto;
    scrollbar-width:thin;
    scrollbar-color:#30486c transparent;
}

#events::-webkit-scrollbar{
    width:5px;
}

#events::-webkit-scrollbar-track{
    background:transparent;
}

#events::-webkit-scrollbar-thumb{
    background:#30486c;
    border-radius:10px;
}

#events .event{
    position:relative;
    margin:0 12px;
    padding:13px 10px;
    border-bottom:1px solid rgba(100,125,165,.08);
    transition:
        background .25s ease,
        transform .25s ease,
        border-color .25s ease;
}

#events .event:hover{
    background:rgba(60,100,170,.075);
    transform:translateX(3px);
    border-color:rgba(90,140,230,.16);
}

#events .event::before{
    content:"";
    position:absolute;
    left:0;
    top:17px;
    width:3px;
    height:22px;
    border-radius:4px;
    background:#416da8;
    opacity:.65;
}

#events .event:has(.severity.critical)::before{
    background:#e95b72;
    box-shadow:0 0 12px rgba(233,91,114,.45);
}

#events .event-icon{
    width:28px;
    height:28px;
    display:flex;
    align-items:center;
    justify-content:center;
    border-radius:8px;
    background:rgba(54,84,130,.20);
    border:1px solid rgba(100,140,200,.14);
    box-shadow:inset 0 1px rgba(255,255,255,.035);
}

#events .event-info{
    min-width:0;
}

#events .event-name{
    font-size:11px;
    font-weight:600;
    letter-spacing:.02em;
    color:#dce6f7;
}

#events .event-path{
    margin-top:3px;
    max-width:270px;
    overflow:hidden;
    text-overflow:ellipsis;
    white-space:nowrap;
    font-size:9px;
    color:#667995;
}

#events .severity{
    padding:5px 8px;
    border-radius:999px;
    font-size:8px;
    font-weight:700;
    letter-spacing:.08em;
    border:1px solid transparent;
}

#events .severity.critical{
    color:#ff8798;
    background:rgba(197,57,81,.12);
    border-color:rgba(225,76,103,.22);
    box-shadow:0 0 14px rgba(210,60,82,.10);
}

#events .severity.warning{
    color:#e5b96d;
    background:rgba(190,137,45,.10);
    border-color:rgba(210,158,70,.18);
}

#events .severity.normal{
    color:#65d6a0;
    background:rgba(43,155,105,.09);
    border-color:rgba(67,190,130,.16);
}

#events .empty{
    min-height:210px;
    display:flex;
    align-items:center;
    justify-content:center;
    color:#50627d;
    font-size:10px;
    letter-spacing:.04em;
}


/* PREMIUM RECENT EVENTS */

#events-section{
    position:relative;
    overflow:hidden;
    background:
        radial-gradient(
            circle at 90% 0%,
            rgba(77,120,181,.10),
            transparent 42%
        ),
        linear-gradient(
            145deg,
            rgba(16,27,48,.98),
            rgba(8,15,29,.98)
        );
}

#events-section::before{
    content:"";
    position:absolute;
    top:0;
    left:0;
    right:0;
    height:1px;
    background:linear-gradient(
        90deg,
        transparent,
        rgba(77,141,255,.65),
        transparent
    );
    opacity:.7;
}

#events-section .panel-header{
    position:relative;
    z-index:2;
}

#events-section .panel-action{
    display:flex;
    align-items:center;
    gap:6px;
}

#events-section .panel-action::before{
    content:"";
    width:6px;
    height:6px;
    border-radius:50%;
    background:#55d6a5;
    box-shadow:0 0 10px rgba(85,214,165,.8);
    animation:eventLivePulse 1.8s ease-in-out infinite;
}

@keyframes eventLivePulse{
    0%,100%{
        opacity:.45;
        transform:scale(.85);
    }
    50%{
        opacity:1;
        transform:scale(1.15);
    }
}

#events-section .events{
    padding:4px 8px 8px;
}

#events-section .event{
    position:relative;
    margin:0;
    padding:11px 10px 11px 14px;
    border-bottom:1px solid rgba(112,140,180,.08);
    background:rgba(255,255,255,.008);
    transition:
        transform .22s ease,
        background .22s ease,
        box-shadow .22s ease;
}

#events-section .event:last-child{
    border-bottom:0;
}

#events-section .event:hover{
    transform:translateX(3px);
    background:rgba(65,105,170,.09);
    box-shadow:
        inset 2px 0 0 rgba(76,141,255,.8),
        0 8px 22px rgba(0,0,0,.14);
}

#events-section .event::before{
    content:"";
    position:absolute;
    left:0;
    top:50%;
    width:2px;
    height:28px;
    transform:translateY(-50%);
    border-radius:3px;
    background:rgba(76,141,255,.55);
}

#events-section .event:has(.severity.critical)::before{
    background:#ef5368;
    box-shadow:0 0 10px rgba(239,83,104,.45);
}

#events-section .event-icon{
    width:25px;
    height:25px;
    min-width:25px;
    display:flex;
    align-items:center;
    justify-content:center;
    border-radius:8px;
    background:
        linear-gradient(
            145deg,
            rgba(57,84,126,.45),
            rgba(20,34,58,.75)
        );
    border:1px solid rgba(107,139,184,.18);
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.05),
        0 4px 12px rgba(0,0,0,.18);
}

#events-section .event-info{
    min-width:0;
}

#events-section .event-name{
    font-size:11px;
    font-weight:600;
    color:#dce7f7;
    letter-spacing:.01em;
    text-transform:capitalize;
}

#events-section .event-path{
    margin-top:3px;
    max-width:250px;
    overflow:hidden;
    text-overflow:ellipsis;
    white-space:nowrap;
    font-size:9px;
    color:#657793;
}

#events-section .severity{
    padding:4px 8px;
    border-radius:999px;
    font-size:8px;
    font-weight:700;
    letter-spacing:.08em;
    border:1px solid rgba(255,255,255,.08);
    transition:.2s ease;
}

#events-section .severity.critical{
    color:#ff7185;
    background:rgba(157,42,63,.13);
    border-color:rgba(239,83,104,.28);
    box-shadow:
        inset 0 0 12px rgba(239,83,104,.04),
        0 0 10px rgba(239,83,104,.05);
}

#events-section .severity.warning{
    color:#e8b967;
    background:rgba(170,118,35,.10);
    border-color:rgba(232,185,103,.25);
}

#events-section .severity.normal{
    color:#63d8a6;
    background:rgba(48,145,104,.10);
    border-color:rgba(99,216,166,.22);
}

#events-section .event:hover .severity.critical{
    box-shadow:
        0 0 14px rgba(239,83,104,.16),
        inset 0 0 10px rgba(239,83,104,.05);
}

#events-section .empty{
    min-height:120px;
    display:flex;
    align-items:center;
    justify-content:center;
    color:#62728b;
}


/* =========================================================
   PREMIUM ACTIVE INCIDENTS
   ========================================================= */

#incidents{
    padding:6px 8px 10px;
}

#incidents .event-row{
    position:relative;
    display:flex;
    align-items:center;
    gap:16px;
    min-height:72px;
    margin:0;
    padding:13px 14px 13px 16px;
    border-bottom:1px solid rgba(112,140,180,.08);
    background:
        linear-gradient(
            90deg,
            rgba(255,255,255,.012),
            rgba(255,255,255,0)
        );
    transition:
        transform .22s ease,
        background .22s ease,
        box-shadow .22s ease;
}

#incidents .event-row:last-child{
    border-bottom:0;
}

#incidents .event-row::before{
    content:"";
    position:absolute;
    left:0;
    top:12px;
    bottom:12px;
    width:2px;
    border-radius:4px;
    background:#ef5368;
    box-shadow:0 0 12px rgba(239,83,104,.35);
}

#incidents .event-row:hover{
    transform:translateX(4px);
    background:
        linear-gradient(
            90deg,
            rgba(72,111,180,.10),
            rgba(72,111,180,.025)
        );
    box-shadow:
        inset 2px 0 0 rgba(76,141,255,.75),
        0 8px 24px rgba(0,0,0,.16);
}

#incidents .event-row strong{
    display:inline-flex;
    align-items:center;
    gap:7px;
    color:#e7effc;
    font-size:11px;
    font-weight:700;
    letter-spacing:.025em;
}

#incidents .event-row strong::before{
    content:"";
    width:7px;
    height:7px;
    border-radius:50%;
    background:#ef5368;
    box-shadow:
        0 0 7px rgba(239,83,104,.8),
        0 0 16px rgba(239,83,104,.3);
    animation:incidentPulse 1.8s ease-in-out infinite;
}

@keyframes incidentPulse{
    0%,100%{
        opacity:.55;
        transform:scale(.8);
    }
    50%{
        opacity:1;
        transform:scale(1.15);
    }
}

#incidents .event-row span{
    color:#8d9db7;
    font-size:10px;
}

#incidents .event-row .muted{
    margin-top:6px;
    color:#5f718e !important;
    font-size:9px;
    letter-spacing:.025em;
}

#incidents .severity{
    display:inline-flex;
    align-items:center;
    justify-content:center;
    min-width:58px;
    padding:5px 9px;
    border-radius:999px;
    font-size:8px;
    font-weight:800;
    letter-spacing:.08em;
    border:1px solid rgba(255,255,255,.08);
}

#incidents .severity.critical{
    color:#ff7185;
    background:
        linear-gradient(
            135deg,
            rgba(181,45,67,.18),
            rgba(90,24,40,.10)
        );
    border-color:rgba(239,83,104,.30);
    box-shadow:
        0 0 12px rgba(239,83,104,.07),
        inset 0 0 12px rgba(239,83,104,.04);
}

#incidents .severity.high{
    color:#ffad72;
    background:rgba(177,91,42,.12);
    border-color:rgba(255,173,114,.25);
}

#incidents .severity.medium{
    color:#e7c86d;
    background:rgba(173,137,40,.10);
    border-color:rgba(231,200,109,.22);
}

#incidents button{
    font-family:inherit;
    font-size:9px !important;
    font-weight:600;
    letter-spacing:.025em;
    padding:6px 10px !important;
    border-radius:7px !important;
    transition:
        transform .18s ease,
        box-shadow .18s ease,
        background .18s ease !important;
}

#incidents button:hover{
    transform:translateY(-1px);
}

#incidents button[onclick*="resolve"]{
    background:
        linear-gradient(
            135deg,
            rgba(25,75,56,.95),
            rgba(13,45,34,.95)
        ) !important;
    border-color:rgba(72,201,145,.35) !important;
    color:#70e0ac !important;
    box-shadow:0 0 12px rgba(72,201,145,.06);
}

#incidents button[onclick*="resolve"]:hover{
    box-shadow:
        0 0 18px rgba(72,201,145,.16),
        inset 0 0 10px rgba(72,201,145,.05);
}

#incidents button[onclick*="delete"]{
    background:
        linear-gradient(
            135deg,
            rgba(91,31,43,.90),
            rgba(45,19,27,.95)
        ) !important;
    border-color:rgba(239,83,104,.28) !important;
    color:#ed8796 !important;
}

#incidents button[onclick*="delete"]:hover{
    box-shadow:0 0 16px rgba(239,83,104,.13);
}

#incidents .empty{
    min-height:130px;
    display:flex;
    align-items:center;
    justify-content:center;
    color:#62728b;
}

/* subtle incident-panel atmosphere */

.card.panel:has(#incidents){
    position:relative;
    overflow:hidden;
    background:
        radial-gradient(
            circle at 100% 0%,
            rgba(239,83,104,.055),
            transparent 35%
        ),
        linear-gradient(
            145deg,
            rgba(15,26,47,.98),
            rgba(8,15,29,.98)
        );
}

.card.panel:has(#incidents)::after{
    content:"";
    position:absolute;
    width:180px;
    height:180px;
    right:-100px;
    top:-100px;
    border-radius:50%;
    background:rgba(76,141,255,.045);
    filter:blur(35px);
    pointer-events:none;
}


/* =========================================================
   PREMIUM FORENSIC EVIDENCE
   ========================================================= */

#evidence-section{
    position:relative;
    overflow:hidden;
    background:
        radial-gradient(
            circle at 92% 5%,
            rgba(65,139,255,.075),
            transparent 34%
        ),
        radial-gradient(
            circle at 5% 100%,
            rgba(72,201,145,.035),
            transparent 30%
        ),
        linear-gradient(
            145deg,
            rgba(14,25,45,.99),
            rgba(7,14,28,.99)
        );
}

#evidence-section::before{
    content:"";
    position:absolute;
    left:0;
    right:0;
    top:0;
    height:1px;
    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(76,141,255,.65),
            rgba(72,201,145,.35),
            transparent
        );
    opacity:.8;
}

#evidence-section .panel-header{
    position:relative;
    z-index:2;
}

#evidence-section .panel-action{
    display:flex;
    align-items:center;
    gap:7px;
}

#evidence-section .panel-action::before{
    content:"";
    width:6px;
    height:6px;
    border-radius:50%;
    background:#6ca5ff;
    box-shadow:0 0 10px rgba(108,165,255,.75);
    animation:evidencePulse 2s ease-in-out infinite;
}

@keyframes evidencePulse{
    0%,100%{
        opacity:.45;
        transform:scale(.8);
    }
    50%{
        opacity:1;
        transform:scale(1.15);
    }
}

#evidence-section .events{
    padding:5px 8px 10px;
}

#evidence-section .event-row{
    position:relative;
    display:grid;
    grid-template-columns:110px minmax(0,1fr);
    gap:18px;
    padding:16px 16px;
    border-bottom:1px solid rgba(112,140,180,.08);
    background:
        linear-gradient(
            90deg,
            rgba(255,255,255,.012),
            transparent
        );
    transition:
        transform .22s ease,
        background .22s ease,
        box-shadow .22s ease;
}

#evidence-section .event-row:last-child{
    border-bottom:0;
}

#evidence-section .event-row:hover{
    transform:translateX(3px);
    background:
        linear-gradient(
            90deg,
            rgba(70,112,180,.10),
            rgba(70,112,180,.018)
        );
    box-shadow:
        inset 2px 0 0 rgba(76,141,255,.65),
        0 8px 22px rgba(0,0,0,.14);
}

#evidence-section .event-row::before{
    content:"";
    position:absolute;
    left:0;
    top:16px;
    bottom:16px;
    width:2px;
    border-radius:4px;
    background:linear-gradient(
        to bottom,
        #4d8cff,
        rgba(77,140,255,.08)
    );
    opacity:.8;
}

#evidence-section .event-row > div:first-child{
    display:flex;
    align-items:flex-start;
}

#evidence-section .event-row strong{
    display:inline-flex;
    align-items:center;
    min-height:27px;
    padding:5px 9px;
    border-radius:7px;
    color:#bcd7ff;
    background:rgba(67,112,184,.10);
    border:1px solid rgba(91,142,219,.20);
    font-size:10px;
    letter-spacing:.04em;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.04);
}

#evidence-section .event-row > div:last-child{
    min-width:0;
}

#evidence-section .event-row > div:last-child > div:first-child{
    color:#dce6f5;
    font-size:11px;
    line-height:1.55;
    font-weight:500;
}

#evidence-section .muted{
    margin-top:7px;
    color:#687b98 !important;
    font-size:9px !important;
    line-height:1.6;
    letter-spacing:.025em;
}

#evidence-section .muted::before{
    content:"EVIDENCE PATH  ";
    color:#4e6d94;
    font-size:8px;
    font-weight:700;
    letter-spacing:.08em;
}

#evidence-section .event-row .muted:nth-of-type(2)::before{
    content:"TYPE  ";
}

#evidence-section .event-row .muted:nth-of-type(3)::before{
    content:"COLLECTED  ";
}

#evidence-section .empty{
    min-height:150px;
    display:flex;
    align-items:center;
    justify-content:center;
    color:#61728c;
    font-size:10px;
    letter-spacing:.02em;
}

#evidence-section .empty::before{
    content:"◈";
    margin-right:9px;
    color:#4d8cff;
    font-size:15px;
    opacity:.7;
}

/* forensic scan-line atmosphere */

#evidence-section::after{
    content:"";
    position:absolute;
    left:0;
    right:0;
    top:-20%;
    height:80px;
    background:linear-gradient(
        to bottom,
        transparent,
        rgba(92,151,255,.025),
        transparent
    );
    pointer-events:none;
    animation:evidenceScan 7s linear infinite;
}

@keyframes evidenceScan{
    from{
        transform:translateY(-20%);
    }
    to{
        transform:translateY(160%);
    }
}


/* =========================================================
   PREMIUM SYSTEM SETTINGS / CONTROL CENTER
   ========================================================= */

#settings-section{
    position:relative;
    overflow:hidden;
    min-height:330px;
    padding-bottom:24px !important;
    background:
        radial-gradient(
            circle at 92% 8%,
            rgba(76,141,255,.10),
            transparent 34%
        ),
        radial-gradient(
            circle at 55% 100%,
            rgba(72,201,145,.045),
            transparent 36%
        ),
        linear-gradient(
            145deg,
            rgba(14,25,45,.99),
            rgba(7,14,28,.99)
        );
}

#settings-section::before{
    content:"";
    position:absolute;
    top:0;
    left:0;
    right:0;
    height:1px;
    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(76,141,255,.7),
            rgba(72,201,145,.3),
            transparent
        );
}

#settings-section::after{
    content:"";
    position:absolute;
    width:300px;
    height:300px;
    right:-150px;
    top:-150px;
    border-radius:50%;
    background:rgba(76,141,255,.045);
    filter:blur(50px);
    pointer-events:none;
}

#settings-section .panel-header{
    position:relative;
    z-index:2;
    padding-bottom:15px;
}

#settings-section .panel-action{
    display:flex;
    align-items:center;
    gap:7px;
}

#settings-section .panel-action::before{
    content:"";
    width:6px;
    height:6px;
    border-radius:50%;
    background:#6ca5ff;
    box-shadow:0 0 10px rgba(108,165,255,.8);
    animation:settingsPulse 2s ease-in-out infinite;
}

@keyframes settingsPulse{
    0%,100%{
        opacity:.45;
        transform:scale(.8);
    }
    50%{
        opacity:1;
        transform:scale(1.15);
    }
}

/* settings content area */

#settings-section > div:not(.panel-header){
    position:relative;
    z-index:2;
}

#settings-section .settings-grid{
    display:grid;
    grid-template-columns:
        minmax(250px,1.35fr)
        minmax(180px,.8fr)
        minmax(180px,.8fr);
    gap:16px;
    padding:18px 18px 8px;
}

#settings-section .setting-card{
    position:relative;
    min-height:145px;
    padding:22px 20px;
    border-radius:12px;
    border:1px solid rgba(108,145,194,.13);
    background:
        linear-gradient(
            145deg,
            rgba(25,39,66,.55),
            rgba(10,20,36,.72)
        );
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.035),
        0 12px 30px rgba(0,0,0,.12);
    transition:
        transform .22s ease,
        border-color .22s ease,
        box-shadow .22s ease;
}

#settings-section .setting-card:hover{
    transform:translateY(-2px);
    border-color:rgba(92,145,221,.28);
    box-shadow:
        0 16px 35px rgba(0,0,0,.18),
        0 0 24px rgba(76,141,255,.045);
}

#settings-section .setting-label{
    color:#647895;
    font-size:8px;
    font-weight:700;
    letter-spacing:.12em;
    text-transform:uppercase;
}

#settings-section .setting-value{
    margin-top:12px;
    color:#e6eefb;
    font-size:22px;
    line-height:1.1;
    font-weight:700;
    letter-spacing:-.025em;
}

#settings-section .setting-description{
    margin-top:10px;
    color:#61728d;
    font-size:9px;
    line-height:1.6;
}

/* monitoring status */

#settings-section .monitoring-status{
    display:flex;
    align-items:center;
    gap:10px;
    margin-top:13px;
}

#settings-section .monitoring-status::before{
    content:"";
    width:9px;
    height:9px;
    border-radius:50%;
    background:#55d6a5;
    box-shadow:
        0 0 8px rgba(85,214,165,.8),
        0 0 18px rgba(85,214,165,.25);
    animation:monitoringPulse 1.8s ease-in-out infinite;
}

@keyframes monitoringPulse{
    0%,100%{
        opacity:.55;
    }
    50%{
        opacity:1;
    }
}

/* existing settings content fallback */

#settings-section .setting-content{
    padding:8px 18px 18px;
}

/* make current raw values breathe */

#settings-section .muted{
    color:#667995 !important;
    line-height:1.7;
}

/* premium control buttons */

#settings-section button{
    font-family:inherit;
    min-height:38px;
    padding:9px 16px !important;
    margin-top:16px;
    border-radius:8px !important;
    font-size:9px !important;
    font-weight:700;
    letter-spacing:.035em;
    transition:
        transform .18s ease,
        box-shadow .18s ease,
        border-color .18s ease;
}

#settings-section button:hover{
    transform:translateY(-1px);
}

#settings-section button[onclick*="stop"]{
    background:
        linear-gradient(
            135deg,
            rgba(105,34,48,.95),
            rgba(55,21,31,.95)
        ) !important;
    border-color:rgba(239,83,104,.32) !important;
    color:#ff8798 !important;
    box-shadow:0 0 16px rgba(239,83,104,.06);
}

#settings-section button[onclick*="stop"]:hover{
    box-shadow:
        0 0 20px rgba(239,83,104,.15),
        inset 0 0 12px rgba(239,83,104,.04);
}

#settings-section button[onclick*="start"]{
    background:
        linear-gradient(
            135deg,
            rgba(25,91,68,.95),
            rgba(13,51,39,.95)
        ) !important;
    border-color:rgba(72,201,145,.32) !important;
    color:#6fe1ad !important;
    box-shadow:0 0 16px rgba(72,201,145,.06);
}

/* responsive */

@media (max-width:900px){
    #settings-section .settings-grid{
        grid-template-columns:1fr 1fr;
    }
}

@media (max-width:620px){
    #settings-section{
        min-height:auto;
    }

    #settings-section .settings-grid{
        grid-template-columns:1fr;
        padding:14px 12px;
    }

    #settings-section .setting-card{
        min-height:120px;
    }
}


/* ===== PREMIUM SECURITY REPORT ===== */

#report-section{
    position:relative;
    overflow:hidden;
    margin-top:28px !important;
    padding:0 !important;
    border:1px solid rgba(100,145,210,.16);
    background:
        radial-gradient(circle at 85% 15%,rgba(80,130,220,.10),transparent 30%),
        linear-gradient(145deg,rgba(15,25,43,.98),rgba(9,16,29,.98));
    box-shadow:
        0 20px 60px rgba(0,0,0,.22),
        inset 0 1px 0 rgba(255,255,255,.025);
}

#report-section::before{
    content:"";
    position:absolute;
    top:0;
    left:0;
    right:0;
    height:1px;
    background:linear-gradient(
        90deg,
        transparent,
        rgba(91,146,235,.55),
        transparent
    );
}

#report-section .panel-header{
    padding:22px 24px;
    margin:0;
    border-bottom:1px solid rgba(100,125,165,.10);
}

#report-section .panel-title{
    font-size:14px;
    letter-spacing:.12em;
}

#report-section .panel-action{
    padding:7px 11px;
    border-radius:999px;
    border:1px solid rgba(83,150,255,.18);
    background:rgba(52,105,190,.08);
    color:#7eaeef;
}

#report{
    padding:24px;
}

.report-grid{
    display:grid;
    grid-template-columns:repeat(4,minmax(0,1fr));
    gap:16px;
}

.report-stat{
    position:relative;
    min-height:126px;
    padding:20px;
    border-radius:14px;
    border:1px solid rgba(105,135,180,.13);
    background:
        linear-gradient(
            145deg,
            rgba(25,39,64,.72),
            rgba(12,21,36,.76)
        );
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.025),
        0 10px 28px rgba(0,0,0,.12);
    transition:
        transform .22s ease,
        border-color .22s ease,
        box-shadow .22s ease;
}

.report-stat:hover{
    transform:translateY(-3px);
    border-color:rgba(90,150,245,.30);
    box-shadow:
        0 14px 35px rgba(0,0,0,.20),
        0 0 24px rgba(64,125,220,.07);
}

.report-stat::after{
    content:"";
    position:absolute;
    left:20px;
    right:20px;
    bottom:0;
    height:2px;
    border-radius:2px;
    background:linear-gradient(
        90deg,
        rgba(79,142,232,.0),
        rgba(79,142,232,.45),
        rgba(79,142,232,.0)
    );
    opacity:.45;
}

.report-stat.warning::after{
    background:linear-gradient(
        90deg,
        transparent,
        rgba(226,167,79,.65),
        transparent
    );
}

.report-stat.danger::after{
    background:linear-gradient(
        90deg,
        transparent,
        rgba(226,82,104,.72),
        transparent
    );
}

.report-stat.success::after{
    background:linear-gradient(
        90deg,
        transparent,
        rgba(83,202,142,.65),
        transparent
    );
}

.report-stat-label{
    color:#71809a;
    font-size:10px;
    font-weight:700;
    letter-spacing:.12em;
    text-transform:uppercase;
    margin-bottom:13px;
}

.report-stat-value{
    font-size:32px;
    line-height:1;
    font-weight:700;
    letter-spacing:-.04em;
    color:#edf4ff;
}

.report-stat-sub{
    margin-top:12px;
    color:#53627a;
    font-size:11px;
}

.report-actions{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:14px;
    padding:0 24px 24px;
    margin-top:2px;
}

.report-actions-copy{
    color:#596981;
    font-size:11px;
    letter-spacing:.03em;
}

.report-buttons{
    display:flex;
    gap:10px;
}

.report-btn{
    display:inline-flex;
    align-items:center;
    gap:8px;
    min-width:120px;
    justify-content:center;
    padding:11px 16px;
    border-radius:10px;
    border:1px solid rgba(91,142,220,.20);
    background:linear-gradient(
        145deg,
        rgba(32,55,88,.80),
        rgba(17,31,52,.90)
    );
    color:#b9cdef;
    font:inherit;
    font-size:11px;
    font-weight:700;
    letter-spacing:.05em;
    cursor:pointer;
    transition:all .2s ease;
}

.report-btn:hover{
    transform:translateY(-2px);
    border-color:rgba(91,154,245,.45);
    color:#e7f0ff;
    box-shadow:0 8px 24px rgba(52,111,205,.16);
}

.report-btn.primary{
    border-color:rgba(73,141,241,.28);
    background:linear-gradient(
        145deg,
        rgba(39,82,142,.92),
        rgba(25,54,94,.95)
    );
    color:#dbeaff;
}

.report-btn .btn-icon{
    font-size:14px;
    opacity:.8;
}

@media(max-width:900px){
    .report-grid{
        grid-template-columns:repeat(2,minmax(0,1fr));
    }
}

@media(max-width:560px){
    .report-grid{
        grid-template-columns:1fr;
    }

    .report-actions{
        align-items:stretch;
        flex-direction:column;
    }

    .report-buttons{
        width:100%;
    }

    .report-btn{
        flex:1;
    }
}


/* EVENTS */

.events{
    padding:3px 0;
}

.event{
    padding:12px 18px;
    border-bottom-color:rgba(67,88,120,.14);
    transition:.18s ease;
}

.event:hover{
    background:rgba(76,141,255,.035);
}

.event-icon{
    width:31px;
    height:31px;
    border:1px solid rgba(94,119,158,.16);
    background:#111c31;
}

.event-name{
    color:#dce6f7;
    font-size:11px;
}

.event-path{
    color:#586a87;
    font-size:9px;
}

.severity{
    border:1px solid transparent;
    font-size:8px;
}

.severity.normal{
    background:rgba(52,211,153,.10);
    border-color:rgba(52,211,153,.16);
}

.severity.warning{
    background:rgba(245,158,11,.10);
    border-color:rgba(245,158,11,.17);
}

.severity.critical{
    background:rgba(239,83,101,.11);
    border-color:rgba(239,83,101,.18);
}

/* EMPTY STATES */

.empty{
    padding:38px 20px;
    color:#53627c;
}

/* ALL LOWER SECTIONS */

section.card.panel[id]{
    margin-top:16px !important;
}

/* INCIDENTS */

#incidents{
    background:
        linear-gradient(145deg,rgba(14,22,39,.97),rgba(9,15,28,.98));
}

#incidents .panel-header{
    min-height:52px;
}

#incidents > div:not(.panel-header){
    border-color:rgba(69,91,125,.14);
}

/* EVIDENCE */

#evidence-section{
    background:
        linear-gradient(145deg,rgba(13,22,39,.97),rgba(8,15,28,.98));
}

#evidence-section .panel-header{
    min-height:52px;
}

/* SETTINGS */

#settings-section{
    position:relative;
    overflow:hidden;
    background:
        radial-gradient(circle at 90% 55%,rgba(52,211,153,.07),transparent 22%),
        linear-gradient(145deg,rgba(14,23,41,.98),rgba(8,15,28,.98));
}

#settings-section:after{
    content:"";
    position:absolute;
    right:-100px;
    top:-100px;
    width:260px;
    height:260px;
    border:1px solid rgba(52,211,153,.06);
    border-radius:50%;
    box-shadow:
        0 0 0 35px rgba(52,211,153,.025),
        0 0 0 70px rgba(52,211,153,.015);
    pointer-events:none;
}

#settings-section .panel-header{
    min-height:52px;
}

#settings-section button{
    border-radius:8px;
    padding:8px 12px;
    font-size:10px;
    cursor:pointer;
    transition:.2s ease;
}

#settings-section button:hover{
    transform:translateY(-1px);
}

/* REPORT */

#report-section{
    background:
        linear-gradient(145deg,rgba(15,24,43,.98),rgba(9,16,30,.98));
}

#report-section .panel-header{
    min-height:52px;
}

#report-section button{
    border:1px solid rgba(76,141,255,.18);
    background:linear-gradient(135deg,rgba(76,141,255,.16),rgba(139,92,246,.14));
    color:#dfeaff;
    border-radius:9px;
    padding:9px 14px;
    cursor:pointer;
    transition:.2s ease;
}

#report-section button:hover{
    border-color:rgba(76,141,255,.4);
    box-shadow:0 0 20px rgba(76,141,255,.10);
    transform:translateY(-1px);
}

/* BUTTONS GENERALLY */

button{
    font-family:inherit;
}

button:not([disabled]):hover{
    filter:brightness(1.08);
}

/* MOBILE */

@media(max-width:1100px){
    .sidebar{
        width:220px;
    }

    .main{
        padding:24px;
    }
}

@media(max-width:850px){
    .sidebar{
        display:none;
    }

    .main{
        padding:18px;
    }

    .metrics{
        grid-template-columns:repeat(2,1fr);
    }
}

@media(max-width:560px){
    .metrics{
        grid-template-columns:1fr;
    }

    h1{
        font-size:25px;
    }

    .topbar{
        flex-direction:column;
    }
}


/* =========================================================
   PREMIUM SYSTEM SETTINGS
   ========================================================= */

.settings-premium {
    position: relative;
    overflow: hidden;
    margin-top: 30px !important;
    border: 1px solid rgba(100,145,210,.18);
    background:
        radial-gradient(circle at 90% 0%, rgba(70,125,220,.10), transparent 32%),
        radial-gradient(circle at 5% 100%, rgba(60,180,150,.055), transparent 28%),
        linear-gradient(145deg, rgba(15,23,38,.98), rgba(9,15,27,.98));
    box-shadow:
        0 18px 55px rgba(0,0,0,.28),
        inset 0 1px rgba(255,255,255,.035);
}

.settings-premium::before {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    background:
        linear-gradient(115deg,
            transparent 0%,
            rgba(120,180,255,.035) 45%,
            transparent 70%);
    transform: translateX(-100%);
    animation: settingsSweep 7s ease-in-out infinite;
}

.settings-header {
    position: relative;
    padding: 22px 24px !important;
    min-height: 72px;
}

.settings-subtitle {
    margin-top: 7px;
    color: #70819d;
    font-size: 11px;
    letter-spacing: .045em;
}

.settings-live {
    padding: 7px 11px;
    border: 1px solid rgba(75,210,155,.18);
    border-radius: 999px;
    background: rgba(45,160,115,.07);
    color: #72dca9;
    box-shadow: 0 0 18px rgba(55,205,145,.06);
}

.settings-content {
    padding: 10px 24px 30px !important;
}

.settings-content .settings-row {
    display: grid !important;
    grid-template-columns: 1.15fr 1fr;
    gap: 18px;
    padding: 0 !important;
}

.settings-content .settings-row > div {
    position: relative;
    min-height: 128px;
    padding: 24px 22px;
    border: 1px solid rgba(110,145,195,.13);
    border-radius: 14px;
    background:
        linear-gradient(145deg,
            rgba(23,34,54,.82),
            rgba(13,21,35,.72));
    box-shadow:
        inset 0 1px rgba(255,255,255,.025),
        0 12px 30px rgba(0,0,0,.12);
    transition:
        transform .25s ease,
        border-color .25s ease,
        box-shadow .25s ease;
}

.settings-content .settings-row > div:hover {
    transform: translateY(-2px);
    border-color: rgba(100,165,235,.28);
    box-shadow:
        0 16px 38px rgba(0,0,0,.2),
        0 0 25px rgba(65,135,230,.055);
}

.settings-content .metric-label {
    margin-bottom: 10px;
    color: #72839f;
    font-size: 10px;
    letter-spacing: .12em;
}

.settings-content .metric-value {
    color: #edf4ff;
    font-weight: 600;
    letter-spacing: -.02em;
}

.settings-content button {
    margin-top: 15px !important;
    min-width: 150px;
    padding: 10px 15px !important;
    border-radius: 9px !important;
    font-weight: 600;
    letter-spacing: .01em;
    transition:
        transform .2s ease,
        box-shadow .2s ease,
        filter .2s ease;
}

.settings-content button:hover {
    transform: translateY(-2px);
    filter: brightness(1.12);
}

@keyframes settingsSweep {
    0%, 65%, 100% {
        transform: translateX(-100%);
        opacity: 0;
    }
    72% {
        opacity: 1;
    }
    88% {
        transform: translateX(100%);
        opacity: 1;
    }
}

@media (max-width: 760px) {
    .settings-content .settings-row {
        grid-template-columns: 1fr;
    }

    .settings-content {
        padding-left: 16px !important;
        padding-right: 16px !important;
    }

    .settings-header {
        padding-left: 18px !important;
        padding-right: 18px !important;
    }
}

</style>

<style id="rdrs-evidence-premium">
/* ===== PREMIUM EVIDENCE SOC PANEL ===== */

#evidence-section {
    position: relative !important;
    overflow: hidden !important;
    margin-top: 28px !important;
    border: 1px solid rgba(88,166,255,.16) !important;
    border-radius: 18px !important;
    background:
        radial-gradient(circle at 92% 10%, rgba(70,130,255,.10), transparent 28%),
        radial-gradient(circle at 8% 90%, rgba(0,220,180,.055), transparent 25%),
        linear-gradient(145deg, rgba(15,24,42,.98), rgba(8,15,29,.98)) !important;
    box-shadow:
        0 18px 60px rgba(0,0,0,.28),
        inset 0 1px 0 rgba(255,255,255,.035) !important;
    transform: translateZ(0);
}

#evidence-section::before {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    background:
        linear-gradient(
            90deg,
            transparent 0%,
            rgba(90,170,255,.035) 48%,
            rgba(90,170,255,.09) 50%,
            rgba(90,170,255,.035) 52%,
            transparent 100%
        );
    background-size: 220% 100%;
    animation: evidenceScan 7s linear infinite;
}

#evidence-section::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(73,160,255,.75),
        rgba(0,235,190,.55),
        transparent
    );
    animation: evidenceLine 4s ease-in-out infinite;
}

#evidence-section .panel-header,
#evidence-section .panel-title {
    position: relative;
    z-index: 2;
}

#evidence-section .panel-title {
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: .04em !important;
    text-transform: uppercase !important;
}

#evidence-section .panel-subtitle,
#evidence-section small {
    opacity: .55;
    letter-spacing: .08em;
    text-transform: uppercase;
}

#evidence-section > div:not(.panel-header),
#evidence-section .evidence-item {
    position: relative;
    z-index: 2;
}

#evidence-section .evidence-item {
    margin: 10px 12px !important;
    padding: 16px 18px !important;
    border: 1px solid rgba(255,255,255,.055) !important;
    border-radius: 12px !important;
    background: linear-gradient(
        135deg,
        rgba(255,255,255,.025),
        rgba(255,255,255,.008)
    ) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.025);
    transition:
        transform .25s ease,
        border-color .25s ease,
        box-shadow .25s ease,
        background .25s ease;
}

#evidence-section .evidence-item:hover {
    transform: translateY(-3px) translateX(2px);
    border-color: rgba(74,158,255,.28) !important;
    background: linear-gradient(
        135deg,
        rgba(55,120,220,.09),
        rgba(255,255,255,.018)
    ) !important;
    box-shadow:
        0 12px 30px rgba(0,0,0,.22),
        0 0 25px rgba(50,130,255,.055);
}

@keyframes evidenceScan {
    0%   { background-position: 220% 0; }
    100% { background-position: -220% 0; }
}

@keyframes evidenceLine {
    0%,100% { opacity: .25; transform: scaleX(.35); }
    50%     { opacity: 1; transform: scaleX(1); }
}

@media (prefers-reduced-motion: reduce) {
    #evidence-section::before,
    #evidence-section::after {
        animation: none;
    }
}
</style>


<style id="rdrs-settings-premium">
/* ===== PREMIUM SYSTEM SETTINGS ===== */

#settings-section {
    position: relative !important;
    overflow: hidden !important;
    margin-top: 28px !important;
    border: 1px solid rgba(74,158,255,.15) !important;
    border-radius: 18px !important;
    background:
        radial-gradient(circle at 88% 18%, rgba(0,210,180,.075), transparent 27%),
        radial-gradient(circle at 12% 90%, rgba(80,130,255,.07), transparent 30%),
        linear-gradient(145deg, rgba(15,24,42,.98), rgba(7,14,27,.98)) !important;
    box-shadow:
        0 18px 55px rgba(0,0,0,.28),
        inset 0 1px 0 rgba(255,255,255,.035) !important;
}

#settings-section::before {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    background:
        linear-gradient(
            115deg,
            transparent 0%,
            transparent 42%,
            rgba(0,220,190,.045) 50%,
            transparent 58%,
            transparent 100%
        );
    background-size: 240% 240%;
    animation: settingsSweep 9s linear infinite;
}

#settings-section::after {
    content: "";
    position: absolute;
    top: 0;
    left: 7%;
    right: 7%;
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(72,160,255,.7),
        rgba(0,230,190,.65),
        transparent
    );
    animation: settingsPulse 4s ease-in-out infinite;
}

#settings-section > * {
    position: relative;
    z-index: 2;
}

#settings-section .panel-title {
    font-size: 13px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: .08em !important;
}

#settings-section button {
    border-radius: 9px !important;
    padding: 9px 15px !important;
    font-weight: 600 !important;
    letter-spacing: .02em !important;
    transition:
        transform .22s ease,
        box-shadow .22s ease,
        border-color .22s ease,
        background .22s ease !important;
}

#settings-section button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(0,0,0,.25) !important;
}

#settings-section button[onclick*="stop"] {
    border: 1px solid rgba(255,75,95,.32) !important;
    background: rgba(170,35,55,.12) !important;
    color: #ff8b98 !important;
}

#settings-section button[onclick*="stop"]:hover {
    border-color: rgba(255,75,95,.65) !important;
    background: rgba(190,40,60,.2) !important;
    box-shadow: 0 0 24px rgba(255,65,85,.12) !important;
}

#settings-section button[onclick*="start"] {
    border: 1px solid rgba(0,225,180,.3) !important;
    background: rgba(0,180,145,.11) !important;
    color: #63e6c7 !important;
}

#settings-section button[onclick*="start"]:hover {
    border-color: rgba(0,240,190,.65) !important;
    background: rgba(0,190,155,.18) !important;
    box-shadow: 0 0 24px rgba(0,220,180,.12) !important;
}

@keyframes settingsSweep {
    0%   { background-position: 240% 0%; }
    100% { background-position: -240% 100%; }
}

@keyframes settingsPulse {
    0%,100% { opacity: .25; transform: scaleX(.45); }
    50%     { opacity: .9; transform: scaleX(1); }
}

@media (prefers-reduced-motion: reduce) {
    #settings-section::before,
    #settings-section::after {
        animation: none;
    }
}
</style>


<style id="rdrs-metric-premium">
/* ===== RDRS PREMIUM METRIC CARDS ===== */
.metric-card,
.stat-card,
.kpi-card {
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(120,150,190,.16) !important;
    border-radius: 16px !important;
    background:
        radial-gradient(circle at 90% 0%, rgba(70,130,255,.13), transparent 42%),
        linear-gradient(145deg, rgba(18,29,52,.96), rgba(9,16,30,.98)) !important;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.045),
        0 10px 35px rgba(0,0,0,.20) !important;
    transition:
        transform .28s ease,
        border-color .28s ease,
        box-shadow .28s ease !important;
}

.metric-card::before,
.stat-card::before,
.kpi-card::before {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    background:
        linear-gradient(
            115deg,
            transparent 25%,
            rgba(255,255,255,.055) 45%,
            transparent 65%
        );
    transform: translateX(-110%);
    transition: transform .7s ease;
}

.metric-card:hover,
.stat-card:hover,
.kpi-card:hover {
    transform: translateY(-5px) scale(1.012);
    border-color: rgba(90,160,255,.38) !important;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.07),
        0 16px 45px rgba(0,0,0,.30),
        0 0 28px rgba(60,130,255,.08) !important;
}

.metric-card:hover::before,
.stat-card:hover::before,
.kpi-card:hover::before {
    transform: translateX(110%);
}

.metric-card .value,
.stat-card .value,
.kpi-card .value,
.metric-value,
.stat-value,
.kpi-value {
    font-weight: 700 !important;
    letter-spacing: -.035em;
    text-shadow: 0 0 22px rgba(100,160,255,.16);
}

.metric-card .label,
.stat-card .label,
.kpi-card .label {
    letter-spacing: .10em;
    text-transform: uppercase;
    opacity: .62;
}

.metric-card:first-child,
.stat-card:first-child,
.kpi-card:first-child {
    background:
        radial-gradient(circle at 90% 0%, rgba(255,80,100,.16), transparent 44%),
        linear-gradient(145deg, rgba(30,25,43,.98), rgba(12,16,29,.98)) !important;
}

@keyframes rdrsCardPulse {
    0%,100% { box-shadow: 0 0 0 rgba(80,150,255,0); }
    50% { box-shadow: 0 0 24px rgba(80,150,255,.055); }
}

.metric-card,
.stat-card,
.kpi-card {
    animation: rdrsCardPulse 4s ease-in-out infinite;
}
</style>


<style id="rdrs-threat-premium">
/* ===== PREMIUM LIVE THREAT ACTIVITY ===== */

#activity {
    position: relative;
    display: flex;
    align-items: flex-end;
    gap: 9px;
    overflow: hidden;
    perspective: 900px;
    isolation: isolate;
    border-radius: 0 0 14px 14px;
}

/* subtle futuristic grid */
#activity::before {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background:
        linear-gradient(rgba(100,150,220,.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(100,150,220,.035) 1px, transparent 1px);
    background-size: 42px 42px;
    mask-image: linear-gradient(to bottom, transparent, black 25%, black 80%, transparent);
}

/* moving scanner */
#activity::after {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    height: 2px;
    top: 10%;
    pointer-events: none;
    z-index: 5;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(80,170,255,.05),
        rgba(100,190,255,.65),
        rgba(80,170,255,.05),
        transparent
    );
    box-shadow: 0 0 18px rgba(80,170,255,.35);
    animation: rdrsScanner 4.5s ease-in-out infinite;
}

#activity .bar {
    position: relative;
    z-index: 2;
    flex: 1 1 0;
    min-width: 10px;
    transform-origin: bottom center;
    transform: translateZ(0) rotateX(0deg);
    border-radius: 7px 7px 3px 3px;
    filter: saturate(1.08);
    box-shadow:
        inset 1px 0 rgba(255,255,255,.08),
        inset -1px 0 rgba(0,0,0,.15),
        0 -8px 22px rgba(65,140,255,.08);
    animation:
        rdrsBarFloat 3.2s ease-in-out infinite,
        rdrsBarGlow 2.8s ease-in-out infinite;
    transition:
        height .8s cubic-bezier(.2,.8,.2,1),
        transform .3s ease,
        filter .3s ease;
}

#activity .bar:nth-child(2n) {
    animation-delay: -.8s;
}

#activity .bar:nth-child(3n) {
    animation-delay: -1.5s;
}

#activity .bar:nth-child(4n) {
    animation-delay: -2.1s;
}

#activity .bar:hover {
    transform: translateY(-5px) scaleX(1.08) scaleY(1.02);
    filter: brightness(1.25) saturate(1.2);
    z-index: 4;
}

#activity .bar::after {
    content: "";
    position: absolute;
    left: 8%;
    right: 8%;
    top: 0;
    height: 2px;
    border-radius: 50%;
    background: rgba(255,255,255,.32);
    box-shadow: 0 0 12px rgba(120,190,255,.35);
}

#activity .bar.high {
    box-shadow:
        inset 1px 0 rgba(255,255,255,.08),
        0 -8px 25px rgba(190,80,110,.12);
}

#activity .bar.peak {
    box-shadow:
        inset 1px 0 rgba(255,255,255,.12),
        0 -10px 35px rgba(240,75,105,.28);
    animation:
        rdrsBarFloat 3s ease-in-out infinite,
        rdrsPeakPulse 1.8s ease-in-out infinite;
}

@keyframes rdrsScanner {
    0%   { top: 8%; opacity: 0; }
    12%  { opacity: 1; }
    50%  { opacity: .85; }
    88%  { opacity: 1; }
    100% { top: 92%; opacity: 0; }
}

@keyframes rdrsBarFloat {
    0%,100% {
        transform: translateY(0) scaleY(1);
    }
    50% {
        transform: translateY(-2px) scaleY(1.015);
    }
}

@keyframes rdrsBarGlow {
    0%,100% {
        filter: brightness(.98) saturate(1);
    }
    50% {
        filter: brightness(1.08) saturate(1.08);
    }
}

@keyframes rdrsPeakPulse {
    0%,100% {
        filter: brightness(1) saturate(1);
        box-shadow:
            inset 1px 0 rgba(255,255,255,.12),
            0 -10px 28px rgba(240,75,105,.18);
    }
    50% {
        filter: brightness(1.18) saturate(1.15);
        box-shadow:
            inset 1px 0 rgba(255,255,255,.16),
            0 -10px 42px rgba(240,75,105,.38);
    }
}

@media (prefers-reduced-motion: reduce) {
    #activity::after,
    #activity .bar {
        animation: none !important;
    }
}
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
<a class="nav-item active" href="#overview"><span class="nav-icon">⌂</span>Overview</a>
<a class="nav-item" href="#events-section"> <span class="nav-icon">◉</span>Events</a>
<a class="nav-item" href="#incidents" onclick="document.getElementById('incidents').scrollIntoView({behavior:'smooth',block:'start'}); return false;"><span class="nav-icon">⚠</span>Incidents</a>
<a class="nav-item" href="#evidence-section" onclick="document.getElementById('evidence-section').scrollIntoView({behavior:'smooth',block:'start'}); return false;"><span class="nav-icon">◈</span>Evidence</a>

<div class="nav-title">Manage</div>
<a class="nav-item" href="#report-section"><span class="nav-icon">▣</span>Reports</a>
<a class="nav-item" href="#settings-section" onclick="document.getElementById('settings-section').scrollIntoView({behavior:'smooth',block:'start'}); return false;"><span class="nav-icon">⚙</span>Settings</a>

<div class="sidebar-bottom">
<div class="system-row"><span>Detection engine</span><span class="online">ONLINE</span></div>
<div style="height:8px"></div>
<div class="system-row"><span>Database</span><span class="online">CONNECTED</span></div>
</div>
</aside>

<main class="main" id="overview">

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

<div class="card panel" id="events-section">
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

<section id="evidence-section" class="card panel" style="margin-top:20px">
<div class="panel-header">
<span class="panel-title">Evidence</span>
<span class="panel-action">INCIDENT EVIDENCE</span>
</div>
<div id="evidence" class="events">
<div class="empty">Select an incident to view its evidence.</div>
</div>
</section>

<section class="card panel settings-premium" id="settings-section" style="margin-top:28px">
<div class="panel-header settings-header">
<div>
        <span class="panel-title">System Settings</span>
        <div class="settings-subtitle">RDRS protection and monitoring controls</div>
    </div>
    <span class="panel-action settings-live">● SYSTEM ONLINE</span>
</div>
<div id="settings" class="settings-content">
    <div class="empty">Loading settings...</div>
</div>
</section>

<section class="card panel" id="report-section" style="margin-top:20px">
<div class="panel-header">
<span class="panel-title">Security Report</span>
    <span class="panel-action">LIVE SUMMARY</span>
</div>
<div id="report">
    <div class="report-grid">

        <div class="report-stat">
            <div class="report-stat-label">Total Events</div>
            <div id="report-total-events" class="report-stat-value">--</div>
            <div class="report-stat-sub">All recorded activity</div>
        </div>

        <div class="report-stat warning">
            <div class="report-stat-label">Suspicious Events</div>
            <div id="report-suspicious-events" class="report-stat-value">--</div>
            <div class="report-stat-sub">Requires investigation</div>
        </div>

        <div class="report-stat danger">
            <div class="report-stat-label">Total Incidents</div>
            <div id="report-total-incidents" class="report-stat-value">--</div>
            <div class="report-stat-sub">Detected security incidents</div>
        </div>

        <div class="report-stat success">
            <div class="report-stat-label">Resolved Incidents</div>
            <div id="report-resolved-incidents" class="report-stat-value">--</div>
            <div class="report-stat-sub">Successfully closed</div>
        </div>

    </div>
</div>

<div class="report-actions">
    <div class="report-actions-copy">
        Export the current security intelligence snapshot
    </div>

    <div class="report-buttons">
        <button class="report-btn"
                onclick="downloadLatestReport('json')">
            <span class="btn-icon">↗</span>
            JSON Report
        </button>

        <button class="report-btn primary"
                onclick="downloadLatestReport('csv')">
            <span class="btn-icon">↓</span>
            CSV Report
        </button>
    </div>
</div>
</section>



<section class="card panel" style="margin-top:20px">

<div id="incidents_secondary" class="events">
    <div class="empty">Loading incidents...</div>
</div>
</section>


</main>
</div>

<script>

async function loadSettings() {
    const el = document.getElementById("settings");
    const el2 = document.getElementById("settings_secondary");
    if (!el) return;

    try {
        const response = await fetch("/api/settings");
        if (!response.ok) throw new Error("settings request failed");

        const settings = await response.json();

        const html = `
            <div class="settings-grid">

                <div class="settings-card">
                    <div class="settings-label">Monitoring Status</div>

                    <div class="settings-control">
                        <div>
                            <div class="settings-value">
                                ${settings.monitoring_enabled ? "Active" : "Offline"}
                            </div>

                            <div style="margin-top:13px">
                                <span class="settings-status ${settings.monitoring_enabled ? "" : "off"}">
                                    <span class="settings-status-dot"></span>
                                    ${settings.monitoring_enabled
                                        ? "SYSTEM MONITORING"
                                        : "MONITORING STOPPED"}
                                </span>
                            </div>
                        </div>

                        ${
                            settings.monitoring_enabled
                            ? `<button class="settings-btn stop"
                                onclick="serviceAction('stop')">
                                Stop Monitoring
                              </button>`
                            : `<button class="settings-btn start"
                                onclick="serviceAction('start')">
                                Start Monitoring
                              </button>`
                        }
                    </div>

                    <div class="settings-description">
                        Real-time file activity detection and threat analysis.
                    </div>
                </div>

                <div class="settings-card">
                    <div class="settings-label">Monitored Path</div>

                    <div class="settings-value">
                        Protected Workspace
                    </div>

                    <div class="settings-path">
                        ${settings.monitored_path}
                    </div>

                    <div class="settings-description">
                        Files created, modified, or removed inside this location
                        are inspected by the detection pipeline.
                    </div>
                </div>

                <div class="settings-card full">
                    <div class="settings-label">Detection Engine</div>

                    <div class="settings-control">
                        <div>
                            <div class="settings-value">
                                RDRS Detection Pipeline
                            </div>

                            <div class="settings-description">
                                Entropy analysis, event processing and incident
                                generation are operating through the active
                                monitoring service.
                            </div>
                        </div>

                        <span class="settings-status">
                            <span class="settings-status-dot"></span>
                            OPERATIONAL
                        </span>
                    </div>
                </div>

            </div>
        `;        el.innerHTML = html;
        if (el2) el2.innerHTML = html;
    } catch (error) {
        console.error("Settings:", error);
        el.innerHTML = '<div class="empty">Unable to load settings.</div>';
    }
}

async function loadReport() {
    const el = document.getElementById("report");
    if (!el) return;

    try {
        const response = await fetch("/api/reports/summary");
        if (!response.ok) throw new Error("report request failed");

        const report = await response.json();

        const totalEvents =
            report.total_events ?? 0;

        const suspiciousEvents =
            report.suspicious_events ?? 0;

        const totalIncidents =
            report.total_incidents ?? 0;

        const resolvedIncidents =
            report.resolved_incidents ?? 0;

        const totalEl =
            document.getElementById("report-total-events");

        const suspiciousEl =
            document.getElementById("report-suspicious-events");

        const incidentsEl =
            document.getElementById("report-total-incidents");

        const resolvedEl =
            document.getElementById("report-resolved-incidents");

        if (totalEl) totalEl.textContent = totalEvents;
        if (suspiciousEl) suspiciousEl.textContent = suspiciousEvents;
        if (incidentsEl) incidentsEl.textContent = totalIncidents;
        if (resolvedEl) resolvedEl.textContent = resolvedIncidents;
    } catch (error) {
        console.error("Report:", error);
        el.innerHTML = '<div class="empty">Unable to load report.</div>';
    }
}



async function loadEvidence(id) {
    const el = document.getElementById("evidence");

    if (!el) return;

    el.innerHTML = '<div class="empty">Loading evidence...</div>';

    try {
        const response = await fetch(`/api/incidents/${id}/evidence`);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const evidence = await response.json();

        if (!evidence.length) {
            el.innerHTML =
                '<div class="empty">No evidence recorded for this incident.</div>';
            return;
        }

        el.innerHTML = evidence.map(item => `
            <div class="event">
                <div class="event-icon">◈</div>
                <div class="event-info">
                    <div class="event-name">
                        ${item.evidence_type || item.type || "Evidence"}
                    </div>
                    <div class="event-path">
                        ${item.description || item.path || item.value || "Evidence recorded"}
                    </div>
                </div>
                <span class="severity normal">EVIDENCE</span>
            </div>
        `).join("");

        document.getElementById("evidence-section")?.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    } catch (error) {
        console.error("Evidence:", error);
        el.innerHTML =
            '<div class="empty">Unable to load evidence.</div>';
    }
}

async function incidentAction(id, action) {
    try {
        const response = await fetch(`/api/incidents/${id}/${action}`, {
            method: "POST"
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        await loadDashboard();
loadEvidence();
        await loadReport();
    } catch (error) {
        console.error(`Incident ${action}:`, error);
        alert(`Unable to ${action} incident.`);
    }
}

async function deleteIncident(id) {
    if (!confirm("Delete this incident?")) return;

    try {
        const response = await fetch(`/api/incidents/${id}`, {
            method: "DELETE"
        });

        if (!response.ok && response.status !== 204) {
            throw new Error(`HTTP ${response.status}`);
        }

        await loadDashboard();
        await loadReport();
    } catch (error) {
        console.error("Delete incident:", error);
        alert("Unable to delete incident.");
    }
}

async function serviceAction(action) {
    try {
        const response = await fetch(`/api/service/${action}`, {
            method: "POST"
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        await loadSettings();
        await loadDashboard();
    } catch (error) {
        console.error(`Service ${action}:`, error);
        alert(`Unable to ${action} monitoring service.`);
    }
}


function goToSection(sectionId) {
    const section = document.getElementById(sectionId);

    if (!section) {
        console.error("Section not found:", sectionId);
        return;
    }

    section.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


async function loadEvidence() {
    const container = document.getElementById("evidence");
    if (!container) return;

    try {
        const incidentsRes = await fetch("/api/incidents");

        if (!incidentsRes.ok) {
            throw new Error(`Incidents HTTP ${incidentsRes.status}`);
        }

        const incidents = await incidentsRes.json();

        const active = incidents.filter(
            incident => incident.status === "open"
        );

        if (!active.length) {
            container.innerHTML =
                '<div class="empty">No active incidents with evidence.</div>';
            return;
        }

        let evidenceItems = [];

        for (const incident of active) {
            try {
                const response = await fetch(
                    `/api/incidents/${incident.id}/evidence`
                );

                if (!response.ok) continue;

                const data = await response.json();

                if (Array.isArray(data)) {
                    for (const item of data) {
                        evidenceItems.push({
                            incident: incident,
                            evidence: item
                        });
                    }
                }
            } catch (err) {
                console.error(
                    "Evidence load failed for incident",
                    incident.id,
                    err
                );
            }
        }

        if (!evidenceItems.length) {
            container.innerHTML =
                '<div class="empty">No evidence found for active incidents.</div>';
            return;
        }

        container.innerHTML = evidenceItems.map(item => {
            const incident = item.incident;
            const evidence = item.evidence;

            const values = Object.entries(evidence)
                .filter(([key, value]) =>
                    value !== null &&
                    value !== undefined &&
                    key !== "id" &&
                    key !== "incident_id"
                )
                .map(([key, value]) => `
                    <div style="margin-top:4px">
                        <span class="muted">${key.replaceAll("_", " ")}:</span>
                        ${String(value)}
                    </div>
                `)
                .join("");

            return `
                <div class="event-row" style="padding:14px 20px;border-bottom:1px solid #172133">
                    <div>
                        <strong>${incident.incident_id}</strong>
                        <div class="muted">
                            ${incident.summary || "Incident evidence"}
                        </div>
                        ${values}
                    </div>
                </div>
            `;
        }).join("");

    } catch (error) {
        console.error("Evidence:", error);
        container.innerHTML =
            '<div class="empty">Unable to load evidence.</div>';
    }
}


async function downloadLatestReport(format) {
    try {
        const response = await fetch("/api/incidents");

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const incidents = await response.json();

        if (!Array.isArray(incidents) || !incidents.length) {
            alert("No incidents available for report generation.");
            return;
        }

        const latest = incidents[0];

        const incidentRef =
            latest.incident_id ??
            latest.id;

        if (incidentRef === undefined || incidentRef === null) {
            throw new Error("Latest incident has no valid ID");
        }

        await downloadIncidentReport(incidentRef, format);

    } catch (error) {
        console.error("Latest report:", error);
        alert("Unable to generate the latest incident report.");
    }
}


async function downloadIncidentReport(incidentRef, format) {
    try {
        const response = await fetch(
            `/api/reports/${encodeURIComponent(incidentRef)}/${format}`
        );

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

        const link = document.createElement("a");
        link.href = url;
        link.download = `incident-${incidentRef}.${format}`;
        link.style.display = "none";

        document.body.appendChild(link);
        link.click();
        link.remove();

        setTimeout(() => URL.revokeObjectURL(url), 1000);
    } catch (error) {
        console.error("Report download:", error);
        alert("Unable to generate incident report.");
    }
}

async function loadDashboard() {
    try {
        const [statsRes, eventsRes, incidentsRes] = await Promise.all([
            fetch("/api/stats"),
            fetch("/api/events?limit=6"),
            fetch("/api/incidents")
        ]);

        if (!statsRes.ok || !eventsRes.ok || !incidentsRes.ok) {
            throw new Error("API unavailable");
        }

        const stats = await statsRes.json();
        const events = await eventsRes.json();
        const incidents = await incidentsRes.json();

        const total = stats.total_events || 0;
        const suspicious = stats.suspicious_events || 0;
        const recent = stats.recent_events || 0;

        const maxThreatScore = incidents.length
            ? Math.max(...incidents.map(i => Number(i.threat_score) || 0))
            : 0;

        const score = Math.min(
            100,
            Math.round(Math.max(maxThreatScore, suspicious * 20 + Math.min(total, 20)))
        );

        const threatScore = document.getElementById("threat-score");
        const eventCount = document.getElementById("event-count");
        const suspiciousCount = document.getElementById("suspicious-count");
        const recentCount = document.getElementById("recent-count");

        if (threatScore) threatScore.textContent = score;
        if (eventCount) eventCount.textContent = total;
        if (suspiciousCount) suspiciousCount.textContent = suspicious;
        if (recentCount) recentCount.textContent = recent;

        const threatLabel = document.getElementById("threat-label");
        if (threatLabel) {
            threatLabel.textContent =
                score >= 70 ? "Elevated activity" :
                score >= 40 ? "Moderate activity" :
                "Low activity";
        }

        const eventContainer = document.getElementById("events");

        if (eventContainer) {
            if (!events.length) {
                eventContainer.innerHTML =
                    '<div class="empty">No events recorded yet.</div>';
            } else {
                eventContainer.innerHTML = events.map(event => {
                    const severity = event.suspicious
                        ? "critical"
                        : event.event_type === "modify"
                            ? "warning"
                            : "normal";

                    const label = event.suspicious
                        ? "CRITICAL"
                        : event.event_type === "modify"
                            ? "WARNING"
                            : "NORMAL";

                    const icon = event.suspicious
                        ? "⚠"
                        : event.event_type === "modify"
                            ? "↻"
                            : "✓";

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
        }

        const incidentContainer = document.getElementById("incidents");

    const activeIncidents = incidents.filter(
        incident => incident.status === "open"
    );

    if (!activeIncidents.length) {
        incidentContainer.innerHTML =
            '';
    } else {
        incidentContainer.innerHTML = activeIncidents.map(incident => `
            <div class="event-row">
                <div style="flex:1">
                    <strong>${incident.incident_id}</strong>
                    <span> — ${incident.summary}</span>
                    <div class="muted">
                        Threat score: ${Number(incident.threat_score || 0).toFixed(1)}
                    </div>
                </div>

                <div style="display:flex;align-items:center;gap:8px">
                    <span class="severity ${String(incident.severity || "").toLowerCase()}">
                        ${String(incident.severity || "").toUpperCase()}
                    </span>

                    <button
                        onclick="incidentAction(${incident.id}, 'resolve')"
                        style="padding:5px 9px;border:1px solid #28533f;border-radius:6px;background:#10251b;color:#69d99d;cursor:pointer">
                        Resolve
                    </button>

                    <button
                        onclick="deleteIncident(${incident.id})"
                        style="padding:5px 9px;border:1px solid #5a3038;border-radius:6px;background:#24151a;color:#e88a98;cursor:pointer">
                        Delete
                    </button>
                </div>
            </div>
        `).join("");
    }

    } catch (error) {
        console.error("RDRS dashboard error:", error);

        const events = document.getElementById("events");
        const incidents = document.getElementById("incidents");

        if (events) {
            events.innerHTML =
                '<div class="empty">Unable to load events.</div>';
        }

        if (incidents) {
            incidents.innerHTML =
                '<div class="empty">Unable to load incidents.</div>';
        }
    }
}

loadDashboard();
loadSettings();
loadReport();
setInterval(loadDashboard, 5000);
setInterval(loadEvidence, 5000);
</script>


<script id="rdrs-threat-live">
(function () {
    function startThreatAnimation() {
        const bars = Array.from(document.querySelectorAll("#activity .bar"));
        if (!bars.length) return;

        setInterval(() => {
            bars.forEach((bar, index) => {
                const peak = bar.classList.contains("peak");
                const high = bar.classList.contains("high");

                let min = high ? 45 : 18;
                let max = peak ? 92 : (high ? 78 : 68);

                const wave = Math.sin(Date.now() / 1400 + index * 0.85);
                const random = Math.random() * 18;
                let value = min + ((wave + 1) / 2) * (max - min) * .65 + random;

                value = Math.max(min, Math.min(max, value));
                bar.style.height = value.toFixed(1) + "%";
            });
        }, 2600);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", startThreatAnimation);
    } else {
        startThreatAnimation();
    }
})();
</script>

</body>
</html>
"""
    return HTMLResponse(content=html)
