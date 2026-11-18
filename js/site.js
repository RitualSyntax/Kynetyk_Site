// kynetyk site bits

// links. empty = button greys out (web just hides)
// installers live on the site repo releases, tagged app-vX.Y.Z
const DL = 'https://github.com/RitualSyntax/Kynetyk_Site/releases/download';
const rel = (app, version, files = {}) => {
  const base = `${DL}/${app}-v${version}/kynetyk-${app}`;
  return {
    version,
    windows: files.windows ?? `${base}-windows.exe`,
    mac: files.mac ?? `${base}-mac.dmg`,
    linux: files.linux ?? `${base}-linux.AppImage`
  };
};

const LINKS = {
  donate: 'https://ko-fi.com/ritualsyntax',
  contact: '',   // mailto: works
  kue: { web: '', ...rel('kue', '0.3.0') },
  vyz: { web: '', ...rel('vyz', '0.1.1') },
  kode: { web: '', ...rel('kode', '0.1.1') },
  konv: { web: '', ...rel('konv', '0.1.0') },
  dekk: { web: '', ...rel('dekk', '0.1.0') },
  lynk: { web: '', ...rel('lynk', '0.1.0') },
  // rakk is windows only for now
  rakk: { web: '', ...rel('rakk', '0.1.0', { windows: `${DL}/rakk-v0.1.0/kynetyk-rakk-setup-0.1.0.exe`, mac: '', linux: '' }) }
};

// 'kue.windows' -> LINKS.kue.windows
const pick = key => key.split('.').reduce((o, k) => (o ? o[k] : ''), LINKS) || '';

const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// wire links
document.querySelectorAll('[data-link]').forEach(a => {
  const url = pick(a.dataset.link);
  if (url) {
    a.href = url;
  } else if (a.hasAttribute('data-optional')) {
    a.remove();
  } else {
    a.removeAttribute('href');
    a.setAttribute('aria-disabled', 'true');
    a.title = 'Coming soon';
  }
});
document.querySelectorAll('[data-text]').forEach(s => { const v = pick(s.dataset.text); if (v) s.textContent = v; });
const yr = document.getElementById('year');
if (yr) yr.textContent = new Date().getFullYear();

// departures board flip
const GLYPHS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
const flips = [...document.querySelectorAll('[data-flip]')];
if (!still && flips.length) {
  const finals = flips.map(el => el.textContent);
  let t = 0;
  const step = () => {
    flips.forEach((el, k) => {
      const row = Math.floor(k / 3);
      const settle = 4 + row * 3 + (k % 3) * 2;
      el.textContent = finals[k].split('').map((ch, i) =>
        (ch === ' ' || t >= settle + i) ? ch : GLYPHS[(i * 7 + t * 13 + k) % GLYPHS.length]).join('');
    });
    if (++t <= 44) setTimeout(step, 45);
    else flips.forEach((el, k) => { el.textContent = finals[k]; });
  };
  step();
}

// ticking timecode, 25fps
const tcEl = document.getElementById('tc');
if (tcEl && !still) {
  let frames = (3600 + 12) * 25;
  const p = x => String(x).padStart(2, '0');
  setInterval(() => {
    frames++;
    const s = Math.floor(frames / 25);
    tcEl.textContent = `${p(Math.floor(s / 3600))}:${p(Math.floor(s / 60) % 60)}:${p(s % 60)}:${p(frames % 25)}`;
  }, 40);
}

// gallery: auto moves on every 6s until someone clicks a tab
const tabs = [...document.querySelectorAll('.tabs [role="tab"]')];
const shots = [...document.querySelectorAll('.stage img')];
const bar = document.querySelector('.stage .bar i');
const cap = document.getElementById('caption');
let cur = 0;
let held = false;
let tick = 0;
function show(i) {
  cur = i;
  shots.forEach((im, k) => im.classList.toggle('on', k === i));
  tabs.forEach((b, k) => b.setAttribute('aria-selected', String(k === i)));
  if (cap) cap.textContent = shots[i].dataset.cap || '';
  tick = 0;
}
tabs.forEach((b, i) => b.addEventListener('click', () => { held = true; show(i); if (bar) bar.style.width = '100%'; }));
// arrow keys between tabs
tabs.forEach((b, i) => b.addEventListener('keydown', e => {
  if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
  const n = (i + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
  held = true;
  show(n);
  tabs[n].focus();
}));
if (shots.length && !still) {
  setInterval(() => {
    if (held) return;
    tick++;
    if (bar) bar.style.width = `${tick / 60 * 100}%`;
    if (tick >= 60) show((cur + 1) % shots.length);
  }, 100);
}

// scroll reveals for browsers without scroll-driven animations
const native = window.CSS && CSS.supports && CSS.supports('animation-timeline: view()');
const els = document.querySelectorAll('.reveal, .slide, .rise');
if (!native) {
  if (still || !('IntersectionObserver' in window)) {
    els.forEach(el => el.classList.add('in'));
  } else {
    const io = new IntersectionObserver(entries => {
      entries.forEach(en => {
        if (!en.isIntersecting) return;
        en.target.classList.add('in');
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -10% 0px' });
    els.forEach(el => io.observe(el));
  }
}

// pause the demo video when it's off screen, saves battery
const vid = document.querySelector('.video-wrap video');
if (vid && 'IntersectionObserver' in window) {
  if (still) { vid.removeAttribute('autoplay'); vid.pause(); }
  new IntersectionObserver(([en]) => {
    if (still) return;
    if (en.isIntersecting) vid.play().catch(() => {});
    else vid.pause();
  }).observe(vid);
}
