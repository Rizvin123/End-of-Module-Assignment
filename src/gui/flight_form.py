from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QDialogButtonBox,
    QMessageBox
)
from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import QDateTimeEdit

from src.record.flight import FlightRecord


class FlightForm(QDialog):
    def __init__(self, repository):
        super().__init__()
        self.repository = repository

        self.setWindowTitle("Flight Form")
        self.resize(350, 250)

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.client_combo = QComboBox()
        self.airline_combo = QComboBox()
        self.date_input = QDateTimeEdit()
        self.date_input.setDateTime(QDateTime.currentDateTime())
        self.start_input = QLineEdit()
        self.end_input = QLineEdit()

        # Populate dropdowns
        self.clients = self.repository.get_all_by_type("client")
        self.airlines = self.repository.get_all_by_type("airline")

        for client in self.clients:
            self.client_combo.addItem(client["name"], client["id"])

        for airline in self.airlines:
            self.airline_combo.addItem(airline["company_name"], airline["id"])

        form_layout.addRow("Client", self.client_combo)
        form_layout.addRow("Airline", self.airline_combo)
        form_layout.addRow("Date", self.date_input)
        form_layout.addRow("From", self.start_input)
        form_layout.addRow("To", self.end_input)

        layout.addLayout(form_layout)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )

        self.buttons.accepted.connect(self._save)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def _save(self):
        try:
            flight = FlightRecord(
                client_id=self.client_combo.currentData(),
                airline_id=self.airline_combo.currentData(),
                date=self.date_input.dateTime().toPyDateTime(),
                start_city=self.start_input.text(),
                end_city=self.end_input.text(),
            )

            self.repository.create_flight(flight)
            self.accept()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))