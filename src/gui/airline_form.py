from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QDialogButtonBox,
    QMessageBox
)

from src.record.airline import AirlineRecord


class AirlineForm(QDialog):
    def __init__(self, repository, airline_id=None):
        super().__init__()
        self.repository = repository
        self.airline_id = airline_id

        self.setWindowTitle("Airline Form")
        self.resize(300, 150)

        self._setup_ui()

        if self.airline_id:
            self._load_existing_data()

    def _setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.company_input = QLineEdit()
        form_layout.addRow("Company Name", self.company_input)

        layout.addLayout(form_layout)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )

        self.buttons.accepted.connect(self._save)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def _load_existing_data(self):
        airline = self.repository.get_airline_by_id(self.airline_id)
        if airline:
            self.company_input.setText(airline["company_name"])

    def _save(self):
        try:
            airline = AirlineRecord(
                company_name=self.company_input.text()
            )

            if self.airline_id:
                data = airline.to_dict()
                data.pop("id", None)
                data.pop("type", None)

                self.repository.update_airline(self.airline_id, data)
            else:
                self.repository.create_airline(airline)

            self.accept()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))