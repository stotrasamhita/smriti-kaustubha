/* Smṛti-kaustubha site behaviour: script switcher, paragraph anchors, copy citation (spec §6).
 * The text is stored in Devanāgarī; other scripts are produced in the browser with Sanscript,
 * whose scheme tables are the same as the Python indic_transliteration package used for the PDF. */
(function () {
  "use strict";
  var KEY = "sk-script";
  var FONTS = {
    devanagari: "Noto+Serif+Devanagari", kannada: "Noto+Serif+Kannada", telugu: "Noto+Serif+Telugu",
    tamil: "Noto+Serif+Tamil", tamil_superscripted: "Noto+Serif+Tamil", grantha: "Noto+Serif+Grantha",
    malayalam: "Noto+Serif+Malayalam", bengali: "Noto+Serif+Bengali", gujarati: "Noto+Serif+Gujarati",
    oriya: "Noto+Serif+Oriya", sharada: "Noto+Sans+Sharada", iast: "Noto+Serif", iso: "Noto+Serif"
  };
  var originals = new WeakMap();
  var loadedFonts = {};

  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } }

  function textNodes(root) {
    var out = [];
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        if (!n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        for (var p = n.parentNode; p && p !== root.parentNode; p = p.parentNode) {
          if (p.nodeType === 1 && (p.classList.contains("sk-noxlit") || /^(CODE|PRE|SCRIPT|STYLE)$/.test(p.tagName)))
            return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    while (walker.nextNode()) out.push(walker.currentNode);
    return out;
  }

  function loadFont(scheme) {
    var fam = FONTS[scheme];
    if (!fam || loadedFonts[fam]) return;
    loadedFonts[fam] = true;
    var l = document.createElement("link");
    l.rel = "stylesheet";
    l.href = "https://fonts.googleapis.com/css2?family=" + fam + ":wght@400;600&display=swap";
    document.head.appendChild(l);
  }

  function transliterate(scheme) {
    if (!window.Sanscript) return;
    loadFont(scheme);
    var roots = document.querySelectorAll(".sk-text, .book-menu nav, .book-toc");
    roots.forEach(function (root) {
      textNodes(root).forEach(function (n) {
        if (!originals.has(n)) originals.set(n, n.nodeValue);
        var src = originals.get(n);
        n.nodeValue = scheme === "devanagari" ? src : Sanscript.t(src, "devanagari", scheme);
      });
    });
    document.documentElement.setAttribute("data-sk-script", scheme);
    var fam = (FONTS[scheme] || "").replace(/\+/g, " ");
    document.querySelectorAll(".markdown").forEach(function (m) {
      m.style.fontFamily = fam ? '"' + fam + '", serif' : "";
    });
  }

  function citation(id) {
    var title = (document.querySelector(".sk-text h1") || {}).textContent || document.title;
    var page = id.replace(/^p(\d+).*$/, "$1");
    return "Smṛtikaustubha (NSP 1931), p." + page + ", " + title.trim() + " — " + location.origin + location.pathname + "#" + id;
  }

  function toast(msg) {
    var t = document.createElement("div");
    t.className = "sk-toast sk-noxlit";
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(function () { t.remove(); }, 1600);
  }

  function addAnchors() {
    document.querySelectorAll(".sk-text p[id], .sk-text .sk-shloka[id]").forEach(function (el) {
      if (!el.querySelector(":scope > .sk-anchor")) {
        var a = document.createElement("a");
        a.className = "sk-anchor sk-noxlit";
        a.href = "#" + el.id;
        a.title = el.id;
        a.textContent = "¶";
        el.insertBefore(a, el.firstChild);
      }
      var b = document.createElement("button");
      b.className = "sk-cite sk-noxlit";
      b.type = "button";
      b.title = "Copy citation";
      b.textContent = "⧉ " + el.id;
      b.addEventListener("click", function () {
        var c = citation(el.id);
        (navigator.clipboard ? navigator.clipboard.writeText(c) : Promise.reject()).then(
          function () { toast("Citation copied"); }, function () { window.prompt("Citation", c); });
      });
      el.appendChild(b);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    addAnchors();
    var sel = document.getElementById("sk-script");
    var scheme = get(KEY) || "devanagari";
    if (sel) {
      sel.value = scheme;
      sel.addEventListener("change", function () { set(KEY, sel.value); transliterate(sel.value); });
    }
    if (scheme !== "devanagari") transliterate(scheme);
  });
})();
