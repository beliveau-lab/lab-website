#!/usr/bin/env python3
"""Builds the static HTML pages with a shared header/footer. Re-run any time
you change the shared chrome or page bodies below. Content that lives in JSON
(team, news, publications) is rendered client-side and is NOT in here."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Static-page images (banner, research figures) live in data/media.json so the
# image localizer can find them too. Missing file => render without images.
try:
    MEDIA = json.loads((ROOT / "data" / "media.json").read_text())
except FileNotFoundError:
    MEDIA = {}

def img_fallback(local, remote, cls, alt=""):
    """An <img> that prefers the local copy and falls back to the Wix CDN
    until images are localized — mirrors the team page behavior."""
    if not (local or remote):
        return ""
    src = local or remote
    onerr = f" onerror=\"this.onerror=null;this.src='{remote}'\"" if (local and remote) else ""
    return f'<img class="{cls}" src="{src}" alt="{alt}" loading="lazy"{onerr}>'

NAV = [
    ("index.html", "Home"), ("research.html", "Research"),
    ("publications.html", "Publications"), ("team.html", "Team"),
    ("news.html", "News"), ("teaching.html", "Teaching"),
    ("tools.html", "Tools"), ("join.html", "Join"),
]

def head(title, extra_js=""):
    links = "\n".join(f'        <a href="{h}">{t}</a>' for h, t in NAV)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | Beliveau Lab</title>
  <meta name="description" content="The Beliveau Lab at the University of Washington builds enabling technologies to study the 3D organization of genomes.">
  <meta property="og:site_name" content="Beliveau Lab">
  <meta property="og:title" content="{title} | Beliveau Lab">
  <meta property="og:type" content="website">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inria+Serif:ital,wght@0,400;0,700;1,400;1,700&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <header class="site-header">
    <nav class="nav">
      <a class="brand" href="index.html">Beliveau Lab</a>
      <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">☰</button>
      <div class="nav-links">
{links}
      </div>
    </nav>
  </header>
"""

FOOTER = """  <footer class="site-footer">
    <div class="wrap">
      <span>&copy; 2025 Brian J. Beliveau, PhD</span>
      <span class="sep">|</span><a href="about.html">About</a>
      <span class="sep">|</span><a href="http://www.washington.edu/" target="_blank" rel="noopener">UW</a>
      <span class="sep">|</span><a href="https://www.uwmedicine.org/" target="_blank" rel="noopener">UW Medicine</a>
      <span class="sep">|</span><a href="http://www.gs.washington.edu/" target="_blank" rel="noopener">Genome Sciences</a>
      <span class="sep">|</span><a href="contact.html">Contact</a>
      <span class="sep">|</span><a href="resources.html">Resources</a>
      <span class="sep">|</span><a href="https://bsky.app/profile/oligopain.bsky.social" target="_blank" rel="noopener">Bluesky</a>
    </div>
  </footer>
  <script src="js/main.js"></script>
%s
</body>
</html>
"""

def page(filename, title, body, page_js=""):
    js = (FOOTER % (f'  <script src="js/{page_js}"></script>' if page_js else "")).rstrip()
    html = head(title) + body + "\n" + js + "\n"
    (ROOT / filename).write_text(html)
    print("wrote", filename)

# ---------- Home ----------
_b = MEDIA.get("banner", {})
_banner = img_fallback(_b.get("photo"), _b.get("photo_remote"), "hero-banner",
                       _b.get("alt", "Beliveau Lab"))
page("index.html", "Home", f"""  <section class="hero">
    <div class="wrap">
      {_banner}
      <h1>Beliveau Lab</h1>
      <p class="tagline">Technologies for understanding genomes</p>
      <p>The Beliveau Lab is focused on building robust and scalable enabling technologies to study the organization of chromosomes in 3D space, the interactions they participate in at the inter- and intra-chromosomal level, and the associated RNAs and proteins that occupy functionally relevant sites. The motivation for this work is to better understand the mechanisms by which the organization and composition of genomic intervals relevant for health and disease impact the essential DNA transactions of transcription, replication, and repair. We also are committed to building ecosystems supported by open-source software, low-cost hardware, and extensive documentation to democratize the adoption of advanced single cell and spatial approaches in order to facilitate their application in a broad range of research settings.</p>
      <p>We believe strongly that science is for everyone.</p>
      <div class="equity-note">
        Please see our <a href="resources.html">Policy on Harassment and Discrimination</a>.
      </div>
    </div>
  </section>
""")

