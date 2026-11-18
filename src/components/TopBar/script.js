
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
