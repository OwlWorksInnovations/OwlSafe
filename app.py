from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QListWidget, QLineEdit, QMessageBox, QListWidgetItem, QDialog
from PyQt5.QtCore import Qt
import sqlite3
from encrypt import generate_password_hash, verify_password_hash, encrypt_password, decrypt_password, load_key, generate_key

def create_db():
        conn = sqlite3.connect("passwords.db")
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password TEXT NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS master_password (
                password TEXT NOT NULL            
            )
        """)
        conn.commit()
        conn.close()

create_db()

try:
    class StartupWindow(QDialog):  
        def __init__(self):
            super().__init__()

            self.setWindowTitle("OwlSafe | ENTER MASTER PASSWORD")
            self.setFixedSize(400, 200)

            self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint)

            layout = QVBoxLayout()
            
            self.line_edit = QLineEdit()
            self.line_edit.setEchoMode(QLineEdit.Password)
            layout.addWidget(self.line_edit)

            confirm_button = QPushButton("Confirm")
            confirm_button.setFixedHeight(40)

            create_password = QPushButton("Create password")
            create_password.setFixedHeight(20)

            layout.addWidget(confirm_button)
            layout.addWidget(create_password)

            self.line_edit.returnPressed.connect(self.verify_password)
            confirm_button.clicked.connect(self.verify_password)
            self.setLayout(layout)

        def verify_password(self):
            password = self.line_edit.text().strip()
    
            conn = sqlite3.connect("password.db")
            cur = conn.cursor()
            cur.execute("SELECT password FROM master_password")
            row = cur.fetchone()

            if not row:
                return

            hash = row

            verify_password_hash(password, hash)
            
            if not password:
                QMessageBox.warning(self, "Warning", "Please enter a password!")
                return
                
            print(password)

            self.accept()

        def closeEvent(self, event):
            event.ignore()

            QMessageBox.information(
                self, 
                "Authentication Required", 
                "You must enter the master password to continue."
            )

    load_key()
except FileNotFoundError:
    generate_key()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        startup = StartupWindow()
        result = startup.exec_()

        if result != QDialog.Accepted:
            QApplication.quit()
            return

        self.setWindowTitle("OwlSafe")
        self.setFixedSize(800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(50, 50, 50, 50)

        # List widget
        self.list_widget = QListWidget()
        for item in self.get_passwords():
            self.list_widget.addItem(item)
        layout.addWidget(self.list_widget)

        # Buttons
        add_button = QPushButton("Add")
        add_button.setFixedHeight(40)
        delete_button = QPushButton("Delete")
        delete_button.setFixedHeight(40)

        test_button = QPushButton("Test")
        test_button.setFixedHeight(40)

        layout.addWidget(add_button)
        layout.addWidget(delete_button)
        layout.addWidget(test_button)

        main_widget.setLayout(layout)

        # Password Line
        self.line_edit = QLineEdit()
        layout.addWidget(self.line_edit)

        # Connect buttons
        add_button.clicked.connect(self.insert_password)
        delete_button.clicked.connect(lambda: self.remove_password())
        test_button.clicked.connect(self.print_passwords)

    # Functions
    def get_passwords(self):
        key = load_key()

        conn = sqlite3.connect("passwords.db")
        cur = conn.cursor()
        cur.execute("SELECT id, password FROM passwords")
        rows = cur.fetchall()
        conn.close()
        
        items = []
        for entry_id, encrypted_password in rows:
            decrypted_password = decrypt_password(encrypted_password, key)
            item = QListWidgetItem(decrypted_password)
            item.setData(Qt.UserRole, entry_id)
            items.append(item)
            
        return items
    
    # def clean_passwords(self):
    #     passwords = self.read_file(password_file)

    #     seen = set()
    #     unique_passwords = []
        
    #     for password in passwords:
    #         password_lower = password.lower()
    #         if password_lower not in seen:
    #             seen.add(password_lower)
    #             unique_passwords.append(password)

    #     return unique_passwords
    
    # def remove_duplicate_passwords(self):
    #     unique_passwords = self.clean_passwords()
    #     self.write_file(password_file, "\n".join(unique_passwords) + "\n")

    #     self.update_list()

    def update_list(self):
        self.list_widget.clear()
        self.list_widget.addItems(self.get_passwords())

    def insert_password(self):
        password = self.line_edit.text().strip()
        if not password:
            return

        key = load_key()
        encrypted_password = encrypt_password(password, key)
        
        conn = sqlite3.connect("passwords.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO passwords (password) VALUES (?)", (encrypted_password,))
        entry_id = cur.lastrowid
        conn.commit()
        conn.close()

        item = QListWidgetItem(password)
        item.setData(Qt.UserRole, entry_id)
        self.list_widget.addItem(item)

        self.line_edit.clear()

    def remove_password(self):
        item = self.list_widget.currentItem()
        if not item:
            return

        entry_id = item.data(Qt.UserRole)

        # Delete from DB
        conn = sqlite3.connect("passwords.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM passwords WHERE id=?", (entry_id,))
        conn.commit()
        conn.close()

        # Remove from list widget
        self.list_widget.takeItem(self.list_widget.row(item))

    def print_passwords(self):
        conn = sqlite3.connect("passwords.db")
        cur = conn.cursor()
        cur.execute("SELECT id, password FROM passwords")
        rows = cur.fetchall()
        conn.close()
        
        items = []
        for pw in rows:
            items.append(pw)
        print(items)

app = QApplication([])

window = MainWindow()
window.show()
app.exec()
