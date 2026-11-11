#!/usr/bin/env python3
"""Derive all WKAite Remote packaging icons from the approved square cover."""

from __future__ import annotations

import argparse
import base64
import io
import struct
from pathlib import Path

from PIL import Image, ImageOps


ICO_SIZES = (16, 24, 32, 48, 64, 128, 256)
TRAY_SIZES = (16, 24, 32, 48)
ANDROID = {
    "mdpi": (48, 108, 24),
    "hdpi": (72, 162, 36),
    "xhdpi": (96, 216, 48),
    "xxhdpi": (144, 324, 72),
    "xxxhdpi": (192, 432, 96),
}
IOS = {
    "Icon-App-20x20@1x.png": 20,
    "Icon-App-20x20@2x.png": 40,
    "Icon-App-20x20@3x.png": 60,
    "Icon-App-29x29@1x.png": 29,
    "Icon-App-29x29@2x.png": 58,
    "Icon-App-29x29@3x.png": 87,
    "Icon-App-40x40@1x.png": 40,
    "Icon-App-40x40@2x.png": 80,
    "Icon-App-40x40@3x.png": 120,
    "Icon-App-60x60@2x.png": 120,
    "Icon-App-60x60@3x.png": 180,
    "Icon-App-76x76@1x.png": 76,
    "Icon-App-76x76@2x.png": 152,
    "Icon-App-83.5x83.5@2x.png": 167,
    "Icon-App-1024x1024@1x.png": 1024,
}
ICNS_CHUNKS = (
    (b"icp4", 16),
    (b"icp5", 32),
    (b"icp6", 64),
    (b"ic07", 128),
    (b"ic08", 256),
    (b"ic09", 512),
    (b"ic10", 1024),
)


def square(image: Image.Image, size: int) -> Image.Image:
    return ImageOps.fit(image.convert("RGB"), (size, size), method=Image.Resampling.LANCZOS)


def write_png(image: Image.Image, path: Path, size: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    square(image, size).save(path, format="PNG", optimize=True)


def write_ico(image: Image.Image, path: Path, sizes: tuple[int, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    square(image, max(sizes)).save(path, format="ICO", sizes=[(s, s) for s in sizes])


def png_bytes(image: Image.Image, size: int) -> bytes:
    buffer = io.BytesIO()
    square(image, size).save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()


def write_embedded_svg(image: Image.Image, path: Path) -> None:
    encoded = base64.b64encode(png_bytes(image, 512)).decode("ascii")
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" '
        'viewBox="0 0 1024 1024">\n'
        f'  <image width="1024" height="1024" preserveAspectRatio="xMidYMid meet" '
        f'href="data:image/png;base64,{encoded}" />\n'
        '</svg>\n'
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")


def write_icns(image: Image.Image, path: Path) -> None:
    chunks = b"".join(tag + struct.pack(">I", len(data) + 8) + data
                      for tag, size in ICNS_CHUNKS
                      for data in (png_bytes(image, size),))
    payload = b"icns" + struct.pack(">I", len(chunks) + 8) + chunks
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def build_assets(source: Path, root: Path, site_dir: Path) -> None:
    image = Image.open(source).convert("RGB")
    res = root / "res"
    for name, size in {
        "icon.png": 1024,
        "128x128@2x.png": 256,
        "128x128.png": 128,
        "64x64.png": 64,
        "32x32.png": 32,
        "mac-icon.png": 1024,
    }.items():
        write_png(image, res / name, size)
    write_ico(image, res / "icon.ico", ICO_SIZES)
    write_ico(image, res / "tray-icon.ico", TRAY_SIZES)
    write_ico(image, root / "flutter/windows/runner/resources/app_icon.ico", ICO_SIZES)
    write_embedded_svg(image, res / "scalable.svg")
    write_embedded_svg(image, root / "flutter/assets/icon.svg")

    write_png(image, root / "flutter/assets/icon.png", 512)
    write_png(image, root / "flutter/assets/logo.png", 512)
    write_icns(image, root / "flutter/macos/Runner/AppIcon.icns")

    android_root = root / "flutter/android/app/src/main/res"
    for density, (launcher, foreground, status) in ANDROID.items():
        folder = android_root / f"mipmap-{density}"
        write_png(image, folder / "ic_launcher.png", launcher)
        write_png(image, folder / "ic_launcher_round.png", launcher)
        write_png(image, folder / "ic_launcher_foreground.png", foreground)
        write_png(image, folder / "ic_stat_logo.png", status)

    ios_root = root / "flutter/ios/Runner/Assets.xcassets/AppIcon.appiconset"
    for name, size in IOS.items():
        write_png(image, ios_root / name, size)

    site_dir.mkdir(parents=True, exist_ok=True)
    square(image, 1200).save(site_dir / "cover.webp", format="WEBP", quality=90, method=6)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--root", required=True, type=Path, help="RustDesk source repository")
    parser.add_argument("--site", required=True, type=Path, help="download-site directory")
    args = parser.parse_args()
    build_assets(args.source.resolve(), args.root.resolve(), args.site.resolve())
    print(f"generated WKAite Remote icons from {args.source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
