(function () {
  var input = document.getElementById('search');
  var box = document.getElementById('results');
  if (!input || !box) return;
  var index = null;

  function load(cb) {
    if (index) return cb();
    fetch('assets/search-index.json').then(function (r) { return r.json(); })
      .then(function (data) { index = data; cb(); })
      .catch(function () { index = []; cb(); });
  }
  function esc(s) {
    return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; });
  }
  function snippet(text, q) {
    var i = text.toLowerCase().indexOf(q);
    if (i < 0) return esc(text.slice(0, 110)) + '…';
    var start = Math.max(0, i - 50);
    var part = text.slice(start, i + q.length + 70);
    var j = part.toLowerCase().indexOf(q);
    return (start > 0 ? '…' : '') + esc(part.slice(0, j)) + '<mark>' + esc(part.slice(j, j + q.length)) + '</mark>' + esc(part.slice(j + q.length)) + '…';
  }
  function run() {
    var q = input.value.trim().toLowerCase();
    if (q.length < 2) { box.style.display = 'none'; return; }
    load(function () {
      var hits = index.map(function (p) {
        var t = p.title.toLowerCase().indexOf(q) >= 0 ? 10 : 0;
        var c = p.text.toLowerCase().split(q).length - 1;
        return { p: p, score: t + c };
      }).filter(function (h) { return h.score > 0; })
        .sort(function (a, b) { return b.score - a.score; }).slice(0, 8);
      box.innerHTML = hits.length ? hits.map(function (h) {
        return '<a href="' + h.p.url + '"><b>' + esc(h.p.title) + '</b><span>' + snippet(h.p.text, q) + '</span></a>';
      }).join('') : '<div class="none">No results</div>';
      box.style.display = 'block';
    });
  }
  input.addEventListener('input', run);
  input.addEventListener('focus', run);
  document.addEventListener('click', function (e) {
    if (!box.contains(e.target) && e.target !== input) box.style.display = 'none';
  });
  document.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); input.focus(); }
    if (e.key === 'Escape') { box.style.display = 'none'; document.body.classList.remove('nav-open'); }
  });
})();
