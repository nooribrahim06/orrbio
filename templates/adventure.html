<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Orbio Adventure — start screen</title>
<style>
  :root{
    --space1:#071827; --space2:#032739;
    --accent:#37a38c; --ui:#ffd24a; --ui-dark:#e39b00; --ice:#9ae7ff;
    --btn-blue:#8fe0ff; --btn-blue-shadow:#2a7eb3;
  }
  html,body{height:100%;margin:0;background:#000;font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Arial}
  .wrap{display:grid;place-items:center;height:100%}
  canvas{background:linear-gradient(180deg,var(--space1),var(--space2));
    box-shadow:0 24px 80px rgba(0,0,0,.7);border-radius:18px;touch-action:none}
  #hud{position:absolute;inset:0;pointer-events:none}

  /* chips (top-left) */
  .chips{position:absolute;left:16px;top:16px;display:flex;gap:10px;pointer-events:auto}
  .chip{display:flex;align-items:center;gap:8px;background:rgba(0,0,0,.28);
    border:1px solid rgba(255,255,255,.14);color:#d6feff;padding:8px 12px;border-radius:12px}
  .coin{width:20px;height:20px;border-radius:50%;background:
    radial-gradient(circle at 30% 30%,#fff6,#0000),
    radial-gradient(circle at 40% 40%,#ffe688 0 50%,#ffb300 51% 100%);
    box-shadow:inset 0 0 0 2px #ffce63,0 2px 0 rgba(0,0,0,.35)}
  .med{width:22px;height:22px;border-radius:6px;background:
    linear-gradient(#b9eeff,#6dd6ff);box-shadow:inset 0 0 0 2px #e1f7ff,0 2px 0 rgba(0,0,0,.35);
    display:grid;place-items:center}
  .med:before{content:"+";color:#035e88;font-weight:1000;line-height:1}

  /* right vertical menu */
  .btn{position:absolute;right:16px;display:flex;align-items:center;justify-content:center;width:54px;height:54px;border-radius:14px;
    color:#311a00;font-weight:900;text-shadow:0 1px 0 rgba(255,255,255,.35);
    pointer-events:auto;user-select:none}
  .btn:active{transform:translateY(3px)}
  .btn-orange{background:linear-gradient(#ffb43a,#ff8b00);box-shadow:0 6px 0 #b85c00,0 10px 20px rgba(0,0,0,.35)}
  .btn-orange:active{box-shadow:0 3px 0 #b85c00,0 6px 12px rgba(0,0,0,.3)}
  .btn-blue{background:linear-gradient(var(--btn-blue),#48b7f3);color:#06304a;
    box-shadow:0 6px 0 var(--btn-blue-shadow),0 10px 20px rgba(0,0,0,.35)}
  .btn-blue:active{box-shadow:0 3px 0 var(--btn-blue-shadow),0 6px 12px rgba(0,0,0,.3)}

  /* start overlay */
  #startOverlay{position:absolute;inset:0;display:grid;place-items:center;
    background:radial-gradient(80% 60% at 50% 40%,rgba(0,80,120,.22),transparent)}
  .card{pointer-events:auto;display:flex;flex-direction:column;align-items:center;gap:16px;padding:26px 28px;background:rgba(0,0,0,.35);
    border:1px solid rgba(255,255,255,.12);backdrop-filter:blur(6px);border-radius:20px;color:#d6feff}
  .title{font-weight:1000;font-size:44px;letter-spacing:1px;display:flex;gap:12px;align-items:center;
    text-shadow:0 4px 0 rgba(0,0,0,.4),0 0 18px rgba(58,199,255,.6)}
  .title .orb{display:inline-block;width:56px;height:56px;border-radius:50%;
    background:radial-gradient(circle at 62% 35%,#ffe7a6 0 40%,#f4a629 41% 100%);box-shadow:0 12px 0 #7a2f25}
  .title .bubble{color:#9ae7ff;text-shadow:0 4px 0 rgba(0,0,0,.4),0 0 20px rgba(0,232,255,.9)}
  .subtitle{font-size:15px;opacity:.85}
  .startBtn{pointer-events:auto;cursor:pointer;font-size:22px;font-weight:900;color:#7a3500;background:linear-gradient(#ffd24a,#ffb326);
    border:none;border-radius:16px;padding:12px 32px;box-shadow:0 8px 0 #e39b00,0 12px 24px rgba(0,0,0,.35)}
  .startBtn:active{transform:translateY(3px);box-shadow:0 5px 0 #e39b00,0 8px 16px rgba(0,0,0,.3)}
  #bar{width:280px;height:22px;border-radius:14px;background:#fff3;border:1px solid #fff4;overflow:hidden}
  #bar>div{height:100%;background:repeating-linear-gradient(45deg,#ffc744 0 16px,#ff9f2a 16px 32px)}

  /* left bottom controls */
  #leftControls{position:absolute;left:16px;bottom:16px;display:flex;gap:10px}
  .glass{width:56px;height:56px;display:grid;place-items:center;border-radius:14px;background:linear-gradient(#f6fbff,#d6f3ff);opacity:.92;
    box-shadow:0 8px 0 #aac6d1,0 12px 24px rgba(0,0,0,.35);pointer-events:auto}
  .glass:active{transform:translateY(3px);box-shadow:0 5px 0 #aac6d1,0 8px 16px rgba(0,0,0,.3)}

  /* toast */
  #toast{position:absolute;left:50%;transform:translateX(-50%);top:14px;background:rgba(0,0,0,.45);border:1px solid rgba(255,255,255,.18);
    color:#d6feff;padding:8px 12px;border-radius:10px;font-size:14px;display:none}

  /* responsive */
  @media (max-width: 820px){
    canvas{width:95vw;height:60vh}
    .title{font-size:36px}
  }
</style>
</head>
<body>
<div class="wrap">
  <canvas id="game" width="1024" height="576" aria-label="Orbio Adventure"></canvas>

  <div id="hud">
    <!-- top-left chips -->
    <div class="chips">
      <div class="chip"><span class="coin"></span><span id="coinsLabel">1500</span></div>
      <div class="chip"><span class="med"></span><span id="healthLabel">+</span></div>
    </div>

    <!-- start card -->
    <div id="startOverlay">
      <div class="card">
        <div class="title">
          <span class="orb"></span>
          <span>Orbio</span>
          <span class="bubble">Adventure</span>
        </div>
        <div class="subtitle">Dodge debris. Collect stars. ← → / A D / drag.</div>
        <button id="start" class="startBtn">START</button>
        <div id="bar"><div style="width:65%"></div></div>
      </div>
    </div>

    <!-- bottom-left -->
    <div id="leftControls">
      <div id="pause" class="glass" title="Pause">⏸</div>
      <div id="play" class="glass" title="Play">▶</div>
    </div>

    <div id="toast"></div>

    <!-- right vertical menu -->
    <div id="menuHome"  class="btn btn-orange" style="top:80px"  title="Home">⌂</div>
    <div id="menuStats" class="btn btn-orange" style="top:146px" title="Stats">≡</div>
    <div id="menuGear"  class="btn btn-orange" style="top:212px" title="Options">⚙</div>
    <div id="menuMusic" class="btn btn-orange" style="top:278px" title="Music">♫</div>
    <div id="menuBack"  class="btn btn-blue"   style="top:344px" title="Back">↶</div>
    <div id="menuClose" class="btn btn-blue"   style="top:410px" title="Close">✕</div>
  </div>
</div>

<script>
(()=>{
  // ===== Canvas + HiDPI =====
  const canvas=document.getElementById('game');
  const ctx=canvas.getContext('2d');
  function fitHiDPI(){
    const ratio=Math.max(1,Math.floor(window.devicePixelRatio||1));
    const cssW=canvas.clientWidth||canvas.width, cssH=canvas.clientHeight||canvas.height;
    canvas.width=Math.round(cssW*ratio); canvas.height=Math.round(cssH*ratio);
    ctx.setTransform(ratio,0,0,ratio,0,0);
  }
  fitHiDPI(); addEventListener('resize',fitHiDPI);
  const W=()=> (canvas.clientWidth||canvas.width);
  const H=()=> (canvas.clientHeight||canvas.height);

  // ===== State =====
  const state={
    running:false, paused:false, t:0, score:0, coins:1500, speed:1,
    debris:[], stars:[], sparks:[], trail:[], keys:new Set(), pointerX:null,
    satellite:{x:W()/2,y:H()-70,w:60,h:60,vx:0}, parallax:[]
  };

  // ===== Utils =====
  const rand=(a,b)=>a+Math.random()*(b-a);
  const lerp=(a,b,t)=>a+(b-a)*t;
  const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
  function toast(msg,ms=1100){
    const el=document.getElementById('toast'); el.textContent=msg; el.style.display='block';
    clearTimeout(el._t); el._t=setTimeout(()=>el.style.display='none',ms);
  }

  // ===== Offscreen sprites =====
  const sprites={
    star: makeCanvas(30,30,(c)=>{
      const g=c.createRadialGradient(15,15,0,15,15,14);
      g.addColorStop(0,'#e9fdff'); g.addColorStop(.5,'#a6edff'); g.addColorStop(1,'#49c9ff');
      c.fillStyle=g; circle(c,15,15,8); c.fill();
      c.globalCompositeOperation='lighter'; c.globalAlpha=.6; circle(c,15,15,13); c.fill();
      c.globalAlpha=1; c.globalCompositeOperation='source-over';
    }),
    debris: makeCanvas(48,48,(c)=>{
      const g=c.createLinearGradient(0,0,48,48);
      g.addColorStop(0,'#d5deea'); g.addColorStop(1,'#7c8796');
      c.fillStyle=g; blob(c,24,24,18); c.fill();
      c.globalCompositeOperation='overlay'; c.globalAlpha=.25; blob(c,24,24,14); c.fill();
      c.globalAlpha=1; c.globalCompositeOperation='source-over';
    }),
    thrust: makeCanvas(60,60,(c)=>{
      const grad=c.createRadialGradient(30,50,0,30,50,26);
      grad.addColorStop(0,'rgba(255,255,255,.95)');
      grad.addColorStop(.4,'rgba(255,210,90,.9)');
      grad.addColorStop(1,'rgba(255,120,0,0)');
      c.fillStyle=grad; c.beginPath(); c.ellipse(30,44,10,18,0,0,6.283); c.fill();
    }),
    planet: makeCanvas(80,80,(c)=>{
      const g=c.createRadialGradient(40,35,5,40,40,40);
      g.addColorStop(0,'#9ae7ff'); g.addColorStop(1,'#256c88');
      c.fillStyle=g; c.arc(40,40,28,0,6.283); c.fill();
      c.strokeStyle='rgba(255,255,255,.25)'; c.lineWidth=2; c.beginPath();
      c.ellipse(40,38,36,10,0,0,6.283); c.stroke();
    })
  };
  function makeCanvas(w,h,draw){const off=document.createElement('canvas');off.width=w;off.height=h;const c=off.getContext('2d');draw(c);return off;}
  function circle(c,x,y,r){c.beginPath();c.arc(x,y,r,0,6.283);}
  function blob(c,x,y,r){
    c.beginPath(); c.moveTo(x-r,y);
    for(let a=0;a<6.283;a+=Math.PI/3){
      const px=x+Math.cos(a)*r*rand(.8,1.1), py=y+Math.sin(a)*r*rand(.8,1.1);
      c.quadraticCurveTo(x+(px-x)*.6,y+(py-y)*.6,px,py);
    } c.closePath();
  }
  function roundRect(c,x,y,w,h,r){
    c.beginPath(); c.moveTo(x+r,y);
    c.arcTo(x+w,y,x+w,y+h,r); c.arcTo(x+w,y+h,x,y+h,r);
    c.arcTo(x,y+h,x,y,r); c.arcTo(x,y,x+w,y,r); c.closePath();
  }

  // ===== Parallax =====
  function initParallax(){
    state.parallax=[]; const w=W(),h=H();
    for(let i=0;i<140;i++) state.parallax.push({x:rand(0,w),y:rand(0,h),r:rand(.6,1.6),d:rand(.15,.45),t:rand(0,999)});
    for(let i=0;i<3;i++) state.parallax.push({planet:true,x:rand(80,w-80),y:rand(60,h*.5),d:rand(.02,.06)});
  }
  initParallax(); addEventListener('resize',initParallax);

  function drawBackground(){
    const w=W(),h=H(); ctx.save();
    for(const s of state.parallax){
      if(s.planet){ const px=s.x+Math.sin(state.t*.00008)*18, py=s.y+Math.cos(state.t*.00006)*8;
        ctx.globalAlpha=.18; ctx.drawImage(sprites.planet,px-40,py-40); ctx.globalAlpha=1; continue; }
      const tw=(Math.sin(state.t*.004+s.t)*.5+.5)*.4+.6;
      ctx.globalAlpha=.6*tw; ctx.fillStyle='#9adfff';
      ctx.fillRect(s.x,(s.y+(state.t*s.d*0.02))%h,s.r,s.r);
    }
    ctx.restore();
  }

  function drawSatellite(s){
    ctx.save(); ctx.translate(s.x,s.y);
    ctx.globalAlpha=.25; ctx.filter='blur(4px)'; circle(ctx,0,0,28); ctx.fillStyle='#00e0ff'; ctx.fill(); ctx.filter='none'; ctx.globalAlpha=1;
    ctx.fillStyle='#2bb2c5'; roundRect(ctx,-70,-20,48,40,6); ctx.fill(); roundRect(ctx,22,-20,48,40,6); ctx.fill();
    ctx.strokeStyle='#89e0ef'; ctx.lineWidth=1;
    for(let i=-46;i<=-26;i+=8){ ctx.beginPath(); ctx.moveTo(i,-18); ctx.lineTo(i,18); ctx.stroke(); }
    for(let i=34;i<=54;i+=8){ ctx.beginPath(); ctx.moveTo(i,-18); ctx.lineTo(i,18); ctx.stroke(); }
    ctx.fillStyle='#d9f6ff'; roundRect(ctx,-10,-28,20,36,8); ctx.fill();
    ctx.fillStyle='#b2e5f6'; roundRect(ctx,-6,-22,12,18,6); ctx.fill();
    ctx.fillStyle='#e6f9ff'; ctx.beginPath(); ctx.ellipse(0,-38,20,6,0,0,Math.PI,true); ctx.fill();
    ctx.fillStyle='#9ae7ff'; ctx.beginPath(); ctx.ellipse(0,-36,30,10,0,0,Math.PI,false); ctx.fill();
    ctx.strokeStyle='#9ae7ff'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(0,-28); ctx.lineTo(0,-46); ctx.stroke();
    ctx.globalAlpha=.85; for(let r=6;r<=18;r+=6){ ctx.beginPath(); ctx.arc(0,-50,r,Math.PI,2*Math.PI); ctx.stroke(); } ctx.globalAlpha=1;
    if(Math.abs(s.vx)>0.8){ ctx.globalCompositeOperation='lighter'; ctx.drawImage(sprites.thrust,-30,-6); ctx.globalCompositeOperation='source-over'; }
    ctx.restore();
  }
  function drawDebris(d){ ctx.save(); ctx.translate(d.x,d.y); ctx.rotate(d.r);
    ctx.globalCompositeOperation='lighter'; ctx.globalAlpha=.25; ctx.drawImage(sprites.debris,-24,-24);
    ctx.globalCompositeOperation='source-over'; ctx.globalAlpha=1; ctx.drawImage(sprites.debris,-24,-24); ctx.restore(); }
  function drawStars(){ for(const st of state.stars){ const tw=(Math.sin(state.t*.02+st.seed)*.5+.5)*.3+.7; ctx.globalAlpha=tw; ctx.drawImage(sprites.star,st.x-15,st.y-15); } ctx.globalAlpha=1; }
  function postFX(){
    const w=W(),h=H(); ctx.globalAlpha=.08; ctx.fillStyle='#000';
    for(let y=0;y<h;y+=2) ctx.fillRect(0,y,w,1);
    ctx.globalAlpha=1; const g=ctx.createRadialGradient(w/2,h/2, Math.min(w,h)*.2, w/2,h/2, Math.min(w,h)*.75);
    g.addColorStop(0,'rgba(0,0,0,0)'); g.addColorStop(1,'rgba(0,0,0,.55)'); ctx.fillStyle=g; ctx.fillRect(0,0,w,h);
  }

  // ===== Spawns & physics =====
  function spawnDebris(){ state.debris.push({x:rand(30,W()-30),y:-30,r:rand(0,6.28),vr:rand(-0.02,0.02),vy:rand(1.3,2.2)*state.speed,w:36,h:36}); }
  function spawnStar(){ state.stars.push({x:rand(30,W()-30),y:-20,vy:rand(1.2,1.9)*state.speed,r:12,alive:true,seed:rand(0,999)}); }
  function addSparks(x,y,n=10){ for(let i=0;i<n;i++) state.sparks.push({x,y,vx:rand(-2,2),vy:rand(-3,-1),life:rand(18,34)}); }
  function rectsOverlap(a,b){ return Math.abs(a.x-b.x)<(a.w/2+b.w/2) && Math.abs(a.y-b.y)<(a.h/2+b.h/2); }

  // ===== Input =====
  addEventListener('keydown',e=>state.keys.add(e.key.toLowerCase()));
  addEventListener('keyup',e=>state.keys.delete(e.key.toLowerCase()));
  canvas.addEventListener('pointerdown',e=>{ state.pointerX=e.offsetX; });
  canvas.addEventListener('pointerup',()=>{ state.pointerX=null; });
  canvas.addEventListener('pointermove',e=>{ if(state.pointerX!=null) state.satellite.x=e.offsetX; });

  // ===== Loop =====
  function step(){
    if(!state.running) return;
    if(state.paused){ requestAnimationFrame(step); return; }
    const dt=16.6; state.t+=dt;

    if(state.t%800<dt)  spawnDebris();
    if(state.t%1300<dt) spawnStar();

    const s=state.satellite, left=state.keys.has('arrowleft')||state.keys.has('a'), right=state.keys.has('arrowright')||state.keys.has('d');
    if(left && !right) s.vx=lerp(s.vx,-6,.35);
    else if(right && !left) s.vx=lerp(s.vx,6,.35);
    else s.vx*=0.86;
    s.x+=s.vx; s.x=clamp(s.x,50,W()-50);

    if(Math.abs(s.vx)>0.5){ state.trail.push({x:s.x,y:s.y+16,a:.6,r:rand(6,12)}); if(state.trail.length>24) state.trail.shift(); }

    for(const d of state.debris){ d.y+=d.vy; d.r+=d.vr; }
    state.debris=state.debris.filter(d=>d.y<H()+40);
    for(const st of state.stars){ st.y+=st.vy; }
    state.stars=state.stars.filter(st=>st.y<H()+30 && st.alive);

    for(const p of state.sparks){ p.x+=p.vx; p.y+=p.vy; p.vy+=0.08; p.life--; }
    state.sparks=state.sparks.filter(p=>p.life>0);

    for(const d of state.debris){
      const boxS={x:s.x,y:s.y,w:80,h:58}, boxD={x:d.x,y:d.y,w:d.w,h:d.h};
      if(rectsOverlap(boxS,boxD)){ gameOver(); break; }
    }
    for(const st of state.stars){
      const boxS={x:s.x,y:s.y,w:60,h:60}, boxT={x:st.x,y:st.y,w:st.r*2,h:st.r*2};
      if(rectsOverlap(boxS,boxT)){
        st.alive=false; state.score+=10; state.coins+=5;
        document.getElementById('coinsLabel').textContent=state.coins;
        addSparks(st.x,st.y,14); toast('+10 score, +5 coins');
      }
    }

    // Render
    ctx.clearRect(0,0,W(),H()); drawBackground();

    ctx.save(); ctx.globalCompositeOperation='lighter';
    for(const t of state.trail){ ctx.globalAlpha=t.a; t.a*=0.92; ctx.filter='blur(6px)'; ctx.fillStyle='#4be3ff'; circle(ctx,t.x,t.y,t.r); ctx.fill(); }
    ctx.filter='none'; ctx.restore();

    drawStars(); for(const d of state.debris) drawDebris(d); drawSatellite(s);

    ctx.save(); ctx.globalCompositeOperation='lighter';
    for(const p of state.sparks){ ctx.globalAlpha=Math.max(0,Math.min(1,p.life/34)); ctx.fillStyle='#ffd24a'; circle(ctx,p.x,p.y,2); ctx.fill(); }
    ctx.restore();

    postFX();
    requestAnimationFrame(step);
  }

  function startGame(){
    state.running=true; state.paused=false; state.t=0; state.score=0;
    state.debris=[]; state.stars=[]; state.sparks=[]; state.trail=[];
    state.satellite.x=W()/2; state.satellite.y=H()-70; state.satellite.vx=0;
    requestAnimationFrame(step);
  }
  function gameOver(){
    state.running=false; addSparks(state.satellite.x,state.satellite.y,60);
    toast('Kaboom 💥 Game Over'); document.getElementById('startOverlay').style.display='grid';
  }

  // ===== UI =====
  document.getElementById('start').addEventListener('click',()=>{ document.getElementById('startOverlay').style.display='none'; startGame(); });
  document.getElementById('pause').addEventListener('click',()=>{ state.paused=true; toast('Paused'); });
  document.getElementById('play').addEventListener('click',()=>{ if(state.running){ state.paused=false; toast('Resume'); }});
  document.getElementById('menuHome').addEventListener('click',()=>{ state.running=false; document.getElementById('startOverlay').style.display='grid'; toast('Home'); });
  document.getElementById('menuStats').addEventListener('click',()=>{ toast(`High score: ${state.score}`); });
  document.getElementById('menuGear').addEventListener('click',()=>{ state.speed = state.speed===1 ? 1.3 : 1; toast(`Speed x${state.speed.toFixed(1)}`); });
  document.getElementById('menuMusic').addEventListener('click',()=>{ toast('Music toggled (visual only)'); });
  document.getElementById('menuBack').addEventListener('click',()=>{ toast('Back'); });
  document.getElementById('menuClose').addEventListener('click',()=>{ gameOver(); });
})();
</script>
</body>
</html>
