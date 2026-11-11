import json
# Component and screen previews. Each entry: name, group, height, html, js, doc (+ css, width).
def I(n, cls=''):
    return '<i class="k-icon%s" data-icon="%s"></i>' % ((' ' + cls) if cls else '', n)

BLOBS = {'0d757135df30d2bf6652f3c0a18483d5': 'saturnus.jpg', 'e6dec074eb9b7a654bf95f13d282f2c2': 'janus.jpg', 'b41733760ffae9de3f6f5d88682af092': 'apollo.jpg', '3ce42143088aadf856d6c3ff5e29859e': 'mars.jpg', '3b21996e74bfecb14fcb2f68061b8c3d': 'vulcanus.jpg', '479cdcb0b9c5173af68ab78ad369c814': 'neptunus.jpg', '29b44e5ca900dac5a146387c59ae71a1': 'pluto.jpg', '0b1aff047346223424503ef8f1b62a91': 'bacchus.jpg'}
SATURNUS, JANUS, APOLLO, MARS, VULCANUS, NEPTUNUS, PLUTO, BACCHUS = ['/_blob/' + k for k in BLOBS]
def WALL(url, extra='', pos='center'):
    return '<div class="k-wall"%s style="background-image:url(%s);background-position:%s"></div>' % (extra, url, pos)
COMPONENTS = []
def comp(name, group, height, html, doc, js='', css='', width=None):
    COMPONENTS.append(dict(name=name, group=group, height=height, html=html, doc=doc, js=js, css=css, width=width))

# ------------------------------------------------------------------ Actions
comp('Button', 'Actions', 110, r'''
<div class="k-stage">
  <button class="k-btn k-btn-primary"><span>Install</span></button>
  <button class="k-btn"><span>Details</span></button>
  <button class="k-btn k-btn-quiet"><span>Cancel</span></button>
  <button class="k-btn k-btn-danger">''' + I('trash-2') + r'''<span>Erase disk</span></button>
  <button class="k-btn k-btn-primary" disabled><span>Install</span></button>
  <button class="k-btn k-btn-primary" data-loading id="load"><span>Checking</span></button>
  <button class="k-btn k-btn-sm"><span>Check</span></button>
  <button class="k-btn" style="max-width:190px"><span>A label that is far too long for its button</span></button>
</div>''', r'''
The one way to trigger an action. `k-btn-primary` (filled with the accent) appears at most once per view, for the thing the view is for. Plain `k-btn` is the secondary action, `k-btn-quiet` is for cancel and dismiss, `k-btn-danger` for actions that destroy data.

- Markup: `<button class="k-btn k-btn-primary"><span>Install</span></button>`. Put the label in a `span` so long text truncates.
- Labels: sentence case, a verb first. "Install", "Check", "Erase disk".
- Loading: set `data-loading`; a short piece runs along the bottom edge. Keep the label, change its wording ("Checking").
- Disabled: the `disabled` attribute. Never hide a button that will come back.
- Do not put two primary buttons side by side, and do not use the accent for anything that is not the main action.
''', js=r'''
document.getElementById('load').addEventListener('click', function () { this.toggleAttribute('data-loading'); });
''')

comp('IconButton', 'Actions', 90, r'''
<div class="k-stage">
  <span class="k-tip"><button class="k-iconbtn" aria-label="Settings">''' + I('settings') + r'''</button><span role="tooltip">Settings</span></span>
  <button class="k-iconbtn" aria-label="Play" aria-pressed="false" id="pp">''' + I('play') + r'''</button>
  <button class="k-iconbtn k-iconbtn-danger" aria-label="Power">''' + I('power') + r'''</button>
  <button class="k-iconbtn k-iconbtn-sm" aria-label="Close">''' + I('x') + r'''</button>
  <button class="k-iconbtn" aria-label="Copy" disabled>''' + I('copy') + r'''</button>
</div>''', r'''
A square button that carries one symbol. Always give it an `aria-label`, and a Tooltip when the symbol alone could be misread.

- Sizes: 36px (`k-iconbtn`) and 28px (`k-iconbtn-sm`, inside dense panels).
- Toggle: set `aria-pressed`; pressed turns the symbol to `accent-text`. Swap the symbol too (play and pause).
- `k-iconbtn-danger` is reserved for power.
''', js=r'''
var pp = document.getElementById('pp');
pp.addEventListener('click', function () {
  var on = pp.getAttribute('aria-pressed') !== 'true';
  pp.setAttribute('aria-pressed', on);
  pp.querySelector('.k-icon').innerHTML = Kit.icon(on ? 'pause' : 'play');
});
''')

# ------------------------------------------------------------------ Inputs
comp('TextField', 'Inputs', 210, r'''
<div class="k-stage" style="align-items:flex-start">
  <div class="k-field"><label for="a">Host name</label><div class="k-input"><input id="a" value="larp"></div><span class="k-help">Lowercase letters, digits and hyphens.</span></div>
  <div class="k-field"><label for="b">Passphrase</label><div class="k-input k-input-pill"><input id="b" type="password" value="hunter22"><button class="k-iconbtn k-iconbtn-sm" aria-label="Show passphrase" id="eye">''' + I('eye') + r'''</button></div><span class="k-help"></span></div>
  <div class="k-field"><label for="c">Password</label><div class="k-input k-input-line"><input id="c" type="password" placeholder="Type to unlock"></div><span class="k-help"></span></div>
  <div class="k-field" data-state="error"><label for="d">Host name</label><div class="k-input"><input id="d" value="My PC" aria-invalid="true"></div><span class="k-help">Spaces are not allowed.</span></div>
  <div class="k-field" data-state="disabled"><label for="e">Disk</label><div class="k-input"><input id="e" value="/dev/nvme0n1" disabled></div><span class="k-help"></span></div>
  <div class="k-field"><label for="f">Empty</label><div class="k-input"><input id="f" placeholder="Nothing typed yet"></div><span class="k-help"></span></div>
</div>''', r'''
One line of text. Three shapes share one behaviour: `k-input` (box, the default in apps), `k-input-pill` (search and the greeter), `k-input-line` (the lock screen: only a bottom line).

- Structure: `.k-field` > `label`, `.k-input` > `input`, `.k-help`. The help line keeps its height so the layout does not jump when an error appears.
- Error: `data-state="error"` on the field and `aria-invalid` on the input. The help text says what is wrong and how to fix it.
- Passwords: `type="password"`; dots are spaced. A wrong password adds the class `k-shake` to the `.k-input` once.
- Focus turns the border to `focus` and adds the ring.
''', js=r'''
document.getElementById('eye').addEventListener('click', function () {
  var i = document.getElementById('b'), show = i.type === 'password';
  i.type = show ? 'text' : 'password';
  this.querySelector('.k-icon').innerHTML = Kit.icon(show ? 'eye-off' : 'eye');
});
''')

comp('SearchField', 'Inputs', 90, r'''
<div class="k-stage">
  <div class="k-field" style="width:340px"><div class="k-input k-input-pill">''' + I('search') + r'''<input aria-label="Search apps" placeholder="Search apps" value="fire"><span class="k-kbd">Esc</span></div></div>
</div>''', r'''
A pill field with the search symbol in front. Used by the app finder, the clipboard history, the store and settings.

- Results update while typing; there is no search button.
- Show the key that closes or clears it as a `k-kbd` hint at the end.
- Give the input an `aria-label`; there is no visible label.
''')

comp('Switch', 'Inputs', 80, r'''
<div class="k-stage">
  <label class="k-switch"><input type="checkbox" checked><span></span>24-hour clock</label>
  <label class="k-switch"><input type="checkbox"><span></span>Greeting</label>
  <label class="k-switch"><input type="checkbox" checked disabled><span></span>Locked on</label>
</div>''', r'''
On or off, applied at once. Use it for settings that take effect immediately; use Checkbox inside forms that are confirmed with a button.

- Markup: `<label class="k-switch"><input type="checkbox"><span></span>Label</label>`.
- The thumb slides with `ease-spring` and stretches slightly while pressed. On is the accent.
- Space toggles it; the ring sits on the track.
''')

comp('Checkbox', 'Inputs', 80, r'''
<div class="k-stage">
  <label class="k-check"><input type="checkbox" checked><span></span>Encrypt the disk</label>
  <label class="k-check"><input type="checkbox"><span></span>Enable hibernation</label>
  <label class="k-check"><input type="checkbox" disabled><span></span>Not available</label>
</div>''', r'''
A choice that is confirmed later, with the form's button. Several may be on at once.

- Markup: `<label class="k-check"><input type="checkbox"><span></span>Label</label>`.
- The mark is a small filled square that pops in; the box fills with the accent.
''')

comp('Radio', 'Inputs', 80, r'''
<div class="k-stage">
  <label class="k-check"><input type="radio" name="r" checked><span></span>English (US)</label>
  <label class="k-check"><input type="radio" name="r"><span></span>Deutsch</label>
  <label class="k-check"><input type="radio" name="r"><span></span>Français</label>
  <label class="k-check"><input type="radio" name="r"><span></span>Italiano</label>
</div>''', r'''
One of several, when all options should stay visible and there are more than four, or the labels are long. For two to four short options use Segmented.

- Markup: the Checkbox markup with `type="radio"` and a shared `name`.
- Arrow keys move the choice inside the group.
''')

comp('Segmented', 'Inputs', 90, r'''
<div class="k-stage">
  <div class="k-seg" aria-label="Variant"><button aria-selected="true">Dark</button><button>Light</button></div>
  <div class="k-seg" aria-label="Clock style"><button>Large</button><button aria-selected="true">Stacked</button><button>Minimal</button></div>
  <div class="k-seg" aria-label="Section"><button aria-selected="true">''' + I('calendar') + r'''Today</button><button>''' + I('gauge') + r'''System</button><button>''' + I('info') + r'''About</button></div>
</div>''', r'''
Two to four short options, one always chosen. Also the tab switch at the top of a panel.

- Markup: `<div class="k-seg"><button aria-selected="true">Dark</button><button>Light</button></div>`. `Kit.hydrate()` adds the thumb.
- The labels never move: every label has the same weight in both states. Only the thumb in the accent glides (`dur-base`, `ease-in-out`).
- As tabs: `data-for="#id"` points at a `.k-tabs` container; its sections switch with a short slide in the direction of travel.
- Listens to `change` with `detail.index` and `detail.value`. Left and right arrows move the choice.
''')

comp('Slider', 'Inputs', 110, r'''
<div class="k-stage-col">
  <label class="k-slider">''' + I('volume-2') + r'''<input type="range" min="0" max="100" value="62" data-unit="%" aria-label="Volume"><output></output></label>
  <label class="k-slider">''' + I('sun') + r'''<input type="range" min="0" max="100" value="35" data-unit="%" aria-label="Brightness"><output></output></label>
</div>''', r'''
A value on a range: volume, brightness, blur, timeouts.

- Markup: `<label class="k-slider"><i class="k-icon" data-icon="volume-2"></i><input type="range"><output></output></label>`.
- A 2px line, in the accent up to the value, with a narrow cream handle. The number at the end follows the handle; `data-unit` adds the unit.
- Arrow keys step by one.
''')

# ------------------------------------------------------------------ Feedback
comp('Progress', 'Feedback', 100, r'''
<div class="k-stage" style="align-items:flex-start">
  <div class="k-progress-row"><div><b>Writing image</b><span id="pv">0%</span></div><div class="k-progress" id="p" role="progressbar" aria-valuemin="0" aria-valuemax="100"><i></i></div></div>
  <div class="k-progress-row"><div><b>Looking for updates</b><span></span></div><div class="k-progress" data-indeterminate role="progressbar"><i></i></div></div>
  <button class="k-btn k-btn-sm" id="again"><span>Run again</span></button>
</div>''', r'''
How far something is, as a 2px line. With a known amount the part in the accent grows; without one, a short piece in the accent runs along the line.

- Markup: `<div class="k-progress" style="--p:40%"><i></i></div>`; unknown amount: add `data-indeterminate`.
- Say what is happening in words above the line (`k-progress-row`), with the number at the right.
- The boot splash uses the indeterminate form only.
''', js=r'''
var p = document.getElementById('p'), pv = document.getElementById('pv'), v = 0, timer;
function run() { clearInterval(timer); v = 0; timer = setInterval(function () { v = Math.min(100, v + 4 + Math.random() * 9); p.style.setProperty('--p', v + '%'); p.setAttribute('aria-valuenow', Math.round(v)); pv.textContent = Math.round(v) + '%'; if (v >= 100) clearInterval(timer); }, 380); }
document.getElementById('again').addEventListener('click', run); run();
''')

