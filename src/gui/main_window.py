from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QStackedWidget)
from src.gui.client_view import ClientView
from src.gui.airline_view import AirlineView
from src.gui.flight_view import FlightView
from src.gui.search_view import SearchView

class MainWindow(QMainWindow):
    def __init__(self, repository):
        super().__init__()
        self.repository = repository
        self.is_dark_mode = False 
        
        self.setWindowTitle("Travel Record Management System")
        self.resize(1000, 600)
        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Sidebar
        sidebar_layout = QVBoxLayout()
        
        self.btn_clients = QPushButton("Clients")
        self.btn_airlines = QPushButton("Airlines")
        self.btn_flights = QPushButton("Flights")
        self.btn_search = QPushButton("Search")

        sidebar_layout.addWidget(self.btn_clients)
        sidebar_layout.addWidget(self.btn_airlines)
        sidebar_layout.addWidget(self.btn_flights)
        sidebar_layout.addWidget(self.btn_search)
        
        # Pushes the toggle button to the bottom
        sidebar_layout.addStretch() 

        # Night Mode Toggle
        self.theme_btn = QPushButton("🌙 Night Mode")
        self.theme_btn.clicked.connect(self.toggle_theme)
        sidebar_layout.addWidget(self.theme_btn)

        # Content Area
        self.stacked_widget = QStackedWidget()
        self.client_view = ClientView(self.repository)
        self.airline_view = AirlineView(self.repository)
        self.flight_view = FlightView(self.repository)
        self.search_view = SearchView(self.repository)

        self.stacked_widget.addWidget(self.client_view)
        self.stacked_widget.addWidget(self.airline_view)
        self.stacked_widget.addWidget(self.flight_view)
        self.stacked_widget.addWidget(self.search_view)

        main_layout.addLayout(sidebar_layout, 1)
        main_layout.addWidget(self.stacked_widget, 4)

        self._connect_signals()

    def toggle_theme(self):
        if not self.is_dark_mode:
            # Apply Dark Styles
            self.setStyleSheet("""
                QWidget { background-color: #2b2b2b; color: #ffffff; }
                QLineEdit { background-color: #3d3d3d; color: white; border: 1px solid #555; }
                QTableWidget { background-color: #2b2b2b; gridline-color: #555; }
                QPushButton { background-color: #444; border: 1px solid #666; padding: 5px; }
            """)
            self.theme_btn.setText("☀️ Day Mode")
            self.is_dark_mode = True
        else:
            # Reset to Light Styles
            self.setStyleSheet("") 
            self.theme_btn.setText("🌙 Night Mode")
            self.is_dark_mode = False

    def _connect_signals(self):
        self.btn_clients.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_airlines.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_flights.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.btn_search.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))

    def closeEvent(self, event):
        self.repository.save()
        event.accept()
