// Renders the current team and alumni from data/team.json.

async function renderTeam() {
  const cur = document.getElementById("team-current");
  const alum = document.getElementById("team-alumni");
  try {
    const data = await (await fetch("data/team.json")).json();

    cur.innerHTML = "";
    const lastName = n => n.trim().split(/\s+/).pop().toLowerCase();
    const members = [...data.current].sort((a, b) => {
      if (!!a.pi !== !!b.pi) return a.pi ? -1 : 1;        // PI stays first
      return lastName(a.name).localeCompare(lastName(b.name));
    });
    members.forEach(m => cur.appendChild(memberCard(m)));
    cur.appendChild(joinCard());

    alum.innerHTML = "";
    data.alumni.forEach(a => alum.appendChild(alumCard(a)));
  } catch (e) {
    cur.innerHTML = '<p class="loading">Couldn\'t load the team list. Refresh to try again.</p>';
    console.error(e);
  }
}

function memberCard(m) {
  const el = document.createElement("div");
  el.className = "member" + (m.pi ? " pi" : "");
  el.appendChild(photoWithFallback(m.photo, m.photo_remote, m.name, "photo"));

  const name = document.createElement("div");
  name.className = "name";
  name.textContent = m.name;
  el.appendChild(name);

  const role = document.createElement("div");
  role.className = "role";
  role.textContent = m.role;
  el.appendChild(role);

  if (m.degree) el.appendChild(meta(m.degree));
  if (m.program) el.appendChild(meta(m.program));
  if (m.email) {
    const wrap = document.createElement("div");
    wrap.appendChild(emailLink(m.email));
    el.appendChild(wrap);
  }
  if (m.social) {
    const s = meta("");
    const a = document.createElement("a");
    a.href = m.social.url; a.textContent = m.social.label; a.target = "_blank"; a.rel = "noopener";
    s.appendChild(a);
    el.appendChild(s);
  }
  if (m.joint) {
    const j = meta("Joint with the ");
    const a = document.createElement("a");
    a.href = m.joint.url; a.textContent = m.joint.name; a.target = "_blank"; a.rel = "noopener";
    j.appendChild(a);
    el.appendChild(j);
  }
  if (m.pronouns) el.appendChild(meta(m.pronouns));
  if (m.joined) el.appendChild(meta("Joined " + m.joined));
  return el;
}

function alumCard(a) {
  const el = document.createElement("div");
  el.className = "alum";
  el.appendChild(photoWithFallback(a.photo, a.photo_remote, a.name, "photo"));

  const name = document.createElement("div");
  name.className = "name"; name.textContent = a.name; el.appendChild(name);

  const role = document.createElement("div");
  role.className = "role"; role.textContent = a.role; el.appendChild(role);

  const dates = document.createElement("div");
  dates.className = "dates"; dates.textContent = a.dates; el.appendChild(dates);

  return el;
}

function joinCard() {
  const el = document.createElement("div");
  el.className = "member join-card";
  const img = document.createElement("img");
  img.className = "photo"; img.alt = "Join the lab"; img.loading = "lazy";
  img.src = "https://static.wixstatic.com/media/b8abaf_1a094f1c902f47febf91f9675624577b~mv2_d_1290_1290_s_2.png/v1/fill/w_300,h_300,al_c,q_85,enc_avif,quality_auto/retina9.png";
  const a = document.createElement("a"); a.href = "join.html"; a.appendChild(img);
  el.appendChild(a);
  const name = document.createElement("div"); name.className = "name"; name.textContent = "You?";
  el.appendChild(name);
  const role = document.createElement("div"); role.className = "meta";
  role.textContent = "Click to learn about opportunities"; el.appendChild(role);
  const btn = document.createElement("a"); btn.href = "join.html"; btn.className = "btn"; btn.textContent = "Join";
  btn.style.marginTop = "8px"; btn.style.display = "inline-block";
  el.appendChild(btn);
  return el;
}

function meta(text) {
  const d = document.createElement("div");
  d.className = "meta"; d.textContent = text; return d;
}

renderTeam();
