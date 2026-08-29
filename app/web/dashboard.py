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
   RDRS STEP 1 — 3D SHELL
   Premium animated SOC environment
   ========================================================= */

:root{
    --rdrs-blue:#4c8dff;
    --rdrs-purple:#8b5cf6;
    --rdrs-cyan:#22d3ee;
    --rdrs-green:#34d399;
}

/* Deep spatial background */

body{
    overflow-x:hidden;
    background:
        radial-gradient(
            circle at 78% 8%,
            rgba(76,141,255,.13),
            transparent 28%
        ),
        radial-gradient(
            circle at 35% 55%,
            rgba(139,92,246,.065),
            transparent 30%
        ),
        radial-gradient(
            circle at 92% 85%,
            rgba(34,211,238,.045),
            transparent 24%
        ),
        #060a13;
}

/* Animated ambient light */

.app{
    position:relative;
    isolation:isolate;
    perspective:1400px;
}

.app::before{
    content:"";
    position:fixed;
    width:420px;
    height:420px;
    left:18%;
    top:12%;
    border-radius:50%;
    background:
        radial-gradient(
            circle,
            rgba(76,141,255,.075),
            transparent 68%
        );
    filter:blur(35px);
    animation:rdrsFloatOne 13s ease-in-out infinite alternate;
    pointer-events:none;
    z-index:-1;
}

.app::after{
    content:"";
    position:fixed;
    width:360px;
    height:360px;
    right:4%;
    bottom:8%;
    border-radius:50%;
    background:
        radial-gradient(
            circle,
            rgba(139,92,246,.065),
            transparent 68%
        );
    filter:blur(35px);
    animation:rdrsFloatTwo 16s ease-in-out infinite alternate;
    pointer-events:none;
    z-index:-1;
}

@keyframes rdrsFloatOne{
    0%{
        transform:translate3d(-30px,-15px,0) scale(.92);
        opacity:.45;
    }
    50%{
        transform:translate3d(55px,35px,0) scale(1.08);
        opacity:.8;
    }
    100%{
        transform:translate3d(-10px,75px,0) scale(.98);
        opacity:.55;
    }
}

@keyframes rdrsFloatTwo{
    0%{
        transform:translate3d(20px,30px,0) scale(.9);
        opacity:.35;
    }
    50%{
        transform:translate3d(-50px,-35px,0) scale(1.12);
        opacity:.7;
    }
    100%{
        transform:translate3d(15px,-70px,0) scale(.96);
        opacity:.45;
    }
}

/* Subtle futuristic grid */

.main{
    position:relative;
}

.main::before{
    content:"";
    position:absolute;
    inset:0;
    pointer-events:none;
    opacity:.18;
    background-image:
        linear-gradient(
            rgba(100,130,180,.055) 1px,
            transparent 1px
        ),
        linear-gradient(
            90deg,
            rgba(100,130,180,.055) 1px,
            transparent 1px
        );
    background-size:48px 48px;
    mask-image:linear-gradient(
        to bottom,
        black,
        transparent 88%
    );
}

/* Sidebar depth */

.sidebar{
    position:sticky;
    z-index:10;
    background:
        linear-gradient(
            180deg,
            rgba(10,17,31,.97),
            rgba(6,11,21,.97)
        );
    box-shadow:
        18px 0 50px rgba(0,0,0,.20),
        inset -1px 0 rgba(91,120,170,.08);
}

/* Animated sidebar edge */

.sidebar::after{
    content:"";
    position:absolute;
    right:-1px;
    top:8%;
    width:1px;
    height:84%;
    background:
        linear-gradient(
            to bottom,
            transparent,
            rgba(76,141,255,.5),
            rgba(139,92,246,.35),
            transparent
        );
    opacity:.65;
    animation:rdrsEdgePulse 4s ease-in-out infinite;
}

@keyframes rdrsEdgePulse{
    0%,100%{opacity:.25}
    50%{opacity:.85}
}

/* Brand */

.brand{
    position:relative;
}

.brand-icon{
    position:relative;
    transform:translateZ(0);
    transition:
        transform .35s cubic-bezier(.2,.8,.2,1),
        box-shadow .35s ease;
}

.brand-icon::after{
    content:"";
    position:absolute;
    inset:-5px;
    border-radius:15px;
    border:1px solid rgba(76,141,255,.16);
    box-shadow:
        0 0 20px rgba(76,141,255,.10);
    animation:rdrsBrandPulse 3.5s ease-in-out infinite;
}

.brand:hover .brand-icon{
    transform:
        translateY(-2px)
        rotateX(5deg)
        rotateY(-5deg);
    box-shadow:
        0 10px 30px rgba(76,141,255,.20),
        0 0 25px rgba(139,92,246,.12);
}

@keyframes rdrsBrandPulse{
    0%,100%{
        opacity:.35;
        transform:scale(.98);
    }
    50%{
        opacity:.9;
        transform:scale(1.05);
    }
}

/* Navigation depth */

.nav-item{
    transform:translateZ(0);
    transform-style:preserve-3d;
    will-change:transform;
}

.nav-item:hover{
    transform:
        translate3d(4px,-1px,8px);
    box-shadow:
        8px 8px 25px rgba(0,0,0,.16);
}

