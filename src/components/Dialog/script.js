
var scrim = document.getElementById('scrim');
function close() { scrim.style.display = 'none'; document.getElementById('open').focus(); }
function open() { scrim.style.display = 'grid'; document.getElementById('no').focus({ preventScroll: true }); }
document.getElementById('open').addEventListener('click', open);
document.getElementById('no').addEventListener('click', close);
document.getElementById('yes').addEventListener('click', close);
document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
