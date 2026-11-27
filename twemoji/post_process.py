from enum import IntEnum
from io import BytesIO
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from toml import load

PARENT_DIR = Path(__file__).parent
BUILD_DIR = PARENT_DIR / "build"
DIST_DIR = PARENT_DIR / "dist"
CONFIG_FILE = PARENT_DIR / "config.toml"
POST_CONFIG_FILE = PARENT_DIR / "post.toml"
SPACE_UPEM_FACTOR = 0.274


class NameID(IntEnum):
    COPYRIGHT = 0
    DESCRIPTION = 10
    LICENCE = 13
    LICENCE_URL = 14


def post_process():
    print("Post-processing font…")

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = load(f)

    with open(POST_CONFIG_FILE, "r", encoding="utf-8") as f:
        post_config = load(f)

    font = TTFont(PARENT_DIR / "build" / config["output_file"])

    metadata_config = post_config["metadata"]

    set_name_records(
        font,
        {
            NameID.COPYRIGHT: metadata_config["copyright"],
            NameID.DESCRIPTION: metadata_config["description"],
            NameID.LICENCE: metadata_config["licence"],
            NameID.LICENCE_URL: metadata_config["licence_url"],
        },
    )

    cmap = font.getBestCmap()

    if cmap is None:
        raise ValueError("cmap is None")

    space_glyph = cmap[0x20]

    if space_glyph is None:
        raise ValueError("space glyph is None")

    advance_width, left_side_bearing = font["hmtx"].metrics[space_glyph]

    new_advance_width = round(font["head"].unitsPerEm * SPACE_UPEM_FACTOR)

    font["hmtx"].metrics[space_glyph] = (new_advance_width, left_side_bearing)
    font["hhea"].advanceWidthMax = max(
        width for width, _ in font["hmtx"].metrics.values()
    )

    DIST_DIR.mkdir(exist_ok=True)
    output_path = DIST_DIR / post_config["output_file"]
    font.save(output_path)

    for variant in post_config["variants"]:
        stream = BytesIO()
        font.save(stream)

        variant_font = TTFont(stream)
        omit = variant["omit"]

        omit_glyphs(variant_font, omit)

        output_name = variant["output_file"]
        variant_font.save(DIST_DIR / output_name)

    print(f"Post-processed font saved to: {output_path}")


def omit_glyphs(font: TTFont, omit: list[str]):
    codepoints = {int(value.removeprefix("U+"), 16) for value in omit}
    keep_unicodes = font.getBestCmap().keys() - codepoints

    options = subset.Options()
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=keep_unicodes)
    subsetter.subset(font)


def set_name_records(font: TTFont, records: dict[int, str]):
    name_table = font["name"]
    for property_id, value in records.items():
        name_table.setName(value, property_id, 3, 1, 1033)


if __name__ == "__main__":
    post_process()
