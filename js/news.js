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
        const li = document.createElement("li");
        li.innerHTML = item;            // lab-authored, may contain <a>
        li.querySelectorAll("a").forEach(a => { a.target = "_blank"; a.rel = "noopener"; });
        ul.appendChild(li);
      });
      block.appendChild(ul);

      if (month.photos && month.photos.length) {
        const gallery = document.createElement("div");
        gallery.className = "news-photos";
        month.photos.forEach((src, i) => {
          // Wrapped in a link so the photo still opens without JS (or in a
          // new tab with cmd/ctrl-click); a plain click opens the lightbox.
          const link = document.createElement("a");
          link.href = src;
          link.setAttribute("aria-label", "Enlarge " + month.month + " lab photo");
          link.addEventListener("click", e => {
            if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
            e.preventDefault();
            openLightbox(month.photos, i, month.month);
          });
          const img = document.createElement("img");
          img.src = src; img.loading = "lazy"; img.alt = month.month + " lab photo";
          link.appendChild(img);
          gallery.appendChild(link);
        });
        block.appendChild(gallery);
      }
      root.appendChild(block);
    });
  } catch (e) {
    root.innerHTML = '<p class="loading">Couldn\'t load news. Refresh to try again.</p>';
    console.error(e);
  }
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
