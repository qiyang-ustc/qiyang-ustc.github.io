const header = document.querySelector(".site-header");
const navToggle = document.querySelector(".nav-toggle");

if (header && navToggle) {
  navToggle.addEventListener("click", () => {
    const isOpen = header.getAttribute("data-open") === "true";
    header.setAttribute("data-open", String(!isOpen));
    navToggle.setAttribute("aria-expanded", String(!isOpen));
  });
}

const path = window.location.pathname.replace(/\/index\.html$/, "/");
document.querySelectorAll(".nav-links a").forEach((link) => {
  const href = new URL(link.href).pathname;
  if (href === path || (href !== "/" && path.startsWith(href))) {
    link.setAttribute("aria-current", "page");
  }
});

const canvas = document.querySelector("[data-tensor-canvas]");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (canvas) {
  const ctx = canvas.getContext("2d");
  let width = 0;
  let height = 0;
  let nodes = [];
  let frame = 0;

  const palette = {
    line: "rgba(251, 252, 247, 0.15)",
    lineHot: "rgba(111, 211, 200, 0.72)",
    node: "rgba(251, 252, 247, 0.72)",
    nodeHot: "rgba(111, 211, 200, 0.95)",
  };

  function resize() {
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    width = canvas.clientWidth;
    height = canvas.clientHeight;
    canvas.width = Math.floor(width * ratio);
    canvas.height = Math.floor(height * ratio);
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    makeLattice();
    draw();
  }

  function makeLattice() {
    const cols = Math.max(6, Math.floor(width / 142));
    const rows = Math.max(4, Math.floor(height / 128));
    const x0 = width * 0.38;
    const xSpan = width * 0.74;
    const y0 = height * 0.12;
    const ySpan = height * 0.76;
    nodes = [];

    for (let y = 0; y < rows; y += 1) {
      for (let x = 0; x < cols; x += 1) {
        const stagger = y % 2 === 0 ? 0 : 0.5;
        nodes.push({
          x: x0 + ((x + stagger) / Math.max(1, cols - 1)) * xSpan,
          y: y0 + (y / Math.max(1, rows - 1)) * ySpan,
          row: y,
          col: x,
          phase: (x * 0.73 + y * 0.41) % Math.PI,
        });
      }
    }
  }

  function drawLine(a, b, energy) {
    ctx.strokeStyle = energy > 0.82 ? palette.lineHot : palette.line;
    ctx.lineWidth = energy > 0.82 ? 1.5 : 1;
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(b.x, b.y);
    ctx.stroke();
  }

  function draw() {
    ctx.clearRect(0, 0, width, height);
    ctx.save();
    ctx.globalCompositeOperation = "source-over";

    const t = reduceMotion ? 0.35 : frame * 0.012;
    const cols = nodes.reduce((m, n) => Math.max(m, n.col), 0) + 1;

    for (const node of nodes) {
      const right = nodes.find((n) => n.row === node.row && n.col === node.col + 1);
      const down = nodes.find((n) => n.row === node.row + 1 && n.col === node.col);
      const diag = nodes.find((n) => n.row === node.row + 1 && n.col === node.col - (node.row % 2));
      const wave = (Math.sin(t + node.phase) + 1) / 2;
      if (right) drawLine(node, right, wave);
      if (down) drawLine(node, down, (Math.cos(t + node.phase + 0.9) + 1) / 2);
      if (diag) drawLine(node, diag, (Math.sin(t * 1.2 + node.phase + 1.7) + 1) / 2);
    }

    for (const node of nodes) {
      const pulse = (Math.sin(t * 1.7 + node.phase) + 1) / 2;
      const edgeFade = Math.max(0.18, 1 - Math.max(0, node.x - width * 0.6) / (width * 0.56));
      ctx.fillStyle = pulse > 0.9 ? palette.nodeHot : palette.node;
      ctx.globalAlpha = edgeFade * (0.54 + pulse * 0.44);
      ctx.beginPath();
      ctx.arc(node.x, node.y, pulse > 0.9 ? 4.2 : 2.7, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.globalAlpha = 0.8;
    ctx.strokeStyle = "rgba(251, 252, 247, 0.16)";
    ctx.strokeRect(width * 0.62, height * 0.16, Math.max(120, width / cols), Math.max(86, height * 0.16));
    ctx.restore();

    if (!reduceMotion) {
      frame += 1;
      requestAnimationFrame(draw);
    }
  }

  resize();
  window.addEventListener("resize", resize);
}
