
var pp = document.getElementById('pp');
pp.addEventListener('click', function () {
  var on = pp.getAttribute('aria-pressed') !== 'true';
  pp.setAttribute('aria-pressed', on);
  pp.querySelector('.k-icon').innerHTML = Kit.icon(on ? 'pause' : 'play');
});
