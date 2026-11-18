
var wins = document.querySelectorAll('.k-win');
Array.prototype.forEach.call(wins, function (w) { w.addEventListener('click', function () { Array.prototype.forEach.call(wins, function (o) { o.removeAttribute('data-active'); o.style.opacity = 'var(--dim-inactive)'; }); w.setAttribute('data-active', ''); w.style.opacity = 1; }); });
