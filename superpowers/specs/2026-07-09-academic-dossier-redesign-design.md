# Academic Dossier Site Redesign

Date: 2026-07-09

## Objective

Redesign Qi Yang's complete academic website as a restrained institutional research dossier. The site must present a computational physicist's work clearly and credibly without looking like a generic portfolio, a software landing page, or a collection of mismatched cards.

The site's long-term visual identity will come from selected figures from Qi Yang's papers. Figure selection is outside this implementation and remains under the user's control.

## Design Principles

1. Information hierarchy comes before decoration.
2. Publications are the primary content and appear immediately after a compact identity block.
3. Repeated items use consistent dimensions, spacing, and metadata placement.
4. Cards are avoided unless an item genuinely needs a framed visual boundary.
5. The palette is neutral white and charcoal with one restrained research-blue link color.
6. Scientific figures are content, not background decoration.
7. The design must remain complete and intentional when no paper figures are installed.

## Visual System

### Color

- Page: white
- Secondary surface: a very light neutral gray used sparingly
- Primary text: near-black charcoal
- Secondary text: neutral gray
- Rules: cool light gray
- Accent: one muted blue for links, active navigation, and focus indicators

No multicolor branding, gradients, glowing effects, glass surfaces, decorative blobs, or dark technology theme will be used.

### Typography

- Navigation, identity, metadata, body copy, publication titles, and note titles use one quiet humanist sans-serif stack.
- Hierarchy comes from size, weight, spacing, and rules rather than mixing unrelated type families.
- Type sizes are based on content role, not viewport width. The name is prominent but not hero-scale.
- Metadata uses tabular numerals where available and remains readable rather than decorative.

### Geometry

- Main content width: approximately 1040-1120 px.
- Border radius: zero to four pixels, used only where needed.
- Dividers establish grouping; shadows are not used.
- Buttons are reserved for clear commands. Most destinations are ordinary text links.
- Topic chips and oversized pill controls are removed.

## Global Structure

The complete site shares one header, navigation system, content width, typography scale, footer, and responsive behavior.

The desktop header is compact and contains the Qi Yang wordmark plus Home, Publications, Talks, Posters, Notes, and CV links. The mobile header uses an accessible menu button and a stable single-column menu.

The footer contains affiliation, email, GitHub, and Google Scholar links without promotional copy.

## Homepage

### Identity Block

The first section is compact enough that selected publications begin in or near the first viewport on common laptop screens.

It contains:

- Qi Yang
- Postdoctoral researcher at the University of Amsterdam
- A concise research statement focused on tensor-network algorithms, iPEPS, long-range interactions, and scientific computing
- Inline links to Google Scholar, GitHub, email, and CV
- A short plain-text research-area line rather than topic pills

There is no generic avatar, abstract brand icon, benchmark card, or separate Current focus panel.

### Selected Publications

The three most relevant recent publications appear as equal-structure rows. Every row contains:

- Year and publication status or venue
- Title
- Authors
- One concise contribution statement
- DOI, arXiv, PDF, and code links when available

Rows use consistent spacing and metadata placement. No publication is visually enlarged merely because it is newer.

### Optional Paper Figure Contract

Paper figures are optional assets selected and supplied by the user.

Each publication row may reference one image using a stable asset path and descriptive alt text. When an image is present, the row switches to a fixed media-and-text grid with a shared image ratio. When no image is configured, the row becomes a full-width text row. Empty frames, broken image icons, and placeholder graphics are forbidden.

Figure presentation rules:

- The same aspect ratio and maximum dimensions are used for all publication thumbnails.
- Images use `object-fit: contain` by default so scientific axes, labels, and diagrams are not cropped.
- A figure may link to its paper, but it does not replace the paper title or metadata.
- Figure captions are short and identify the scientific content, not the visual style.

### Secondary Homepage Content

Code and tools appear as a compact text index with repository name, one-line purpose, and source link. Notes appear as date-title-summary rows. These sections use the same divider rhythm as publications and do not become independent card grids.

## Subpages

### Publications

The full publication page uses a chronological list grouped by year. Journal and preprint metadata remain close to citation form. Links are explicit and consistently ordered. The page supports the same optional figure contract but does not require figures for every publication.

### Notes

The notes index uses a reading-oriented list with date, title, summary, and optional thumbnail. Article pages use a comfortable prose width, clear heading hierarchy, reliable MathJax rendering, and figures that remain legible on mobile.

### CV

The CV is organized as an unframed timeline or sectioned document. Dates occupy a stable column on desktop and move above entries on mobile. Repeated card containers are removed.

### Talks And Posters

Talks and posters use compact chronological rows. PDF links are visually consistent. Poster thumbnails may be added later but are not required for the layout to look complete.

## Responsive Behavior

- Desktop layouts use a single dominant reading column with small metadata columns where useful.
- At tablet widths, metadata columns narrow before content stacks.
- At mobile widths, every section becomes one column, publication metadata moves above the title, and optional figures remain full-width within their row.
- No horizontal scrolling is allowed at 320 px and above.
- Long paper titles and URLs must wrap without clipping.
- Fixed-format images use stable aspect ratios to prevent layout shift.

## Accessibility And Interaction

- Semantic landmarks and heading order are preserved.
- Keyboard focus is visible on every interactive element.
- Link color meets WCAG AA contrast against the page background.
- The navigation toggle exposes its expanded state.
- Motion is limited to subtle hover and menu transitions and respects `prefers-reduced-motion`.
- Images require meaningful alt text; decorative images use empty alt text.

## Implementation Boundaries

- Keep the site static and dependency-light.
- Preserve all current published content and valid external destinations.
- Use shared CSS and JavaScript rather than page-specific visual systems.
- Remove obsolete homepage-only styling and unused animation code where it no longer serves the design.
- Do not select, crop, or install paper highlight images during this implementation.
- Do not introduce a framework unless the existing static structure makes a requirement impossible.

## Verification

Before deployment:

1. Validate internal links and local assets across every generated HTML page.
2. Run a markup or structural sanity check and `git diff --check`.
3. Inspect the homepage, publications, notes, CV, talks, and posters pages in a browser.
4. Check desktop and 390 px mobile layouts for overflow, clipping, broken images, and inconsistent repeated-item dimensions.
5. Confirm keyboard navigation, focus visibility, mobile menu behavior, and reduced-motion behavior.
6. Confirm the site remains visually complete with no paper highlight images installed.
7. After pushing, verify the GitHub Pages deployment and inspect the live homepage.

## Success Criteria

- The site reads first as an academic research record and second as a personal website.
- The homepage reaches selected publications quickly.
- Repeated content has a consistent visual rhythm with no arbitrary large and small cards.
- The design has no dependency on unselected paper images.
- Adding user-selected figures later increases identity without requiring another layout redesign.
- All current content remains reachable on desktop and mobile.