comp('Ring', 'Feedback', 130, r'''
<div class="k-stage">
  <div class="k-ringset"><div class="k-ring" data-value="12"></div>CPU</div>
  <div class="k-ringset"><div class="k-ring" data-value="38"></div>GPU</div>
  <div class="k-ringset"><div class="k-ring" data-value="71"></div>RAM</div>
  <button class="k-btn k-btn-sm" id="shuffle"><span>New values</span></button>
</div>''', r'''
A share of a whole at a glance: load, memory, battery. Three side by side in the System panel.

- Markup: `<div class="k-ring" data-value="38"></div>`; update with `Kit.ring(el, value)`.
- The arc fills over `dur-reveal`; the number rolls digit by digit.
- Always put the name under it. The ring alone says nothing.
''', js=r'''
document.getElementById('shuffle').addEventListener('click', function () {
  Array.prototype.forEach.call(document.querySelectorAll('.k-ring'), function (r) { Kit.ring(r, Math.round(Math.random() * 100)); });
});
''')

comp('Badge', 'Feedback', 80, r'''
<div class="k-stage">
  <span class="k-badge">Installed</span>
  <span class="k-badge k-badge-accent">Update</span>
  <span class="k-badge k-badge-error">''' + I('circle-alert') + r'''Offline</span>
  <span class="k-badge k-badge-count">3</span>
  <span class="k-muted" style="font-size:12px"><span class="k-dot k-dot-live"></span> Recording</span>
</div>''', r'''
One or two words of state beside a name, or a count.

- `k-badge` outlined grey for neutral state, `k-badge-accent` filled with the accent for the one thing that wants attention, `k-badge-error` with a symbol for a fault, `k-badge-count` for numbers.
- A badge is words, not a colour code: never rely on its colour alone.
- `k-dot` is the 6px dot in the accent for "live" (recording); `k-dot-live` lets it breathe.
''')

comp('Tooltip', 'Feedback', 110, r'''
<div class="k-stage" style="padding:48px 24px 24px 96px">
  <span class="k-tip" data-open><button class="k-iconbtn" aria-label="Wi-Fi">''' + I('wifi') + r'''</button><span role="tooltip">Wi-Fi :: Fibernet</span></span>
  <span class="k-tip"><button class="k-btn"><span>Hover me</span></button><span role="tooltip">Appears after a short wait</span></span>
</div>''', r'''
The name of a control that shows only a symbol, or one extra fact about it.

- Markup: wrap the control in `.k-tip` and add `<span role="tooltip">…</span>`.
- Appears above after `dur-slow` of hover or on keyboard focus, and leaves at once.
- One short line. Nothing a person needs in order to proceed belongs in a tooltip.
''')

comp('Notification', 'Feedback', 230, r'''
<div class="k-stage" style="align-items:flex-start">
  <div class="k-notif-stack" id="stack">
    <div class="k-notif k-surface">''' + I('download') + r'''<div><b>Update ready</b><p>Version 0.2.0 has been downloaded. It is applied the next time you restart.</p></div><time>21:04</time><footer><button class="k-btn k-btn-sm"><span>Restart</span></button><button class="k-btn k-btn-sm k-btn-quiet" data-x><span>Later</span></button></footer></div>
    <div class="k-notif k-surface" data-urgency="critical">''' + I('triangle-alert') + r'''<div><b>Disk almost full</b><p>Less than 2 GiB left on /home.</p></div><time>21:06</time></div>
  </div>
  <button class="k-btn k-btn-sm" id="send"><span>Send one</span></button>
</div>''', r'''
A message from the system or an app, top right under the bar.

- Parts: symbol, bold title, up to three lines of text, time, optional actions in a footer.
- Normal messages leave after a few seconds. `data-urgency="critical"` gets a border and symbol in the accent and a draining line, and stays until dismissed.
- Enters from the right (`k-notif-in`), leaves to the right (`Kit.dismiss(el)`); the rest of the stack closes the gap.
- Title: what happened. Text: what it means or what to do. No exclamation marks.
''', js=r'''
var stack = document.getElementById('stack'), n = 0;
var samples = [['clipboard', 'Copied', 'Screenshot saved to the clipboard.'], ['bluetooth', 'Headphones connected', 'Battery at 80%.'], ['package', 'Installed', 'The app is ready in the app finder.']];
function bind(el) { var x = el.querySelector('[data-x]'); if (x) x.addEventListener('click', function () { Kit.dismiss(el); }); }
Array.prototype.forEach.call(stack.children, bind);
document.getElementById('send').addEventListener('click', function () {
  var s = samples[n++ % samples.length], el = document.createElement('div');
  el.className = 'k-notif k-surface k-notif-in';
  el.innerHTML = '<i class="k-icon">' + Kit.icon(s[0]) + '</i><div><b>' + s[1] + '</b><p>' + s[2] + '</p></div><time>now</time>';
  stack.insertBefore(el, stack.firstChild);
  setTimeout(function () { Kit.dismiss(el); }, 4000);
});
''')

comp('Osd', 'Feedback', 90, r'''
<div class="k-stage">
  <div class="k-osd k-surface" id="osd">''' + I('volume-2') + r'''<div class="k-progress" style="--p:62%"><i></i></div><output>62</output></div>
  <button class="k-btn k-btn-sm" id="dn"><span>Volume down</span></button><button class="k-btn k-btn-sm" id="up"><span>Volume up</span></button>
</div>''', r'''
The answer to a hardware key: volume, brightness, mute. A pill at the bottom centre, above the dock.

- Parts: symbol, line, number. It never takes focus and leaves by itself after 1.5 seconds.
- The line follows the keys with `dur-fast` so repeated presses feel direct.
''', js=r'''
var val = 62, osd = document.getElementById('osd');
function set(d) { val = Math.max(0, Math.min(100, val + d)); osd.querySelector('.k-progress').style.setProperty('--p', val + '%'); osd.querySelector('output').textContent = val; }
document.getElementById('dn').addEventListener('click', function () { set(-5); });
document.getElementById('up').addEventListener('click', function () { set(5); });
''')

comp('Dialog', 'Feedback', 260, r'''
<div style="position:relative;height:260px">
  <div class="k-stage"><button class="k-btn" id="open"><span>Open dialog</span></button></div>
  <div class="k-scrim" id="scrim"><div class="k-dialog k-surface" role="dialog" aria-modal="true" aria-labelledby="dt">
    <h3 id="dt">Erase this disk?</h3>
    <p>Everything on /dev/nvme0n1 (512 GiB) will be deleted. This cannot be undone.</p>
    <footer><button class="k-btn k-btn-quiet" id="no"><span>Cancel</span></button><button class="k-btn k-btn-danger" id="yes"><span>Erase disk</span></button></footer>
  </div></div>
</div>''', r'''
A question that must be answered before anything else. Rare: only for actions that cannot be undone, or that end the session.

- Parts: a serif title that is the question, one or two sentences that name the consequence, actions bottom right with the safe one first.
- The button repeats the verb of the title ("Erase disk"), never "OK" or "Yes".
- Opens with a fade of the `scrim` and a small rise; Escape and the quiet button close it. Focus starts on the safe action.
''', js=r'''
var scrim = document.getElementById('scrim');
function close() { scrim.style.display = 'none'; document.getElementById('open').focus(); }
function open() { scrim.style.display = 'grid'; document.getElementById('no').focus({ preventScroll: true }); }
document.getElementById('open').addEventListener('click', open);
document.getElementById('no').addEventListener('click', close);
document.getElementById('yes').addEventListener('click', close);
document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
''')

# ------------------------------------------------------------------ Data
comp('List', 'Data', 230, r'''
<div class="k-stage" style="align-items:flex-start">
  <ul class="k-list k-surface" role="listbox" aria-label="Apps" id="list" tabindex="0">
    <li class="k-row k-enter" style="--i:0" role="option" aria-selected="true">''' + I('app-window') + r'''<span class="k-grow"><b>Fire</b>fox</span><small>Browser</small></li>
    <li class="k-row k-enter" style="--i:1" role="option">''' + I('folder') + r'''<span class="k-grow"><b>Fi</b>les</span><small>File manager</small></li>
    <li class="k-row k-enter" style="--i:2" role="option">''' + I('terminal') + r'''<span class="k-grow">Ghostty</span><small>Terminal</small></li>
    <li class="k-row k-enter" style="--i:3" role="option">''' + I('settings') + r'''<span class="k-grow">A setting with a name so long that it has to be cut off at the end</span><small>Settings</small></li>
    <li class="k-row k-enter" style="--i:4" role="option" aria-disabled="true">''' + I('package') + r'''<span class="k-grow">Store</span><small>Offline</small></li>
  </ul>
  <div class="k-list k-surface" style="width:220px"><div class="k-empty">Nothing copied yet.</div></div>
</div>''', r'''
Rows to pick from: app finder results, clipboard history, networks, devices.

- A row: symbol, name (`k-grow`, truncates), a faint note at the end.
- The chosen row gets a raised ground and a `>` in `accent-text` in front, like a cursor in a terminal. No coloured stripe.
- Rows enter one after another: class `k-enter` with `--i` as the position (`stagger` apart).
- Up and down move the choice, Enter takes it. Matching letters of a search are bold.
- Empty: one calm sentence in `k-empty`.
''', js=r'''
var list = document.getElementById('list'), rows = Array.prototype.filter.call(list.children, function (r) { return r.getAttribute('aria-disabled') !== 'true'; }), cur = 0;
function pick(i) { cur = (i + rows.length) % rows.length; Array.prototype.forEach.call(list.children, function (r) { r.setAttribute('aria-selected', r === rows[cur]); }); }
rows.forEach(function (r, i) { r.addEventListener('click', function () { pick(i); }); });
list.addEventListener('keydown', function (e) { if (e.key === 'ArrowDown') { e.preventDefault(); pick(cur + 1); } if (e.key === 'ArrowUp') { e.preventDefault(); pick(cur - 1); } });
''')

comp('SettingRow', 'Data', 260, r'''
<div class="k-stage-col">
  <div>
    <div class="k-setting"><div><b>24-hour clock</b><p>Show 21:04 instead of 9:04 pm.</p></div><label class="k-switch"><input type="checkbox" checked aria-label="24-hour clock"><span></span></label></div>
    <div class="k-setting"><div><b>Layout</b><p>Where the clock and the password field sit.</p></div><div class="k-seg" aria-label="Layout"><button>Centered</button><button aria-selected="true">Left</button></div></div>
    <div class="k-setting"><div><b>Password field</b><p>The shape of the field on the lock screen.</p></div><div class="k-seg" aria-label="Password field"><button>Pill</button><button>Box</button><button aria-selected="true">Line</button></div></div>
    <div class="k-setting"><div><b>Blur</b><p>How soft the wallpaper is behind the lock.</p></div><label class="k-slider" style="width:150px"><input type="range" min="0" max="20" value="6" aria-label="Blur"><output></output></label></div>
  </div>
</div>''', r'''
One setting per row: a bold title, one line that says what it does, and the control at the right.

- Markup: `.k-setting` > `div` (`b` title, `p` description) + one control (Switch, Segmented, Slider or a small Button).
- The description says what changes, in one line. If it needs two, the setting is two settings.
- Rows are separated by a hair line; there are no boxes around them.
''')

comp('InfoBlock', 'Data', 215, r'''
<div class="k-stage">
  <dl class="k-info">
    <h4>larp</h4>
    <dt>OS</dt><i>::</i><dd>Strix 0.1.0</dd>
    <dt>Kernel</dt><i>::</i><dd>6.18.2</dd>
    <dt>Shell</dt><i>::</i><dd>Quickshell on Hyprland</dd>
    <dt>Theme</dt><i>::</i><dd>Saturnus, dark</dd>
    <dt>Memory</dt><i>::</i><dd>7.4 GiB of 32 GiB</dd>
    <dt>Disk</dt><i>::</i><dd>162 GiB of 952 GiB, btrfs</dd>
    <dt>Uptime</dt><i>::</i><dd>3 hours, 19 minutes</dd>
  </dl>
</div>''', r'''
Facts as label and value, framed by double-line brackets with open corners. The signature frame of the system.

- Markup: `<dl class="k-info">` with `dt` label, `<i>::</i>`, `dd` value per row; an optional serif `h4` on top.
- Labels are bold, values regular and muted, `::` between them is faint.
- The brackets are `line` at reduced strength. Use the frame for system facts only (system info, About, the installer summary, `strix-info` in the terminal), at most once per view.
''')

comp('Card', 'Data', 150, r'''
<div class="k-stage">
  <div class="k-card" data-interactive tabindex="0"><h3>Ghostty</h3><p>A fast terminal that follows the theme, with shaders.</p></div>
  <div class="k-card"><h3>No network</h3><p>The store needs a connection to load the app list.</p><div style="margin-top:8px"><button class="k-btn k-btn-sm"><span>Try again</span></button></div></div>
</div>''', r'''
A bordered box for one self-contained thing: an app in the store, a state with its own action.

- Parts: serif title, a short muted text, optional action.
- `data-interactive` makes the whole card a target: the border brightens and it lifts by 2px on hover.
- Cards do not nest, and a list of plain facts is not a card: use List or InfoBlock.
''')

comp('Calendar', 'Data', 220, r'''
<div class="k-stage"><div class="k-cal" data-date="2026-11-10"></div></div>''', r'''
One month, Monday first, today marked in the accent. Lives in the Today panel.

- Markup: `<div class="k-cal" data-date="2026-11-10"></div>`; without `data-date` it shows the current day.
- The arrows step by month. Days of the neighbouring months are faint.
''')

