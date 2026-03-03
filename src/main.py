import sys
from PyQt6.QtWidgets import QApplication
from src.data.storage import JsonStorage
from src.data.repository import RecordRepository
from src.gui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    storage = JsonStorage("records.json")
    repository = RecordRepository(storage)

    window = MainWindow(repository)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()