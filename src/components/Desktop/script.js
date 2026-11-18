
(function () {
  var ws = document.querySelectorAll('.k-ws button');
  Array.prototype.forEach.call(ws, function (b) { b.addEventListener('click', function () { Array.prototype.forEach.call(ws, function (o) { o.removeAttribute('aria-current'); }); b.setAttribute('aria-current', 'true'); b.setAttribute('data-used', ''); document.dispatchEvent(new CustomEvent('workspace', { detail: Array.prototype.indexOf.call(ws, b) })); }); });
  function tick() {
    var d = new Date(), c = document.getElementById('clock');
    if (c) c.textContent = ('0' + d.getHours()).slice(-2) + ':' + ('0' + d.getMinutes()).slice(-2);
    var cpu = 8 + Math.round(Math.random() * 40), tmp = 42 + Math.round(Math.random() * 14);
    var a = document.getElementById('m-cpu'), t = document.getElementById('m-tmp');
    if (a) { Kit.roll(a, (cpu < 10 ? ' ' : '') + cpu + '%'); a.parentNode.querySelector('u').style.setProperty('--p', cpu + '%'); }
    if (t) { Kit.roll(t, tmp + '°'); t.parentNode.querySelector('u').style.setProperty('--p', tmp + '%'); }
  }
  tick(); if (!Kit.reduced()) setInterval(tick, 2500);
})();

(function () {
  var d = new Date(), days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], mon = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  document.getElementById('dow').textContent = days[d.getDay()];
  document.getElementById('dmy').textContent = d.getDate() + ' ' + mon[d.getMonth()];
  document.getElementById('pdate').textContent = days[d.getDay()].slice(0, 3) + ' ' + d.getDate() + ' ' + mon[d.getMonth()].slice(0, 3);
  var part = Math.round((d.getHours() * 60 + d.getMinutes()) / 14.4);
  document.getElementById('dayp').textContent = part + '%';
  document.getElementById('dayl').style.setProperty('--p', part + '%');
  var b = document.getElementById('up-b'), t = document.getElementById('up-t'), s = document.getElementById('up-s'), p = document.getElementById('up-p'), i = document.getElementById('up-i');
  b.addEventListener('click', function () {
    b.disabled = true; t.textContent = 'Looking for updates'; s.textContent = 'Asking the stable channel'; p.style.display = 'block'; i.innerHTML = Kit.icon('refresh-cw');
    setTimeout(function () { t.textContent = 'Installing 0.2.0'; s.textContent = 'Building the new system'; }, 1600);
    setTimeout(function () { b.disabled = false; p.style.display = 'none'; t.textContent = 'You are up to date'; s.textContent = 'Now on 0.2.0. Checked just now'; i.innerHTML = Kit.icon('check'); }, 4200);
  });
})();

(function () {
  var tiles = document.getElementById('tiles'), plate = document.getElementById('plate'), ws = document.querySelectorAll('.k-ws button');
  var wins = document.querySelectorAll('#tiles .k-win');
  Array.prototype.forEach.call(wins, function (w) { w.addEventListener('click', function () { Array.prototype.forEach.call(wins, function (o) { o.removeAttribute('data-active'); }); w.setAttribute('data-active', ''); }); });
  function go(i) {
    Array.prototype.forEach.call(ws, function (b, n) { if (n === i) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current'); });
    if (i === 1) { tiles.removeAttribute('data-hidden'); plate.style.opacity = 0; } else { tiles.setAttribute('data-hidden', ''); plate.style.opacity = 1; }
  }
  ws[2].removeAttribute('data-used');
  document.addEventListener('workspace', function (e) { go(e.detail); });
  go(0);
})();
