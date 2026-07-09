# Academic Dossier Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the complete static site as a consistent academic research dossier that remains visually complete without paper highlight images.

**Architecture:** Keep the existing dependency-free HTML, CSS, and JavaScript site. Replace the shared visual system in `docs/assets/site.css`, simplify `docs/assets/site.js` to navigation state only, rebuild the homepage around equal publication records, and normalize each supporting page to the same unframed record-list language. Add a standard-library Python audit so link, asset, accessibility, and asset-version regressions are detected before deployment.

**Tech Stack:** Static HTML5, CSS, vanilla JavaScript, Python 3 standard library, GitHub Actions, GitHub Pages.

---

## File Map

- `scripts/check_site.py`: static HTML contract audit for internal links, local assets, image alt text, duplicate IDs, heading presence, and shared asset versions.
- `docs/assets/site.css`: complete shared academic dossier visual system and responsive behavior.
- `docs/assets/site.js`: mobile navigation state and current-page navigation marker.
- `docs/index.html`: compact identity block, selected publication records, tool index, and notes records.
- `docs/research/publications/index.html`: chronological publication records and explicit publication links.
- `docs/blog/index.html`: notes record list with optional existing thumbnails.
- `docs/cv/index.html`: unframed CV sections with stable date columns.
- `docs/talks/index.html`: chronological talk records.
- `docs/posters/index.html`: chronological poster records.
- `docs/blog/*/index.html`: article asset-version update and shared reading layout.
- `docs/404.html`: compact dossier-style error page.

No paper highlight image is created, copied, cropped, or installed by this plan.

### Task 1: Add A Static Site Contract Audit

**Files:**
- Create: `scripts/check_site.py`

- [ ] **Step 1: Create the audit script**

Create `scripts/check_site.py` with this complete implementation:

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[tuple[str, str]] = []
        self.ids: list[str] = []
        self.images_without_alt: list[str] = []
        self.h1_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            self.ids.append(element_id)
        if tag == "h1":
            self.h1_count += 1
        if tag == "img" and "alt" not in values:
            self.images_without_alt.append(values.get("src") or "<missing src>")
        for attribute in ("href", "src"):
            value = values.get(attribute)
            if value:
                self.references.append((attribute, value))


def local_target(root: Path, page: Path, raw_value: str) -> Path | None:
    value = raw_value.strip()
    if not value or value.startswith("#"):
        return None
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        return None
    clean_path = unquote(parsed.path)
    if not clean_path:
        return None
    target = root / clean_path.lstrip("/") if clean_path.startswith("/") else page.parent / clean_path
    if clean_path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target.resolve()


