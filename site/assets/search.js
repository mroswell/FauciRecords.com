/* Client-side full-text search over the released records + claims.
   Small corpus (~30 pages), so a tokenized scan with light ranking is plenty. */
(function () {
  "use strict";
  var D = window.__DATA__ || { search: [] };
  var RECORDS = D.search || [];

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function tokenize(s) {
    return (s.toLowerCase().match(/[a-z0-9][a-z0-9''-]*/g) || []);
  }
  // precompute lowercase text
  RECORDS.forEach(function (r) { r._lc = r.text.toLowerCase(); });

  function score(rec, terms) {
    var s = 0, lc = rec._lc, titleLc = rec.title.toLowerCase();
    terms.forEach(function (t) {
      var idx = lc.indexOf(t);
      if (idx === -1) { s -= 100; return; }        // missing term heavily penalized
      // count occurrences
      var count = lc.split(t).length - 1;
      s += Math.min(count, 8);
      if (titleLc.indexOf(t) > -1) s += 6;          // title hits weigh more
      if (rec.kind === "claim") s += 2;             // surface claims a little higher
    });
    return s;
  }

  function snippet(text, terms) {
    var lc = text.toLowerCase(), pos = -1;
    for (var i = 0; i < terms.length; i++) {
      var p = lc.indexOf(terms[i]);
      if (p > -1 && (pos === -1 || p < pos)) pos = p;
    }
    if (pos === -1) pos = 0;
    var start = Math.max(0, pos - 70);
    var frag = text.slice(start, start + 240);
    if (start > 0) frag = "…" + frag;
    if (start + 240 < text.length) frag = frag + "…";
    frag = esc(frag);
    // highlight terms
    terms.forEach(function (t) {
      var re = new RegExp("(" + t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "gi");
      frag = frag.replace(re, "<mark>$1</mark>");
    });
    return frag;
  }

  function render(results, terms, q) {
    var meta = document.getElementById("searchmeta");
    var out = document.getElementById("results");
    out.innerHTML = "";
    if (!q) {
      meta.textContent = RECORDS.length + " records indexed — 5 claims, " +
        (RECORDS.length - 5) + " documents";
      return;
    }
    meta.textContent = results.length + " result" + (results.length === 1 ? "" : "s") +
      ' for “' + q + "”";
    results.forEach(function (r) {
      var a = document.createElement("a");
      a.className = "result" + (r.kind === "claim" ? " result--claim" : "");
      a.href = r.url;
      a.innerHTML =
        '<div class="result__kind">' + esc(r.subtitle) + "</div>" +
        '<div class="result__title">' + esc(r.title) + "</div>" +
        '<p class="result__snippet">' + snippet(r.text, terms) + "</p>";
      out.appendChild(a);
    });
    if (!results.length) {
      out.innerHTML = '<p style="color:var(--ink-soft)">No records match that query. Try a name, a date, or a phrase such as “delete”, “MERS-CoV”, or “Gottlieb”.</p>';
    }
  }

  function run(q) {
    var terms = tokenize(q);
    if (!terms.length) { render([], [], ""); return; }
    var scored = RECORDS.map(function (r) { return { r: r, s: score(r, terms) }; })
      .filter(function (x) { return x.s > 0; })
      .sort(function (a, b) { return b.s - a.s; })
      .map(function (x) { return x.r; });
    render(scored, terms, q);
  }

  document.addEventListener("DOMContentLoaded", function () {
    var input = document.getElementById("q");
    render([], [], "");
    // deep link ?q=
    var m = /[?&]q=([^&]+)/.exec(window.location.search);
    if (m) { input.value = decodeURIComponent(m[1].replace(/\+/g, " ")); run(input.value); }
    input.focus();
    input.addEventListener("input", function () { run(input.value.trim()); });
  });
})();