comp('ContextMenu', 'Data', 170, r'''
<div class="k-stage" style="align-items:flex-start">
  <div class="k-menu k-surface" role="menu">
    <button role="menuitem">''' + I('copy') + r'''Copy<kbd>Ctrl C</kbd></button>
    <button role="menuitem">''' + I('clipboard') + r'''Paste<kbd>Ctrl V</kbd></button>
    <button role="menuitem" disabled>''' + I('image') + r'''Set as wallpaper</button>
    <hr>
    <button role="menuitem" data-danger>''' + I('trash-2') + r'''Delete<kbd>Del</kbd></button>
  </div>
</div>''', r'''
Actions for the thing under the pointer.

- Rows: symbol, verb, the key at the far right. Destructive actions sit last, after a divider, in `error`.
- Opens at the pointer with a quick pop from its top left corner; Escape or a click elsewhere closes it.
- At most eight rows. No sub-menus.
''')

# ------------------------------------------------------------------ Shell
SEARCH_JS = r'''
(function () {
  /* The index. In the shell it comes from the search service; here it is sample data in the same shape:
     k kind (app, action, setting, command, group), t title, p path, i symbol, w extra words, key binding, v current value */
  var E = [
    {k: 'group', t: 'Apps', i: 'layout-grid', id: 'apps'},
    {k: 'group', t: 'Style', i: 'swatch-book', id: 'style'},
    {k: 'group', t: 'Capture', i: 'scan', id: 'capture'},
    {k: 'group', t: 'Clipboard', i: 'clipboard', id: 'clipboard'},
    {k: 'group', t: 'Settings', i: 'sliders-horizontal', id: 'settings'},
    {k: 'group', t: 'Update', i: 'refresh-cw', id: 'update'},
    {k: 'group', t: 'System', i: 'power', id: 'system'},
    {k: 'group', t: 'Learn', i: 'book-open', id: 'learn'},
    {k: 'group', t: 'Commands', i: 'square-terminal', id: 'commands'},

    {k: 'app', t: 'Firefox', p: ['Apps'], i: 'app-window', w: 'browser web internet', g: 'apps'},
    {k: 'app', t: 'Ghostty', p: ['Apps'], i: 'terminal', w: 'terminal shell console', g: 'apps'},
    {k: 'app', t: 'Files', p: ['Apps'], i: 'folder', w: 'file manager explorer', g: 'apps'},
    {k: 'app', t: 'Text editor', p: ['Apps'], i: 'file', w: 'notes write code', g: 'apps'},
    {k: 'app', t: 'Image viewer', p: ['Apps'], i: 'image', w: 'photos pictures', g: 'apps'},
    {k: 'app', t: 'Music', p: ['Apps'], i: 'music', w: 'audio player songs', g: 'apps'},
    {k: 'app', t: 'Calculator', p: ['Apps'], i: 'plus', w: 'math', g: 'apps'},
    {k: 'app', t: 'Settings', p: ['Apps'], i: 'settings', w: 'preferences control panel', g: 'apps'},

    {k: 'action', t: 'Theme', p: ['Style'], i: 'palette', w: 'theme picker look colours wallpaper god', key: 'Super Ctrl Space', g: 'style', page: 1, id: 'theme'},
    {k: 'action', t: 'Keep this theme', p: ['Style', 'Theme'], i: 'lock', w: 'pin stop change cycle rotate god', key: 'K', g: 'theme'},
    {k: 'setting', t: 'Change theme', p: ['Settings', 'Appearance'], i: 'history', v: 'Every 10 minutes', w: 'cycle rotate interval god wallpaper'},
    {k: 'action', t: 'Saturnus', p: ['Style', 'Theme'], i: 'swatch-book', w: 'theme god wallpaper red default strix saturn time sickle', g: 'theme'},
    {k: 'action', t: 'Janus', p: ['Style', 'Theme'], i: 'swatch-book', w: 'theme god wallpaper patina green door', g: 'theme'},
    {k: 'action', t: 'Apollo', p: ['Style', 'Theme'], i: 'swatch-book', w: 'theme god wallpaper antique gold brass sun', g: 'theme'},
    {k: 'action', t: 'Mars', p: ['Style', 'Theme'], i: 'swatch-book', w: 'theme god wallpaper rust war', g: 'theme'},
    {k: 'action', t: 'Vulcanus', p: ['Style', 'Theme'], i: 'swatch-book', w: 'theme god wallpaper olive forge smith fire', g: 'theme'},
    {k: 'action', t: 'Neptunus', p: ['Style', 'Theme'], i: 'swatch-book', w: 'theme god wallpaper sea water blue trident', g: 'theme'},
    {k: 'action', t: 'Pluto', p: ['Style', 'Theme'], i: 'swatch-book', w: 'theme god wallpaper heather plum violet underworld', g: 'theme'},
    {k: 'action', t: 'Bacchus', p: ['Style', 'Theme'], i: 'swatch-book', w: 'theme god wallpaper claret wine', g: 'theme'},
    {k: 'action', t: 'Switch to light', p: ['Style'], i: 'sun', w: 'variant light dark appearance', g: 'style'},
    {k: 'action', t: 'Next wallpaper', p: ['Style'], i: 'images', w: 'background cycle', g: 'style'},
    {k: 'action', t: 'Region screenshot', p: ['Capture'], i: 'crop', w: 'screenshot area select snip', key: 'Print', g: 'capture'},
    {k: 'action', t: 'Window screenshot', p: ['Capture'], i: 'app-window', w: 'screenshot window', key: 'Shift Print', g: 'capture'},
    {k: 'action', t: 'Screen screenshot', p: ['Capture'], i: 'monitor', w: 'screenshot full display', key: 'Ctrl Print', g: 'capture'},
    {k: 'action', t: 'Record a region', p: ['Capture'], i: 'video', w: 'screencast recording video', g: 'capture'},
    {k: 'action', t: 'Colour picker', p: ['Capture'], i: 'pipette', w: 'color hex eyedropper', g: 'capture'},
    {k: 'action', t: 'History', p: ['Clipboard'], i: 'history', w: 'clipboard paste copied', key: 'Super V', g: 'clipboard'},
    {k: 'action', t: 'Clear history', p: ['Clipboard'], i: 'trash-2', w: 'clipboard delete', g: 'clipboard'},
    {k: 'action', t: 'Check for updates', p: ['Update'], i: 'refresh-cw', w: 'upgrade new version', g: 'update'},
    {k: 'action', t: 'Rebuild the system', p: ['Update'], i: 'hard-drive-download', w: 'rebuild switch nixos', g: 'update'},
    {k: 'action', t: 'What changed', p: ['Update'], i: 'file', w: 'release notes changelog', g: 'update'},
    {k: 'action', t: 'Lock', p: ['System'], i: 'lock', w: 'lock screen', key: 'Super Escape', g: 'system'},
    {k: 'action', t: 'Log out', p: ['System'], i: 'log-out', w: 'sign out session', g: 'system'},
    {k: 'action', t: 'Suspend', p: ['System'], i: 'moon', w: 'sleep', g: 'system'},
    {k: 'action', t: 'Hibernate', p: ['System'], i: 'moon-star', w: 'sleep disk', g: 'system'},
    {k: 'action', t: 'Restart', p: ['System'], i: 'rotate-cw', w: 'reboot', g: 'system'},
    {k: 'action', t: 'Shut down', p: ['System'], i: 'power', w: 'power off', g: 'system'},
    {k: 'action', t: 'All hotkeys', p: ['Learn'], i: 'keyboard', w: 'cheat sheet shortcuts keybindings keys', key: 'Super K', g: 'learn'},
    {k: 'action', t: 'Manual', p: ['Learn'], i: 'book-open', w: 'help documentation', g: 'learn'},

    {k: 'setting', t: 'Appearance', p: ['Settings'], i: 'swatch-book', w: 'theme look', g: 'settings', page: 1},
    {k: 'setting', t: 'Lock screen', p: ['Settings'], i: 'lock', w: 'lockscreen', g: 'settings', page: 1},
    {k: 'setting', t: 'Display', p: ['Settings'], i: 'monitor', w: 'screen monitor', g: 'settings', page: 1},
    {k: 'setting', t: 'Sound', p: ['Settings'], i: 'volume-2', w: 'audio volume', g: 'settings', page: 1},
    {k: 'setting', t: 'Network', p: ['Settings'], i: 'wifi', w: 'wi-fi wifi internet', g: 'settings', page: 1},
    {k: 'setting', t: 'Bluetooth', p: ['Settings'], i: 'bluetooth', w: 'devices pair', g: 'settings', page: 1},
    {k: 'setting', t: 'Keyboard', p: ['Settings'], i: 'keyboard', w: 'layout input', g: 'settings', page: 1},
    {k: 'setting', t: 'Hotkeys', p: ['Settings'], i: 'command', w: 'shortcuts keybindings keys bind change add', g: 'settings', page: 1},
    {k: 'setting', t: 'Notifications', p: ['Settings'], i: 'bell', w: 'alerts', g: 'settings', page: 1},
    {k: 'setting', t: 'Theme', p: ['Settings', 'Appearance'], i: 'palette', v: 'Saturnus', w: 'colours look god'},
    {k: 'setting', t: 'Variant', p: ['Settings', 'Appearance'], i: 'sun', v: 'Dark', w: 'light dark'},
    {k: 'setting', t: 'Text size', p: ['Settings', 'Appearance'], i: 'type', v: '100%', w: 'font scale'},
    {k: 'setting', t: 'Clock style', p: ['Settings', 'Lock screen'], i: 'clock', v: 'Stacked', w: 'time'},
    {k: 'setting', t: '24-hour clock', p: ['Settings', 'Lock screen'], i: 'clock', v: 'On', w: 'time format'},
    {k: 'setting', t: 'Password field', p: ['Settings', 'Lock screen'], i: 'lock', v: 'Line', w: 'input shape'},
    {k: 'setting', t: 'Background blur', p: ['Settings', 'Lock screen'], i: 'image', v: '6', w: 'wallpaper soft'},
    {k: 'setting', t: 'Wallpaper', p: ['Settings', 'Lock screen'], i: 'images', v: 'Another theme at each lock', w: 'god theme change rotate random'},
    {k: 'setting', t: 'Scale', p: ['Settings', 'Display'], i: 'monitor', v: '100%', w: 'resolution hidpi zoom'},
    {k: 'setting', t: 'Night light', p: ['Settings', 'Display'], i: 'moon', v: 'Off', w: 'warm blue light colour temperature'},
    {k: 'setting', t: 'Output device', p: ['Settings', 'Sound'], i: 'volume-2', v: 'Headphones', w: 'speaker audio'},
    {k: 'setting', t: 'Layout', p: ['Settings', 'Keyboard'], i: 'keyboard', v: 'Swiss German', w: 'keymap language'},
    {k: 'setting', t: 'Do not disturb', p: ['Settings', 'Notifications'], i: 'bell', v: 'Off', w: 'silence quiet mute'},

    {k: 'command', t: 'strix-update', p: ['Fetch and apply the latest release'], i: 'square-terminal', w: 'update upgrade', g: 'commands'},
    {k: 'command', t: 'strix-rebuild switch', p: ['Build the configuration in /etc/nixos and switch to it'], i: 'square-terminal', w: 'rebuild nixos', g: 'commands'},
    {k: 'command', t: 'strix-theme list', p: ['Show every theme and variant'], i: 'square-terminal', w: 'themes', g: 'commands'},
    {k: 'command', t: 'strix-theme set saturnus', p: ['Switch to the Saturnus theme'], i: 'square-terminal', w: 'theme'},
    {k: 'command', t: 'strix-theme set neptunus', p: ['Switch to the Neptunus theme'], i: 'square-terminal', w: 'theme god'},
    {k: 'command', t: 'strix-theme status', p: ['Check that every part shows the current theme'], i: 'square-terminal', w: 'theme'}
  ];
  var KINDS = ['all', 'app', 'action', 'setting', 'command'], LABEL = {app: 'App', action: 'Action', setting: 'Setting', command: 'Command', group: 'Menu'};
  var root = document.getElementById('srch'), input = root.querySelector('input'), list = document.getElementById('hits');
  var crumb = document.getElementById('crumb'), seg = document.getElementById('filter'), out = document.getElementById('said');
  var stack = [], filter = 'all', sel = 0, shown = [];

  function pathOf(e) { return (e.p || []).concat(e.k === 'setting' && !e.page ? [] : []); }
  function children(id) {
    if (id === 'settings') return E.filter(function (e) { return e.k === 'setting' && e.page; });
    var page = E.filter(function (e) { return e.k === 'setting' && e.page && e.t.toLowerCase().replace(/ /g, '') === id; })[0];
    if (page) return E.filter(function (e) { return e.k === 'setting' && e.p.length === 2 && e.p[1] === page.t; });
    return E.filter(function (e) { return e.g === id; });
  }
  function score(q, e) {
    var best = null, m;
    if ((m = Kit.fuzzy(q, e.t))) best = {score: m.score + 6, hits: m.hits};
    var extra = [(e.p || []).join(' '), e.w || ''].join(' ');
    if ((m = Kit.fuzzy(q, e.t + ' ' + extra)) && (!best || m.score * 0.55 > best.score)) best = {score: m.score * 0.55, hits: m.hits.filter(function (h) { return h < e.t.length; })};
    if (best && e.k === 'group') best.score -= 4;
    return best;
  }
  function search() {
    var q = input.value.trim(), here = stack.length ? stack[stack.length - 1] : null, pool, res;
    if (!q) {
      pool = here ? children(here.id) : E.filter(function (e) { return e.k === 'group'; });
      res = pool.map(function (e) { return {e: e, hits: []}; });
    } else {
      pool = here ? collect(here.id) : E;
      res = [];
      pool.forEach(function (e) { var m = score(q, e); if (m) res.push({e: e, hits: m.hits, s: m.score}); });
      res.sort(function (a, b) { return b.s - a.s; });
      if (res.length) { var top = res[0].s; res = res.filter(function (r) { return r.s >= top * 0.45; }); }
    }
    if (filter !== 'all') res = res.filter(function (r) { return r.e.k === filter || (r.e.k === 'group' && false); });
    return res.slice(0, 40);
  }
  function collect(id) {
    var acc = [], seen = {};
    (function walk(i) { children(i).forEach(function (e) { if (seen[e.t + e.p]) return; seen[e.t + e.p] = 1; acc.push(e); if (e.k === 'group' || e.page) walk(e.id || e.t.toLowerCase().replace(/ /g, '')); }); })(id);
    return acc;
  }
  function row(r, n) {
    var e = r.e, right = '';
    if (e.k === 'group' || e.page) right = '<i class="k-icon">' + Kit.icon('chevron-right') + '</i>';
    else if (e.v) right = '<em>' + e.v + '</em>' + LABEL[e.k];
    else if (e.key) right = e.key.split(' ').map(function (k) { return '<span class="k-kbd">' + k + '</span>'; }).join('') + LABEL[e.k];
    else right = LABEL[e.k];
    var path = (e.p && e.p.length) ? '<span class="p">' + e.p.join('<i>›</i>') + '</span>' : '';
    return '<li class="k-hit" role="option" data-kind="' + e.k + '" data-n="' + n + '" aria-selected="' + (n === sel) + '"><i class="k-icon">' + Kit.icon(e.i) + '</i><div><span class="t">' + Kit.mark(e.t, r.hits) + '</span>' + path + '</div><span class="r">' + right + '</span></li>';
  }
  function draw(dir) {
    shown = search();
    if (sel >= shown.length) sel = Math.max(0, shown.length - 1);
    list.innerHTML = shown.length ? shown.map(row).join('') : '<li class="k-empty">Nothing matches. <span class="k-kbd">Enter</span> runs it in a terminal.</li>';
    if (dir) { list.removeAttribute('data-dir'); void list.offsetWidth; list.setAttribute('data-dir', dir); }
    crumb.style.display = stack.length ? 'inline-flex' : 'none';
    crumb.innerHTML = stack.map(function (s) { return s.t; }).join('<i>›</i>');
    input.placeholder = stack.length ? 'Search in ' + stack[stack.length - 1].t : 'Search apps, actions, settings and commands';
    var cur = list.querySelector('[aria-selected="true"]'); if (cur) cur.scrollIntoView({block: 'nearest'});
  }
  function enter(e) { stack.push({id: e.id || e.t.toLowerCase().replace(/ /g, ''), t: e.t}); input.value = ''; sel = 0; draw(1); }
  function up() { if (!stack.length) return false; stack.pop(); sel = 0; draw(-1); return true; }
  function run(r) {
    if (!r) { if (input.value.trim()) out.textContent = 'Runs in a terminal :: ' + input.value.trim(); return; }
    var e = r.e;
    if (e.k === 'group' || e.page) return enter(e);
    var what = {app: 'Opens ', action: 'Runs ', setting: 'Opens Settings at ', command: 'Runs in a terminal :: '}[e.k];
    out.textContent = what + (e.k === 'setting' ? e.p.slice(1).concat(e.t).join(' › ') : e.k === 'action' ? (e.p || []).concat(e.t).join(' › ') : e.t);
    var gods = JSON.parse(root.getAttribute('data-gods') || '{}'), g = e.t.toLowerCase();
    if (e.p && e.p[1] === 'Theme' && gods[g]) {
      var host = root.closest('[data-wall-host]'); host.setAttribute('data-theme', g);
      host.querySelector('.k-wall').style.backgroundImage = 'url(' + gods[g] + ')';
    }
  }
  input.addEventListener('input', function () { sel = 0; out.textContent = ''; draw(); });
  input.addEventListener('keydown', function (ev) {
    if (ev.key === 'ArrowDown') { ev.preventDefault(); sel = Math.min(shown.length - 1, sel + 1); draw(); }
    else if (ev.key === 'ArrowUp') { ev.preventDefault(); sel = Math.max(0, sel - 1); draw(); }
    else if (ev.key === 'Enter') { ev.preventDefault(); run(shown[sel]); }
    else if (ev.key === 'Tab') { ev.preventDefault(); var i = (KINDS.indexOf(filter) + (ev.shiftKey ? KINDS.length - 1 : 1)) % KINDS.length; seg._k.select(i); }
    else if (ev.key === 'Backspace' && !input.value) { if (up()) ev.preventDefault(); }
    else if (ev.key === 'Escape') { ev.preventDefault(); if (input.value) { input.value = ''; draw(); } else if (!up()) { out.textContent = 'Closes'; } }
  });
  list.addEventListener('mousemove', function (ev) { var li = ev.target.closest('.k-hit'); if (li && +li.dataset.n !== sel) { sel = +li.dataset.n; Array.prototype.forEach.call(list.children, function (c) { c.setAttribute('aria-selected', +c.dataset.n === sel); }); } });
  list.addEventListener('click', function (ev) { var li = ev.target.closest('.k-hit'); if (li) { sel = +li.dataset.n; run(shown[sel]); input.focus({preventScroll: true}); } });
  seg.addEventListener('change', function (ev) { filter = KINDS[ev.detail.index]; sel = 0; draw(); input.focus({preventScroll: true}); });
  input.value = root.getAttribute('data-query') || '';
  draw();
  try { input.focus({preventScroll: true}); } catch (e) {}
})();
'''

