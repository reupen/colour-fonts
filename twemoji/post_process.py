from enum import IntEnum
from pathlib import Path

from fontTools.ttLib import TTFont
from toml import load

PARENT_DIR = Path(__file__).parent
CONFIG_FILE = PARENT_DIR / "config.toml"
POST_CONFIG_FILE = PARENT_DIR / "POST.toml"
SPACE_UPEM_FACTOR = 0.274


class NameID(IntEnum):
    COPYRIGHT = 0
    DESCRIPTION = 10
    LICENCE = 13
    LICENCE_URL = 14


def post_process():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = load(f)

    with open(POST_CONFIG_FILE, "r", encoding="utf-8") as f:
        post_config = load(f)

    font = TTFont(PARENT_DIR / "build" / config["output_file"])

    name_table = font["name"]

    copyright = post_config["metadata"]["copyright"]
    description = post_config["metadata"]["description"]
    licence = post_config["metadata"]["licence"]
    licence_url = post_config["metadata"]["licence_url"]

    name_table.setName(copyright, NameID.COPYRIGHT, 3, 1, 0x409)
    name_table.setName(description, NameID.DESCRIPTION, 3, 1, 0x409)
    name_table.setName(licence, NameID.LICENCE, 3, 1, 0x409)
    name_table.setName(licence_url, NameID.LICENCE_URL, 3, 1, 0x409)

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

    output_path = PARENT_DIR / "build" / post_config["output_file"]
    font.save(output_path)

    print(f"Post-processed font saved to: {output_path}")


if __name__ == "__main__":
    post_process()