# ---------- Research ----------
RESEARCH = [
 ("Imaging chromosome structure at the nanoscale",
  'We use multiplexed <a href="https://www.nature.com/articles/ncomms8147.pdf" target="_blank" rel="noopener">DNA-PAINT and STORM</a> single-molecule super-resolution microscopy in combination with programmable <a href="http://www.pnas.org/content/pnas/109/52/21301.full.pdf" target="_blank" rel="noopener">Oligopaint</a> FISH probes to visualize the nanoscale structure of chromosomes. This approach provides a ~10-fold improvement in resolution compared to conventional microscopy and allows us to map the conformation and folding of chromosomes with exquisite detail.'),
 ("Visualizing chromatin dynamics",
  "We are interested in dynamic and structural properties of chromosomes in live cells. We use advanced live-cell imaging approaches such as single-particle tracking, fluorescence correlation spectroscopy, and super-resolution imaging to investigate the behavior of chromosomes in vivo."),
 ("Spatial transcriptomics",
  'Technologies such as single-cell RNA sequencing are producing a wealth of information about cell populations in different tissues during and after development. Determining the spatial arrangement of these cells remains much more challenging. We deploy our <a href="https://www.biorxiv.org/content/early/2018/08/27/401810" target="_blank" rel="noopener">SABER multiplexed imaging technology</a> in combination with advanced microscopy to map patterns of gene expression in their native contexts.'),
 ("High-throughput screening",
  'We are interested in deploying high-throughput approaches such as <a href="http://journals.plos.org/plosgenetics/article/file?id=10.1371/journal.pgen.1002667&type=printable" target="_blank" rel="noopener">Hi-FISH</a> and targeted mass spectrometry to identify the molecular factors that shape and structure the 3D genome.'),
 ("Genome mining and thermodynamic modeling",
  'We build and use <a href="http://www.pnas.org/content/pnas/early/2018/02/16/1714530115.full.pdf" target="_blank" rel="noopener">computational tools</a> to find optimal sites for molecular reagents such as in situ hybridization probes on a genome-wide scale. We also use machine learning and analytical computing to predict the thermodynamic behavior of nucleic acid systems and to investigate the sequence and structural properties of the genome.'),
 ("Genomics technology development",
  'We develop new <a href="http://www.pnas.org/content/109/52/21301" target="_blank" rel="noopener">enabling molecular technologies</a> to allow researchers to investigate a broad range of questions involving genome organization and gene expression.'),
 ("Advanced microscopy and instrumentation",
  'Multiplexed super-resolution imaging of chromosomes in their in situ context presents significant technical challenges. We design and build <a href="https://www.nature.com/articles/s41467-017-02028-8.pdf" target="_blank" rel="noopener">custom optical configurations</a> and apply advanced optical methods to increase our ability to visualize genome organization in single cells.'),
]
_figs = MEDIA.get("research", [])
def _research_card(i, t, b):
    fig = _figs[i] if i < len(_figs) else {}
    im = img_fallback(fig.get("photo"), fig.get("photo_remote"), "research-fig", t)
    return f'      <div class="research-card">{im}<h3>{t}</h3><p>{b}</p></div>'
cards = "\n".join(_research_card(i, t, b) for i, (t, b) in enumerate(RESEARCH))
page("research.html", "Research", f"""  <div class="wrap page-head">
    <h1>Research</h1>
    <p class="lead">Each human nucleus contains two meters of DNA packaged into an organelle a mere ~10&nbsp;&micro;m in diameter. Despite this dramatic difference in scale, the three-dimensional organization of the genome is non-random and plays a critical functional role in both health and disease. Our laboratory uses a combination of computational, molecular, and optical approaches to investigate the causes and consequences of 3D genome organization in single cells.</p>
  </div>
  <main class="wrap">
    <section>
      <div class="research-grid">
{cards}
      </div>
    </section>
  </main>
""")

# ---------- Publications ----------
page("publications.html", "Publications", """  <div class="wrap page-head">
    <h1>Publications</h1>
    <div class="pub-links-top" id="pub-top-links"></div>
  </div>
  <main class="wrap">
    <div id="pubs-root"><p class="loading">Loading publications…</p></div>
  </main>
""", "publications.js")

# ---------- Team ----------
page("team.html", "Team", """  <div class="wrap page-head">
    <h1>Our Team</h1>
  </div>
  <main class="wrap">
    <section>
      <div class="team-grid" id="team-current"><p class="loading">Loading team…</p></div>
    </section>
    <section>
      <h2>Alumni</h2>
      <div class="alumni-grid" id="team-alumni"></div>
    </section>
  </main>
""", "team.js")

# ---------- News ----------
page("news.html", "News", """  <div class="wrap page-head">
    <h1>News</h1>
  </div>
  <main class="wrap">
    <div id="news-root"><p class="loading">Loading news…</p></div>
  </main>
""", "news.js")

# ---------- Teaching ----------
page("teaching.html", "Teaching", """  <div class="wrap page-head">
    <h1>Teaching</h1>
  </div>
  <main class="wrap">
    <ul class="link-list">
      <li><b>GEN 559</b></li>
      <li><b>GEN 575</b> — <a href="https://github.com/beliveau-lab/gen575.2022" target="_blank" rel="noopener">course materials on GitHub</a></li>
    </ul>
  </main>
""")

