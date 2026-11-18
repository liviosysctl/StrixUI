var P = {{THEMES}};

(function () {
  var scr = document.getElementById('scr'), track = document.getElementById('track'), car = document.getElementById('car'), rev = document.getElementById('rev'), base = document.getElementById('base');
  var picker = document.getElementById('picker'), reopen = document.getElementById('reopen'), plate = document.getElementById('plate');
  track.innerHTML = P.map(function (p, i) {
    return '<button class="k-slant" aria-selected="' + (p[0] === Kit.theme()) + '" aria-label="' + p[2] + '"><span class="k-slant-art"><img alt="" src="' + p[1] + '"></span><span class="k-slant-edge"></span><span class="k-slant-name">' + p[2] + '<small><i class="dot" style="background:' + p[5] + '"></i>' + p[3] + '</small></span></button>';
  }).join('');
  Kit.hydrate(document);
  function caption() { plate.textContent = P[car._k.index][4]; }
  car.addEventListener('change', caption); caption();
  // the theme on the desktop: set by hand, or by the cycle every 10 minutes
  var cur = 0, PERIOD = 10 * 60 * 1000, speed = 1, last = Date.now(), virt = 0, prev = Date.now();
  // the picker opens on the theme the page shows, and follows the page when it switches
  Kit.onTheme(function (id) {
    for (var i = 0; i < P.length; i++) if (P[i][0] === id) { cur = i; car._k.select(i, true); }
    scr.removeAttribute('data-theme'); rev.removeAttribute('data-on'); virt = 0; caption();
  });
  var keep = document.getElementById('keep'), fast = document.getElementById('fast'), next = document.getElementById('next');
  function show(i, x, y, close) {
    var p = P[i]; cur = i;
    rev.style.backgroundImage = 'url("' + p[1] + '")';
    return Kit.reveal(rev, x, y).then(function () {
      base.style.backgroundImage = 'url("' + p[1] + '")'; scr.setAttribute('data-theme', p[0]);
      if (close) picker.setAttribute('data-out', '');
      setTimeout(function () { rev.removeAttribute('data-on'); if (close) reopen.style.display = 'inline-flex'; }, 260);
    });
  }
  car.addEventListener('apply', function (e) {
    show(e.detail.index, e.detail.x, e.detail.y, true);
    virt = 0;                                    // a theme chosen by hand starts a new cycle
  });
  function mmss(ms) { var t = Math.ceil(ms / 1000); return Math.floor(t / 60) + ':' + ('0' + t % 60).slice(-2); }
  setInterval(function () {
    var now = Date.now(); virt += (now - prev) * speed; prev = now;
    if (virt >= PERIOD) {
      virt -= PERIOD;                            // the cycle keeps counting whether the theme is kept or not
      if (!keep.checked) {
        var i; do { i = Math.floor(Math.random() * P.length); } while (i === cur);
        var r = scr.getBoundingClientRect(); show(i, r.left + r.width / 2, r.top + r.height / 2, false);
      }
    }
    next.textContent = (keep.checked ? 'Kept. The cycle still counts: ' : 'Next theme in ') + mmss(PERIOD - virt);
  }, 200);
  fast.addEventListener('change', function () { speed = fast.checked ? 60 : 1; });
  document.addEventListener('keydown', function (e) {
    if (picker.hasAttribute('data-out')) return;
    if (e.key === 'Enter') { var c = track.querySelector('[aria-selected="true"]').getBoundingClientRect(); car.dispatchEvent(new CustomEvent('apply', { detail: { index: car._k.index, x: c.left + c.width / 2, y: c.top + c.height / 2 } })); }
    if (e.key === 'ArrowRight') car._k.select(car._k.index + 1);
    if (e.key === 'ArrowLeft') car._k.select(car._k.index - 1);
    if ((e.key === 'k' || e.key === 'K') && !e.ctrlKey && !e.metaKey && !e.altKey) { keep.checked = !keep.checked; keep.dispatchEvent(new Event('change', { bubbles: true })); }
  });
  reopen.addEventListener('click', function () { reopen.style.display = 'none'; picker.removeAttribute('data-out'); });
})();
