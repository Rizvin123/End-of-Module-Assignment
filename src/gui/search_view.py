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

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Top Controls
        control_layout = QHBoxLayout()

        self.type_combo = QComboBox()
        self.type_combo.addItems(["client", "airline", "flight"])

        self.field_input = QLineEdit()
        self.field_input.setPlaceholderText("Field name (e.g., city, company_name)")

        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Value")

        self.search_btn = QPushButton("Search")

        control_layout.addWidget(QLabel("Type:"))
        control_layout.addWidget(self.type_combo)
        control_layout.addWidget(self.field_input)
        control_layout.addWidget(self.value_input)
        control_layout.addWidget(self.search_btn)

        layout.addLayout(control_layout)

        # Results Table
        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.search_btn.clicked.connect(self._perform_search)

    def _perform_search(self):
        record_type = self.type_combo.currentText()
        field = self.field_input.text().strip()
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