
document.getElementById('shuffle').addEventListener('click', function () {
  Array.prototype.forEach.call(document.querySelectorAll('.k-ring'), function (r) { Kit.ring(r, Math.round(Math.random() * 100)); });
});