comp('Search', 'Shell', 560, r'''
<div data-wall-host data-theme="saturnus" style="position:relative;height:560px;overflow:hidden;background:var(--background)">''' + WALL(SATURNUS, ' data-dim', pos='center 30%') + r'''
  <div class="k-grain"></div>
  <div style="position:absolute;inset:0;display:flex;justify-content:center;align-items:flex-start;padding-top:56px">
    <div class="k-search k-surface" id="srch" data-query="theme" data-gods=''' + "'" + json.dumps(dict(zip(['saturnus', 'janus', 'apollo', 'mars', 'vulcanus', 'neptunus', 'pluto', 'bacchus'], [SATURNUS, JANUS, APOLLO, MARS, VULCANUS, NEPTUNUS, PLUTO, BACCHUS]))) + "'" + r''' role="dialog" aria-label="Search">
      <div class="k-search-head">''' + I('search') + r'''<span class="k-crumb" id="crumb"></span><input aria-label="Search" autocomplete="off" spellcheck="false"><span class="k-kbd">Esc</span></div>
      <div class="k-search-filter"><div class="k-seg" id="filter" aria-label="Show"><button aria-selected="true">All</button><button>Apps</button><button>Actions</button><button>Settings</button><button>Commands</button></div><span class="k-plate">one field for everything</span></div>
      <ul class="k-hits" id="hits" role="listbox"></ul>
      <div class="k-search-foot"><output id="said"></output></div>
    </div>
  </div>
</div>''', r'''
One field finds everything: apps, the actions of the system menu, settings down to a single row, and commands. It replaces a separate app launcher and system menu. Opens with Super Space, centred near the top over the dimmed desktop; Super Alt Space opens it with the Apps filter set.

- With an empty field it is the system menu: Apps, Style, Capture, Clipboard, Settings, Update, System, Learn, Commands. Enter on a group opens it, the group shows as a crumb in the field, Backspace on an empty field goes back up. Typing searches inside the open group.
- Typing searches every level at once. Each result shows where it lives under its name, in the serif italic: "Style › Theme", "Settings › Lock screen". The same word can appear more than once with different places; the place tells them apart.
- Kinds, named at the right of each row: App, Action, Setting, Command, Menu. Actions show their keybinding, settings show their current value.
- Enter: an app starts, an action runs, a setting opens Settings scrolled to that row with the row marked, a command runs in a terminal. Text that matches nothing runs as a command in a terminal.
- Matching is fuzzy: the letters in order, word starts count most, so "nl" finds Night light and "rs" finds Region screenshot. Titles count more than places and extra words; results far below the best one are left out; frequently used entries rise.
- Tab and Shift Tab cycle the filter (All, Apps, Actions, Settings, Commands). Up and Down move, Esc clears the field, a second Esc closes.
- Rows: 40px, symbol, title in mono with the matched letters in `text` and semibold, the place in `aside` style, kind in `micro`. The chosen row has the raised ground and the caret in `accent-text`, as in List.
- Motion: the panel drops 8px into place over `dur-base`; entering a group slides the list in from the right, going back from the left; results update in place without animation while typing.
- Markup: `.k-search.k-surface` > `.k-search-head` (symbol, `.k-crumb`, `input`, the Esc chip), `.k-search-filter` (a Segmented), `ul.k-hits` > `li.k-hit[data-kind]`, `.k-search-foot` (only the result line, hidden while empty; the keys are on the cheat sheet). `Kit.fuzzy(query, text)` and `Kit.mark(text, hits)` do the matching and the highlighting.
''', js=SEARCH_JS)


BAR = r'''
<div class="k-bar" role="toolbar" aria-label="Status">
  <div>
    <button aria-label="Search apps">''' + I('search') + r'''<b id="clock">21:04</b></button>
    <span class="k-meter" title="CPU">''' + I('cpu') + r'''<u style="--p:17%"></u><span class="k-roll" data-value="17%" id="m-cpu"></span></span>
    <span class="k-meter" title="Memory">''' + I('memory-stick') + r'''<u style="--p:24%"></u><span>7.4 GiB</span></span>
    <span class="k-meter" title="Temperature">''' + I('thermometer') + r'''<u style="--p:46%"></u><span class="k-roll" data-value="46°" id="m-tmp"></span></span>
  </div>
  <div>
    <span class="k-ws" role="tablist" aria-label="Workspaces"><button aria-label="Workspace 1" data-used></button><button aria-label="Workspace 2" data-used aria-current="true"></button><button aria-label="Workspace 3" data-used></button><button aria-label="Workspace 4"></button><button aria-label="Workspace 5"></button></span>
    <button class="k-track" aria-label="Now playing">''' + I('music') + r'''<span>Nocturne in E-flat major</span></button>
  </div>
  <div>
    <button class="k-rec" aria-label="Recording">''' + I('video') + r'''<span class="k-dot k-dot-live"></span></button>
    <button aria-label="Notifications, 3 new">''' + I('bell') + r'''<b>3</b></button>
    <button class="k-power" aria-label="Session">''' + I('power') + r'''</button>
  </div>
</div>'''
BAR_JS = r'''
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
'''
comp('TopBar', 'Shell', 120, r'''
<div style="position:relative;height:120px;overflow:hidden">''' + WALL(SATURNUS, pos='center top') + r'''<div style="position:relative">''' + BAR + r'''</div></div>''', r'''
The status line at the top of the screen. It has no surface of its own: small text and symbols sit straight on the wallpaper, in grey, with the accent for the one active thing.

- Left: search with the clock, then CPU, memory and temperature, each as symbol, a 3px vertical meter and a value.
- Middle: workspaces as dots, the active one a pill in the accent; next to them the playing track.
- Right: recording (with a dot in the accent while it runs), the bell with its count, power in `accent-text`.
- The bar is for reading. Search opens Search, the track opens the media player in the dock, the bell opens notifications, power opens the session menu. Everything adjustable lives in the dock.
- Height `bar-height`. Values roll when they change; the workspace pill slides.
''', js=BAR_JS)

