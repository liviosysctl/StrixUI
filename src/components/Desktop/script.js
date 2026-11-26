(function () {
  var ws = document.querySelectorAll('.k-ws button');
  Array.prototype.forEach.call(ws, function (b) { b.addEventListener('click', function () { Array.prototype.forEach.call(ws, function (o) { o.removeAttribute('aria-current'); }); b.setAttribute('aria-current', 'true'); b.setAttribute('data-used', ''); document.dispatchEvent(new CustomEvent('workspace', { detail: Array.prototype.indexOf.call(ws, b) })); }); });
  var days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], mon = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  function tick() {
    var d = new Date(), c = document.getElementById('clock');
    if (c) c.textContent = days[d.getDay()] + ' ' + d.getDate() + ' ' + mon[d.getMonth()] + '\u2002' + ('0' + d.getHours()).slice(-2) + ':' + ('0' + d.getMinutes()).slice(-2);
    var cpu = 8 + Math.round(Math.random() * 40), a = document.getElementById('m-cpu');
    if (a) Kit.roll(a, (cpu < 10 ? '\u2007' : '') + cpu + '%');
  }
  tick(); if (!Kit.reduced()) setInterval(tick, 2500);
})();

(function () {
  var tiles = document.getElementById('tiles'), ws = document.querySelectorAll('.k-ws button');
  var wins = document.querySelectorAll('#tiles .k-win');
  Array.prototype.forEach.call(wins, function (w) { w.addEventListener('click', function () { Array.prototype.forEach.call(wins, function (o) { o.removeAttribute('data-active'); }); w.setAttribute('data-active', ''); }); });
  function go(i) {
    Array.prototype.forEach.call(ws, function (b, n) { if (n === i) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current'); });
    if (i === 1) tiles.removeAttribute('data-hidden'); else tiles.setAttribute('data-hidden', '');
  }
  ws[2].removeAttribute('data-used');
  document.addEventListener('workspace', function (e) { go(e.detail); });
  go(0);
})();
