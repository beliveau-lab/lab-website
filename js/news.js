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
        month.photos.forEach(src => {
          const img = document.createElement("img");
          img.src = src; img.loading = "lazy"; img.alt = month.month + " lab photo";
          gallery.appendChild(img);
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

renderNews();