DOCK = r'''
<div class="k-dock" id="dock">
  <div class="k-panel k-surface" id="p-main">
    <div class="k-panel-head"><div class="k-seg" data-for="#tabs" aria-label="Section"><button aria-selected="true">''' + I('calendar') + r'''Today</button><button>''' + I('gauge') + r'''System</button><button>''' + I('info') + r'''About</button></div></div>
    <div class="k-tabs" id="tabs">
      <section data-active>
        <div class="k-today">
          <div><span class="k-plate" id="dow">Tuesday</span><h3 id="dmy">10 November</h3>
            <div class="k-rule"><i></i></div>
            <div class="k-wx">''' + I('cloud-sun') + r'''<div><b>8°</b>Partly cloudy :: Basel</div></div>
            <div class="k-progress-row k-day" style="width:100%"><div><b>Day</b><span id="dayp">88%</span></div><div class="k-progress" id="dayl" style="width:100%"><i></i></div></div>
          </div>
          <div class="k-cal"></div>
        </div>
      </section>
      <section>
        <div class="k-sys">
          <div class="k-ringset"><div class="k-ring" data-target="17"></div>CPU</div>
          <div class="k-ringset"><div class="k-ring" data-target="6"></div>GPU</div>
          <div class="k-ringset"><div class="k-ring" data-target="24"></div>RAM</div>
        </div>
        <div class="k-progress-row"><div><b>Disk /</b><span>162 GiB of 952 GiB</span></div><div class="k-progress" style="--p:17%"><i></i></div></div>
      </section>
      <section>
        <div class="k-about">
          <div><h3>Strix<small>0.1.0</small></h3><span class="k-motto">nocte vigilat</span></div>
          <div class="k-rule"><i></i></div>
          <div class="k-up"><i class="k-icon" data-icon="check" id="up-i"></i><div><b id="up-t">You are up to date</b><small id="up-s">Channel :: stable. Checked just now</small><div class="k-progress" id="up-p" data-indeterminate style="width:100%;margin-top:6px;display:none"><i></i></div></div><button class="k-btn k-btn-sm" id="up-b"><span>Check</span></button></div>
        </div>
      </section>
    </div>
  </div>
  <div class="k-panel k-surface" data-size="sm" id="p-wifi">
    <h4>Wi-Fi<label class="k-switch"><input type="checkbox" checked aria-label="Wi-Fi"><span></span></label></h4>
    <ul class="k-list" role="listbox"><li class="k-row" role="option" aria-selected="true">''' + I('wifi') + r'''<span class="k-grow">Fibernet</span><small>Connected</small></li><li class="k-row" role="option">''' + I('wifi') + r'''<span class="k-grow">Atelier</span>''' + I('lock') + r'''</li><li class="k-row" role="option">''' + I('wifi') + r'''<span class="k-grow">Guest</span></li></ul>
  </div>
  <div class="k-panel k-surface" data-size="sm" id="p-bt">
    <h4>Bluetooth<label class="k-switch"><input type="checkbox" checked aria-label="Bluetooth"><span></span></label></h4>
    <ul class="k-list" role="listbox"><li class="k-row" role="option" aria-selected="true">''' + I('bluetooth') + r'''<span class="k-grow">Headphones</span><small>80%</small></li><li class="k-row" role="option">''' + I('keyboard') + r'''<span class="k-grow">Keyboard</span><small>Paired</small></li></ul>
  </div>
  <div class="k-panel k-surface" data-size="sm" id="p-vol">
    <h4>Sound</h4>
    <label class="k-slider" style="width:100%">''' + I('volume-2') + r'''<input type="range" min="0" max="100" value="62" data-unit="%" aria-label="Volume"><output></output></label>
  </div>
  <div class="k-panel k-surface" id="p-media" style="width:344px;padding:0">
    <div class="k-media"><div class="k-cover">''' + I('disc-3') + r'''</div><div style="min-width:0"><b>Nocturne in E-flat major</b><small>Sample artist</small></div>
      <div class="k-ctl"><span>1:12</span><div class="k-progress" style="--p:27%"><i></i></div><span>4:31</span><button class="k-iconbtn k-iconbtn-sm" aria-label="Previous">''' + I('skip-back') + r'''</button><button class="k-iconbtn k-iconbtn-sm" aria-label="Pause">''' + I('pause') + r'''</button><button class="k-iconbtn k-iconbtn-sm" aria-label="Next">''' + I('skip-forward') + r'''</button></div></div>
  </div>
  <div class="k-edge" role="toolbar" aria-label="Dock"><u></u><div class="k-edge-in">
    <button aria-label="Settings">''' + I('settings') + r'''</button><s></s>
    <button data-panel="#p-main" data-tab="0" aria-label="Today">''' + I('cloud-sun') + r'''<b>8°</b><span id="pdate">Tue 10 Nov</span></button><s></s>
    <button data-panel="#p-media" aria-label="Media">''' + I('music') + r'''</button>
    <button data-panel="#p-wifi" aria-label="Wi-Fi">''' + I('wifi') + r'''</button>
    <button data-panel="#p-bt" aria-label="Bluetooth">''' + I('bluetooth') + r'''</button>
    <button data-panel="#p-vol" aria-label="Sound">''' + I('volume-2') + r'''</button><s></s>
    <button data-panel="#p-main" data-tab="2" aria-label="About">''' + I('info') + r'''</button>
  </div></div>
</div>'''
DOCK_JS = r'''
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
'''
comp('EdgeDock', 'Shell', 380, r'''
<div style="position:relative;height:380px;overflow:hidden">''' + WALL(NEPTUNUS, pos='center 30%') + r'''
  <div class="micro" style="position:absolute;right:16px;top:12px;color:var(--text-faint)">Preview only: move the pointer to the bottom edge</div>
  <div class="k-dockbar">''' + DOCK + r'''</div>
</div>''', r'''
The dock is part of the bottom edge of the screen, not a floating bar. At rest it is a tab 5px high and 132px wide with a short line in the accent, flush with the edge, its corners flaring into it. When the pointer reaches the bottom edge it rises to 28px and widens to fit its content. When the pointer leaves, it sinks back after a short wait.

- Everything that can be adjusted starts here: settings, the date with the weather, media, Wi-Fi, Bluetooth, sound, about. A click on a symbol lets its panel grow upward out of that symbol; a second click, Escape or a click elsewhere folds it back.
- Main panel: a Segmented with Today (date, weather, calendar, the day as a line), System (three rings and the disk) and About (name, version, channel, and "Check", which runs the update and shows its progress in place).
- Small panels (`data-size="sm"`): Wi-Fi and Bluetooth as a switch with a List, sound as a Slider, media as a MediaPlayer.
- While a panel is open or a control inside has keyboard focus, the dock stays out.
- Motion: height over `dur-base`, width over `dur-slow`, content fades in `dur-fast` later. A panel scales up from its symbol over `dur-slow`.
- Markup: `.k-dockbar` (the hot strip along the bottom edge) > `.k-dock` > panels (`.k-panel.k-surface` with an id) + `.k-edge` > `u` (the line in the accent) + `.k-edge-in` > buttons with `data-panel="#id"` and optional `data-tab`. Thin `s` elements separate groups.
- `data-pinned` on `.k-dock` keeps it out, for touch screens.
''', js=DOCK_JS + "\nsetTimeout(function () { var d = document.getElementById('dock')._k; d.show(); d.open(document.querySelector('.k-edge [data-panel=\"#p-main\"]')); }, 500);")

comp('MediaPlayer', 'Shell', 130, r'''
<div class="k-stage"><div class="k-media k-surface"><div class="k-cover">''' + I('disc-3') + r'''</div><div style="min-width:0"><b>Nocturne in E-flat major, a title that runs on</b><small>Sample artist</small></div>
  <div class="k-ctl"><span>1:12</span><div class="k-progress" style="--p:27%"><i></i></div><span>4:31</span><button class="k-iconbtn k-iconbtn-sm" aria-label="Previous">''' + I('skip-back') + r'''</button><button class="k-iconbtn k-iconbtn-sm" aria-label="Pause">''' + I('pause') + r'''</button><button class="k-iconbtn k-iconbtn-sm" aria-label="Next">''' + I('skip-forward') + r'''</button></div></div></div>''', r'''
What is playing, with the three transport buttons. Opens from the music symbol in the dock or from the track in the top bar.

- Parts: cover (a disc symbol when there is none), serif title, muted artist, elapsed and total time around a Progress line, previous, play or pause, next.
- Title and artist truncate; they never wrap.
- Nothing playing: the pill hides its music symbol and the top bar shows no track.
''')

comp('Visualizer', 'Shell', 150, r'''
<div class="k-stage" style="display:block"><div class="k-viz" data-bars="56"></div></div>''', r'''
Bars that follow the sound. Grey at rest, the accent at the peaks.

- Markup: `<div class="k-viz" data-bars="56"></div>`. Feed it with `el._k.frame(levels)` (values 0 to 1); without a source it idles on a soft signal.
- Bars above 0.72 switch to `accent` (`chart-1`); the rest are `text-muted`.
- With reduced motion it stands still.
''')

comp('SlantCard', 'Shell', 320, r'''
<div class="k-carousel" style="height:320px" tabindex="-1" aria-label="Themes"><div class="k-carousel-track" id="track"></div></div>''', r'''
The tall slanted card of the theme picker, and the carousel that holds a row of them. The preview shows the eight god themes.

- Each card is a parallelogram that overlaps its neighbour. The chosen card in the middle is 420px wide and taller, with a cream hair edge and the theme's name in blackletter; all others are 96px wide and dimmed.
- Markup: `.k-carousel` > `.k-carousel-track` > `button.k-slant` with `.k-slant-art` (the preview), `.k-slant-edge`, `.k-slant-name`.
- Paging: left and right arrows, the wheel, or a click on a neighbour. The row glides over `dur-slow` while the old middle narrows and the new one widens.
- A click on the middle card fires `apply` with the pointer position, which is where the circular reveal starts (`Kit.reveal`).
- The art is the theme's or the god's own engraving, never a screenshot of somebody else's work.
''', js=r'''
var GODS = ''' + json.dumps([['Saturnus', SATURNUS], ['Janus', JANUS], ['Apollo', APOLLO], ['Mars', MARS], ['Vulcanus', VULCANUS], ['Neptunus', NEPTUNUS], ['Pluto', PLUTO], ['Bacchus', BACCHUS]]) + r''';
document.getElementById('track').innerHTML = GODS.map(function (g, i) {
  return '<button class="k-slant" aria-selected="' + (i === 0) + '" aria-label="' + g[0] + '"><span class="k-slant-art"><img alt="" src="' + g[1] + '"></span><span class="k-slant-edge"></span><span class="k-slant-name">' + g[0] + '</span></button>';
}).join('');
Kit.hydrate(document);
''')

comp('WindowFrame', 'Shell', 260, r'''
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:12px;height:260px">
  <div class="k-win" data-active id="w1"><div class="k-win-body"><span class="k-muted">Active window :: quiet accent border</span></div></div>
  <div style="display:grid;grid-template-rows:1fr 1fr;gap:12px;min-height:0">
    <div class="k-win" id="w2" style="opacity:var(--dim-inactive)"><div class="k-win-body"><span class="k-muted">Inactive :: grey border</span></div></div>
    <div class="k-win"><div class="k-titlebar"><b>Bootstick</b><span>Write the installer to a USB stick</span><button aria-label="Minimize">''' + I('minus') + r'''</button><button aria-label="Maximize">''' + I('square') + r'''</button><button aria-label="Close" data-close>''' + I('x') + r'''</button></div><div class="k-win-body"><span class="k-muted">App title bar on Windows</span></div></div>
  </div>
</div>''', r'''
How a window looks. Under Hyprland the compositor draws it: 1px border, 4px corners (`radius-md`), `shadow-window`, 12px (`space-3`) between windows and to the screen edge. The focused window has a quiet border in the accent (`border-active`, the accent quietened toward `border`), all others the grey one and are a touch dimmer. The border eases over `dur-slow`; focus never flashes.

- Tiled windows have no title bar. The border colour fades over `dur-base` when focus moves.
- Apps that run outside Hyprland (the Windows bootstick app) draw `k-titlebar`: serif app name, a muted subtitle, then minimise, maximise, close as 40px wide targets; close fills with the accent on hover.
- Click a window in the preview to move focus.
''', js=r'''
var wins = document.querySelectorAll('.k-win');
Array.prototype.forEach.call(wins, function (w) { w.addEventListener('click', function () { Array.prototype.forEach.call(wins, function (o) { o.removeAttribute('data-active'); o.style.opacity = 'var(--dim-inactive)'; }); w.setAttribute('data-active', ''); w.style.opacity = 1; }); });
''')

# ------------------------------------------------------------------ Screens
SCREENS = []
def screen(name, height, html, doc, js='', css='', width=1280):
    SCREENS.append(dict(name=name, group='Screens', height=height, html=html, doc=doc, js=js, css=css, width=width))

