# -*- coding: utf-8 -*-
"""
Extracts zlib-compressed streams from a Settlers 5 .s5x map archive.

Note:
- This extractor only handles zlib streams found inside the BAF payload.
- file_0.bin / file_1.bin are not directly extracted yet (non-zlib encoding).
"""

import argparse
import json
import pathlib
import zlib
from datetime import datetime

from map_extract_config import EXTRACTED_DIR

DEFAULT_S5X = r"C:\Users\marku\OneDrive\Desktop\Gold edition\extra2\shr\maps\User\(4) EMS Wintersturm.s5x"
DEFAULT_OUT = str(EXTRACTED_DIR)


def find_zlib_streams(blob: bytes):
    streams = []
    for i in range(len(blob) - 2):
        cmf = blob[i]
        flg = blob[i + 1]
        if cmf & 0x0F != 8:
            continue
        if ((cmf << 8) + flg) % 31 != 0:
            continue
        try:
            out = zlib.decompress(blob[i:])
        except Exception:
            continue
        streams.append((i, out))
    return streams


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--s5x", default=DEFAULT_S5X)
    parser.add_argument("--out", default=DEFAULT_OUT)
    args = parser.parse_args()

    s5x_path = pathlib.Path(args.s5x)
    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    data = s5x_path.read_bytes()
    if data[:3] != b"BAF":
        raise SystemExit("Not a BAF/S5X file header")

    baf_len = int.from_bytes(data[28:32], "little")
    baf_start = 32
    baf = data[baf_start:baf_start + baf_len]

    streams = find_zlib_streams(baf)

    report = {
        "s5x": str(s5x_path),
        "extracted_at": datetime.now().isoformat(timespec="seconds"),
        "baf_length": baf_len,
        "streams": [],
    }

    mapdata_bytes = None
    small_xml_bytes = None
    bin_2728 = None
    other_outputs = []

    for offset, out in sorted(streams, key=lambda x: x[0]):
        entry = {
            "offset": offset,
            "length": len(out),
            "head": out[:16].hex(),
        }
        if out.startswith(b"<?xml"):
            entry["type"] = "xml"
            if b"<MapProps" in out and len(out) > 1_000_000:
                entry["role"] = "mapdata.xml"
                mapdata_bytes = out
            else:
                entry["role"] = "small_xml"
                small_xml_bytes = out
        elif len(out) == 2728:
            entry["type"] = "bin"
            entry["role"] = "bin_2728"
            bin_2728 = out
        elif out.startswith(b"--") or out.startswith(b"GFXSetHandler"):
            entry["type"] = "text"
            entry["role"] = "lua_or_script"
            other_outputs.append((offset, out))
        else:
            entry["type"] = "bin"
            entry["role"] = "unknown_bin"
            other_outputs.append((offset, out))

        report["streams"].append(entry)

    if mapdata_bytes is not None:
        (out_dir / "mapdata.xml").write_bytes(mapdata_bytes)
        (out_dir / "block_0.xml").write_bytes(mapdata_bytes)
    if small_xml_bytes is not None:
        (out_dir / "block_1.xml").write_bytes(small_xml_bytes)
        (out_dir / "block_4.xml").write_bytes(small_xml_bytes)
    if bin_2728 is not None:
        (out_dir / "block_5.bin").write_bytes(bin_2728)
        (out_dir / "data_2.bin").write_bytes(bin_2728)

    for offset, out in other_outputs:
        if out.startswith(b"--") or out.startswith(b"GFXSetHandler"):
            name = f"ba_stream_{offset}.lua"
        else:
            name = f"ba_stream_{offset}.bin"
        (out_dir / name).write_bytes(out)

    (out_dir / "s5x_extract_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )

    print(f"Extracted {len(streams)} zlib streams from {s5x_path}")
    print(f"mapdata.xml: {'yes' if mapdata_bytes else 'no'}")
    print(f"small xml: {'yes' if small_xml_bytes else 'no'}")
    print(f"bin_2728: {'yes' if bin_2728 else 'no'}")
    print(f"Report: {out_dir / 's5x_extract_report.json'}")


if __name__ == "__main__":
    main()
