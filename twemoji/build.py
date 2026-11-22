from pathlib import Path
from subprocess import run

from post_process import post_process

PARENT_DIR = Path(__file__).parent
ROOT_DIR = PARENT_DIR.parent
CONFIG_FILE = (PARENT_DIR / "config.toml").relative_to(ROOT_DIR)
BUILD_DIR = (PARENT_DIR / "build").relative_to(ROOT_DIR)


def main():
    run(["nanoemoji", "--build_dir", BUILD_DIR, CONFIG_FILE], check=True)
    post_process()


if __name__ == "__main__":
    main()