# ---------- Tools ----------
page("tools.html", "Tools", """  <div class="wrap page-head">
    <h1>Tools</h1>
  </div>
  <main class="wrap">
    <ul class="link-list">
      <li>The <b>PaintSHOP</b> webserver for oligo FISH probe set design: <a href="http://paintshop.io" target="_blank" rel="noopener">paintshop.io</a></li>
      <li>PaintSHOP probes and appending sequences are hosted on the <a href="https://github.com/beliveau-lab/PaintSHOP_resources" target="_blank" rel="noopener">lab GitHub page</a></li>
      <li><b>SABER</b> resources: <a href="http://saber.fish" target="_blank" rel="noopener">saber.fish</a></li>
      <li><b>OligoMiner</b> scripts: <a href="https://github.com/beliveau-lab/OligoMiner" target="_blank" rel="noopener">lab GitHub page</a></li>
      <li>OligoMiner oligos can be downloaded from the <a href="https://yin.hms.harvard.edu/oligoMiner/list.html" target="_blank" rel="noopener">Yin Lab website</a></li>
      <li>Information about <b>Oligopaints</b>: <a href="https://oligopaints.hms.harvard.edu/" target="_blank" rel="noopener">Oligopaints website</a> hosted by the Wu lab</li>
    </ul>
  </main>
""")

# ---------- Join ----------
page("join.html", "Join", """  <div class="wrap page-head">
    <h1>Join our team</h1>
    <p class="lead">The Beliveau Lab is always happy to accept applications from UW undergraduates, UW graduate students, and postdocs. As our funding and space situation is constantly changing, interested applicants are encouraged to get in touch in advance of the desired start date. We use a combination of computational and experimental approaches, and lab members may undertake projects anchored in one or both of these areas. In all cases, experience with or willingness to learn Python programming is a plus.</p>
  </div>
  <main class="wrap">
    <div class="join-block">
      <h3>Chromatin Structure and Proteomics Postdoc</h3>
      <p>The <a href="https://www.schweppelab.org/" target="_blank" rel="noopener">Schweppe</a> and Beliveau Labs are looking to recruit a joint postdoctoral fellow to help lead projects at the interface of chromosome biology, 3D genome architecture, and nuclear proteomics.</p>
    </div>
    <div class="join-block">
      <h3>Undergraduate students</h3>
      <p>Please send (1) a brief description of your research interests and any prior research experience, (2) a current CV, and (3) your transcript to <a href="mailto:beliveau@uw.edu">beliveau [at] uw.edu</a>.</p>
    </div>
    <div class="join-block">
      <h3>Graduate students</h3>
      <p>We welcome interested UW graduate students to rotate in the lab. The lab currently can only accept graduate students from the <a href="http://www.gs.washington.edu/academics/gradprogram/index.htm" target="_blank" rel="noopener">Genome Sciences</a> and <a href="https://depts.washington.edu/mcb/" target="_blank" rel="noopener">MCB</a> programs for their dissertation research, but students in other UW programs may still be able to set up a rotation. If you are interested in rotating, please <a href="contact.html">email Brian</a> to discuss timing, potential rotation projects, and any program-related logistics.</p>
    </div>
    <div class="join-block">
      <h3>Postdocs</h3>
      <p>Please send (1) a cover letter describing your research interests and accomplishments and (2) a current CV containing contact information for three references to <a href="mailto:beliveau@uw.edu">beliveau [at] uw.edu</a>.</p>
    </div>
  </main>
""")

# ---------- Footer stubs (so footer links don't 404) ----------
page("resources.html", "Resources", """  <div class="wrap page-head">
    <h1>Resources</h1>
  </div>
  <main class="wrap">
    <section>
      <h2>Policy on Harassment and Discrimination</h2>
      <p>We believe strongly that science is for everyone. The Beliveau Lab does not tolerate harassment or discrimination of any kind.</p>
      <p style="color:var(--muted)"><em>Migration note: paste the lab's full policy text and any additional resource links here, then delete this note. (This content was not part of the main page scrape.)</em></p>
    </section>
  </main>
""")

page("contact.html", "Contact", """  <div class="wrap page-head">
    <h1>Contact</h1>
  </div>
  <main class="wrap">
    <section>
      <p>Brian J. Beliveau, PhD<br>Department of Genome Sciences, University of Washington<br><a href="mailto:beliveau@uw.edu">beliveau [at] uw.edu</a></p>
      <p style="color:var(--muted)"><em>Migration note: add the lab's mailing address / office and shipping details here.</em></p>
    </section>
  </main>
""")

page("about.html", "About", """  <div class="wrap page-head">
    <h1>About</h1>
  </div>
  <main class="wrap">
    <section>
      <p style="color:var(--muted)"><em>Migration note: add the PI bio / lab background here. (This page was not part of the main scrape.)</em></p>
    </section>
  </main>
""")

print("All pages built.")
