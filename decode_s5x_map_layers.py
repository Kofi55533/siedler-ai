#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Decode map layers from a Settlers 5 .s5x archive.

Extracts zlib streams with magic 0x191A370D and decodes:
- Height map (u16, size w2 x w2)
- Low-res terrain/type map (u8, size N x N) from the tail payload

Outputs .npy files and a JSON report into the extract directory.
"""

import argparse
import json
import pathlib
import struct
import zlib

import numpy as np

from map_extract_config import EXTRACTED_DIR

DEFAULT_S5X = r"C:\Users\marku\OneDrive\Desktop\Gold edition\extra2\shr\maps\User\(4) EMS Wintersturm.s5x"

MAGIC = 0x191A370D


def _find_zlib_streams(blob: bytes):
    """Return list of (offset, decompressed_bytes) for zlib streams."""
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


def _find_raw_magic_streams(blob: bytes):
    """Find raw (uncompressed) streams by MAGIC header inside a blob."""
    magic_bytes = struct.pack("<I", MAGIC)
    offsets = []
    start = 0
    while True:
        idx = blob.find(magic_bytes, start)
        if idx == -1:
            break
        offsets.append(idx)
        start = idx + 1

    streams = []
    for idx in offsets:
        if idx + 8 > len(blob):
            continue
        try:
            header = struct.unpack("<12I", blob[idx:idx + 48])
        except Exception:
            continue
        # Stream length stored in header[1] (+8 bytes header)
        length = header[1] + 8
        if idx + length > len(blob):
            continue
        streams.append((idx, blob[idx:idx + length]))
    return streams


def _parse_height_and_tail(stream: bytes):
    """Parse a 0x191A370D stream into height map + low-res terrain map."""
    if len(stream) < 64:
        return None

    header = struct.unpack("<12I", stream[:48])
    magic = header[0]
    if magic != MAGIC:
        return None

    w1, h1, w2, h2 = header[8], header[9], header[10], header[11]
    if any(v == 0x80808080 for v in (w1, h1, w2, h2)):
        # Constant layer stream (e.g., vertex colors); skip for now.
        return None

    if w2 != h2:
        raise ValueError(f"Non-square height map: {w2}x{h2}")

    # Height map directly after 48-byte header
    height_count = w2 * w2
    height_bytes = height_count * 2
    height_start = 48
    height_end = height_start + height_bytes
    if height_end > len(stream):
        raise ValueError("Height map exceeds stream length")

    height = np.frombuffer(stream[height_start:height_end], dtype=np.uint16).copy()
    height = height.reshape((w2, w2))

    # Tail section
    tail = stream[height_end:]
    if len(tail) < 40:
        raise ValueError("Tail too small for header+subheader")

    tail_header = struct.unpack("<4I", tail[:16])
    tail_magic_1, tail_magic_2, tail_len, tail_version = tail_header
    if tail_len != len(tail) - 16:
        # Keep going but record mismatch
        tail_len = len(tail) - 16

    payload = tail[16:]
    sub = struct.unpack("<6I", payload[:24])
    a1, a2, b1, b2, const1, const2 = sub
    if b1 != b2:
        raise ValueError(f"Low-res grid not square: {b1}x{b2}")

    grid_len = b1 * b1 * 4
    grid_start = 24
    grid_end = grid_start + grid_len
    if grid_end > len(payload):
        raise ValueError("Low-res grid exceeds tail payload length")

    grid_u32 = np.frombuffer(payload[grid_start:grid_end], dtype=np.uint32).copy()
    grid_u32 = grid_u32.reshape((b1, b1))
    # Use first byte as terrain/type id
    grid_u8 = (grid_u32 & 0xFF).astype(np.uint8)

    return {
        "w1": w1,
        "h1": h1,
        "w2": w2,
        "h2": h2,
        "height": height,
        "tail_header": {
            "magic_1": tail_magic_1,
            "magic_2": tail_magic_2,
            "len": tail_len,
            "version": tail_version,
        },
        "lowres": {
            "a1": a1,
            "a2": a2,
            "b1": b1,
            "b2": b2,
            "const1": const1,
            "const2": const2,
            "grid_u32": grid_u32,
            "grid_u8": grid_u8,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--s5x", default=DEFAULT_S5X)
    parser.add_argument("--out", default=str(EXTRACTED_DIR))
    parser.add_argument("--dump-raw", action="store_true")
    args = parser.parse_args()

    s5x_path = pathlib.Path(args.s5x)
    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    data = s5x_path.read_bytes()
    if data[:3] != b"BAF":
        raise SystemExit("Not a BAF/S5X file header")

    baf_len = struct.unpack("<I", data[28:32])[0]
    baf = data[32:32 + baf_len]

    streams = _find_zlib_streams(baf)
    decoded = None
    for offset, stream in streams:
        if len(stream) < 4:
            continue
        if struct.unpack("<I", stream[:4])[0] != MAGIC:
            continue
        parsed = _parse_height_and_tail(stream)
        if parsed is not None:
            decoded = parsed
            decoded["stream_offset"] = offset
            decoded["stream_len"] = len(stream)
            break

    raw_streams = None
    if decoded is None:
        # Try raw (uncompressed) streams inside BAF (extra1 maps)
        raw_streams = _find_raw_magic_streams(baf)
        for offset, stream in raw_streams:
            parsed = _parse_height_and_tail(stream)
            if parsed is not None:
                decoded = parsed
                decoded["stream_offset"] = offset
                decoded["stream_len"] = len(stream)
                break

        if decoded is None:
            raise SystemExit("No decodable 0x191A370D stream found")

    height = decoded["height"]
    lowres_u8 = decoded["lowres"]["grid_u8"]
    lowres_u32 = decoded["lowres"]["grid_u32"]

    # Save outputs
    height_path = out_dir / f"height_map_{height.shape[0]}.npy"
    lowres_u8_path = out_dir / f"terrain_lowres_{lowres_u8.shape[0]}.npy"
    lowres_u32_path = out_dir / f"terrain_lowres_{lowres_u8.shape[0]}_u32.npy"
    np.save(height_path, height)
    np.save(lowres_u8_path, lowres_u8)
    np.save(lowres_u32_path, lowres_u32)

    if args.dump_raw:
        # Write the decoded stream (always)
        raw_path = out_dir / f"raw_stream_{decoded['stream_offset']}.bin"
        raw_path.write_bytes(
            baf[decoded["stream_offset"]:decoded["stream_offset"] + decoded["stream_len"]]
        )
        # If we had raw stream list, dump all of them for completeness
        if raw_streams:
            for offset, stream in raw_streams:
                out_path = out_dir / f"raw_stream_{offset}.bin"
                if out_path.exists():
                    continue
                out_path.write_bytes(stream)

    report = {
        "s5x": str(s5x_path),
        "stream_offset": decoded["stream_offset"],
        "stream_len": decoded["stream_len"],
        "height_map": {
            "shape": list(height.shape),
            "min": int(height.min()),
            "max": int(height.max()),
        },
        "lowres": {
            "shape": list(lowres_u8.shape),
            "unique_values": int(len(np.unique(lowres_u8))),
        },
        "tail_header": decoded["tail_header"],
        "lowres_header": {
            "a1": decoded["lowres"]["a1"],
            "a2": decoded["lowres"]["a2"],
            "b1": decoded["lowres"]["b1"],
            "b2": decoded["lowres"]["b2"],
            "const1": decoded["lowres"]["const1"],
            "const2": decoded["lowres"]["const2"],
        },
    }

    report_path = out_dir / "decoded_map_layers_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("Decoded layers:")
    print(f"  height map: {height_path}")
    print(f"  lowres terrain (u8): {lowres_u8_path}")
    print(f"  lowres terrain (u32): {lowres_u32_path}")
    print(f"  report: {report_path}")


if __name__ == "__main__":
    main()