screen('LockScreen', 720, r'''
<div class="k-screen" id="scr" data-theme="saturnus">
  ''' + WALL(SATURNUS, ' data-dim id="wall"') + r'''
  <div class="k-grain"></div>
  <div id="lock">
    <div class="col">
      <div class="clock" id="hh">21</div><div class="clock" id="mm">04</div>
      <div class="caption k-muted" id="date" style="margin-top:14px">Tuesday, 10 November</div>
      <div class="motto" id="greet" style="color:var(--text)">good evening, livio</div>
      <div class="k-field" id="field" style="width:200px;margin-top:22px"><div class="k-input k-input-line"><input id="pw" type="password" aria-label="Password" placeholder="Password" autocomplete="off"></div><span class="k-help" id="help"></span></div>
      <div style="display:flex;gap:2px;margin:2px 0 0 -7px">
        <span class="k-tip"><button class="k-iconbtn" aria-label="Log out">''' + I('log-out') + r'''</button><span role="tooltip">Log out</span></span>
        <span class="k-tip"><button class="k-iconbtn" aria-label="Shut down">''' + I('power') + r'''</button><span role="tooltip">Shut down</span></span>
        <span class="k-tip"><button class="k-iconbtn" aria-label="Suspend">''' + I('moon') + r'''</button><span role="tooltip">Suspend</span></span>
        <span class="k-tip"><button class="k-iconbtn" aria-label="Restart">''' + I('rotate-cw') + r'''</button><span role="tooltip">Restart</span></span>
      </div>
    </div>
    <div class="foot caption k-muted"><b>3 notifications</b><br><b>CPU</b> <i>::</i> 8%&emsp;<b>RAM</b> <i>::</i> 24%&emsp;<b>GPU</b> <i>::</i> 3%</div>
    <div class="mark"><div class="k-wordmark">Strix</div><div class="k-rule" style="margin:4px 0 2px"><i></i></div><div class="k-motto">nocte vigilat</div></div>
    <div class="plate k-plate" id="lplate">Saturnus with his sickle, lord of time, in his niche. Engraved by Hendrick Goltzius after Polidoro da Caravaggio, 1592</div>
    <div class="hint micro">Preview only: the password is strix</div>
  </div>
  <button class="k-btn" id="relock" style="position:absolute;left:50%;bottom:40px;transform:translateX(-50%);display:none"><span>Lock again</span></button>
</div>''', r'''
The lock screen, left layout. Every time the screen locks, it shows another god theme: the plate, the accent and the tinted grounds change together, and the same god never comes twice in a row. The desktop keeps its own theme; after unlocking, its colours come back. A narrow column on the left over the dimmed engraving: a very light clock with hours stacked over minutes, the date, a greeting in spaced italic, the password as a single hair line, and four session buttons. Bottom left: notifications and load. Bottom right: the blackletter wordmark, a lozenge rule and the motto. Bottom centre: the plate caption of the engraving.

- States, all in this preview: empty, typing (dots), wrong password (the line turns to `error`, shakes once, and says "Wrong password"), Caps Lock ("Caps Lock is on"), locked out after three tries with a countdown, unlocking.
- Unlock: the column fades and slides left while the engraving sharpens and brightens over `dur-reveal`.
- The demo password is `strix`. Type anything else to see the error. "Lock again" locks with the next god.
- Settings › Lock screen › Wallpaper turns the change off and keeps one god instead.
- Text: date as "Tuesday, 10 November"; greeting lowercase by time of day with the user name.
- The centred layout and the greeter use the same parts, centred, with the wordmark above the field.
''', css=r'''
#lock { position: absolute; inset: 0; transition: opacity var(--dur-slow) var(--ease-in), transform var(--dur-slow) var(--ease-in); }
#lock[data-out] { opacity: 0; transform: translateX(-24px); pointer-events: none; }
#lock .col { position: absolute; left: var(--space-8); top: 76px; }
#lock .clock { color: var(--text); margin-left: -6px; }
#lock .foot { position: absolute; left: var(--space-8); bottom: var(--space-6); line-height: 18px; }
#lock .foot b { color: var(--text); font-weight: 500; }
#lock .foot i { font-style: normal; color: var(--text-faint); }
#lock .mark { position: absolute; right: var(--space-8); bottom: var(--space-6); text-align: center; }
#lock .plate { position: absolute; left: 0; right: 0; bottom: var(--space-6); text-align: center; opacity: 0.8; }
#lock .hint { position: absolute; right: var(--space-5); top: var(--space-4); color: var(--text-faint); }
.k-wall[data-clear] { filter: none; transform: none; }
''', js=r'''
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
  var GODS = __LOCK_GODS__, scr = document.getElementById('scr'), plate = document.getElementById('lplate'), last = -1;
  function pick() {
    var i; do { i = Math.floor(Math.random() * GODS.length); } while (i === last && GODS.length > 1);
    last = i; var g = GODS[i];
    scr.setAttribute('data-theme', g[0]); wall.style.backgroundImage = 'url(' + g[1] + ')'; plate.textContent = g[2];
  }
  try { pick(); } catch (e) {}
  document.getElementById('relock').addEventListener('click', function () { this.style.display = 'none'; pick(); lock.removeAttribute('data-out'); wall.removeAttribute('data-clear'); pw.value = ''; });
})();
''')

CODE = r'''<span class="ln"> 1</span>  <span class="cm">// Reads a theme and checks its contrast rules.</span>
<span class="ln"> 2</span>  <span class="kw">use</span> <span class="ty">std::path::Path</span><span class="op">;</span>
<span class="ln"> 3</span>
<span class="ln"> 4</span>  <span class="co">#[derive(Debug)]</span>
<span class="ln"> 5</span>  <span class="kw">pub struct</span> <span class="ty">Variant</span> <span class="op">{</span>
<span class="ln"> 6</span>      <span class="kw">pub</span> name<span class="op">:</span> <span class="ty">String</span><span class="op">,</span>
<span class="ln"> 7</span>      <span class="kw">pub</span> colors<span class="op">:</span> <span class="ty">Colors</span><span class="op">,</span>
<span class="ln"> 8</span>  <span class="op">}</span>
<span class="ln"> 9</span>
<span class="ln">10</span>  <span class="kw">pub fn</span> <span class="fn">check</span><span class="op">(</span>path<span class="op">:</span> <span class="op">&amp;</span><span class="ty">Path</span><span class="op">)</span> <span class="op">-&gt;</span> <span class="ty">Result</span><span class="op">&lt;</span><span class="ty">Variant</span><span class="op">&gt;</span> <span class="op">{</span>
<span class="ln">11</span>      <span class="kw">let</span> text <span class="op">=</span> <span class="fn">read</span><span class="op">(</span>path<span class="op">)?;</span>
<span class="ln">12</span>      <span class="kw">let</span> v<span class="op">:</span> <span class="ty">Variant</span> <span class="op">=</span> toml<span class="op">::</span><span class="fn">from_str</span><span class="op">(&amp;</span>text<span class="op">)?;</span>
<span class="ln">13</span>      <span class="kw">if</span> <span class="fn">ratio</span><span class="op">(</span>v<span class="op">.</span>colors<span class="op">.</span>text<span class="op">,</span> v<span class="op">.</span>colors<span class="op">.</span>surface<span class="op">)</span> <span class="op">&lt;</span> <span class="nu">4.5</span> <span class="op">{</span>
<span class="ln">14</span>          <span class="kw">return</span> <span class="fn">fail</span><span class="op">(</span><span class="st">"text needs 4.5:1 on surface"</span><span class="op">);</span>
<span class="ln">15</span>      <span class="op">}</span>
<span class="ln">16</span>      <span class="co">Ok</span><span class="op">(</span>v<span class="op">)</span><span class="k-caret"></span>
<span class="ln">17</span>  <span class="op">}</span>'''


screen('Desktop', 720, r'''
<div class="k-screen">
  ''' + WALL(SATURNUS) + r'''
  <div class="k-grain"></div>
  <div style="position:absolute;inset:0 0 auto 0">''' + BAR + r'''</div>
  <div class="k-plate" id="plate">Saturnus with his sickle. Engraved by Hendrick Goltzius after Polidoro da Caravaggio, 1592</div>
  <div id="tiles" data-hidden>
    <div class="k-win" data-active><div class="k-win-body"><pre class="k-code">''' + CODE + r'''</pre></div></div>
    <div class="k-win"><div class="k-win-body"><div style="display:flex;gap:20px;align-items:center"><div style="text-align:center"><div class="k-wordmark">Strix</div><div class="k-motto" style="font-size:11px">nocte vigilat</div></div>
      <dl class="k-info"><dt>OS</dt><i>::</i><dd>Strix 0.1.0</dd><dt>Kernel</dt><i>::</i><dd>6.18.2</dd><dt>Shell</dt><i>::</i><dd>Quickshell</dd><dt>Memory</dt><i>::</i><dd>7.4 of 32 GiB</dd><dt>Uptime</dt><i>::</i><dd>3 h 19 min</dd></dl></div>
      <pre class="k-code" style="margin-top:12px"><b>livio@larp</b> <span class="ty">~</span> <span class="op">&gt;</span> <span class="k-caret"></span></pre></div></div>
    <div class="k-win"><div class="k-win-body" style="display:flex;align-items:flex-end"><div class="k-viz" data-bars="120" style="height:100%"></div></div></div>
  </div>
  <div class="k-dockbar">''' + DOCK + r'''</div>
</div>''', r'''
The desktop. Workspace 1 is empty: the engraving, the top bar on it, and the dock as a thin tab on the bottom edge. Workspace 2 holds three tiled windows: an editor with the syntax colours, a terminal with the system InfoBlock, and the Visualizer.

- Click the workspace dots in the bar to switch between the empty and the busy desktop. Windows slide in from the side with a fade.
- Move the pointer to the bottom edge to bring the dock out; click its symbols to open Today, System, About, media, Wi-Fi, Bluetooth and sound.
- Gaps: `space-3` between windows and to the screen edge; the bar takes `bar-height` at the top; at rest the dock takes no room.
- The focused window has the quiet accent border (`border-active`). Click another window to move focus.
- Bottom left on the empty desktop: the plate caption of the wallpaper, in the serif italic.
''', css=r'''
#tiles { position: absolute; inset: 32px 12px 12px 12px; display: grid; grid-template-columns: 1.25fr 1fr; grid-template-rows: 1fr 1fr; gap: var(--space-3); transition: opacity var(--dur-slow) var(--ease-in-out), transform var(--dur-slow) var(--ease-in-out); }
#tiles[data-hidden] { opacity: 0; transform: translateX(20%); pointer-events: none; }
#tiles > .k-win:first-child { grid-row: 1 / 3; }
#tiles .k-win:not([data-active]) { opacity: var(--dim-inactive); }
#plate { position: absolute; left: var(--space-5); bottom: var(--space-4); transition: opacity var(--dur-base) var(--ease-out); }
''', js=BAR_JS + DOCK_JS + r'''
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
''')

import themes as _pan
_CAP = {
    'saturnus': ('Goltzius, 1592', 'Saturnus with his sickle, lord of time, in his niche. Engraved by Hendrick Goltzius after Polidoro da Caravaggio, 1592'),
    'janus': ('Audenaerd, about 1700', 'Janus with both faces opens the door of the year. Engraved by Robert van Audenaerd after Carlo Maratta'),
    'apollo': ('Goltzius, 1592', 'Apollo as Sol, the sun, with lyre and quiver in his niche. Engraved by Hendrick Goltzius after Polidoro da Caravaggio, 1592'),
    'mars': ('Quellinus, 1655', 'Mars in armour, a dragon on his helmet. Hubert Quellinus after the statue by Artus Quellinus, Amsterdam, 1655'),
    'vulcanus': ('Goltzius, 1592', 'Vulcanus, the smith of the gods, in his niche. Engraved by Hendrick Goltzius after Polidoro da Caravaggio, 1592'),
    'neptunus': ('Goltzius, 1592', 'Neptunus with his crown and trident, in his niche. Engraved by Hendrick Goltzius after Polidoro da Caravaggio, 1592'),
    'pluto': ('Goltzius, 1592', 'Pluto in his niche. Engraved by Hendrick Goltzius after Polidoro da Caravaggio, 1592'),
    'bacchus': ('Goltzius, 1592', 'Bacchus in his niche. Engraved by Hendrick Goltzius after Polidoro da Caravaggio, 1592'),
}
_URL = dict(zip([g[0] for g in _pan.GODS], [SATURNUS, JANUS, APOLLO, MARS, VULCANUS, NEPTUNUS, PLUTO, BACCHUS]))
PLATES = [(g[0], _URL[g[0]], g[1], _CAP[g[0]][0], _CAP[g[0]][1], _pan.colours(g[0])['accent']) for g in _pan.GODS]
THEMES = [(p[0], p[1], p[2], 'dark', p[4], p[5]) for p in PLATES]
for _s in SCREENS:
    if _s['name'] == 'LockScreen':
        _s['js'] = _s['js'].replace('__LOCK_GODS__', json.dumps([[p[0], p[1], p[4]] for p in PLATES]))
WP_JS = 'var P = ' + json.dumps(THEMES) + ';\n' + r"""
(function () {
  var scr = document.getElementById('scr'), track = document.getElementById('track'), car = document.getElementById('car'), rev = document.getElementById('rev'), base = document.getElementById('base');
  var picker = document.getElementById('picker'), reopen = document.getElementById('reopen'), plate = document.getElementById('plate');
  track.innerHTML = P.map(function (p, i) {
    return '<button class="k-slant" aria-selected="' + (i === 0) + '" aria-label="' + p[2] + '"><span class="k-slant-art"><img alt="" src="' + p[1] + '"></span><span class="k-slant-edge"></span><span class="k-slant-name">' + p[2] + '<small><i class="dot" style="background:' + p[5] + '"></i>' + p[3] + '</small></span></button>';
  }).join('');
  Kit.hydrate(document);
  function caption() { plate.textContent = P[car._k.index][4]; }
  car.addEventListener('change', caption); caption();
  // the theme on the desktop: set by hand, or by the cycle every 10 minutes
  var cur = 0, PERIOD = 10 * 60 * 1000, speed = 1, last = Date.now(), virt = 0, prev = Date.now();
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
"""

