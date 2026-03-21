from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedWidget
)

from src.gui.client_view import ClientView
from src.gui.airline_view import AirlineView
from src.gui.flight_view import FlightView
from src.gui.search_view import SearchView


class MainWindow(QMainWindow):
    def __init__(self, repository):
        super().__init__()
        self.repository = repository

        self.setWindowTitle("Travel Record Management System")
        self.resize(1000, 600)

        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        main_layout = QHBoxLayout()

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
        sidebar_layout.addStretch()

        # Stacked Widget (content area)
        self.stacked_widget = QStackedWidget()

        self.client_view = ClientView(self.repository)
        self.airline_view = AirlineView(self.repository)
        self.flight_view = FlightView(self.repository)
        self.search_view = SearchView(self.repository)

        self.stacked_widget.addWidget(self.client_view)
        self.stacked_widget.addWidget(self.airline_view)
        self.stacked_widget.addWidget(self.flight_view)
        self.stacked_widget.addWidget(self.search_view)

        # Layout assembly
        main_layout.addLayout(sidebar_layout, 1)
        main_layout.addWidget(self.stacked_widget, 4)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self._connect_signals()

    def _connect_signals(self):
        self.btn_clients.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_airlines.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_flights.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.btn_search.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))

    def closeEvent(self, event):
        self.repository.save()
        event.accept()