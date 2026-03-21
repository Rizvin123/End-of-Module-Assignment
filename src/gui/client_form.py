from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QDialogButtonBox,
    QMessageBox
)

from src.record.client import ClientRecord


class ClientForm(QDialog):
    def __init__(self, repository, client_id=None):
        super().__init__()
        self.repository = repository
        self.client_id = client_id

        self.setWindowTitle("Client Form")
        self.resize(400, 400)

        self._setup_ui()

        if self.client_id:
            self._load_existing_data()

    def _setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.addr1_input = QLineEdit()
        self.addr2_input = QLineEdit()
        self.addr3_input = QLineEdit()
        self.city_input = QLineEdit()
        self.state_input = QLineEdit()
        self.zip_input = QLineEdit()
        self.country_input = QLineEdit()
        self.phone_input = QLineEdit()

        form_layout.addRow("Name", self.name_input)
        form_layout.addRow("Address Line 1", self.addr1_input)
        form_layout.addRow("Address Line 2", self.addr2_input)
        form_layout.addRow("Address Line 3", self.addr3_input)
        form_layout.addRow("City", self.city_input)
        form_layout.addRow("State", self.state_input)
        form_layout.addRow("Zip Code", self.zip_input)
        form_layout.addRow("Country", self.country_input)
        form_layout.addRow("Phone", self.phone_input)

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
        client = self.repository.get_client_by_id(self.client_id)
        if not client:
            return

        self.name_input.setText(client["name"])
        self.addr1_input.setText(client["address_line_1"])
        self.addr2_input.setText(client["address_line_2"])
        self.addr3_input.setText(client["address_line_3"])
        self.city_input.setText(client["city"])
        self.state_input.setText(client["state"])
        self.zip_input.setText(client["zip_code"])
        self.country_input.setText(client["country"])
        self.phone_input.setText(client["phone_number"])

    def _save(self):
        try:
            client = ClientRecord(
                name=self.name_input.text(),
                address_line_1=self.addr1_input.text(),
                address_line_2=self.addr2_input.text(),
                address_line_3=self.addr3_input.text(),
                city=self.city_input.text(),
                state=self.state_input.text(),
                zip_code=self.zip_input.text(),
                country=self.country_input.text(),
                phone_number=self.phone_input.text(),
            )

            if self.client_id:
                data = client.to_dict()
                data.pop("id", None)
                data.pop("type", None)

                self.repository.update_client(self.client_id, data)
            else:
                self.repository.create_client(client)

            self.accept()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))