// Renders publications from data/publications.json, grouped by year, with
// preprints first. The PI's name is bolded automatically.

function boldBeliveau(authors) {
  // Escape, then bold any "Beliveau" surname token.
  const esc = authors.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  return esc.replace(/(Beliveau,?\s*B(?:\.J\.|\.)?)/g, "<b>$1</b>");
}

function pubEl(p) {
  const el = document.createElement("div");
  el.className = "pub";

  const title = document.createElement("div");
  title.className = "pub-title";
  if (p.num != null) {
    const n = document.createElement("span");
    n.className = "pub-num"; n.textContent = "[" + p.num + "]";
    title.appendChild(n);
  }
  title.appendChild(document.createTextNode(p.title));
  el.appendChild(title);

  const authors = document.createElement("div");
  authors.className = "pub-authors";
  authors.innerHTML = boldBeliveau(p.authors);
  el.appendChild(authors);

  const venue = document.createElement("div");
  venue.className = "pub-venue";
  venue.textContent = p.venue;
  el.appendChild(venue);

  if (p.links && p.links.length) {
    const links = document.createElement("div");
    links.className = "pub-links";
    p.links.forEach(l => {
      const a = document.createElement("a");
      a.href = l.url; a.textContent = l.label; a.target = "_blank"; a.rel = "noopener";
      links.appendChild(a);
    });
    el.appendChild(links);
  }
  return el;
}

async function renderPubs() {
  const root = document.getElementById("pubs-root");
  try {
    const data = await (await fetch("data/publications.json")).json();

    // Top links
    const top = document.getElementById("pub-top-links");
    if (top) {
      top.innerHTML = "";
      const gs = document.createElement("a");
      gs.className = "btn"; gs.href = data.scholar; gs.textContent = "Google Scholar";
      gs.target = "_blank"; gs.rel = "noopener";
      const pm = document.createElement("a");
      pm.className = "btn ghost"; pm.href = data.pubmed; pm.textContent = "PubMed";
      pm.target = "_blank"; pm.rel = "noopener";
      top.appendChild(gs); top.appendChild(pm);
    }

    root.innerHTML = "";

    if (data.preprints && data.preprints.length) {
      const head = document.createElement("h2");
      head.className = "pub-year"; head.textContent = "Preprints";
      root.appendChild(head);
      data.preprints.forEach(p => root.appendChild(pubEl(p)));
    }

    // Group papers by year, descending.
    const byYear = {};
    data.papers.forEach(p => { (byYear[p.year] = byYear[p.year] || []).push(p); });
    Object.keys(byYear).map(Number).sort((a, b) => b - a).forEach(year => {
      const head = document.createElement("h2");
      head.className = "pub-year"; head.textContent = year;
      root.appendChild(head);
      byYear[year].sort((a, b) => b.num - a.num).forEach(p => root.appendChild(pubEl(p)));
    });
  } catch (e) {
    root.innerHTML = '<p class="loading">Couldn\'t load publications. Refresh to try again.</p>';
    console.error(e);
  }
}

renderPubs();
