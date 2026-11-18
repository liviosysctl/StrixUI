
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