.nav-item.active{
    box-shadow:
        inset 3px 0 var(--rdrs-blue),
        8px 8px 28px rgba(0,0,0,.14),
        0 0 22px rgba(76,141,255,.055);
}

/* Header depth */

.topbar{
    position:relative;
    z-index:2;
}

.topbar h1{
    text-shadow:
        0 2px 25px rgba(76,141,255,.10);
}

.eyebrow{
    text-shadow:
        0 0 16px rgba(76,141,255,.18);
}

/* Live status */

.status{
    position:relative;
    overflow:hidden;
}

.status::before{
    content:"";
    position:absolute;
    inset:0;
    background:
        linear-gradient(
            110deg,
            transparent 20%,
            rgba(255,255,255,.09) 48%,
            transparent 70%
        );
    transform:translateX(-120%);
    animation:rdrsStatusSweep 4.5s ease-in-out infinite;
}

@keyframes rdrsStatusSweep{
    0%,45%{
        transform:translateX(-120%);
    }
    65%,100%{
        transform:translateX(120%);
    }
}

.status-dot{
    box-shadow:
        0 0 7px rgba(52,211,153,.75),
        0 0 15px rgba(52,211,153,.35);
    animation:rdrsLiveDot 1.8s ease-in-out infinite;
}

@keyframes rdrsLiveDot{
    0%,100%{
        transform:scale(1);
        opacity:1;
    }
    50%{
        transform:scale(1.45);
        opacity:.65;
    }
}

/* Smooth rendering */

.card,
.nav-item,
.status{
    backface-visibility:hidden;
    -webkit-font-smoothing:antialiased;
}

/* Respect reduced-motion accessibility */

@media(prefers-reduced-motion:reduce){
    *,
    *::before,
    *::after{
        animation-duration:.01ms !important;
        animation-iteration-count:1 !important;
        transition-duration:.01ms !important;
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

<section class="card panel" id="settings-section" style="margin-top:20px">
<div class="panel-header">
<span class="panel-title">System Settings</span>
    <span class="panel-action">CONFIGURATION</span>
</div>
<div id="settings" class="events">
    <div class="empty">Loading settings...</div>
</div>
</section>

<section class="card panel" id="report-section" style="margin-top:20px">
<div class="panel-header">
<span class="panel-title">Security Report</span>
    <span class="panel-action">LIVE SUMMARY</span>
</div>
<div id="report" class="events">
    <div class="empty">Loading report...</div>
</div>

<div style="padding:0 20px 18px;display:flex;gap:8px;flex-wrap:wrap">
    <button class="nav-item"
            style="border:1px solid #1d273a;background:#111b2d;cursor:pointer"
            onclick="downloadIncidentReport('latest','json')">
        JSON Report
    </button>
    <button class="nav-item"
            style="border:1px solid #1d273a;background:#111b2d;cursor:pointer"
            onclick="downloadIncidentReport('latest','csv')">
        CSV Report
    </button>
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
            <div class="settings-row">
                <div>
                    <div class="metric-label">MONITORING</div>
                    <div class="metric-value" style="font-size:20px">
                        ${settings.monitoring_enabled ? "ENABLED" : "DISABLED"}
                    </div>
                    <div style="margin-top:10px">
                        ${
                            settings.monitoring_enabled
                            ? `<button onclick="serviceAction('stop')"
                                style="padding:7px 12px;border:1px solid #5a3038;border-radius:7px;background:#24151a;color:#e88a98;cursor:pointer">
                                Stop Monitoring
                              </button>`
                            : `<button onclick="serviceAction('start')"
                                style="padding:7px 12px;border:1px solid #28533f;border-radius:7px;background:#10251b;color:#69d99d;cursor:pointer">
                                Start Monitoring
                              </button>`
                        }
                    </div>
                </div>
                <div>
                    <div class="metric-label">MONITORED PATH</div>
                    <div>${settings.monitored_path}</div>
                </div>
                <div>
                    <div class="metric-label">ENTROPY THRESHOLD</div>
                    <div>${settings.entropy_threshold}</div>
                </div>
            </div>
        `;
        el.innerHTML = html;
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

        el.innerHTML = `
            <div class="settings-row">
                <div>
                    <div class="metric-label">TOTAL EVENTS</div>
                    <div class="metric-value" style="font-size:22px">
                        ${report.total_events ?? 0}
                    </div>
                </div>
                <div>
                    <div class="metric-label">SUSPICIOUS EVENTS</div>
                    <div class="metric-value" style="font-size:22px">
                        ${report.suspicious_events ?? 0}
                    </div>
                </div>
                <div>
                    <div class="metric-label">TOTAL INCIDENTS</div>
                    <div class="metric-value" style="font-size:22px">
                        ${report.total_incidents ?? 0}
                    </div>
                </div>
                <div>
                    <div class="metric-label">RESOLVED INCIDENTS</div>
                    <div class="metric-value" style="font-size:22px">
                        ${report.resolved_incidents ?? 0}
                    </div>
                </div>
            </div>
        `;
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
        document.body.appendChild(link);
        link.click();
        link.remove();

        URL.revokeObjectURL(url);
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

</body>
</html>
"""
    return HTMLResponse(content=html)
