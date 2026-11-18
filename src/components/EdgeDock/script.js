
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

setTimeout(function () { var d = document.getElementById('dock')._k; d.show(); d.open(document.querySelector('.k-edge [data-panel="#p-main"]')); }, 500);