// Shared site behavior: nav active state, mobile menu, email + image helpers.

document.addEventListener("DOMContentLoaded", () => {
  // Highlight the current page in the nav.
  const here = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav-links a").forEach(a => {
    const target = a.getAttribute("href");
    if (target === here || (here === "" && target === "index.html")) {
      a.classList.add("active");
    }
  });

  // Mobile nav toggle.
  const toggle = document.querySelector(".nav-toggle");
  const links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", () => links.classList.toggle("open"));
  }
});

// Render an email as a mailto link while keeping it lightly obfuscated in the
// markup (matches the lab's existing "user [a t] uw.edu" anti-scrape style).
function emailLink(addr) {
  const [user, domain] = addr.split("@");
  const a = document.createElement("a");
  a.href = "mailto:" + user + "@" + domain;
  a.className = "email";
  a.textContent = user + " [at] " + domain;
  return a;
}

// Use the local photo path, silently falling back to the original remote URL
// if the local file isn't present yet (so the site looks right before images
// are downloaded with download_images.py).
function photoWithFallback(local, remote, alt, cls) {
  const img = document.createElement("img");
  img.className = cls;
  img.loading = "lazy";
  img.alt = alt;
  img.src = local || remote || "";
  if (remote && local) {
    img.addEventListener("error", function handler() {
      img.removeEventListener("error", handler);
      img.src = remote;
    });
  }
  return img;
}