def audit(root: Path, expected_asset_version: str | None) -> list[str]:
    errors: list[str] = []
    pages = sorted(root.rglob("*.html"))
    for page in pages:
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        relative = page.relative_to(root)

        duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
        if duplicates:
            errors.append(f"{relative}: duplicate ids: {', '.join(duplicates)}")
        if parser.h1_count != 1:
            errors.append(f"{relative}: expected one h1, found {parser.h1_count}")
        for src in parser.images_without_alt:
            errors.append(f"{relative}: image missing alt: {src}")

        for attribute, value in parser.references:
            target = local_target(root, page, value)
            if target is not None and not target.exists():
                errors.append(f"{relative}: broken {attribute}: {value}")
            if expected_asset_version and ("assets/site.css" in value or "assets/site.js" in value):
                if urlsplit(value).query != f"v={expected_asset_version}":
                    errors.append(
                        f"{relative}: shared asset version must be {expected_asset_version}: {value}"
                    )

    print(f"HTML pages checked: {len(pages)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="docs")
    parser.add_argument("--asset-version")
    args = parser.parse_args()
    errors = audit(Path(args.root).resolve(), args.asset_version)
    if errors:
        for error in errors:
            print(error)
        print(f"Errors: {len(errors)}")
        return 1
    print("Errors: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run the audit against the current site**

Run:

```bash
python3 scripts/check_site.py
```

Expected output:

```text
HTML pages checked: 10
Errors: 0
```

- [ ] **Step 3: Commit the audit**

```bash
git add scripts/check_site.py
git commit -m "Add static site contract audit"
```

### Task 2: Replace The Shared Visual System

**Files:**
- Modify: `docs/assets/site.css`
- Modify: `docs/assets/site.js`

- [ ] **Step 1: Replace the design tokens and global foundations**

Rewrite the top-level token block in `docs/assets/site.css` around this fixed system:

```css
:root {
  --ink: #202124;
  --ink-soft: #3c4043;
  --muted: #687078;
  --paper: #ffffff;
  --surface: #f7f8fa;
  --rule: #d8dde3;
  --rule-strong: #aeb7c1;
  --link: #315f7d;
  --link-hover: #183f58;
  --focus: #9fc3d8;
  --measure: 1080px;
  --reading: 760px;
  --sans: "Helvetica Neue", Helvetica, Arial, system-ui, sans-serif;
  --mono: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  color: var(--ink);
  background: var(--paper);
  font-family: var(--sans);
  line-height: 1.55;
  text-rendering: optimizeLegibility;
}
a { color: var(--link); text-decoration-thickness: 1px; text-underline-offset: 0.18em; }
a:hover { color: var(--link-hover); }
img { display: block; max-width: 100%; }
```

Remove all Google color tokens, display-font aliases, shadows, large radii, topic pills, animated canvas rules, and card-specific decorative backgrounds.

- [ ] **Step 2: Implement the shared dossier components**

The rewritten stylesheet must define these component contracts with the stated behavior:

```css
.site-header { position: sticky; top: 0; z-index: 20; border-bottom: 1px solid var(--rule); background: rgb(255 255 255 / 0.96); }
.nav-shell { width: min(var(--measure), calc(100% - 40px)); min-height: 56px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; gap: 24px; }
.brand { color: var(--ink); font-size: 0.94rem; font-weight: 700; text-decoration: none; }
.brand-mark { display: none; }
.nav-links { display: flex; align-items: center; gap: 24px; }
.nav-links a { color: var(--muted); font-size: 0.88rem; font-weight: 600; text-decoration: none; }
.nav-links a[aria-current="page"], .nav-links a:hover { color: var(--ink); }

.page-hero, .home-intro { border-bottom: 1px solid var(--rule); }
.page-hero-inner, .home-intro-inner { width: min(var(--measure), calc(100% - 40px)); margin: 0 auto; padding: 44px 0 34px; }
.page-hero h1, .home-intro h1 { margin: 0; font-size: 3.5rem; line-height: 1; letter-spacing: 0; }
.page-hero p, .home-summary { max-width: 720px; color: var(--ink-soft); }

.page-section, .home-section { width: min(var(--measure), calc(100% - 40px)); margin: 0 auto; padding: 38px 0; }
.section-header, .record-heading { display: flex; align-items: baseline; justify-content: space-between; gap: 24px; margin-bottom: 10px; }
.section-header h2, .record-heading h2 { margin: 0; font-size: 1rem; line-height: 1.3; }

.record-list, .paper-table, .talk-timeline, .note-list { border-top: 1px solid var(--rule-strong); }
.record, .paper-item, .talk-card, .note-row, .poster-card { display: grid; grid-template-columns: 112px minmax(0, 1fr) auto; gap: 20px; padding: 18px 0 20px; border: 0; border-bottom: 1px solid var(--rule); border-radius: 0; background: transparent; }
.record-date, .paper-year, .talk-date { color: var(--muted); font-family: var(--mono); font-size: 0.76rem; font-variant-numeric: tabular-nums; }
.record h3, .paper-item h3, .talk-card h3, .note-row h3, .poster-card h3 { margin: 0 0 6px; font-size: 1.02rem; line-height: 1.32; }
.record p, .paper-item p, .talk-card p, .note-row p, .poster-card p { margin: 0; color: var(--muted); }

.paper-visual { width: 180px; aspect-ratio: 3 / 2; object-fit: contain; border: 1px solid var(--rule); background: var(--paper); }
.paper-item:not(.has-visual) .paper-visual { display: none; }
.paper-item.has-visual { grid-template-columns: 112px 180px minmax(0, 1fr); }

.article { width: min(var(--reading), calc(100% - 40px)); margin: 0 auto; padding: 52px 0 72px; }
.article h1 { margin: 10px 0 18px; font-size: 3.25rem; line-height: 1.06; }
.article figure { margin: 28px 0; border: 0; border-radius: 0; background: transparent; }
.article figcaption { padding: 8px 0 0; border: 0; color: var(--muted); font-size: 0.82rem; }
```

The final file must also style CV sections, tool indexes, footer links, buttons as compact text commands, code blocks, and article lists using the same tokens.

- [ ] **Step 3: Implement responsive and accessibility rules**

Add exact behavior at `860px` and `640px`:

```css
@media (max-width: 860px) {
  .nav-toggle { display: grid; }
  .nav-links { position: absolute; left: 20px; right: 20px; top: 56px; display: none; padding: 12px 16px; border: 1px solid var(--rule); background: var(--paper); }
  .site-header[data-open="true"] .nav-links { display: grid; gap: 0; }
  .nav-links a { padding: 9px 0; }
}

@media (max-width: 640px) {
  .nav-shell, .page-hero-inner, .home-intro-inner, .page-section, .home-section, .footer-inner, .article { width: min(100% - 24px, var(--measure)); }
  .record, .paper-item, .talk-card, .note-row, .poster-card, .paper-item.has-visual { grid-template-columns: 1fr; gap: 8px; }
  .paper-visual { width: 100%; }
  .page-hero h1, .home-intro h1 { font-size: 2.35rem; }
  .article h1 { font-size: 2.1rem; }
  .section-header, .record-heading, .footer-inner { align-items: flex-start; flex-direction: column; }
}

:focus-visible { outline: 3px solid var(--focus); outline-offset: 3px; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { scroll-behavior: auto !important; transition-duration: 0.001ms !important; animation-duration: 0.001ms !important; }
}
```

- [ ] **Step 4: Remove unused canvas behavior from JavaScript**

Replace `docs/assets/site.js` with navigation-only behavior:

```javascript
const header = document.querySelector(".site-header");
const navToggle = document.querySelector(".nav-toggle");

if (header && navToggle) {
  navToggle.addEventListener("click", () => {
    const open = header.getAttribute("data-open") === "true";
    header.setAttribute("data-open", String(!open));
    navToggle.setAttribute("aria-expanded", String(!open));
  });
}

const path = window.location.pathname.replace(/\/index\.html$/, "/");
document.querySelectorAll(".nav-links a").forEach((link) => {
  const href = new URL(link.href).pathname;
  if (href === path || (href !== "/" && path.startsWith(href))) {
    link.setAttribute("aria-current", "page");
  } else {
    link.removeAttribute("aria-current");
  }
});
```

- [ ] **Step 5: Run the static audit and CSS sanity checks**

Run:

```bash
python3 scripts/check_site.py
git diff --check
rg -n "linear-gradient|radial-gradient|box-shadow|google-red|google-yellow|google-green|data-tensor-canvas" docs/assets/site.css docs/assets/site.js
```

Expected: the audit reports zero errors, `git diff --check` is silent, and `rg` returns no matches.

- [ ] **Step 6: Commit the shared system**

```bash
git add docs/assets/site.css docs/assets/site.js
git commit -m "Rebuild shared academic dossier styles"
```

### Task 3: Rebuild The Homepage Around Research Records

**Files:**
- Modify: `docs/index.html`

- [ ] **Step 1: Replace the profile hero with a compact identity block**

Use this structure and preserve the existing research statement and destinations:

```html
<section class="home-intro">
  <div class="home-intro-inner">
    <p class="page-label">Postdoctoral researcher / University of Amsterdam</p>
    <h1>Qi Yang</h1>
    <p class="home-summary">I develop tensor-network algorithms and scientific software for strongly correlated quantum matter, with a focus on iPEPS, long-range interactions, and scalable contractions.</p>
    <p class="research-line"><strong>Research:</strong> tensor networks, iPEPS, CTMRG, long-range systems, and numerical linear algebra.</p>
    <nav class="profile-links" aria-label="Profile links">
      <a href="https://t.ly/P9R_s">Google Scholar</a>
      <a href="https://github.com/qiyang-ustc">GitHub</a>
      <a href="mailto:q.yang2@uva.nl">Email</a>
      <a href="/cv/">CV</a>
    </nav>
  </div>
</section>
```

Remove the brand icon from the shared header markup, Current focus panel, research figure, topic pills, button row, sticky profile sidebar, and benchmark image.

- [ ] **Step 2: Convert recent publications into equal record rows**

Create a `.home-section` containing `.record-list` and three `.record` articles. Each article must contain `.record-date`, a body with venue, linked title, complete authors, contribution sentence, and `.record-links`. Use the existing links for arXiv `2606.20522`, PRB `113, L201106`, and PRB `113, 085109`. Do not add `.paper-visual` or an image in this implementation.

- [ ] **Step 3: Convert tools and notes into unframed indexes**

Represent QRCTM, Gaussian-fPEPS, varbench, and TeneT.jl as `.tool-index` rows with repository name, one-line purpose, and source link. Represent the three notes as `.record` rows with date, title, and one-line summary. Remove `.compact-grid`, `.compact-card`, and all homepage card markup.

- [ ] **Step 4: Verify the homepage contract**

Run:

```bash
python3 scripts/check_site.py
rg -n "profile-aside|profile-topics|compact-grid|compact-card|research-figure|data-tensor-canvas" docs/index.html
rg -n "home-intro|record-list|tool-index|arXiv:2606.20522" docs/index.html
git diff --check
```

Expected: the first `rg` returns no matches; the second reports all four required homepage markers; the audit reports zero errors; `git diff --check` is silent.

- [ ] **Step 5: Commit the homepage**

```bash
git add docs/index.html
git commit -m "Rebuild homepage as research dossier"
```

### Task 4: Normalize Publications, Notes, CV, Talks, Posters, And 404

**Files:**
- Modify: `docs/research/publications/index.html`
- Modify: `docs/blog/index.html`
- Modify: `docs/cv/index.html`
- Modify: `docs/talks/index.html`
- Modify: `docs/posters/index.html`
- Modify: `docs/404.html`

- [ ] **Step 1: Normalize the publications page**

Keep all publication titles, authors, venues, and destinations. Remove pill tags and sentence-style section headings. Use plain `.pub-links` anchors in the order DOI, arXiv, PDF, code whenever those links exist. Keep the two current manuscripts and all six journal articles in chronological record lists. Add no figures.

- [ ] **Step 2: Normalize the notes index**

Remove the featured note card and duplicate link to the same article. Render exactly three date-title-summary records. Existing benchmark images are optional note thumbnails and must share one fixed ratio if retained; the index must remain balanced when a record has no image.

- [ ] **Step 3: Normalize the CV**

Remove `.split-grid`, `.cv-sidebar`, card borders, and button pills. Place contact links in the page introduction. Convert education, positions, research experience, selected talks, and references into unframed sections with stable date columns. Preserve every current CV entry and contact destination.

- [ ] **Step 4: Normalize talks and posters**

Keep every talk, date, venue, and PDF destination. Render talk and poster entries as chronological rows with a compact text link labeled `Slides` or `PDF`. Remove poster grids, poster cards, and large rounded buttons.

- [ ] **Step 5: Simplify the 404 page**

Keep one `h1`, one explanatory sentence, and plain links to Home and Publications. Use the shared header and page-introduction layout.

- [ ] **Step 6: Verify page content and structure**

Run:

```bash
python3 scripts/check_site.py
rg -n "notes-layout|note-card|poster-grid|poster-card|split-grid|cv-sidebar|button light|tag teal" docs/research/publications/index.html docs/blog/index.html docs/cv/index.html docs/talks/index.html docs/posters/index.html docs/404.html
git diff --check
```

Expected: the audit reports zero errors, the legacy-class search returns no matches, and `git diff --check` is silent.

- [ ] **Step 7: Commit the supporting pages**

```bash
git add docs/research/publications/index.html docs/blog/index.html docs/cv/index.html docs/talks/index.html docs/posters/index.html docs/404.html
git commit -m "Align supporting pages with dossier layout"
```

### Task 5: Update Articles, Cache Version, And Verify The Complete Site

**Files:**
- Modify: `docs/index.html`
- Modify: `docs/404.html`
- Modify: `docs/blog/index.html`
- Modify: `docs/blog/lmsvd/index.html`
- Modify: `docs/blog/mkdocs/index.html`
- Modify: `docs/blog/llm-agentic-coding-cpp-computational-physics/index.html`
- Modify: `docs/cv/index.html`
- Modify: `docs/posters/index.html`
- Modify: `docs/research/publications/index.html`
- Modify: `docs/talks/index.html`

- [ ] **Step 1: Normalize the repeated header markup**

In all ten HTML pages, replace the `.brand` link contents with this exact markup so no abstract icon or inline SVG remains:

```html
<a class="brand" href="/">Qi Yang</a>
```

- [ ] **Step 2: Set the shared asset version everywhere**

Replace every `site.css?v=20260707b` and `site.js?v=20260707b` reference with `20260709a` in all ten HTML pages.

- [ ] **Step 3: Verify article structure**

Confirm each article page has exactly one `h1`, a readable `.article` main element, meaningful alt text for every image, and no card wrapper around figures. Preserve MathJax script loading on the LMSVD article.

- [ ] **Step 4: Run complete static verification**

Run:

```bash
python3 scripts/check_site.py --asset-version 20260709a
rg -n "brand-mark|<svg" docs -g "*.html"
git diff --check
git status -sb
```

Expected: ten HTML pages checked, zero errors, the SVG/header search returns no matches, no whitespace failures, and only intentional redesign files are modified.

- [ ] **Step 5: Start a local static server**

Run:

```bash
python3 -m http.server 8015 --directory docs
```

If port `8015` is occupied, increment the port once and report the chosen URL.

- [ ] **Step 6: Verify desktop and mobile in the in-app browser**

Inspect these routes at desktop `1280x720` and mobile `390x844`:

```text
/
/research/publications/
/blog/
/cv/
/talks/
/posters/
/blog/llm-agentic-coding-cpp-computational-physics/
```

For each route verify:

```text
document.documentElement.scrollWidth === document.documentElement.clientWidth
[...document.images].every(image => image.complete && image.naturalWidth > 0)
document.querySelectorAll("h1").length === 1
```

On the homepage also verify that Selected publications begins near the first viewport, all three publication records share the same grid structure, and there are no empty image frames. On mobile verify menu open/close state and visible keyboard focus.

- [ ] **Step 7: Commit final article and cache updates**

```bash
git add docs
git commit -m "Finalize academic dossier site"
```

- [ ] **Step 8: Push main and verify deployment**

```bash
git push origin main
```

Wait for the `Deploy static site` workflow to complete, then request the live homepage and `assets/site.css?v=20260709a`. Confirm the live HTML contains `home-intro`, the live CSS contains `--measure: 1080px`, and no browser console errors occur.

## Plan Self-Review

- Spec coverage: global layout, homepage, publications, notes, CV, talks, posters, articles, responsive behavior, accessibility, optional figure contract, static verification, and live deployment each map to an explicit task.
- Image boundary: no task downloads, selects, crops, edits, or installs paper figures.
- Naming consistency: `home-intro`, `record-list`, `record`, `paper-visual`, `tool-index`, and asset version `20260709a` are used consistently across tasks.
- Scope: one static site with one shared visual system; no framework or unrelated content migration is introduced.
- Placeholder scan: no unresolved marker, deferred implementation instruction, or undefined helper is present.
