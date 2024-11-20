from pathlib import Path

import config


def run_app():
    print(Path(config.DATA_BASE_FILE))


if __name__ == "__main__":
    run_app()
