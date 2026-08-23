# trace-ai-labs.github.io

The TRACE AI Labs homepage: who we are, what we work on, and our papers.

Live at **https://trace-ai-labs.github.io**.

## Structure

- `index.html` — the whole site. Single file, no build step, no dependencies. Styles are
  inline in a `<style>` block at the top; light and dark themes follow the visitor's system
  setting via `prefers-color-scheme`.
- `assets/` — one header figure per paper (PNG, taken from each paper's own figure 1).
- `.nojekyll` — serve the files as-is instead of running them through Jekyll.

## Adding a paper

Copy an existing `<article class="paper">` block in `index.html` and fill in the title,
authors, venue, description, figure, links, and BibTeX. Newest paper goes at the top of its
group. Drop the figure in `assets/` — line drawings on a white background work best, since
the figure plate stays light in both themes. Keep images under a few hundred KB; downscale
to ~1200px wide if needed.

## Preview locally

```sh
python -m http.server 8000
# then open http://localhost:8000
```

## Related sites

- Per-paper sites: [`pact-website`](https://github.com/trace-ai-labs/pact-website) → https://trace-ai-labs.github.io/pact/,
  [`ai-incentives`](https://github.com/trace-ai-labs/ai-incentives) → https://trace-ai-labs.github.io/ai-incentives/
- The org profile README lives in [`trace-ai-labs/.github`](https://github.com/trace-ai-labs/.github);
  keep its paper list in sync with this page.
