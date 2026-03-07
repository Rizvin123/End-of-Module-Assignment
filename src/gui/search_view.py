from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, 
                             QTableWidget, QTableWidgetItem)

class SearchView(QWidget):
    def __init__(self, repository):
        super().__init__()
        # This line fixes the 'AttributeError' crash
        self.repository = repository 
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Robust search bar - filters as you type
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by ID, Client, or Airline...")
        self.search_input.textChanged.connect(self._on_search_changed)
        layout.addWidget(self.search_input)

        # Results Table
        self.table = QTableWidget()
        layout.addWidget(self.table)
        
        self.setLayout(layout)

    def _on_search_changed(self, text):
        query = text.strip().casefold()
        if not query:
            self.table.setRowCount(0)
            return

        all_results = []
        # Checks every record type for a match
        for record_type in ["client", "airline", "flight"]:
            results = self.repository.search(record_type, {}) 
            for r in results:
                # Robust check: looks through every column in the row
                if any(query in str(v).casefold() for v in r.values()):
                    all_results.append(r)
        
        self._populate_table(all_results)

    def _populate_table(self, records):
        if not records:
            self.table.setRowCount(0)
            return
            
        headers = list(records[0].keys())
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(records))
        
        for row, record in enumerate(records):
            for col, key in enumerate(headers):
                self.table.setItem(row, col, QTableWidgetItem(str(record[key])))
