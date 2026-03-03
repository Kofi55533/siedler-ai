# -*- coding: utf-8 -*-
"""
Query the offline engine value dump produced by dump_all_original_values.py.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


DEFAULT_DUMP = Path("config/all_original_values.jsonl")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dump", default=str(DEFAULT_DUMP))
    parser.add_argument("--pattern", required=True, help="Regex pattern to search")
    parser.add_argument(
        "--field",
        default="any",
        choices=["any", "file", "path", "value"],
        help="Field to search in",
    )
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()

    dump_path = Path(args.dump)
    if not dump_path.exists():
        raise SystemExit(f"Dump not found: {dump_path}")

    rx = re.compile(args.pattern, re.IGNORECASE)
    found = 0

    with dump_path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            try:
                item = json.loads(line)
            except Exception:
                continue

            file_v = str(item.get("file", ""))
            path_v = str(item.get("path", ""))
            value_v = str(item.get("value", ""))

            if args.field == "file":
                hit = rx.search(file_v) is not None
            elif args.field == "path":
                hit = rx.search(path_v) is not None
            elif args.field == "value":
                hit = rx.search(value_v) is not None
            else:
                hit = (
                    rx.search(file_v) is not None
                    or rx.search(path_v) is not None
                    or rx.search(value_v) is not None
                )

            if not hit:
                continue

            found += 1
            print(
                json.dumps(
                    {
                        "file": item.get("file"),
                        "path": item.get("path"),
                        "kind": item.get("kind"),
                        "key": item.get("key"),
                        "value": item.get("value"),
                    },
                    ensure_ascii=False,
                )
            )

            if found >= args.limit:
                break

    print(f"matches={found}")


if __name__ == "__main__":
    main()
