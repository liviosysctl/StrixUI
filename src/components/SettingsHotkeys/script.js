var HK = {{HOTKEYS}};

var HK_DEFAULT = HK.map(function (h) { return h.k; });
function keys(k) { return '<span class="k-keys">' + k.split(' ').map(function (p) { return '<span class="k-kbd">' + p + '</span>'; }).join('') + '</span>'; }
function groups(list) { var o = [], m = {}; list.forEach(function (h) { if (!m[h.g]) { m[h.g] = []; o.push(h.g); } m[h.g].push(h); }); return o.map(function (g) { return [g, m[g]]; }); }

// Settings › Hotkeys: every action can get new keys; own hotkeys can be added and removed
function Settings(root, onClose) {
  var main = root.querySelector('.k-settings-main'), list = root.querySelector('#hklist'), q = root.querySelector('#hkq'), rec = null;
  function combo(e) {
    var m = [], k = e.key;
    if (e.metaKey) m.push('Super'); if (e.ctrlKey) m.push('Ctrl'); if (e.altKey) m.push('Alt'); if (e.shiftKey) m.push('Shift');
    if (['Meta', 'Control', 'Alt', 'Shift', 'OS'].indexOf(k) >= 0) return null;
    k = { ' ': 'Space', Enter: 'Return', Escape: 'Escape', ArrowLeft: 'Left', ArrowRight: 'Right', ArrowUp: 'Up', ArrowDown: 'Down', PrintScreen: 'Print' }[k] || (k.length === 1 ? k.toUpperCase() : k);
    return m.concat([k]).join(' ');
  }
  function draw(mark) {
    var f = q.value.trim().toLowerCase();
    var shown = HK.filter(function (h) { return !f || (h.t + ' ' + h.k + ' ' + h.g + ' ' + h.w).toLowerCase().indexOf(f) >= 0; });
    list.innerHTML = groups(shown).map(function (gr) {
      return '<section class="k-hk-group"><h3>' + gr[0] + '</h3>' + gr[1].map(function (h) {
        var changed = !h.own && h.k !== HK_DEFAULT[h.id];
        var tail = h.own ? '<button class="k-iconbtn" data-del="' + h.id + '" aria-label="Remove ' + h.t + '">' + '<i class=\"k-icon\">' + Kit.icon('trash-2') + '</i>' + '</button>'
          : changed ? '<button class="k-iconbtn" data-reset="' + h.id + '" aria-label="Back to ' + HK_DEFAULT[h.id] + '">' + '<i class=\"k-icon\">' + Kit.icon('undo-2') + '</i>' + '</button>' : '<span></span>';
        return '<div class="k-hk" data-id="' + h.id + '"' + (mark === h.id ? ' data-mark' : '') + '><div><b>' + h.t + '</b><small>' + h.w + '</small></div><button class="k-keyrec" data-rec-id="' + h.id + '" aria-label="Keys for ' + h.t + ': ' + h.k + '">' + keys(h.k).replace(/^<span class="k-keys">|<\/span>$/g, '') + '</button>' + tail + '</div>';
      }).join('') + '</section>';
    }).join('') || '<p class="k-empty">No hotkey matches.</p>';
    if (mark != null) { var row = list.querySelector('[data-id="' + mark + '"]'); if (row) { row.scrollIntoView({ block: 'center' }); setTimeout(function () { row.removeAttribute('data-mark'); }, 1600); } }
  }
  function stop() { if (rec) { rec.removeAttribute('data-rec'); rec = null; } }
  list.addEventListener('click', function (e) {
    var b = e.target.closest('[data-rec-id]'), r = e.target.closest('[data-reset]'), d = e.target.closest('[data-del]'), y = e.target.closest('[data-replace]'), n = e.target.closest('[data-cancel]');
    if (b) { stop(); rec = b; b.setAttribute('data-rec', ''); return; }
    if (r) { HK[+r.dataset.reset].k = HK_DEFAULT[+r.dataset.reset]; draw(); return; }
    if (d) { HK = HK.filter(function (h) { return h.id !== +d.dataset.del; }); draw(); return; }
    if (y) { var p = JSON.parse(y.dataset.replace); HK.forEach(function (h) { if (h.id === p[1]) h.k = 'None'; if (h.id === p[0]) h.k = p[2]; }); draw(p[0]); return; }
    if (n) { draw(); }
  });
  document.addEventListener('keydown', function (e) {
    if (!rec) return;
    e.preventDefault();
    if (e.key === 'Escape' && !e.metaKey && !e.ctrlKey && !e.altKey && !e.shiftKey) { stop(); return; }
    var c = combo(e); if (!c) return;
    var id = +rec.dataset.recId, h = HK.filter(function (x) { return x.id === id; })[0], clash = HK.filter(function (x) { return x.k === c && x.id !== id; })[0];
    stop();
    if (clash) {
      var row = list.querySelector('[data-id="' + id + '"]');
      row.insertAdjacentHTML('beforeend', '<div class="k-hk-note">' + '<i class=\"k-icon\">' + Kit.icon('triangle-alert') + '</i>' + c + ' already does ' + clash.t + '.<button class="k-btn k-btn-sm" data-replace=\'' + JSON.stringify([id, clash.id, c]) + '\'><span>Use it here</span></button><button class="k-btn k-btn-sm k-btn-quiet" data-cancel><span>Keep the old</span></button></div>');
      Kit.hydrate(row);
    } else { h.k = c; draw(id); }
  }, true);
  q.addEventListener('input', function () { draw(); });
  // a new hotkey: a name, what it runs, and its keys
  var form = root.querySelector('#hknew'), add = root.querySelector('#hkadd');
  add.addEventListener('click', function () { form.hidden = false; form.querySelector('input').focus(); });
  form.querySelector('[data-cancel-new]').addEventListener('click', function () { form.hidden = true; });
  form.querySelector('[data-save-new]').addEventListener('click', function () {
    var name = form.querySelector('#hkname').value.trim() || 'My hotkey', cmd = form.querySelector('#hkcmd').value.trim() || 'notify-send hello';
    var id = HK.reduce(function (m, h) { return Math.max(m, h.id); }, 0) + 1;
    HK.push({ g: 'Your hotkeys', t: name, k: 'None', w: cmd, id: id, own: true }); HK_DEFAULT[id] = 'None';
    form.hidden = true; q.value = ''; draw(id);
    var b = list.querySelector('[data-rec-id="' + id + '"]'); rec = b; b.setAttribute('data-rec', '');
  });
  if (onClose) root.querySelector('[data-close]').addEventListener('click', onClose);
  return { draw: draw };
}

(function () { var S = Settings(document.getElementById('settings')); S.draw(); })();
