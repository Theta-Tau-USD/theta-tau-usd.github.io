# USD Theta Tau Website

Welcome! This is the static website for the USD Theta Tau chapter. It’s all HTML/CSS/JS and doesn’t need a build step.

## How the site works
- Pages are plain HTML files: `index.html`, `recruitment/index.html`, `exec-board/index.html`.
- Shared styles live in `assets/css/` and shared scripts in `assets/js/`.
- Images live in `assets/img/` and are organized by page:
  - `assets/img/home/` (home page photos + company logos)
  - `assets/img/exec-board/` (exec board photos/placeholders)
  - `assets/img/recruitment/` (recruitment-specific images; empty for now)
  - `assets/img/shared/` (shared assets like `icon.ico`)
- The Exec Board page loads data from `exec-board/exec-board.json` via `assets/js/exec-board.js` and renders cards on page load.

## Local preview
You can open any HTML file directly in a browser:
- `index.html`
- `recruitment/index.html`
- `exec-board/index.html`

## Content updates
- Home page copy and images: edit `index.html`.
- Recruitment page copy: edit `recruitment/index.html`.
- Exec board members: edit `exec-board/exec-board.json`.
  - Each entry needs: `position`, `name`, `major`, `bio`, `photo`.
  - Example photo path: `../assets/img/exec-board/exec-placeholder.svg`.

## Image guidelines
- Put page-specific images under the matching folder in `assets/img/`.
- Update HTML/CSS paths accordingly (paths are relative to the file).
- Keep filenames lowercase and avoid spaces.

## Contributing
Thanks for helping out! A typical workflow:
1) Create a new branch.
2) Make your changes.
3) Open the pages in a browser and sanity-check the layout.
4) Open a pull request with a short summary (screenshots appreciated if the UI changed).

## Common pitfalls
- Broken relative paths after moving files: double-check `../` levels.
- Mixing shared and page-specific images: keep them in their respective folders.
