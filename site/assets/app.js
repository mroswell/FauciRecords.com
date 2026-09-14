/* The Fauci Records — rendering for home + exhibit pages.
   Data comes from data/data.js as window.__DATA__ (works over http:// and file://). */
(function () {
  "use strict";
  var D = window.__DATA__ || { claims: [], exhibits: [], meta: {} };
  var exById = {};
  D.exhibits.forEach(function (e) { exById[e.id] = e; });

  /* ---------- helpers ---------- */
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }
  // short, readable label for a document link chip
  function shortLabel(ex) {
    var t = ex.title;
    var dash = t.indexOf("—");
    if (dash > -1) t = t.slice(dash + 1);
    t = t.replace(/^\s*[“"']|[”"']\s*$/g, "").trim();
    if (t.length > 30) t = t.slice(0, 29).trim() + "…";
    return t;
  }
  function kindLabel(k) { return k.charAt(0).toUpperCase() + k.slice(1); }

  function docLink(ex) {
    return '<a class="doclink" href="exhibit.html?id=' + esc(ex.id) + '" title="' +
      esc(ex.title) + '"><span style="text-transform:none;letter-spacing:0">' +
      esc(shortLabel(ex)) + "</span></a>";
  }
  function noteHtml(text) {
    if (!text) return "";
    return '<div class="context-note">' + esc(text) + "</div>";
  }

  // Render a reflowed transcript: blank-line-separated blocks become paragraphs,
  // multi-line structural blocks keep their line breaks, tabular blocks stay
  // monospaced and aligned.
  function transcriptHtml(text) {
    if (!text) return '<p class="empty">[No machine-readable text on this page.]</p>';
    return text.split(/\n[ \t]*\n/).map(function (block) {
      var lines = block.split("\n");
      var tabular = lines.some(function (l) {
        return (l.match(/\S {2,}/g) || []).length >= 2;
      });
      if (tabular) return '<pre class="tbl">' + esc(block) + "</pre>";
      if (lines.length > 1) {
        return '<p class="stack">' + lines.map(esc).join("<br>") + "</p>";
      }
      return "<p>" + esc(block) + "</p>";
    }).join("");
  }

  // Canonical release stamp shown at the top of every source page. The wording is
  // constant; only the printed release number (release) varies, and is null for
  // the Fauci emails, which carry no release number.
  function stampHtml(release) {
    var num = (release === null || release === undefined) ? "" :
      '<span class="release-stamp__num">' + esc(String(release)) + "</span>";
    return '<div class="release-stamp">' +
      '<span class="release-stamp__text">Released by Chairman Rand Paul — ' +
      "Entered into the record by Chairman Rand Paul at the July 29, 2026 HSGAC " +
      'Hearing titled, “Testimony of Anthony Fauci”.</span>' + num + "</div>";
  }

  /* ---------- notes toggle (persisted) ---------- */
  function initNotesToggle() {
    // Editor's notes are ON by default; a prior explicit toggle (localStorage) wins.
    var stored = null;
    try { stored = localStorage.getItem("show-notes"); } catch (e) {}
    var on = stored === null ? true : stored === "1";
    // deep link: ?notes=1 / ?notes=0 forces state (shareable view)
    var nm = /[?&]notes=([01])/.exec(window.location.search);
    if (nm) { on = nm[1] === "1"; try { localStorage.setItem("show-notes", nm[1]); } catch (e) {} }
    document.body.classList.toggle("show-notes", on);
    var btns = document.querySelectorAll(".notes-toggle");
    function sync() {
      var isOn = document.body.classList.contains("show-notes");
      btns.forEach(function (b) {
        b.setAttribute("aria-pressed", isOn ? "true" : "false");
        var lab = b.querySelector(".label");
        if (lab) lab.textContent = isOn ? "Editor’s notes: on" : "Editor’s notes: off";
      });
    }
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        var isOn = document.body.classList.toggle("show-notes");
        try { localStorage.setItem("show-notes", isOn ? "1" : "0"); } catch (e) {}
        sync();
      });
    });
    sync();
  }

  /* ---------- home page ---------- */
  function renderHome() {
    // cover intro
    var intro = document.getElementById("intro");
    if (intro && D.meta.intro) intro.textContent = D.meta.intro;

    var wrap = document.getElementById("claims");
    if (wrap) {
      D.claims.forEach(function (c, i) {
        var card = el("article", "claim");
        card.id = c.id;
        card.style.animationDelay = (0.06 * i) + "s";

        var facts = c.facts.map(function (f) {
          var links = f.exhibits.map(function (id) {
            return exById[id] ? docLink(exById[id]) : "";
          }).join("");
          return (
            '<li class="fact"><span class="fact__text">' + esc(f.text) + "</span>" +
            '<span class="fact__links">' + links + "</span>" +
            noteHtml(f.note) +
            "</li>"
          );
        }).join("");

        card.innerHTML =
          '<div class="claim__num">' + String(c.number).padStart(2, "0") + "</div>" +
          '<div class="claim__body">' +
            '<div class="claim__kicker">Claim ' + c.number + " · What the documents show</div>" +
            '<h3 class="claim__headline">' + esc(c.headline) + "</h3>" +
            '<p class="claim__text">' + esc(c.body) + "</p>" +
            noteHtml(c.note) +
            '<ul class="facts">' + facts + "</ul>" +
          "</div>";
        wrap.appendChild(card);
      });
    }

    // exhibit index grid
    var grid = document.getElementById("exgrid");
    if (grid) {
      D.exhibits.forEach(function (ex) {
        var a = el("a", "excard");
        a.href = "exhibit.html?id=" + ex.id;
        var claims = (ex.claims || []).map(function (n) {
          return '<span class="claimtag">Claim ' + n + "</span>";
        }).join("");
        var release = ex.release ? '<span class="chip chip--release">Release ' + esc(ex.release) + "</span>" : "";
        a.innerHTML =
          '<div class="excard__top"><span class="chip chip--kind">' + esc(kindLabel(ex.kind)) + "</span>" +
            '<span class="mono" style="font-size:.66rem;color:var(--ink-faint)">' + esc(ex.date) + "</span></div>" +
          '<h3 class="excard__title">' + esc(ex.title) + "</h3>" +
          '<p class="excard__sum">' + esc(ex.summary) + "</p>" +
          '<div class="excard__foot">' + claims + release + "</div>";
        grid.appendChild(a);
      });
    }
    initNotesToggle();
  }

  /* ---------- exhibit page ---------- */
  function getParam(name) {
    var m = new RegExp("[?&]" + name + "=([^&]+)").exec(window.location.search);
    return m ? decodeURIComponent(m[1]) : null;
  }
  function renderExhibit() {
    var id = getParam("id");
    var ex = exById[id];
    var root = document.getElementById("exhibit");
    if (!ex) {
      root.innerHTML = '<div class="exhibit-head"><a class="backlink" href="index.html">← Back to the records</a>' +
        '<h1 class="exhibit-title">Document not found</h1></div>';
      return;
    }
    document.title = ex.title + " — The Fauci Records";

    var release = ex.release ? '<span class="chip chip--release">Release ' + esc(ex.release) + "</span>" : "";
    var pagesLabel = ex.pageRange[0] === ex.pageRange[1]
      ? "Source page " + ex.pageRange[0]
      : "Source pages " + ex.pageRange[0] + "–" + ex.pageRange[1];

    var supports = (ex.claims || []).map(function (n) {
      var c = D.claims.filter(function (x) { return x.number === n; })[0];
      return '<a class="doclink" href="index.html#' + esc(c.id) + '"><span style="text-transform:none;letter-spacing:0">Claim ' +
        n + "</span></a>";
    }).join("");

    var head = el("div", "exhibit-head");
    head.innerHTML =
      '<a class="backlink" href="index.html">← Back to the records</a>' +
      '<h1 class="exhibit-title">' + esc(ex.title) + "</h1>" +
      '<div class="exhibit-meta">' +
        '<span class="chip chip--kind">' + esc(kindLabel(ex.kind)) + "</span>" +
        '<span class="mono" style="font-size:.72rem;color:var(--ink-faint)">' + esc(ex.date) + "</span>" +
        release +
        '<span class="mono" style="font-size:.72rem;color:var(--ink-faint)">' + pagesLabel + "</span>" +
      "</div>" +
      '<p class="exhibit-summary">' + esc(ex.summary) + "</p>" +
      '<div class="exhibit-actions">' +
        '<a class="btn" href="' + esc(ex.pdf) + '" download>↓ Download this document (PDF)</a>' +
        '<a class="btn btn--ghost" href="' + esc(ex.pdf) + '" target="_blank" rel="noopener">Open PDF in new tab</a>' +
      "</div>" +
      (supports ? '<div class="supports"><span class="lbl">Supports</span>' + supports + "</div>" : "");
    root.appendChild(head);

    var pages = el("div", "pages");
    ex.pages.forEach(function (p) {
      var block = el("div", "pageblock");
      var ocrFlag = p.ocr ? '<span class="ocr-flag">OCR transcript</span>' : "<span>Extracted text</span>";
      block.innerHTML =
        '<div class="pageblock__img">' +
          '<img class="pageblock__scan" loading="lazy" src="' + esc(p.img) +
            '" alt="Scan of source page ' + p.page + '">' +
          '<div class="pageblock__label"><span>Page ' + p.page + "</span>" + ocrFlag + "</div>" +
        "</div>" +
        '<div class="transcript"><h4>Transcript — page ' + p.page + "</h4>" +
          stampHtml(p.release) +
          transcriptHtml(p.text) + "</div>";
      pages.appendChild(block);
    });
    root.appendChild(pages);
  }

  /* ---------- boot ---------- */
  document.addEventListener("DOMContentLoaded", function () {
    var page = document.body.getAttribute("data-page");
    if (page === "home") renderHome();
    else if (page === "exhibit") renderExhibit();
  });
})();
