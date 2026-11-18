
var p = document.getElementById('p'), pv = document.getElementById('pv'), v = 0, timer;
function run() { clearInterval(timer); v = 0; timer = setInterval(function () { v = Math.min(100, v + 4 + Math.random() * 9); p.style.setProperty('--p', v + '%'); p.setAttribute('aria-valuenow', Math.round(v)); pv.textContent = Math.round(v) + '%'; if (v >= 100) clearInterval(timer); }, 380); }
document.getElementById('again').addEventListener('click', run); run();
