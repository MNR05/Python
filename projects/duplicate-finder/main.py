"""Find duplicate file contents without deleting or modifying any files."""
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_duplicates(folder: str | Path) -> list[list[str]]:
    root = Path(folder).resolve()
    if not root.is_dir():
        raise ValueError(f"Not a directory: {root}")
    by_size: dict[int, list[Path]] = defaultdict(list)
    for path in root.rglob("*"):
        if path.is_file() and not path.is_symlink():
            try:
                by_size[path.stat().st_size].append(path)
            except OSError:
                continue
    result = []
    for candidates in by_size.values():
        if len(candidates) < 2:
            continue
        hashes: dict[str, list[str]] = defaultdict(list)
        for path in candidates:
            try:
                hashes[sha256_file(path)].append(str(path.relative_to(root)))
            except OSError:
                continue
        result.extend(sorted(group) for group in hashes.values() if len(group) > 1)
    return sorted(result)


def main() -> None:
    parser = argparse.ArgumentParser(description="List exact duplicate files (read-only).")
    parser.add_argument("folder")
    args = parser.parse_args()
    print(json.dumps({"duplicate_groups": find_duplicates(args.folder)}, indent=2))


if __name__ == "__main__":
    main()
