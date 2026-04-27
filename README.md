# USD Theta Tau Website

Static website for the USD Theta Tau chapter. The site is plain HTML, CSS, and JavaScript with no build step.

## Structure
- `index.html`: home page
- `directory/index.html`: member directory
- `recruitment/index.html`: recruitment page
- `faq/index.html`: FAQ page
- `faq/faq.json`: FAQ content
- `directory/members.json`: member directory data
- `assets/css/`: shared and page-specific styles
- `assets/js/`: page scripts
- `assets/img/`: images grouped by area

## Current pages
- Home
- Brothers directory
- Recruitment
- FAQ

The old exec board page has been removed from this repo.

## Directory
The directory page is driven by `directory/members.json` and rendered by `assets/js/directory.js`.

Each member entry currently includes:
- `name`
- `photo`
- `linkedin`
- `github` when available
- `email`
- `major`
- `graduationYear`
- `inductionSeason`
- `inductionSortKey`

Directory behavior:
- Members display as responsive cards
- The induction season dropdown filters to a specific class such as `Fall 2025` or `Spring 2024`
- Cards are otherwise shown in most-recent induction-season-first order

## Images
Image folders in active use:
- `assets/img/home/`: home page images and company logos
- `assets/img/directory/`: local member headshots
- `assets/img/shared/`: shared assets like `icon.ico` and the profile placeholder

Directory headshots:
- Are stored locally in `assets/img/directory/`
- Use lowercase kebab-case filenames such as `grace-morgan.jpg`
- Have been resized to web-friendly dimensions

## Updating content
Home page:
- Edit `index.html`

Directory members:
- Edit `directory/members.json`
- Keep image paths relative to `directory/index.html`, for example `../assets/img/directory/grace-morgan.jpg`
- Keep induction seasons consistent, for example `Fall 2025`

FAQ:
- Edit `faq/faq.json`

Recruitment:
- Edit `recruitment/index.html`

## Local preview
Because the directory and FAQ pages fetch JSON, use a local HTTP server instead of opening the files directly in the browser.

Example:

```bash
python3 -m http.server 8000
```

Then open:
- `http://localhost:8000/`
- `http://localhost:8000/directory/`
- `http://localhost:8000/recruitment/`
- `http://localhost:8000/faq/`

## Editing guidelines
- Keep filenames lowercase and avoid spaces for repo assets
- Double-check relative paths when moving files
- Put shared images in `assets/img/shared/`
- Put directory headshots in `assets/img/directory/`
- Validate JSON after editing structured data files

Useful checks:

```bash
python3 -m json.tool directory/members.json >/dev/null
python3 -m json.tool faq/faq.json >/dev/null
node --check assets/js/directory.js
node --check assets/js/faq.js
```

## Deployment note
This repo is configured for GitHub Pages and includes `CNAME` for the custom domain.
