from sys import argv
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QListWidget, QPushButton, QDialog, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from db import create_db, read_db_rows, read_db_row, insert_db
from encrypt import generate_key, encrypt_password, decrypt_password, generate_password_hash, verify_password_hash, derive_key_from_password, encrypt_master_key_file, load_master_key_file
from cryptography.fernet import InvalidToken

db_name: str = "passwords"
password_table: str = "password"
columns: list = ["passwords"]

master_password_table: str = "master_password"
master_password_columns: list = ["passwords"]

keyfile = "master.key.enc"

class InitialWindow(QDialog):
    def __init__(self):
        super().__init__()

        create_db(db_name, password_table, columns)
        create_db(db_name, master_password_table, master_password_columns)

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

        create_password = QPushButton("Create password")
        create_password.setFixedHeight(40)
        create_password.clicked.connect(self.create_password)
        layout.addWidget(create_password)

        self.setLayout(layout)

    def validate_password(self):
        password = self.password_input.text().strip()
        try:
            master_password = load_master_key_file(password, keyfile)
            if master_password is None:
                raise FileNotFoundError("Keyfile not found")
            
            self.accept()
        except InvalidToken:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Invalid Password")
            msg.setText("Incorrect master password. Please try again.")
            msg.exec_()

            self.password_input.setFocus()
            self.password_input.clear()
        except FileNotFoundError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("File Not Found")
            msg.setText(f"The master password does not exists. First create it.")
            msg.exec_()

            self.password_input.setFocus()
            self.password_input.clear()

    def create_password(self):
        password = self.password_input.text().strip()
        password_hash = generate_password_hash(password)

        row = read_db_row(db_name, master_password_table, master_password_columns[0])

        if row:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Password already exists")
            msg.setText("Password already exists. Try confirming.")
            msg.exec_()

            self.password_input.setFocus()
            self.password_input.clear()
            return

        insert_db(db_name, master_password_table, master_password_columns[0], str(password_hash))
        generate_key()
        encrypt_master_key_file(password, keyfile)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Password added")
        msg.setText("Password added. Try confirming.")
        msg.exec_()
        self.password_input.setFocus()
        self.password_input.clear()

class InputWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enter master password")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()
        
        label = QLabel("Enter your master password.")
        layout.addWidget(label)

        self.master_password_input = QLineEdit()
        self.master_password_input.setEchoMode(QLineEdit.Password)
        self.master_password_input.returnPressed.connect(self.verify_password)
        layout.addWidget(self.master_password_input)

        self.setLayout(layout)
    
    def verify_password(self):
        password = self.master_password_input.text().strip()
        try:
            master_password = load_master_key_file(password, keyfile)
            if master_password is None:
                raise FileNotFoundError("Keyfile not found")
            
            self.accept()
        except InvalidToken:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Invalid Password")
            msg.setText("Incorrect master password. Please try again.")
            msg.exec_()

            self.master_password_input.setFocus()
            self.master_password_input.clear()
        except FileNotFoundError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("File Not Found")
            msg.setText(f"The master password does not exists. First create it.")
            msg.exec_()

            self.master_password_input.setFocus()
            self.master_password_input.clear()
        

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
        self.list_widget = QListWidget()
        # list_widget.addItem("Test")
        layout.addWidget(self.list_widget)

        # Input line widgets
        self.password_input = QLineEdit()
        self.password_input.returnPressed.connect(self.add_password)
        layout.addWidget(self.password_input)

        # Button widgets
        add_button = QPushButton("Add")
        add_button.setFixedHeight(40)
        delete_button = QPushButton("Delete")
        delete_button.setFixedHeight(40)
        layout.addWidget(add_button)
        layout.addWidget(delete_button)

        add_button.clicked.connect(self.add_password)

        widget.setLayout(layout)

    def add_password(self):
        password: str = self.password_input.text().strip()
        try:
            self.add_password_db()
            self.list_widget.addItem(password)
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Could not add password")
            msg.setText("Could not add password. Please try again.")
            msg.exec_()

    def add_password_db(self):
        password: str = self.password_input.text().strip()

        input_window = InputWindow()
        result = input_window.exec_()

        if result == QDialog.Accepted:
            master_password = input_window.master_password_input.text().strip()
            try:
                encrypted_password = encrypt_password(password, load_master_key_file(master_password, keyfile))
                insert_db(db_name, password_table, columns[0], str(encrypted_password))
            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Could not encrypt password")
                msg.setText("Could not encrypt password or add to the database. Please try again.")
                msg.exec_()

app = QApplication(argv)

initial_window = InitialWindow()
result = initial_window.exec_()

if result == QDialog.Accepted:
    main_window = MainWindow()
    main_window.show()
    app.exec_()