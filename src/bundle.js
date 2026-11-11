(function () {
  'use strict';
  var ICONS = __ICONS__;
  var WALL = __WALL__;
  var K = {};
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

  K.icons = Object.keys(ICONS);
  K.icon = function (name) {
    return '<svg viewBox="0 0 24 24" aria-hidden="true">' + (ICONS[name] || '') + '</svg>';
  };
  K.wallpaper = function () { return WALL; };
  K.reduced = function () {
    return document.documentElement.getAttribute('data-motion') === 'reduced' ||
      (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  };
  function each(root, sel, fn) { Array.prototype.forEach.call(root.querySelectorAll(sel), fn); }
  function emit(el, name, detail) { el.dispatchEvent(new CustomEvent(name, { bubbles: true, detail: detail })); }

  /* Segmented: the thumb glides, labels stay where they are */
  K.segmented = function (el) {
    if (el._k) return el._k;
    var buttons = Array.prototype.slice.call(el.querySelectorAll('button'));
    var thumb = document.createElement('i');
    thumb.className = 'k-seg-thumb';
    el.insertBefore(thumb, el.firstChild);
    el.setAttribute('role', 'tablist');
    el.setAttribute('data-ready', '0');
    var index = Math.max(0, buttons.findIndex(function (b) { return b.getAttribute('aria-selected') === 'true'; }));
    function place() {
      var b = buttons[index];
      thumb.style.width = b.offsetWidth + 'px';
      thumb.style.transform = 'translateX(' + b.offsetLeft + 'px)';
    }
    function select(i, silent) {
      var from = index;
      index = Math.max(0, Math.min(buttons.length - 1, i));
      buttons.forEach(function (b, n) {
        b.setAttribute('role', 'tab');
        b.setAttribute('aria-selected', n === index ? 'true' : 'false');
        b.tabIndex = n === index ? 0 : -1;
      });
      place();
      var target = el.getAttribute('data-for');
      if (target) {
        var tabs = document.querySelector(target);
        if (tabs) {
          tabs.style.setProperty('--dir', index >= from ? 1 : -1);
          Array.prototype.forEach.call(tabs.children, function (s, n) {
            if (n === index) s.setAttribute('data-active', ''); else s.removeAttribute('data-active');
          });
        }
      }
      if (!silent) emit(el, 'change', { index: index, value: buttons[index].value || buttons[index].textContent.trim() });
    }
    buttons.forEach(function (b, n) { b.addEventListener('click', function () { select(n); }); });
    el.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        e.preventDefault();
        select(index + (e.key === 'ArrowRight' ? 1 : -1));
        buttons[index].focus();
      }
    });
    select(index, true);
    requestAnimationFrame(function () { place(); requestAnimationFrame(function () { el.setAttribute('data-ready', '1'); }); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(place);
    window.addEventListener('resize', place);
    el._k = { select: select, place: place, get index() { return index; } };
    return el._k;
  };

  /* Slider: keeps the filled part and the output in step */
  K.slider = function (input) {
    if (input._k) return; input._k = true;
    function sync() {
      var min = +input.min || 0, max = +input.max || 100;
      input.style.setProperty('--p', ((input.value - min) / (max - min)) * 100 + '%');
      var out = input.parentNode.querySelector('output');
      if (out) out.textContent = input.value + (input.getAttribute('data-unit') || '');
    }
    input.addEventListener('input', sync);
    sync();
  };

  /* Ring gauge */
  K.ring = function (el, value) {
    var r = 28, c = 2 * Math.PI * r;
    if (!el._k) {
      el.insertAdjacentHTML('afterbegin', '<svg viewBox="0 0 60 60"><circle class="t" cx="30" cy="30" r="' + r + '"/><circle class="v" cx="30" cy="30" r="' + r + '" stroke-dasharray="' + c + '" stroke-dashoffset="' + c + '"/></svg>');
      el._k = el.querySelector('.v');
      if (!el.querySelector('b')) el.insertAdjacentHTML('beforeend', '<b><span class="k-roll"></span>%</b>');
    }
    if (value == null) value = +el.getAttribute('data-value') || 0;
    el.setAttribute('data-value', value);
    var v = el._k;
    requestAnimationFrame(function () { v.style.strokeDashoffset = c * (1 - value / 100); });
    var roll = el.querySelector('.k-roll');
    if (roll) K.roll(roll, String(Math.round(value)));
  };

  /* Rolling numbers: every digit is a column that slides */
  K.roll = function (el, text) {
    if (text == null) text = el.getAttribute('data-value') || el.textContent;
    text = String(text);
    if (el._len !== text.length) {
      el.innerHTML = '';
      text.split('').forEach(function (ch) {
        var col = document.createElement('span');
        col.innerHTML = /\d/.test(ch) ? '<i>0</i><i>1</i><i>2</i><i>3</i><i>4</i><i>5</i><i>6</i><i>7</i><i>8</i><i>9</i>' : '<i>' + ch + '</i>';
        el.appendChild(col);
      });
      el._len = text.length;
    }
    Array.prototype.forEach.call(el.children, function (col, n) {
      var ch = text[n];
      if (/\d/.test(ch) && col.children.length === 10) col.style.transform = 'translateY(' + (-1.2 * +ch) + 'em)';
      else if (col.children.length === 1) col.firstChild.textContent = ch;
    });
    el.setAttribute('aria-label', text);
  };

  /* Calendar: one month, Monday first */
  K.calendar = function (el, date) {
    var today = date || (el.getAttribute('data-date') ? new Date(el.getAttribute('data-date')) : new Date());
    var shown = new Date(today.getFullYear(), today.getMonth(), 1);
    function draw() {
      var y = shown.getFullYear(), m = shown.getMonth();
      var first = (new Date(y, m, 1).getDay() + 6) % 7;
      var days = new Date(y, m + 1, 0).getDate(), prev = new Date(y, m, 0).getDate();
      var h = '<header><b>' + MONTHS[m] + ' ' + y + '</b><span><button class="k-iconbtn k-iconbtn-sm" aria-label="Previous month" data-step="-1"><i class="k-icon">' + K.icon('chevron-left') + '</i></button><button class="k-iconbtn k-iconbtn-sm" aria-label="Next month" data-step="1"><i class="k-icon">' + K.icon('chevron-right') + '</i></button></span></header><div class="k-cal-grid">';
      'Mo Tu We Th Fr Sa Su'.split(' ').forEach(function (d) { h += '<span>' + d + '</span>'; });
      for (var i = 0; i < 42; i++) {
        var d = i - first + 1, out = d < 1 || d > days;
        var label = d < 1 ? prev + d : d > days ? d - days : d;
        var cur = !out && d === today.getDate() && m === today.getMonth() && y === today.getFullYear();
        h += '<button' + (out ? ' data-out tabindex="-1"' : '') + (cur ? ' aria-current="date"' : '') + '>' + label + '</button>';
        if (i >= 34 && d >= days) break;
      }
      el.innerHTML = h + '</div>';
      each(el, '[data-step]', function (b) {
        b.addEventListener('click', function () { shown = new Date(y, m + (+b.getAttribute('data-step')), 1); draw(); });
      });
    }
    draw();
  };

  /* Visualizer: bars driven by a level source; without one it idles on a soft synthetic signal */
  K.visualizer = function (el) {
    if (el._k) return el._k;
    var n = +el.getAttribute('data-bars') || 96, bars = [], t = 0, timer = null;
    for (var i = 0; i < n; i++) { var b = document.createElement('i'); el.appendChild(b); bars.push(b); }
    function frame(levels) {
      t += 1;
      bars.forEach(function (b, i) {
        var x = i / (n - 1), bell = Math.exp(-Math.pow((x - 0.5) / 0.26, 2));
        var v = levels ? levels[i] : bell * (0.45 + 0.4 * Math.sin(t * 0.7 + i * 0.9) * Math.sin(t * 0.23 + i * 0.31)) + 0.06 + 0.05 * Math.sin(t * 0.5 + i);
        v = Math.max(0.03, Math.min(1, v));
        b.style.transform = 'scaleY(' + v.toFixed(3) + ')';
        if (v > 0.72) b.setAttribute('data-peak', ''); else b.removeAttribute('data-peak');
      });
    }
    function start() { if (!timer && !K.reduced()) timer = setInterval(function () { if (!document.hidden) frame(); }, 110); }
    function stop() { clearInterval(timer); timer = null; }
    frame();
    if (el.getAttribute('data-paused') == null) start();
    el._k = { frame: frame, start: start, stop: stop };
    return el._k;
  };

  /* Carousel of slanted cards. Geometry mirrors bundle.css: card 96, selected 420, overlap 37, gap 3 */
  K.carousel = function (el) {
    if (el._k) return el._k;
    var track = el.querySelector('.k-carousel-track');
    var cards = Array.prototype.slice.call(track.children);
    if (!cards.length) return null;
    var index = Math.max(0, cards.findIndex(function (c) { return c.getAttribute('aria-selected') === 'true'; }));
    var STEP = 96 - 37 + 3, WIDE = 420, OVER = 37;
    function select(i, silent) {
      index = Math.max(0, Math.min(cards.length - 1, i));
      cards.forEach(function (c, n) { c.setAttribute('aria-selected', n === index ? 'true' : 'false'); c.tabIndex = n === index ? 0 : -1; });
      track.style.transform = 'translate(' + (-(index * STEP - OVER + WIDE / 2)) + 'px, -50%)';
      if (!silent) emit(el, 'change', { index: index, value: cards[index].getAttribute('data-value') });
    }
    cards.forEach(function (c, n) {
      c.addEventListener('click', function (e) {
        if (n === index) emit(el, 'apply', { index: n, value: c.getAttribute('data-value'), x: e.clientX, y: e.clientY });
        else select(n);
      });
    });
    el.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); select(index + 1); cards[index].focus(); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); select(index - 1); cards[index].focus(); }
    });
    el.addEventListener('wheel', function (e) { e.preventDefault(); select(index + (e.deltaY > 0 || e.deltaX > 0 ? 1 : -1)); }, { passive: false });
    select(index, true);
    el._k = { select: select, get index() { return index; } };
    return el._k;
  };

  /* Circular reveal from a point. Resolves when the circle covers the layer */
  K.reveal = function (layer, x, y) {
    var r = layer.getBoundingClientRect();
    layer.style.setProperty('--x', (x - r.left) + 'px');
    layer.style.setProperty('--y', (y - r.top) + 'px');
    layer.removeAttribute('data-on');
    void layer.offsetWidth;
    layer.setAttribute('data-on', '');
    return new Promise(function (resolve) {
      var done = false;
      function end() { if (!done) { done = true; resolve(); } }
      layer.addEventListener('transitionend', end, { once: true });
      setTimeout(end, K.reduced() ? 20 : 900);
    });
  };

  /* Dock: a thin tab on the bottom edge. It rises and widens when the pointer reaches the edge,
     and panels grow out of the button that opened them */
  K.dock = function (el) {
    if (el._k) return el._k;
    var edge = el.querySelector('.k-edge'), inner = el.querySelector('.k-edge-in');
    var zone = el.parentNode && el.parentNode.classList.contains('k-dockbar') ? el.parentNode : el;
    var openBtn = null, timer = null, inside = false, pinned = el.hasAttribute('data-pinned');
    function measure() { el.style.setProperty('--w', Math.ceil(inner.scrollWidth) + 2 + 'px'); }
    function show() { clearTimeout(timer); measure(); el.setAttribute('data-out', ''); }
    function hide() {
      clearTimeout(timer);
      timer = setTimeout(function () {
        if (inside || openBtn || pinned || el.contains(document.activeElement)) return;
        el.removeAttribute('data-out');
      }, 420);
    }
    function close() {
      each(el, '.k-panel[data-open]', function (p) { p.removeAttribute('data-open'); });
      each(edge, '[aria-expanded="true"]', function (b) { b.setAttribute('aria-expanded', 'false'); });
      openBtn = null;
      hide();
    }
    function open(btn) {
      var panel = el.querySelector(btn.getAttribute('data-panel'));
      if (!panel) return;
      var same = openBtn === btn;
      each(el, '.k-panel[data-open]', function (p) { p.removeAttribute('data-open'); });
      each(edge, '[aria-expanded="true"]', function (b) { b.setAttribute('aria-expanded', 'false'); });
      openBtn = null;
      if (same) { hide(); return; }
      show();
      var pr = el.getBoundingClientRect(), br = btn.getBoundingClientRect();
      var w = panel.offsetWidth, center = br.left + br.width / 2 - pr.left - (pr.width / 2 - w / 2);
      panel.style.transformOrigin = Math.max(0, Math.min(w, center)) + 'px 100%';
      panel.setAttribute('data-open', '');
      btn.setAttribute('aria-expanded', 'true');
      openBtn = btn;
      var tab = btn.getAttribute('data-tab'), seg = panel.querySelector('.k-seg');
      if (seg && seg._k) { if (tab != null) seg._k.select(+tab, true); setTimeout(seg._k.place, 0); }
      each(panel, '.k-ring', function (r) { K.ring(r, 0); setTimeout(function () { K.ring(r, +r.getAttribute('data-target') || 0); }, 160); });
      emit(el, 'open', { panel: panel });
    }
    each(edge, 'button[data-panel]', function (b) {
      b.setAttribute('aria-expanded', 'false');
      b.addEventListener('click', function (e) { e.stopPropagation(); open(b); });
    });
    zone.addEventListener('mouseenter', function () { inside = true; show(); });
    zone.addEventListener('mouseleave', function () { inside = false; hide(); });
    edge.addEventListener('click', function () { show(); });
    el.addEventListener('focusin', show);
    el.addEventListener('focusout', hide);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    document.addEventListener('click', function (e) { if (!el.contains(e.target)) close(); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
    measure();
    if (pinned) show();
    el._k = { open: open, close: close, show: show, hide: hide };
    return el._k;
  };

  /* Dismiss with the exit animation, then remove */
  K.dismiss = function (el, cls) {
    el.classList.add(cls || 'k-notif-out');
    var done = false;
    function end() { if (!done) { done = true; if (el.parentNode) el.parentNode.removeChild(el); } }
    el.addEventListener('animationend', end, { once: true });
    setTimeout(end, 500);
  };

  K.hydrate = function (root) {
    root = root || document;
    each(root, '.k-icon[data-icon]', function (i) { if (!i.firstChild) i.innerHTML = K.icon(i.getAttribute('data-icon')); });
    each(root, '.k-wall[data-chart]', function (w) { if (!w.firstChild) w.innerHTML = WALL; });
    each(root, '.k-seg', K.segmented);
    each(root, '.k-slider input', K.slider);
    each(root, '.k-ring[data-value]', function (r) { K.ring(r); });
    each(root, '.k-roll[data-value]', function (r) { K.roll(r); });
    each(root, '.k-cal', function (c) { if (!c.firstChild) K.calendar(c); });
    each(root, '.k-viz', K.visualizer);
    each(root, '.k-carousel', K.carousel);
    each(root, '.k-dock', K.dock);
  };

  window.Kit = K;
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { K.hydrate(document); });
  else K.hydrate(document);
})();
