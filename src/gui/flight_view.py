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

from src.gui.flight_form import FlightForm


class FlightView(QWidget):
    def __init__(self, repository):
        super().__init__()
        self.repository = repository
        self._setup_ui()
        self.load_data()

    def _setup_ui(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Client", "Airline", "Date", "From", "To"]
        )
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()

        self.btn_create = QPushButton("Create")
        self.btn_delete = QPushButton("Delete")
        self.btn_refresh = QPushButton("Refresh")

        btn_layout.addWidget(self.btn_create)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_refresh)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.btn_create.clicked.connect(self._create_flight)
        self.btn_delete.clicked.connect(self._delete_flight)
        self.btn_refresh.clicked.connect(self.load_data)

    def load_data(self):
        flights = self.repository.get_all_by_type("flight")

        self.table.setRowCount(len(flights))

        for row, flight in enumerate(flights):
            client = self.repository.get_client_by_id(flight["client_id"])
            airline = self.repository.get_airline_by_id(flight["airline_id"])

            self.table.setItem(row, 0, QTableWidgetItem(client["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(airline["company_name"]))
            self.table.setItem(row, 2, QTableWidgetItem(flight["date"]))
            self.table.setItem(row, 3, QTableWidgetItem(flight["start_city"]))
            self.table.setItem(row, 4, QTableWidgetItem(flight["end_city"]))

    def _get_selected_row(self):
        return self.table.currentRow()

    def _create_flight(self):
        dialog = FlightForm(self.repository)
        if dialog.exec():
            self.load_data()

    def _delete_flight(self):
        row = self._get_selected_row()
        if row < 0:
            QMessageBox.warning(self, "Warning", "Select a flight first.")
            return

        flights = self.repository.get_all_by_type("flight")
        flight = flights[row]

        self.repository.records.remove(flight)
        self.load_data()