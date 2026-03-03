from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)
from PyQt6.QtCore import Qt

from src.gui.airline_form import AirlineForm


class AirlineView(QWidget):
    def __init__(self, repository):
        super().__init__()
        self.repository = repository
        self._setup_ui()
        self.load_data()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Company Name"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout.addWidget(self.table)

        # Buttons
        btn_layout = QHBoxLayout()

        self.btn_create = QPushButton("Create")
        self.btn_update = QPushButton("Update")
        self.btn_delete = QPushButton("Delete")
        self.btn_refresh = QPushButton("Refresh")

        btn_layout.addWidget(self.btn_create)
        btn_layout.addWidget(self.btn_update)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_refresh)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self._connect_signals()

    def _connect_signals(self):
        self.btn_create.clicked.connect(self._create_airline)
        self.btn_update.clicked.connect(self._update_airline)
        self.btn_delete.clicked.connect(self._delete_airline)
        self.btn_refresh.clicked.connect(self.load_data)

    def load_data(self):
        airlines = self.repository.get_all_by_type("airline")

        self.table.setRowCount(len(airlines))

        for row, airline in enumerate(airlines):
            self.table.setItem(row, 0, QTableWidgetItem(str(airline["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(airline["company_name"]))

    def _get_selected_airline_id(self):
        selected = self.table.currentRow()
        if selected < 0:
            return None

        item = self.table.item(selected, 0)
        return int(item.text())

    def _create_airline(self):
        dialog = AirlineForm(self.repository)
        if dialog.exec():
            self.load_data()

    def _update_airline(self):
        airline_id = self._get_selected_airline_id()
        if airline_id is None:
            QMessageBox.warning(self, "Warning", "Select an airline first.")
            return

        dialog = AirlineForm(self.repository, airline_id=airline_id)
        if dialog.exec():
            self.load_data()

    def _delete_airline(self):
        airline_id = self._get_selected_airline_id()
        if airline_id is None:
            QMessageBox.warning(self, "Warning", "Select an airline first.")
            return

        try:
            self.repository.delete_airline(airline_id)
            self.load_data()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))