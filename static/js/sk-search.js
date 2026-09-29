/* Search (spec §6): the Pagefind index is built on Devanāgarī, so a query typed in any Indic script,
 * or in IAST / Harvard-Kyoto, is converted to Devanāgarī first. */
(function () {
  "use strict";
  var BLOCKS = [ // [first code point, last, sanscript scheme]
    [0x0900, 0x097F, "devanagari"], [0x0980, 0x09FF, "bengali"], [0x0A80, 0x0AFF, "gujarati"],
    [0x0B00, 0x0B7F, "oriya"], [0x0B80, 0x0BFF, "tamil"], [0x0C00, 0x0C7F, "telugu"],
    [0x0C80, 0x0CFF, "kannada"], [0x0D00, 0x0D7F, "malayalam"], [0x11300, 0x1137F, "grantha"],
    [0x11180, 0x111DF, "sharada"]
  ];

  function detect(q) {
    for (var ch of q) {
      var cp = ch.codePointAt(0);
      for (var i = 0; i < BLOCKS.length; i++) if (cp >= BLOCKS[i][0] && cp <= BLOCKS[i][1]) return BLOCKS[i][2];
    }
    // Latin: IAST if it has diacritics, otherwise Harvard-Kyoto (which also reads plain ASCII IAST).
    return /[āīūṛṝḷḹṅñṭḍṇśṣṃḥ]/i.test(q) ? "iast" : "hk";
  }

  function toDeva(q) {
    var s = detect(q);
    if (s === "devanagari" || !window.Sanscript) return q;
    return Sanscript.t(s === "iast" ? q.toLowerCase() : q, s, "devanagari");
  }

  var pagefind;
  async function run(q) {
    var list = document.getElementById("sk-results");
    var shown = document.getElementById("sk-q-dev");
    list.innerHTML = "";
    if (!q.trim()) { shown.textContent = ""; return; }
    var dq = toDeva(q.trim());
    shown.textContent = dq !== q.trim() ? "→ " + dq : "";
    pagefind = pagefind || await import(new URL("../pagefind/pagefind.js", document.baseURI).href);
    var res = await pagefind.search(dq);
    var data = await Promise.all(res.results.slice(0, 20).map(function (r) { return r.data(); }));
    data.forEach(function (d) {
      var li = document.createElement("li");
      li.innerHTML = '<a href="' + d.url + '">' + (d.meta.title || d.url) + "</a><br><small>" + d.excerpt + "</small>";
      list.appendChild(li);
    });
    if (!data.length) list.innerHTML = "<li>No results.</li>";
  }

  document.addEventListener("DOMContentLoaded", function () {
    var box = document.getElementById("sk-q");
    var t;
    box.addEventListener("input", function () { clearTimeout(t); t = setTimeout(function () { run(box.value); }, 250); });
  });
})();