screen('ThemePicker', 720, r'''
<div class="k-screen" id="scr" data-theme="saturnus">
  ''' + WALL(SATURNUS, ' id="base"') + r'''
  <div class="k-reveal" id="rev" style="background:var(--background) center / cover no-repeat"></div>
  <div class="k-grain"></div>
  <div id="picker">
    <div class="k-scrim" style="animation:none"></div>
    <div class="tools"><div class="k-toolbar"><div class="k-seg" id="variant" aria-label="Variant"><button aria-selected="true" value="dark">Dark</button><button value="light" disabled title="Comes later">Light</button></div></div></div>
    <div class="k-carousel" id="car" tabindex="-1" aria-label="Themes"><div class="k-carousel-track" id="track"></div></div>
    <div class="k-plate" id="plate"></div>
    <div class="cycle"><label class="k-switch"><input type="checkbox" id="keep"><span></span>Keep this theme</label><span class="k-kbd">K</span><span class="caption k-muted" id="next"></span></div>
    <label class="k-switch micro demo"><input type="checkbox" id="fast"><span></span>Preview only: one minute in one second</label>
  </div>
  <button class="k-btn k-btn-primary" id="reopen" style="position:absolute;left:50%;bottom:40px;transform:translateX(-50%);display:none"><span>Open theme picker</span></button>
</div>''', r'''
The theme picker (Super Ctrl Space) over the dimmed desktop. Strix has one theme per Roman god, and Saturnus is the default. Each theme is a plate and its colours: the plate is the wallpaper, the colours tint the whole system to match it. Choosing a theme sets both at once.

- The themes, in order: Saturnus (Strix red, the default), Janus (patina), Apollo (antique gold), Mars (rust), Vulcanus (olive), Neptunus (slate blue), Pluto (heather), Bacchus (claret). All gods but Saturnus are muted, as in dark academia: deep, warm, never bright.
- The middle card names the theme in blackletter, with a dot in its accent and its variant under it; the plate caption stands below the carousel. Light is greyed out until the light variant exists.
- A theme changes only the accent and its family (`accent`, `accent-hover`, `accent-pressed`, `accent-soft`, `accent-text`, `on-accent`, `focus`, `border-active`, terminal cursor and selection) and tints the grounds (`background`, the surfaces, `border`) a little toward the god's hue. Text, `line`, the status colours and syntax stay the same in every theme, so readability never depends on the god. In code: `data-theme="mars"` on the root, or on any element to scope it.
- The theme changes by itself every 10 minutes (`theme-cycle`): another god at random, never the same one, spreading from the middle of the screen with the same reveal. A theme chosen by hand starts a new cycle.
- "Keep this theme" stops the change; K turns it on and off while the picker is open. The cycle keeps counting while it is on, and a change that falls due is skipped. Turned off again, nothing happens at once: the next theme comes at the next turn of the running cycle. Under the switch the time to the next theme is shown, or, while kept, the time to the next turn.
- The lock screen keeps its own rule: another god theme at every lock, whatever the desktop shows.
- Browse with the arrow keys, the wheel or a click on a neighbour; Enter or a click on the middle card spreads the plate as a growing circle from the click point over `dur-reveal`, then the colours switch and the picker fades.
''', css=r'''
#picker { position: absolute; inset: 0; transition: opacity var(--dur-base) var(--ease-in); }
#picker[data-out] { opacity: 0; pointer-events: none; }
#picker .tools { position: absolute; top: 122px; left: 0; right: 0; display: flex; justify-content: center; z-index: 3; }
#picker .k-carousel { position: absolute; top: 170px; left: 0; right: 0; height: 300px; }
#plate { position: absolute; top: 482px; left: 160px; right: 160px; text-align: center; font-size: 14px; line-height: 20px; }
#picker .cycle { position: absolute; top: 536px; left: 0; right: 0; display: flex; justify-content: center; align-items: center; gap: var(--space-4); }
#picker .cycle .caption { min-width: 260px; font-variant-numeric: tabular-nums; }
#picker .demo { position: absolute; right: var(--space-5); top: var(--space-4); color: var(--text-faint); }
.k-slant-name .dot { display: inline-block; width: 6px; height: 6px; border-radius: 50%; margin-right: 6px; vertical-align: 1px; }
.k-slant-name .var { font-weight: inherit; }
''', js=WP_JS)


# ------------------------------------------------------------------ Hotkeys: cheat sheet and settings
# group, action, keys, where it comes from (shown in Settings)
HOTKEYS = [
    ('Learn', 'All hotkeys', 'Super K', 'This sheet'),
    ('Learn', 'Search', 'Super Space', 'Apps, actions, settings and commands'),
    ('Apps', 'Terminal', 'Super Return', 'Ghostty'),
    ('Apps', 'Browser', 'Super Shift Return', 'Firefox'),
    ('Apps', 'Files', 'Super Shift F', 'File manager'),
    ('Apps', 'Text editor', 'Super Shift E', 'Editor'),
    ('Apps', 'Music', 'Super Shift M', 'Music player'),
    ('Windows', 'Close window', 'Super W', 'Window'),
    ('Windows', 'Full screen', 'Super F', 'Window'),
    ('Windows', 'Float or tile', 'Super T', 'Window'),
    ('Windows', 'Split direction', 'Super J', 'Window'),
    ('Windows', 'Move focus', 'Super Arrows', 'Window'),
    ('Windows', 'Swap windows', 'Super Shift Arrows', 'Window'),
    ('Windows', 'Grow or shrink', 'Super = -', 'Window'),
    ('Workspaces', 'Go to workspace', 'Super 1–9', 'Workspace'),
    ('Workspaces', 'Move window there', 'Super Shift 1–9', 'Workspace'),
    ('Workspaces', 'Next workspace', 'Super Tab', 'Workspace'),
    ('Workspaces', 'Scratchpad', 'Super S', 'Special workspace'),
    ('Style', 'Theme picker', 'Super Ctrl Space', 'Themes and wallpapers'),
    ('Style', 'Keep this theme', 'K', 'In the theme picker'),
    ('Style', 'Toggle the top bar', 'Super Shift Space', 'Bar'),
    ('Capture', 'Region screenshot', 'Print', 'Capture'),
    ('Capture', 'Window screenshot', 'Shift Print', 'Capture'),
    ('Capture', 'Screen screenshot', 'Ctrl Print', 'Capture'),
    ('Capture', 'Record a region', 'Alt Print', 'Capture'),
    ('Capture', 'Colour picker', 'Super Print', 'Capture'),
    ('Clipboard', 'Clipboard history', 'Super V', 'Clipboard'),
    ('System', 'Lock', 'Super Escape', 'Session'),
    ('System', 'Session menu', 'Super Shift Escape', 'Log out, suspend, restart, shut down'),
    ('System', 'Notifications', 'Super N', 'Panel'),
    ('System', 'Do not disturb', 'Super Shift N', 'Notifications'),
]
HK_JS = 'var HK = ' + json.dumps([dict(g=g, t=t, k=k, w=w, id=i) for i, (g, t, k, w) in enumerate(HOTKEYS)]) + ';\n' + r"""
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
"""

def SETTINGS_HTML(close=True):
    nav = [('swatch-book', 'Appearance'), ('lock', 'Lock screen'), ('monitor', 'Display'), ('volume-2', 'Sound'), ('wifi', 'Network'),
           ('bluetooth', 'Bluetooth'), ('keyboard', 'Keyboard'), ('command', 'Hotkeys'), ('bell', 'Notifications')]
    return r'''
<div class="k-win" data-active id="settings" style="position:absolute;left:150px;right:150px;top:64px;bottom:64px">
  <div class="k-settings">
    <nav class="k-settings-nav" aria-label="Settings">
      <div class="who"><i>L</i><span>Livio</span></div>
      ''' + ''.join('<button%s>%s%s</button>' % (' aria-current="page"' if t == 'Hotkeys' else '', I(i), t) for i, t in nav) + r'''
    </nav>
    <div class="k-settings-main">
      <header><h2>Hotkeys</h2>
        <div class="k-input" style="width:220px;height:28px">''' + I('search') + r'''<input id="hkq" aria-label="Filter hotkeys" placeholder="Filter" autocomplete="off"></div>
        <button class="k-btn k-btn-primary" id="hkadd">''' + I('plus') + r'''<span>Add hotkey</span></button>''' + ('''
        <button class="k-iconbtn" data-close aria-label="Close settings">''' + I('x') + '''</button>''' if close else '<span data-close hidden></span>') + r'''
      </header>
      <div class="k-hk-new" id="hknew" hidden>
        <div class="row"><div class="k-input" style="width:200px"><input id="hkname" aria-label="Name" placeholder="Name"></div><div class="k-input" style="flex:1"><input id="hkcmd" aria-label="Command" placeholder="Command, app or action"></div></div>
        <div class="row"><button class="k-btn k-btn-quiet" data-cancel-new><span>Cancel</span></button><button class="k-btn k-btn-primary" data-save-new><span>Next: the keys</span></button></div>
      </div>
      <div id="hklist"></div>
    </div>
  </div>
</div>'''

CHEAT_JS = HK_JS + r"""
(function () {
  var body = document.getElementById('cheat-body'), input = document.getElementById('cheat-q'), sheet = document.getElementById('cheat'), out = document.getElementById('said');
  var setWin = document.getElementById('settings'), sel = 0, shown = [];
  var S = Settings(setWin, function () { setWin.hidden = true; sheet.hidden = false; input.focus({ preventScroll: true }); });
  setWin.hidden = true;
  function draw() {
    var q = input.value.trim(), i = 0;
    shown = [];
    var html = groups(HK).map(function (gr) {
      var rows = gr[1].map(function (h) {
        var mt = q ? Kit.fuzzy(q, h.t) : null, mk = q ? Kit.fuzzy(q, h.k) : null;
        if (q && !mt && !mk) return '';
        shown.push(h);
        var t = mt ? Kit.mark(h.t, mt.hits) : h.t;
        return '<div class="k-cheat-row" role="option" data-n="' + (i++) + '"><span class="t">' + t + '</span>' + keys(h.k) + '<button class="edit" data-edit="' + h.id + '" aria-label="Change the keys for ' + h.t + '">' + '<i class=\"k-icon\">' + Kit.icon('pencil') + '</i>' + '</button></div>';
      }).join('');
      return rows ? '<section class="k-cheat-group"><h3>' + gr[0] + '</h3>' + rows + '</section>' : '';
    }).join('');
    body.innerHTML = html || '<p class="k-empty">No hotkey matches.</p>';
    sel = Math.min(sel, Math.max(0, shown.length - 1)); mark();
  }
  function mark() { Array.prototype.forEach.call(body.querySelectorAll('.k-cheat-row'), function (r) { r.setAttribute('aria-selected', +r.dataset.n === sel && input.value.trim() !== ''); }); }
  function edit(id) { sheet.hidden = true; setWin.hidden = false; S.draw(id); }
  body.addEventListener('click', function (e) {
    var b = e.target.closest('[data-edit]'); if (b) { edit(+b.dataset.edit); return; }
    var r = e.target.closest('.k-cheat-row'); if (r) out.textContent = 'Runs ' + shown[+r.dataset.n].t;
  });
  document.getElementById('cheat-edit').addEventListener('click', function () { edit(null); });
  input.addEventListener('input', function () { sel = 0; out.textContent = ''; draw(); });
  input.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowDown') { e.preventDefault(); sel = Math.min(shown.length - 1, sel + 1); mark(); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); sel = Math.max(0, sel - 1); mark(); }
    else if (e.key === 'Enter' && shown[sel]) { e.preventDefault(); out.textContent = 'Runs ' + shown[sel].t; }
    else if (e.key === 'Escape') { e.preventDefault(); if (input.value) { input.value = ''; draw(); } else out.textContent = 'Closes'; }
  });
  draw();
  try { input.focus({ preventScroll: true }); } catch (e) {}
})();
"""

