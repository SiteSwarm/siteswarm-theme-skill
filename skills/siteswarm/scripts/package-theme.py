#!/usr/bin/env python3
"""Package SiteSwarm source paths into a flat ZIP."""

import argparse
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

SOURCE_DIRS = {
    "assets", "config", "data", "dataset_templates", "dropins", "layout",
    "locales", "page_templates", "sections", "snippets", "templates",
}
ROOT_FILES = {
    "siteswarm.json", "hostnet.json", "thumbnail.png", "thumbnail.jpg",
    "thumbnail.jpeg", "thumbnail.webp",
}
PRIVATE_SUFFIXES = {".key", ".pem", ".p12", ".pfx"}


def theme_files(root):
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if relative.parts[0] not in SOURCE_DIRS and relative.as_posix() not in ROOT_FILES:
            continue
        if any(part.startswith(".") or part == "node_modules" for part in relative.parts):
            continue
        if path.suffix.lower() in PRIVATE_SUFFIXES:
            continue
        if path.is_symlink():
            raise ValueError(f"Replace the symlink with a regular theme file: {relative}")
        if path.is_file():
            yield path, relative.as_posix()


def package(root, output):
    root = root.resolve(strict=True)
    if output.is_symlink():
        raise ValueError("Choose a ZIP destination that is not a symlink.")
    output = output.resolve()
    if output.suffix.lower() != ".zip" or output.is_relative_to(root):
        raise ValueError("Choose a .zip destination outside the theme directory.")
    files = list(theme_files(root))
    if not {"layout/theme.liquid", "layout/theme.html"}.intersection(name for _, name in files):
        raise ValueError("Missing layout/theme.liquid or layout/theme.html.")
    with output.open("xb") as target:
        try:
            with ZipFile(target, "w", compression=ZIP_DEFLATED) as archive:
                for path, name in files:
                    archive.write(path, name)
        except BaseException:
            target.close()
            output.unlink()
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("theme", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        package(args.theme, args.output)
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    sys.exit(main())
