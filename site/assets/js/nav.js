/* nav.js -- the application shell: top bar, hamburger, navigation drawer.
 *
 * Every page sets <body data-page="..." data-root=""> and this builds the
 * chrome, so the navigation has exactly one source of truth.
 */
(function () {
  const PAGES = [
    {
      group: "Workspace",
      items: [
        { id: "index", href: "index.html", label: "Overview", n: "01" },
        { id: "chart", href: "chart.html", label: "Cast a chart", n: "02" },
        { id: "panchanga", href: "panchanga.html", label: "Panchanga", n: "03" },
        { id: "transits", href: "transits.html", label: "Transits", n: "04" },
      ],
    },
    {
      group: "Reference",
      items: [
        { id: "knowledge", href: "knowledge.html", label: "Knowledge base", n: "05" },
        { id: "api", href: "api.html", label: "API & CLI", n: "06" },
        { id: "about", href: "about.html", label: "Provenance", n: "07" },
      ],
    },
  ];

  const REPO = "https://github.com/apsideslabs/vedic-astrology";
  const LIVE = "https://apsideslabs.github.io/vedic-astrology/";

  function el(tag, attrs, html) {
    const n = document.createElement(tag);
    for (const k in attrs || {}) n.setAttribute(k, attrs[k]);
    if (html != null) n.innerHTML = html;
    return n;
  }

  function build() {
    const root = document.body.dataset.root || "";
    const page = document.body.dataset.page || "";

    /* ---- top bar ---- */
    const bar = el("div", { class: "appbar" });
    const burger = el("button", {
      class: "burger", type: "button", "aria-label": "Open navigation",
      "aria-expanded": "false", "aria-controls": "site-drawer",
    }, "<span></span>");
    const mark = el("a", { class: "wordmark", href: root + "index.html" }, "Jyoti<em>sh</em>");
    const spacer = el("div", { class: "spacer" });

    let where = "";
    for (const g of PAGES) for (const it of g.items) if (it.id === page) where = it.label;
    const whereEl = el("div", { class: "where" }, where);

    const gh = el("a", {
      class: "chip-link", href: REPO, target: "_blank", rel: "noopener",
    }, "Source");
    bar.append(burger, mark, spacer, whereEl, gh);
    document.body.prepend(bar);

    /* ---- scrim + drawer ---- */
    const scrim = el("div", { class: "scrim" });
    const drawer = el("aside", {
      class: "drawer", id: "site-drawer", "aria-hidden": "true", "aria-label": "Site navigation",
    });

    const head = el("div", { class: "head" },
      '<span class="name">Jyoti<em>sh</em></span><span class="ver">v1.0</span>');
    drawer.append(head);

    const nav = el("nav");
    for (const g of PAGES) {
      const grp = el("div", { class: "grp" });
      grp.append(el("div", { class: "lbl" }, g.group));
      for (const it of g.items) {
        const a = el("a", {
          class: "item" + (it.id === page ? " on" : ""),
          href: root + it.href,
          "aria-current": it.id === page ? "page" : "false",
        }, `<span class="n">${it.n}</span><span>${it.label}</span>`);
        grp.append(a);
      }
      nav.append(grp);
    }
    drawer.append(nav);

    const foot = el("div", { class: "foot" },
      `<a href="${REPO}" target="_blank" rel="noopener">Repository ↗</a><br>` +
      `<a href="${LIVE}">Live site ↗</a><br>` +
      `<span>MIT · astronomy-engine</span>`);
    drawer.append(foot);

    document.body.append(scrim, drawer);

    /* ---- behaviour ---- */
    let lastFocus = null;
    const open = () => {
      lastFocus = document.activeElement;
      document.body.classList.add("nav-open");
      burger.setAttribute("aria-expanded", "true");
      drawer.setAttribute("aria-hidden", "false");
      const first = drawer.querySelector("a.item");
      if (first) setTimeout(() => first.focus(), 60);
    };
    const close = () => {
      document.body.classList.remove("nav-open");
      burger.setAttribute("aria-expanded", "false");
      drawer.setAttribute("aria-hidden", "true");
      if (lastFocus) lastFocus.focus();
    };
    burger.addEventListener("click", () =>
      document.body.classList.contains("nav-open") ? close() : open());
    scrim.addEventListener("click", close);
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && document.body.classList.contains("nav-open")) close();
    });
    drawer.addEventListener("click", (e) => {
      if (e.target.closest("a")) close();
    });
  }

  /* ---- scroll-spy for in-page tab strips ---- */
  function spy() {
    if (typeof IntersectionObserver === "undefined") return;
    const tabs = [...document.querySelectorAll(".tabs a[href^='#']")];
    if (!tabs.length) return;
    const targets = tabs
      .map((a) => document.querySelector(a.getAttribute("href")))
      .filter(Boolean);
    const setActive = (id) => {
      for (const a of tabs) a.classList.toggle("on", a.getAttribute("href") === "#" + id);
    };
    const io = new IntersectionObserver((entries) => {
      const visible = entries
        .filter((e) => e.isIntersecting)
        .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
      if (visible.length) setActive(visible[0].target.id);
    }, { rootMargin: "-88px 0px -60% 0px", threshold: 0 });
    for (const t of targets) io.observe(t);
  }

  document.addEventListener("DOMContentLoaded", () => {
    build();
    spy();
  });
})();
