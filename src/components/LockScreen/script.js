
(function () {
  var d = new Date(), days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], mon = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  function two(n) { return ('0' + n).slice(-2); }
  function tick() { var n = new Date(); document.getElementById('hh').textContent = two(n.getHours()); document.getElementById('mm').textContent = two(n.getMinutes()); }
  tick(); setInterval(tick, 10000);
  document.getElementById('date').textContent = days[d.getDay()] + ', ' + d.getDate() + ' ' + mon[d.getMonth()];
  var h = d.getHours();
  document.getElementById('greet').textContent = 'good ' + (h < 12 ? 'morning' : h < 18 ? 'afternoon' : 'evening') + ', livio';
  var pw = document.getElementById('pw'), field = document.getElementById('field'), help = document.getElementById('help'), lock = document.getElementById('lock'), wall = document.getElementById('wall'), tries = 0, wait = 0;
  function err(msg) { field.setAttribute('data-state', 'error'); help.textContent = msg; var box = pw.parentNode; box.classList.remove('k-shake'); void box.offsetWidth; box.classList.add('k-shake'); }
  pw.addEventListener('keydown', function (e) {
    if (wait) { e.preventDefault(); return; }
    if (e.getModifierState && e.getModifierState('CapsLock')) { field.removeAttribute('data-state'); help.textContent = 'Caps Lock is on'; }
    else if (e.key !== 'Enter' && field.getAttribute('data-state') !== 'error') help.textContent = '';
    if (e.key !== 'Enter') { if (e.key.length === 1) { field.removeAttribute('data-state'); } return; }
    if (pw.value === 'strix') {
      help.textContent = ''; lock.setAttribute('data-out', ''); wall.setAttribute('data-clear', '');
      setTimeout(function () { document.getElementById('relock').style.display = 'inline-flex'; }, 700);
    } else {
      tries++; pw.value = '';
      if (tries >= 3) {
        wait = 10; pw.disabled = true; err('Too many tries. Wait ' + wait + ' s');
        var t = setInterval(function () { wait--; help.textContent = 'Too many tries. Wait ' + wait + ' s'; if (wait <= 0) { clearInterval(t); tries = 0; pw.disabled = false; field.removeAttribute('data-state'); help.textContent = ''; pw.focus({ preventScroll: true }); } }, 1000);
      } else err('Wrong password');
    }
  });
  // a different god at every lock, never the same twice in a row
  var GODS = {{LOCK_GODS}}, scr = document.getElementById('scr'), plate = document.getElementById('lplate'), last = -1;
  function pick() {
    var i; do { i = Math.floor(Math.random() * GODS.length); } while (i === last && GODS.length > 1);
    last = i; var g = GODS[i];
    scr.setAttribute('data-theme', g[0]); wall.style.backgroundImage = 'url(' + g[1] + ')'; plate.textContent = g[2];
  }
  // the first lock shows the theme the page shows; the page switching theme starts over from there
  Kit.onTheme(function (id) {
    scr.removeAttribute('data-theme');
    for (var i = 0; i < GODS.length; i++) if (GODS[i][0] === id) { last = i; plate.textContent = GODS[i][2]; }
  });
  document.getElementById('relock').addEventListener('click', function () { this.style.display = 'none'; pick(); lock.removeAttribute('data-out'); wall.removeAttribute('data-clear'); pw.value = ''; });
})();
