
var list = document.getElementById('list'), rows = Array.prototype.filter.call(list.children, function (r) { return r.getAttribute('aria-disabled') !== 'true'; }), cur = 0;
function pick(i) { cur = (i + rows.length) % rows.length; Array.prototype.forEach.call(list.children, function (r) { r.setAttribute('aria-selected', r === rows[cur]); }); }
rows.forEach(function (r, i) { r.addEventListener('click', function () { pick(i); }); });
list.addEventListener('keydown', function (e) { if (e.key === 'ArrowDown') { e.preventDefault(); pick(cur + 1); } if (e.key === 'ArrowUp') { e.preventDefault(); pick(cur - 1); } });
