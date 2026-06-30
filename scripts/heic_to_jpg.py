#!/usr/bin/env python3

import os
import sys
from pathlib import Path

try:
    from PIL import Image
    import pillow_heif
except ImportError:
    print("Missing dependencies. Install with:")
    print("  pip install pillow pillow-heif")
    sys.exit(1)

# --- Configuration ---
INPUT_FOLDER = Path.home() / "Documents" / "Cars" / "Jeep" / "Originals"
OUTPUT_FOLDER = Path.home() / "Documents" / "Cars" / "Jeep" / "Exports"
QUALITY = 85  # 1–95; higher = better quality, larger file size
# ---------------------

pillow_heif.register_heif_opener()


def convert_heic_to_jpg(input_folder: str, output_folder: str, quality: int) -> None:
    input_path = Path(input_folder)
    output_path = Path(output_folder)

    if not input_path.exists():
        print(f"Input folder not found: {input_folder}")
        sys.exit(1)

    output_path.mkdir(parents=True, exist_ok=True)

    heic_files = list(input_path.glob("*.heic")) + list(input_path.glob("*.HEIC"))

    if not heic_files:
        print("No HEIC files found in the input folder.")
        return

    print(f"Found {len(heic_files)} HEIC file(s). Converting at quality={quality}...")

    for heic_file in heic_files:
        jpg_file = output_path / (heic_file.stem + ".jpg")
        try:
            with Image.open(heic_file) as img:
                rgb_img = img.convert("RGB")
                rgb_img.save(jpg_file, "JPEG", quality=quality)
            print(f"  {heic_file.name} -> {jpg_file.name}")
        except Exception as e:
            print(f"  ERROR converting {heic_file.name}: {e}")

    print("Done.")


if __name__ == "__main__":
    convert_heic_to_jpg(INPUT_FOLDER, OUTPUT_FOLDER, QUALITY)
