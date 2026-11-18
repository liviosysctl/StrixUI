
document.getElementById('eye').addEventListener('click', function () {
  var i = document.getElementById('b'), show = i.type === 'password';
  i.type = show ? 'text' : 'password';
  this.querySelector('.k-icon').innerHTML = Kit.icon(show ? 'eye-off' : 'eye');
});
