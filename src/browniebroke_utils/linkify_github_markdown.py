"""
Script to add GitHub URLs to release notes.

This script:
1. Converts @username mentions to markdown links pointing to their GitHub profiles
2. Converts pull request URLs to markdown links in format [#NNNN](url)

Existing links are preserved and not modified.
"""

import argparse
import re
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> None:
    """Main function to process the release notes file."""
    parser = argparse.ArgumentParser(
        description="Add GitHub URLs to release notes content",
    )
    parser.add_argument("input_file", help="Input file path")
    parser.add_argument("output_file", help="Output file path")

    args = parser.parse_args(argv)

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    content = input_path.read_text()
    content = add_pull_request_links(content)
    content = add_github_profile_links(content)

    Path(args.output_file).write_text(content)
    print(f"Successfully processed {input_path} -> {args.output_file}")


def get_link_ranges(text: str) -> list[tuple[int, int]]:
    """Get character ranges of existing markdown links."""
    pattern = r"\[[^]]+\]\([^)]+\)"
    return [(m.start(), m.end()) for m in re.finditer(pattern, text)]


def add_github_profile_links(content: str) -> str:
    """Convert @username mentions to GitHub profile links."""
    link_ranges = get_link_ranges(content)

    def replace(match: re.Match) -> str:
        start, end = match.span()
        username = match.group(1)

        # Skip if inside existing link or is a decorator like @versioning_class()
        is_inside_link = any(s <= start < e for s, e in link_ranges)
        is_decorator = end < len(content) and content[end] == "("

        if is_inside_link or is_decorator:
            return match.group(0)

        url_username = username.replace("[bot]", "[bot]")
        return f"[@{username}](https://github.com/{url_username})"

    return re.sub(r"@([\w-]+(?:\[bot\])?)", replace, content)


def add_pull_request_links(content: str) -> str:
    """Convert pull request URLs to markdown links in format [#NNNN](url)."""
    link_ranges = get_link_ranges(content)

    def replace(match: re.Match) -> str:
        if any(s <= match.start() < e for s, e in link_ranges):
            return match.group(0)
        return f"[#{match.group(3)}]({match.group(0)})"

    return re.sub(
        r"https://github\.com/([\w\-]+)/([\w\-]+)/pull/(\d+)", replace, content
    )
