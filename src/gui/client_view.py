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

from src.gui.client_form import ClientForm


class ClientView(QWidget):
    def __init__(self, repository):
        super().__init__()
        self.repository = repository
        self._setup_ui()
        self.load_data()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Name", "City", "Country", "Phone"]
        )
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
        self.btn_create.clicked.connect(self._create_client)
        self.btn_update.clicked.connect(self._update_client)
        self.btn_delete.clicked.connect(self._delete_client)
        self.btn_refresh.clicked.connect(self.load_data)

    def load_data(self):
        clients = self.repository.get_all_by_type("client")

        self.table.setRowCount(len(clients))

        for row, client in enumerate(clients):
            self.table.setItem(row, 0, QTableWidgetItem(str(client["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(client["name"]))
            self.table.setItem(row, 2, QTableWidgetItem(client["city"]))
            self.table.setItem(row, 3, QTableWidgetItem(client["country"]))
            self.table.setItem(row, 4, QTableWidgetItem(client["phone_number"]))

    def _get_selected_client_id(self):
        selected = self.table.currentRow()
        if selected < 0:
            return None

        item = self.table.item(selected, 0)
        return int(item.text())

    def _create_client(self):
        dialog = ClientForm(self.repository)
        if dialog.exec():
            self.load_data()

    def _update_client(self):
        client_id = self._get_selected_client_id()
        if client_id is None:
            QMessageBox.warning(self, "Warning", "Select a client first.")
            return

        dialog = ClientForm(self.repository, client_id=client_id)
        if dialog.exec():
            self.load_data()

    def _delete_client(self):
        client_id = self._get_selected_client_id()
        if client_id is None:
            QMessageBox.warning(self, "Warning", "Select a client first.")
            return

        try:
            self.repository.delete_client(client_id)
            self.load_data()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))