screen('Cheatsheet', 720, r'''
<div class="k-screen" data-theme="saturnus">
  ''' + WALL(SATURNUS, ' data-dim') + r'''
  <div class="k-grain"></div>
  <div class="k-scrim" style="animation:none;place-items:start center;padding-top:44px">
    <div class="k-cheat k-surface" id="cheat" role="dialog" aria-label="Hotkeys">
      <div class="k-cheat-head"><span class="title">Hotkeys</span>''' + I('search') + r'''<input id="cheat-q" aria-label="Filter hotkeys" placeholder="Filter by action or keys" autocomplete="off" spellcheck="false"><output id="said" class="caption k-muted"></output><button class="k-btn k-btn-quiet" id="cheat-edit">''' + I('pencil') + r'''<span>Edit</span></button><span class="k-kbd">Esc</span></div>
      <div class="k-cheat-body" id="cheat-body" role="listbox"></div>
    </div>
  </div>
  ''' + SETTINGS_HTML() + r'''
</div>''', r'''
The cheat sheet (Super K) is the one place that explains the keys. Components carry no instructions of their own; at most a single key chip stands next to a control where one key matters (Esc in Search, K in the theme picker). Everything else is learned here.

- Over the dimmed desktop, a wide panel lists every hotkey of the system in groups: Learn, Apps, Windows, Workspaces, Style, Capture, Clipboard, System. Group names in the serif italic, actions in mono, keys as chips at the right.
- Typing filters by action or by keys, fuzzy as in Search: "shot" finds the screenshots, "super shift" every binding with both. Up and Down move, Enter runs the action, Esc clears the field and a second Esc closes.
- Edit opens Settings › Hotkeys. The pencil next to a row opens Settings at that very row, marked for a moment, ready to take new keys.
- The list is read from the live bindings, so a hotkey changed or added in Settings shows here at once.
''', css=r'''
#settings[hidden], #cheat[hidden] { display: none; }
#settings { animation: k-win-in var(--dur-slow) var(--ease-out) both; }
#said { margin-right: var(--space-2); white-space: nowrap; }
''', js=CHEAT_JS)

screen('SettingsHotkeys', 720, r'''
<div class="k-screen" data-theme="saturnus">
  ''' + WALL(SATURNUS) + r'''
  <div class="k-grain"></div>
  ''' + SETTINGS_HTML(close=False) + r'''
</div>''', r'''
Settings › Hotkeys: every action of the cheat sheet in the same groups, each with its keys at the right.

- A click on the keys starts recording: the field turns to the accent and waits. Press the new combination; Esc alone cancels. Super, Ctrl, Alt and Shift count as modifiers.
- If the keys already belong to another action, the row says so in `warning` and offers "Use it here" (the other action loses its keys) or "Keep the old".
- A changed hotkey gets a reset button that brings back the default. Own hotkeys get a remove button instead.
- Add hotkey asks for a name and what it runs (a command, an app or an action), then records the keys. Own hotkeys collect in the group "Your hotkeys".
- The filter field narrows the list by action, keys or group. Changes apply at once; Hyprland reloads its bindings, and the cheat sheet shows them the next time it opens.
''', css=r'''
#settings { left: 120px; right: 120px; top: 48px; bottom: 48px; }
''', js=HK_JS + r"""
(function () { var S = Settings(document.getElementById('settings')); S.draw(); })();
""")

def sw(n):
    return '<span class="k-swatch" style="background:var(--term-%s)" title="%s"></span>' % (n, n)
ANSI = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
screen('Terminal', 720, r'''
<div class="k-screen" data-theme="saturnus">
  ''' + WALL(SATURNUS) + r'''
  <div class="k-grain"></div>
  <div style="position:absolute;inset:0 0 auto 0">''' + BAR + r'''</div>
  <div class="k-win term" data-active>
    <div class="k-win-body">
      <img class="ghost" alt="" src="''' + SATURNUS + r'''">
<pre class="k-code" style="color:var(--term-foreground)"><span class="d">~/strixos</span> <span class="g">main</span> <span class="pc">›</span> strix-info
<span class="m">╓</span>                                        <span class="m">╖</span>
  <span class="p">larp</span>   <span class="i">Strix 0.1.0</span>
  <span class="b">Kernel</span>  <span class="m">::</span> 6.18.2
  <span class="b">Shell</span>   <span class="m">::</span> Quickshell on Hyprland
  <span class="b">Theme</span>   <span class="m">::</span> <span class="pc">Saturnus</span>, dark, 4 more min
  <span class="b">Disk</span>    <span class="m">::</span> 162 GiB of 952 GiB
  <span class="sw">''' + ''.join('<i style="background:var(--term-%s)"></i>' % a for a in ANSI) + r'''</span>
  <span class="sw">''' + ''.join('<i style="background:var(--term-bright-%s)"></i>' % a for a in ANSI) + r'''</span>
<span class="m">╙</span>                                        <span class="m">╜</span>

<span class="d">~/strixos</span> <span class="g">main</span> <span class="pc">›</span> git log --oneline -3
<span class="y">d207083</span> <span class="m">(</span><span class="c">HEAD</span> <span class="m">→</span> <span class="g">main</span><span class="m">,</span> <span class="v">origin/main</span><span class="m">)</span> ci: update flake inputs and crates every week
<span class="y">952d81c</span> <span class="m">(</span><span class="y">tag: v0.1.0</span><span class="m">,</span> <span class="v">origin/stable</span><span class="m">)</span> release: 0.1.0
<span class="y">7c1e0aa</span> feat(installer): ask for the language first

<span class="d">~/strixos</span> <span class="g">main</span> <span class="pc">›</span> cargo build
<span class="g">   Compiling</span> theme-engine v0.1.0
<span class="rb">error[E0308]</span><span class="b">: mismatched types</span>
  <span class="m">--&gt;</span> src/check.rs:14:16
<span class="m">14 |</span>         return fail(4.5);
   <span class="m">|</span>                     <span class="r">^^^ expected `&amp;str`, found floating-point number</span>
<span class="yb">warning</span><span class="b">: unused variable: `text`</span>

<span class="d">~/strixos</span> <span class="g">main</span> <span class="pc">›</span> ls
<span class="bl">hosts</span>  <span class="bl">installer</span>  <span class="bl">modules</span>  <span class="bl">packages</span>  <span class="bl">themes</span>  <span class="g">build.sh</span>  flake.lock  flake.nix  README.md

<span class="d">~/strixos</span> <span class="g">main</span> <span class="pc">›</span> <span class="k-caret" style="background:var(--term-cursor)"></span></pre>
    </div>
  </div>
</div>''', r'''
Ghostty in the Strix theme, tiled on the desktop under the bar: `strix-info`, `git log`, a compiler error and a warning, and `ls`.

- Colours: the 16 `term-` colours are muted like the rest of the system, brick, olive, brass, slate, heather, patina and old paper, each 4.5:1 or more on the ground of every theme. The ground (`term-background`), the cursor and the selection follow the theme; the cursor is a block in the accent.
- The plate of the theme lies in the ground of the terminal at 6%, desaturated and anchored bottom right (Ghostty `background-image` with `background-image-opacity`), so the terminal belongs to the desktop without losing contrast.
- Prompt: path, branch, and a single `›` in the accent. One line, no symbols that need a patched font, no colour blocks.
- `strix-info` prints the facts as `label :: value` between the same double corner marks as InfoBlock, with the 16 colours as a strip. The motto and the wordmark stay out of the terminal.
- Errors are `term-bright-red` and bold, warnings `term-bright-yellow`; that is the loudest the terminal gets. Font `mono` at 13px with 20px line height; padding 16px by 20px; no title bar under Hyprland.
''', css=r'''
.term { position: absolute; left: 12px; right: 12px; top: 38px; bottom: 12px; }
.term .k-win-body { position: relative; background: var(--term-background); padding: 16px 20px; }
.term .ghost { position: absolute; right: -40px; bottom: -60px; width: 760px; opacity: 0.06; filter: grayscale(1); pointer-events: none; }
.term pre { position: relative; margin: 0; font-size: 13px; line-height: 20px; }
.k-code .p { color: var(--term-bright-white); font-weight: 600; } .k-code .i { color: var(--term-white); }
.k-code .d { color: var(--term-blue); } .k-code .g { color: var(--term-green); } .k-code .pc { color: var(--term-cursor); }
.k-code .m { color: var(--term-bright-black); } .k-code .y { color: var(--term-yellow); } .k-code .c { color: var(--term-cyan); } .k-code .v { color: var(--term-magenta); }
.k-code .r { color: var(--term-red); } .k-code .rb { color: var(--term-bright-red); font-weight: 600; } .k-code .yb { color: var(--term-bright-yellow); font-weight: 600; }
.k-code .bl { color: var(--term-blue); font-weight: 600; } .k-code .b { font-weight: 600; color: var(--term-bright-white); }
.k-code .sw { display: inline-flex; vertical-align: -2px; } .k-code .sw i { display: inline-block; width: 26px; height: 12px; }
''')

screen('BootSplash', 540, r'''
<div style="height:540px;background:var(--background);display:flex;flex-direction:column">
  <div class="splash" id="splash" data-state="boot">
    <div class="display" style="color:var(--text)">Strix</div>
    <div class="k-rule" style="width:150px;margin:6px 0 4px"><i></i></div>
    <div class="motto k-muted">nocte vigilat</div>
    <div class="slot">
      <div class="k-progress" data-indeterminate id="run"><i></i></div>
      <div class="k-field" id="pass" style="width:220px"><div class="k-input k-input-line"><input type="password" aria-label="Passphrase" placeholder="Passphrase" id="pp"></div><span class="k-help" id="msg">Enter the passphrase for this disk</span></div>
    </div>
  </div>
  <div style="display:flex;justify-content:center;padding:16px"><div class="k-seg" id="state" aria-label="State"><button aria-selected="true">Start</button><button>Passphrase</button><button>Wrong passphrase</button><button>Shut down</button></div></div>
</div>''', r'''
The boot splash (Plymouth): the blackletter wordmark on plain `background`, a lozenge rule, the motto, and one hair line.

- Start and shut down: no percentage. A short piece in the accent runs along the line (Progress, indeterminate).
- Disk passphrase: the line becomes the line field; typed characters show as dots.
- Wrong passphrase: the field shakes once and the text under it reads "Wrong passphrase. Try again." in `error`.
- Colours used: `background`, `text`, `text-muted`, `line`, `accent`, `error`. Nothing else, so the splash can be built per variant from six values.
- Switch the states with the control under the preview.
''', css=r'''
.splash { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.splash .slot { height: 60px; margin-top: 36px; display: flex; flex-direction: column; align-items: center; }
.splash[data-state="boot"] #pass, .splash[data-state="off"] #pass { display: none; }
.splash[data-state="pass"] #run, .splash[data-state="wrong"] #run { display: none; }
.splash #run { width: 180px; }
.splash .k-help { text-align: center; }
''', js=r'''
(function () {
  var s = document.getElementById('splash'), msg = document.getElementById('msg'), pass = document.getElementById('pass'), pp = document.getElementById('pp');
  var names = ['boot', 'pass', 'wrong', 'off'];
  function set(i) {
    s.setAttribute('data-state', names[i]);
    pass.removeAttribute('data-state'); msg.textContent = 'Enter the passphrase for this disk'; pp.value = i === 2 ? '' : pp.value;
    if (i === 2) { pass.setAttribute('data-state', 'error'); msg.textContent = 'Wrong passphrase. Try again.'; var b = pp.parentNode; b.classList.remove('k-shake'); void b.offsetWidth; b.classList.add('k-shake'); }
    if (i === 1) pp.value = 'correct horse';
  }
  document.getElementById('state').addEventListener('change', function (e) { set(e.detail.index); });
})();
''', width=960)

DTS = r'''// The bundle is plain CSS classes (prefix k-) plus a small script, window.Kit. No framework.
// Markup for every component is in its README and preview.

export interface SegmentedHandle { select(index: number, silent?: boolean): void; place(): void; readonly index: number }
export interface CarouselHandle { select(index: number, silent?: boolean): void; readonly index: number }
export interface DockHandle { open(button: HTMLElement): void; close(): void; show(): void; hide(): void }
export interface VisualizerHandle { frame(levels?: number[]): void; start(): void; stop(): void }

export interface FuzzyMatch { score: number; hits: number[] }

export interface KitApi {
  /** Wires every component inside root: icons, wallpaper, segmented, sliders, rings, rolling numbers, calendars, visualizers, carousels, docks. Safe to call again. */
  hydrate(root?: ParentNode): void;
  /** Names of the bundled symbols. */
  icons: string[];
  /** SVG markup for one symbol (24px grid, 1.5 stroke, currentColor). */
  icon(name: string): string;
  /** SVG markup of the default wallpaper, drawn with the theme's tokens. */
  wallpaper(): string;
  /** True when motion should be reduced (system setting, or data-motion="reduced" on the html element). */
  reduced(): boolean;
  segmented(el: HTMLElement): SegmentedHandle;
  slider(input: HTMLInputElement): void;
  ring(el: HTMLElement, value?: number): void;
  roll(el: HTMLElement, text?: string): void;
  calendar(el: HTMLElement, date?: Date): void;
  visualizer(el: HTMLElement): VisualizerHandle;
  carousel(el: HTMLElement): CarouselHandle;
  dock(el: HTMLElement): DockHandle;
  /** Circular reveal of layer from a viewport point; resolves when it covers the layer. */
  reveal(layer: HTMLElement, x: number, y: number): Promise<void>;
  /** Fuzzy match of query in text: characters in order, word starts and runs score higher. Null when it does not match. */
  fuzzy(query: string, text: string): FuzzyMatch | null;
  /** text as HTML with the matched positions wrapped in <b>. */
  mark(text: string, hits: number[]): string;
  /** Plays the exit animation, then removes the element. */
  dismiss(el: HTMLElement, className?: string): void;
}
declare global { interface Window { Kit: KitApi } }
'''
