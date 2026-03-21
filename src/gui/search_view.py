from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QComboBox,
    QLineEdit,
    QMessageBox
)


class SearchView(QWidget):
    def __init__(self, repository):
        super().__init__()
        self.repository = repository
        self._setup_ui()
        self.search_fields = {
            "client": [
                "name",
                "city",
                "state",
                "country",
                "zip_code",
                "phone_number"
            ],
            "airline": [
                "company_name"
            ],
            "flight": [
                "client_id",
                "airline_id",
                "start_city",
                "end_city"
            ]
        }
        self._update_fields()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Top Controls
        control_layout = QHBoxLayout()

        self.type_combo = QComboBox()
        self.type_combo.addItems(["client", "airline", "flight"])

        self.field_combo = QComboBox()

        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Value")

        self.search_btn = QPushButton("Search")

        control_layout.addWidget(QLabel("Type:"))
        control_layout.addWidget(self.type_combo)
        control_layout.addWidget(QLabel("Field:"))
        control_layout.addWidget(self.field_combo)
        control_layout.addWidget(self.value_input)
        control_layout.addWidget(self.search_btn)

        layout.addLayout(control_layout)

        # Results Table
        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.total_label = QLabel("Results: 0")
        layout.addWidget(self.total_label)

        self.setLayout(layout)
        self.type_combo.currentTextChanged.connect(self._update_fields)
        self.search_btn.clicked.connect(self._perform_search)

    def _perform_search(self):
        self.total_label.setText("Results: 0")
        record_type = self.type_combo.currentText()
        field = self.field_combo.currentText()
        value = self.value_input.text().strip()

        if not field or not value:
            QMessageBox.warning(self, "Warning", "Enter both field and value.")
            return

        results = self.repository.search(record_type, {field: value})

        if not results:
            QMessageBox.information(self, "No Results", "No matching records found.")
            self.table.setRowCount(0)
            return

        self._populate_table(results)
        self.total_label.setText(f"Results: {len(results)}")

    def _populate_table(self, records):
        headers = records[0].keys()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(list(headers))
        self.table.setRowCount(len(records))

        for row, record in enumerate(records):
            for col, key in enumerate(headers):
                self.table.setItem(
                    row,
                    col,
                    QTableWidgetItem(str(record[key]))
                )
    def _update_fields(self):
        record_type = self.type_combo.currentText()

        self.field_combo.clear()
        self.field_combo.addItems(self.search_fields.get(record_type, []))