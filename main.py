"""Launch the Smart File & Media Manager desktop application."""

import sys
from PyQt6.QtWidgets import QApplication
from app.controller import AppController
from app.view import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Smart File & Media Manager")
    app.setOrganizationName("Advanced Programming Project")
    window = MainWindow()
    controller = AppController(window)
    window.controller = controller  # Keep the coordinator alive for the window lifetime.
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
