
function at(id) { return Math.max(0, Kit.gods.findIndex(function (g) { return g.id === id; })); }
document.getElementById('track').innerHTML = Kit.gods.map(function (g, i) {
  return '<button class="k-slant" aria-selected="' + (i === at(Kit.theme())) + '" aria-label="' + g.name + '"><span class="k-slant-art"><img alt="" src="' + g.wall + '"></span><span class="k-slant-edge"></span><span class="k-slant-name">' + g.name + '</span></button>';
}).join('');
Kit.hydrate(document);
var car = document.querySelector('.k-carousel');
Kit.onTheme(function (id) { car._k.select(at(id)); });
