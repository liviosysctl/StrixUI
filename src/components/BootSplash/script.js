
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
