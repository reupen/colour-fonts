from pathlib import Path

from toml import dump, load

PARENT_DIR = Path(__file__).parent
CONFIG_FILE = PARENT_DIR / "config.toml"
SVG_DIR = PARENT_DIR / "src" / "assets" / "svg"


def main():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = load(f)

    files = [
        str(file.relative_to(PARENT_DIR).as_posix())
        for file in sorted(SVG_DIR.glob("*.svg"))
    ]

    config["master"]["regular"]["srcs"] = files

    with open(CONFIG_FILE, "w") as f:
        dump(config, f)


if __name__ == "__main__":
    main()
