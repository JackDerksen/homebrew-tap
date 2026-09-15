"""Advance the formula to GitHub's latest stable Redox release."""

import hashlib
import json
import os
from pathlib import Path
import re
import urllib.request


def stable_version(tag):
    match = re.fullmatch(r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", tag)
    if not match:
        raise ValueError(f"expected a stable release tag, got {tag!r}")
    return tuple(map(int, match.groups()))


def update_formula():
    headers = {"User-Agent": "redox-homebrew-tap", "Accept": "application/vnd.github+json"}
    if token := os.environ.get("GH_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(
        "https://api.github.com/repos/JackDerksen/redox/releases/latest", headers=headers
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        release = json.load(response)
    if release["draft"] or release["prerelease"]:
        raise ValueError("latest release must be published and stable")
    tag = release["tag_name"]
    version = stable_version(tag)
    formula_path = Path("Formula/redox.rb")
    formula = formula_path.read_text()
    current = re.search(r'/refs/tags/(v[0-9]+\.[0-9]+\.[0-9]+)\.tar\.gz"', formula)
    if not current:
        raise ValueError("cannot find the current formula version")
    if version <= stable_version(current[1]):
        print(f"Formula is already at {current[1]} or newer than {tag}")
        return

    url = f"https://github.com/JackDerksen/redox/archive/refs/tags/{tag}.tar.gz"
    checksum = hashlib.sha256()
    # Download the archive anonymously; the API token must not be sent to redirects.
    with urllib.request.urlopen(url, timeout=60) as archive:
        while chunk := archive.read(1024 * 1024):
            checksum.update(chunk)
    formula, url_count = re.subn(r'^  url ".*"$', f'  url "{url}"', formula, flags=re.MULTILINE)
    formula, checksum_count = re.subn(
        r'^  sha256 "[0-9a-f]{64}"$', f'  sha256 "{checksum.hexdigest()}"', formula, flags=re.MULTILINE
    )
    if (url_count, checksum_count) != (1, 1):
        raise ValueError("expected exactly one source URL and checksum")
    formula_path.write_text(formula)
    print(f"Updated Redox to {tag}")


if __name__ == "__main__":
    update_formula()
