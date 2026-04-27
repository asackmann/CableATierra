const DATA_ROOT = "./data";
const SONG_ROOT = `${DATA_ROOT}/canciones`;

const els = {
  nav: document.querySelector("#track-nav"),
  home: document.querySelector("#home-view"),
  track: document.querySelector("#track-view"),
  trackContent: document.querySelector("#track-content"),
  trackMeta: document.querySelector("#track-meta"),
  title: document.querySelector("#page-title"),
  subtitle: document.querySelector("#page-subtitle"),
  back: document.querySelector("#back-button"),
};

let tracks = [];

const homeCopy =
  "Navegación rápida del setlist y notas por track.";

function parseRoute() {
  const hash = window.location.hash || "#/";
  const match = hash.match(/^#\/track\/(.+)$/);
  return match ? { type: "track", slug: decodeURIComponent(match[1]) } : { type: "home" };
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function renderNav() {
  els.nav.innerHTML = tracks
    .map(
      (track) => `
        <a class="track-link" data-slug="${track.slug}" href="#/track/${track.slug}">
          <span class="track-number">${track.number.toString().padStart(2, "0")}</span>
          <span class="track-link-title">${escapeHtml(track.title)}</span>
          <span class="track-nav-subtitle">${escapeHtml(track.artist)} • ${escapeHtml(track.bpm)}</span>
        </a>
      `
    )
    .join("");
}

function renderHome() {
  els.title.textContent = "CableATierra";
  els.subtitle.textContent = homeCopy;

  els.home.innerHTML = `
    <div class="home-grid">
      ${tracks
        .map(
          (track) => `
            <a class="track-card" href="#/track/${track.slug}">
              <span class="track-number">${track.number.toString().padStart(2, "0")} / 10</span>
              <h2>${escapeHtml(track.title)}</h2>
              <p class="card-copy">${escapeHtml(track.artist)}</p>
              <div class="card-meta">
                <span class="meta-chip">${escapeHtml(track.bpm)}</span>
                <span class="meta-chip">${escapeHtml(track.key)}</span>
                <span class="meta-chip">${escapeHtml(track.status)}</span>
              </div>
            </a>
          `
        )
        .join("")}
    </div>
  `;

  els.home.classList.remove("hidden");
  els.track.classList.add("hidden");
}

function setActiveNav(slug) {
  for (const link of els.nav.querySelectorAll(".track-link")) {
    link.classList.toggle("is-active", link.dataset.slug === slug);
  }
}

function rewriteRelativeMedia(container) {
  for (const image of container.querySelectorAll("img")) {
    const src = image.getAttribute("src") || "";
    if (!src || /^(https?:|data:|\/)/.test(src)) {
      continue;
    }

    const clean = src.replace(/^<|>$/g, "");
    image.setAttribute("src", `${SONG_ROOT}/${clean}`);
  }
}

async function renderTrack(slug) {
  const track = tracks.find((item) => item.slug === slug);
  if (!track) {
    renderHome();
    return;
  }

  els.title.textContent = track.title;
  els.subtitle.textContent = `${track.artist} • ${track.bpm} • ${track.key}`;

  const response = await fetch(`${SONG_ROOT}/${track.file}`);
  if (!response.ok) {
    els.trackContent.innerHTML = "<p>No pude cargar este track.</p>";
  } else {
    const markdown = await response.text();
    els.trackContent.innerHTML = marked.parse(markdown);
    rewriteRelativeMedia(els.trackContent);
  }

  els.trackMeta.innerHTML = `
    <span class="meta-chip">Track ${track.number}</span>
    <span class="meta-chip">${escapeHtml(track.bpm)}</span>
    <span class="meta-chip">${escapeHtml(track.status)}</span>
  `;

  els.home.classList.add("hidden");
  els.track.classList.remove("hidden");
  setActiveNav(slug);
}

async function renderRoute() {
  const route = parseRoute();

  if (route.type === "home") {
    setActiveNav("");
    renderHome();
    return;
  }

  await renderTrack(route.slug);
}

async function init() {
  const response = await fetch(`${DATA_ROOT}/tracks.json`);
  tracks = await response.json();
  renderNav();
  await renderRoute();
}

els.back.addEventListener("click", () => {
  window.location.hash = "#/";
});

window.addEventListener("hashchange", () => {
  renderRoute();
});

init();
