#!/usr/bin/env python3
"""Add a member to directory/members.json and optionally copy the headshot."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parent.parent
MEMBERS_PATH = REPO_ROOT / "directory" / "members.json"
DIRECTORY_IMG_PATH = REPO_ROOT / "assets" / "img" / "directory"


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value.lower()).strip("-")
    if not slug:
        raise ValueError("Could not derive a filename slug from the provided name.")
    return slug


def parse_graduation_year(value: str) -> int:
    match = re.search(r"(20\d{2})", value)
    if not match:
        raise ValueError(f"Could not find a graduation year in: {value}")
    return int(match.group(1))


def normalize_induction_season(value: str) -> str:
    cleaned = value.strip()
    cleaned = re.sub(r"\bof\b", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    match = re.fullmatch(r"(Spring|Fall)\s+(20\d{2})", cleaned, flags=re.IGNORECASE)
    if not match:
        raise ValueError(
            "Induction season must look like 'Spring 2026' or 'Fall 2025'."
        )

    season = match.group(1).capitalize()
    year = match.group(2)
    return f"{season} {year}"


def induction_sort_key(induction_season: str) -> int:
    season, year = induction_season.split()
    season_code = {"Spring": 1, "Fall": 3}[season]
    return int(f"{year}{season_code}")


def normalize_linkedin(url: str | None) -> str | None:
    if not url:
        return None

    cleaned = url.strip()
    if not cleaned or cleaned.upper() == "N/A":
        return None

    parsed = urlparse(cleaned)
    if not parsed.scheme:
        cleaned = f"https://{cleaned.lstrip('/')}"
        parsed = urlparse(cleaned)

    path = parsed.path.rstrip("/")
    if not path.startswith("/in/"):
        return cleaned.rstrip("/")

    return f"https://www.linkedin.com{path}"


def normalize_github(url: str | None) -> str | None:
    if not url:
        return None

    cleaned = url.strip()
    if not cleaned or cleaned.upper() == "N/A":
        return None

    parsed = urlparse(cleaned)
    if not parsed.scheme:
        cleaned = f"https://{cleaned.lstrip('/')}"
        parsed = urlparse(cleaned)

    path = parsed.path.rstrip("/")
    if not path:
        return cleaned.rstrip("/")

    return f"https://github.com{path}"


def load_members() -> list[dict]:
    with MEMBERS_PATH.open("r", encoding="utf-8") as members_file:
        return json.load(members_file)


def save_members(members: list[dict]) -> None:
    with MEMBERS_PATH.open("w", encoding="utf-8") as members_file:
        json.dump(members, members_file, indent=2, ensure_ascii=False)
        members_file.write("\n")


def copy_photo(source: Path, member_name: str, photo_name: str | None) -> str:
    if not source.exists():
        raise FileNotFoundError(f"Photo source does not exist: {source}")

    extension = source.suffix.lower()
    if extension == ".jpeg":
        extension = ".jpg"
    if not extension:
        raise ValueError("Photo source must have a file extension.")

    destination_name = photo_name or f"{slugify(member_name)}{extension}"
    destination = DIRECTORY_IMG_PATH / destination_name
    shutil.copy2(source, destination)
    return f"../assets/img/directory/{destination_name}"


def build_photo_path(source: Path, member_name: str, photo_name: str | None) -> str:
    extension = source.suffix.lower()
    if extension == ".jpeg":
        extension = ".jpg"
    if not extension:
        raise ValueError("Photo source must have a file extension.")

    destination_name = photo_name or f"{slugify(member_name)}{extension}"
    return f"../assets/img/directory/{destination_name}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Add a directory member and optionally copy the headshot."
    )
    parser.add_argument("--name", required=True, help="Full name")
    parser.add_argument(
        "--graduation",
        required=True,
        help="Graduation text such as 'Spring 2028' or '2028'",
    )
    parser.add_argument(
        "--major",
        required=True,
        help="Major/minor/degree text as it should appear in the directory",
    )
    parser.add_argument(
        "--induction",
        required=True,
        help="Induction season such as 'Fall 2025' or 'Fall of 2025'",
    )
    parser.add_argument("--email", required=True, help="Email address")
    parser.add_argument("--linkedin", help="LinkedIn profile URL")
    parser.add_argument("--github", help="GitHub profile URL")
    parser.add_argument(
        "--photo-source",
        help="Path to the source headshot file to copy into assets/img/directory",
    )
    parser.add_argument(
        "--photo-name",
        help="Optional destination filename, e.g. 'grace-morgan.jpg'",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the member JSON without writing files",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    members = load_members()
    existing_names = {member["name"].casefold() for member in members}
    if args.name.casefold() in existing_names:
        print(f"Member already exists: {args.name}", file=sys.stderr)
        return 1

    normalized_induction = normalize_induction_season(args.induction)

    member = {
        "id": max(member["id"] for member in members) + 1,
        "name": args.name.strip(),
        "graduationYear": parse_graduation_year(args.graduation),
        "major": args.major.strip(),
        "inductionSeason": normalized_induction,
        "inductionSortKey": induction_sort_key(normalized_induction),
        "linkedin": normalize_linkedin(args.linkedin),
        "email": args.email.strip(),
    }

    github = normalize_github(args.github)
    if github:
        member["github"] = github

    if args.dry_run:
        if not args.photo_source:
            raise ValueError("--photo-source is required when using --dry-run.")
        member["photo"] = build_photo_path(
            Path(args.photo_source).expanduser(),
            member_name=member["name"],
            photo_name=args.photo_name,
        )
        print(json.dumps(member, indent=2, ensure_ascii=False))
        return 0

    if not args.photo_source:
        raise ValueError("--photo-source is required.")

    member["photo"] = copy_photo(
        Path(args.photo_source).expanduser(),
        member_name=member["name"],
        photo_name=args.photo_name,
    )

    members.append(member)
    members.sort(
        key=lambda item: (-item["inductionSortKey"], item["name"].casefold())
    )
    save_members(members)

    print(f"Added {member['name']} to {MEMBERS_PATH}.")
    print(f"Photo: {member['photo']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
