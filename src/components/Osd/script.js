
var val = 62, osd = document.getElementById('osd');
function set(d) { val = Math.max(0, Math.min(100, val + d)); osd.querySelector('.k-progress').style.setProperty('--p', val + '%'); osd.querySelector('output').textContent = val; }
document.getElementById('dn').addEventListener('click', function () { set(-5); });
document.getElementById('up').addEventListener('click', function () { set(5); });
