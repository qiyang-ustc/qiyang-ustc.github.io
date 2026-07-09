const header = document.querySelector(".site-header");
const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelector(".nav-links");

if (header && navToggle) {
  const openNavigation = () => {
    header.setAttribute("data-open", "true");
    navToggle.setAttribute("aria-expanded", "true");
    navLinks?.querySelector("a")?.focus();
  };

  const closeNavigation = () => {
    header.removeAttribute("data-open");
    navToggle.setAttribute("aria-expanded", "false");
    if (document.activeElement !== navToggle) {
      navToggle.focus();
    }
  };

  navToggle.addEventListener("click", () => {
    const isOpen = header.getAttribute("data-open") === "true";
    if (isOpen) {
      closeNavigation();
    } else {
      openNavigation();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && header.getAttribute("data-open") === "true") {
      closeNavigation();
    }
  });
}

function normalizePath(pathname) {
  const withoutIndex = pathname.replace(/\/index\.html$/, "/");
  if (withoutIndex === "/" || withoutIndex.endsWith("/")) {
    return withoutIndex;
  }
  return `${withoutIndex}/`;
}

const currentPath = normalizePath(window.location.pathname);

document.querySelectorAll(".nav-links a").forEach((link) => {
  const linkPath = normalizePath(new URL(link.href, window.location.href).pathname);
  const isCurrent =
    linkPath === currentPath ||
    (linkPath !== "/" && currentPath.startsWith(linkPath));

  if (isCurrent) {
    link.setAttribute("aria-current", "page");
  } else {
    link.removeAttribute("aria-current");
  }
});
