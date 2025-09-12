from sys import argv
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QListWidget, QPushButton, QDialog, QLabel

class InitialWindow(QDialog):
    def __init__(self):
        super().__init__()

        # Window paramaters
        self.setWindowTitle("OwlSafe | Enter Master Password")
        self.setFixedSize(400, 200)

        # Layout setup
        layout = QVBoxLayout()

        # Input field and label widgets
        label = QLabel("Enter your master password.")
        layout.addWidget(label)
        
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window paramaters
        self.setWindowTitle("OwlSafe")
        self.setFixedSize(800, 600)

        widget = QWidget()
        self.setCentralWidget(widget)

        # Layout setup
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(50, 50, 50, 50)

        # List widget
        list_widget = QListWidget()
        list_widget.addItem("Test")
        layout.addWidget(list_widget)

        # Button Widgets
        add_button = QPushButton("Add")
        add_button.setFixedHeight(40)
        delete_button = QPushButton("Delete")
        delete_button.setFixedHeight(40)
        layout.addWidget(add_button)
        layout.addWidget(delete_button)

        widget.setLayout(layout)

app = QApplication(argv)
window = MainWindow()
window.show()
app.exec()
