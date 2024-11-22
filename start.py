from app_ui.ui import UserInterface
from validators.run_validator import RunValidator


def run_app():
    RunValidator.check_db()
    RunValidator.check_last_generated_pk()

    ui = UserInterface()


if __name__ == "__main__":
    run_app()
