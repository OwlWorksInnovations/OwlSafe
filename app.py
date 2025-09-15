from sys import argv
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QListWidget, QPushButton, QDialog, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from db import create_db, read_db, insert_db

db_name: str = "passwords"
password_table: str = "password"
columns: list = ["passwords"]

master_password_table: str = "master_password"
master_password_columns: list = ["passwords"]

class InitialWindow(QDialog):
    def __init__(self):
        super().__init__()

        create_db(db_name, password_table, columns)
        create_db(db_name, master_password_table, master_password_columns)

        insert_db(db_name, password_table, "passwords", "test123")

        print(read_db(db_name, password_table, columns[0]))

        # Window paramaters
        self.setWindowTitle("OwlSafe | Enter Master Password")
        self.setFixedSize(400, 200)

        # Layout setup
        layout = QVBoxLayout()

        # Input field and label widgets
        label = QLabel("Enter your master password.")
        layout.addWidget(label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self.validate_password)
        layout.addWidget(self.password_input)

        confirm_button = QPushButton("Confirm")
        confirm_button.setFixedHeight(40)
        confirm_button.clicked.connect(self.validate_password)
        layout.addWidget(confirm_button)

        self.setLayout(layout)

    def validate_password(self):
        master_password: str = "test123"

        input_password = self.password_input.text().strip()

        if input_password == master_password:
            self.accept()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Invalid Password")
            msg.setText("Incorrect master password. Please try again.")
            msg.exec_()

            self.password_input.setFocus()
            self.password_input.clear()

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

initial_window = InitialWindow()
result = initial_window.exec_()

if result == QDialog.Accepted:
    main_window = MainWindow()
    main_window.show()
    app.exec_()