// Renders the news timeline from data/news.json.
// Item text may contain inline <a> tags (trusted, lab-authored content).

async function renderNews() {
  const root = document.getElementById("news-root");
  try {
    const months = await (await fetch("data/news.json")).json();
    root.innerHTML = "";
    months.forEach(month => {
      const block = document.createElement("div");
      block.className = "news-month";

      const h = document.createElement("h3");
      h.textContent = month.month;
      block.appendChild(h);

      const ul = document.createElement("ul");
      ul.className = "news-list";
      (month.items || []).forEach(item => {
        // An item is either a string (text only) or { text, photos: [...] }.
        const isObj = item && typeof item === "object" && !Array.isArray(item);
        const text = isObj ? (item.text || "") : item;
        const photos = isObj && Array.isArray(item.photos) ? item.photos : null;

        const li = document.createElement("li");
        li.innerHTML = text;            // lab-authored, may contain <a>
        li.querySelectorAll("a").forEach(a => { a.target = "_blank"; a.rel = "noopener"; });
        if (photos && photos.length) li.appendChild(makeGallery(photos, month.month));
        ul.appendChild(li);
      });
      block.appendChild(ul);

      // Legacy: month-level photos still render as one gallery under the month.
      if (month.photos && month.photos.length) {
        block.appendChild(makeGallery(month.photos, month.month));
      }
      root.appendChild(block);
    });
  } catch (e) {
    root.innerHTML = '<p class="loading">Couldn\'t load news. Refresh to try again.</p>';
    console.error(e);
  }
}

// Builds a justified gallery of click-to-enlarge photos, used for both
// per-item and legacy month-level galleries. Photos keep their order and full
// frame (no cropping); photos in a row share one height and rows run flush to
// the gallery width. Row breaks are re-chosen when an image loads (its aspect
// ratio becomes known) or the gallery is resized.
const GALLERY_GAP = 8;       // px; keep in sync with .news-row gap in style.css
const GALLERY_MAX_H = 320;   // px; caps row height so 1-2 photo sets stay modest

function makeGallery(photos, label) {
  const gallery = document.createElement("div");
  gallery.className = "news-photos";
  const links = photos.map((src, i) => {
    // Wrapped in a link so the photo still opens without JS (or in a new tab
    // with cmd/ctrl-click); a plain click opens the lightbox.
    const link = document.createElement("a");
    link.href = src;
    link.setAttribute("aria-label", "Enlarge " + label + " lab photo");
    link.addEventListener("click", e => {
      if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      e.preventDefault();
      openLightbox(photos, i, label);
    });
    const img = document.createElement("img");
    img.loading = "lazy"; img.alt = label + " lab photo";
    img.addEventListener("load", () => layoutGallery(gallery, links));
    img.src = src;
    link.appendChild(img);
    return link;
  });
  new ResizeObserver(() => layoutGallery(gallery, links)).observe(gallery);
  return gallery;
}

function layoutGallery(gallery, links) {
  const W = gallery.clientWidth;
  if (!W) return;
  const ars = links.map(l => {
    const im = l.firstChild;
    return im.naturalWidth ? im.naturalWidth / im.naturalHeight : 4 / 3;
  });
  const key = W + ":" + ars.map(a => a.toFixed(3)).join(",");
  if (gallery.dataset.layout === key) return;   // nothing changed
  gallery.dataset.layout = key;

  // Height a row of photos i..j-1 needs to span the full width.
  const sum = (i, j) => ars.slice(i, j).reduce((a, b) => a + b, 0);
  const rowH = (i, j) => (W - GALLERY_GAP * (j - i - 1)) / sum(i, j);

  // Pick row breaks (photos stay in order) that keep every row as close as
  // possible to the target height.
  const target = Math.min(230, Math.max(120, W * 0.32));
  const n = ars.length, cost = [0], from = [0];
  for (let j = 1; j <= n; j++) {
    cost[j] = Infinity;
    for (let i = 0; i < j; i++) {
      const c = cost[i] + (rowH(i, j) - target) ** 2;
      if (c < cost[j]) { cost[j] = c; from[j] = i; }
    }
  }
  const rows = [];
  for (let j = n; j > 0; j = from[j]) rows.unshift([from[j], j]);

  gallery.replaceChildren(...rows.map(([i, j]) => {
    const row = document.createElement("div");
    row.className = "news-row";
    const h = rowH(i, j);
    // A row that would be taller than the cap stays at the cap and doesn't
    // stretch to full width (e.g. a lone photo).
    if (h > GALLERY_MAX_H) {
      row.style.maxWidth = (sum(i, j) * GALLERY_MAX_H + GALLERY_GAP * (j - i - 1)) + "px";
    }
    for (let k = i; k < j; k++) {
      links[k].style.flex = `${ars[k]} 1 0px`;
      links[k].style.aspectRatio = ars[k];
      row.appendChild(links[k]);
    }
    return row;
  }));
}

// ---- Click-to-enlarge viewer for news photos ----

let lightbox = null, lbImg = null, lbPhotos = [], lbIndex = 0, lbLabel = "", lbReturnFocus = null;

function buildLightbox() {
  lightbox = document.createElement("div");
  lightbox.className = "lightbox";
  lightbox.setAttribute("role", "dialog");
  lightbox.setAttribute("aria-modal", "true");
  lightbox.hidden = true;
  lightbox.innerHTML =
    '<button type="button" class="lb-close" aria-label="Close">&times;</button>' +
    '<button type="button" class="lb-prev" aria-label="Previous photo">&#8249;</button>' +
    '<img class="lb-img" alt="">' +
    '<button type="button" class="lb-next" aria-label="Next photo">&#8250;</button>';
  lbImg = lightbox.querySelector(".lb-img");

  // Arrows step through the month's photos; any other click closes.
  lightbox.addEventListener("click", e => {
    if (e.target.closest(".lb-prev")) stepLightbox(-1);
    else if (e.target.closest(".lb-next")) stepLightbox(1);
    else closeLightbox();
  });
  document.addEventListener("keydown", e => {
    if (lightbox.hidden) return;
    if (e.key === "Escape") closeLightbox();
    else if (e.key === "ArrowLeft") stepLightbox(-1);
    else if (e.key === "ArrowRight") stepLightbox(1);
  });
  document.body.appendChild(lightbox);
}

function showLightboxPhoto() {
  lbImg.src = lbPhotos[lbIndex];
  lbImg.alt = lbLabel + " lab photo" +
    (lbPhotos.length > 1 ? ` (${lbIndex + 1} of ${lbPhotos.length})` : "");
  const multi = lbPhotos.length > 1;
  lightbox.querySelector(".lb-prev").hidden = !multi;
  lightbox.querySelector(".lb-next").hidden = !multi;
}

function openLightbox(photos, index, label) {
  if (!lightbox) buildLightbox();
  lbPhotos = photos; lbIndex = index; lbLabel = label;
  lbReturnFocus = document.activeElement;
  showLightboxPhoto();
  lightbox.hidden = false;
  document.body.style.overflow = "hidden";
  lightbox.querySelector(".lb-close").focus();
}

function stepLightbox(delta) {
  if (lbPhotos.length < 2) return;
  lbIndex = (lbIndex + delta + lbPhotos.length) % lbPhotos.length;
  showLightboxPhoto();
}

function closeLightbox() {
  lightbox.hidden = true;
  lbImg.removeAttribute("src");
  document.body.style.overflow = "";
  if (lbReturnFocus) lbReturnFocus.focus();
}

renderNews();
