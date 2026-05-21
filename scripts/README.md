# Scripts

This folder contains small utilities for maintaining the site data.

## Directory Data

The member directory is driven by `directory/members.json`. It is a JSON array where each object represents one member card on the directory page.

Fields used by the site:

- `id`: Internal numeric identifier. Keep it unique.
- `name`: Full name shown on the card.
- `graduationYear`: Year displayed as `Class of <year>`.
- `major`: Freeform academic text. This can include majors, minors, concentrations, or degree program notes.
- `inductionSeason`: Rush or induction term, such as `Spring 2026` or `Fall 2025`.
- `inductionSortKey`: Numeric value used for sorting and filter order. The current convention is `YYYY1` for Spring and `YYYY3` for Fall.
- `linkedin`: Optional LinkedIn profile URL.
- `github`: Optional GitHub profile URL.
- `photo`: Path to the headshot, relative to `directory/index.html`. Example: `../assets/img/directory/grace-morgan.jpg`
- `email`: Email address shown on the card.

Behavior to keep in mind:

- The directory sorts members by `inductionSortKey` descending, then by `name`.
- The season dropdown is generated from `inductionSeason`.
- If `github` is missing, only the LinkedIn button is shown.
- If both `linkedin` and `github` are missing, the profiles area is left blank.
- If `photo` does not load, the page falls back to the shared placeholder image.

## `add_member.py`

Use `add_member.py` to add a new member without editing JSON by hand.

What it does:

- assigns the next available `id`
- extracts `graduationYear` from values like `Spring 2028`
- normalizes `inductionSeason`
- computes `inductionSortKey`
- normalizes LinkedIn and GitHub profile URLs
- copies the headshot into `assets/img/directory/`
- writes the updated list back in sorted order

Basic usage:

```bash
python3 scripts/add_member.py \
  --name "Jane Doe" \
  --graduation "Spring 2028" \
  --major "Mechanical Engineering, Minor in Mathematics" \
  --induction "Fall 2025" \
  --email "janedoe@sandiego.edu" \
  --linkedin "https://www.linkedin.com/in/jane-doe/?utm_source=share" \
  --github "https://github.com/janedoe" \
  --photo-source "Jane Doe Headshot.jpeg"
```

Useful notes:

- `--photo-source` is required.
- If the source image ends in `.jpeg`, the copied filename is converted to `.jpg`.
- If `--photo-name` is omitted, the script creates a lowercase kebab-case filename from the member name.
- `N/A` values for LinkedIn or GitHub are treated as missing.

For the full argument list:

```bash
python3 scripts/add_member.py --help
```
