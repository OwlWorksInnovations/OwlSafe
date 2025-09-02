from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QListWidget, QLineEdit, QMessageBox

password_file = 'passwords.txt'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OwlSafe")
        self.setFixedSize(800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(50, 50, 50, 50)

        # List widget
        self.list_widget = QListWidget()
        self.list_widget.addItems(self.get_passwords())
        layout.addWidget(self.list_widget)

        # Buttons
        add_button = QPushButton("Add")
        add_button.setFixedHeight(40)
        delete_button = QPushButton("Delete")
        delete_button.setFixedHeight(40)
        layout.addWidget(add_button)
        layout.addWidget(delete_button)

        main_widget.setLayout(layout)

        # Password Line
        self.line_edit = QLineEdit()
        layout.addWidget(self.line_edit)

        # Connect buttons
        add_button.clicked.connect(self.add_password)
        delete_button.clicked.connect(lambda: self.remove_password())
    
    # Functions
    def append_file(self, filename, text):
        with open(filename, 'a') as f:
            f.write(f"{text}\n")

        self.remove_duplicate_passwords()

    def write_file(self, filename: str, text: str):
        with open(filename, 'w') as f:
            f.write(text)

    def read_file(self, filename):
        file_lines = []
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line_content = line.strip()
                    file_lines.append(line_content)
        except FileNotFoundError:
            with open(filename, 'w') as f:
                pass

            return []
        
        return file_lines

    def get_passwords(self):
        return self.read_file(password_file)
    
    def clean_passwords(self):
        passwords = self.read_file(password_file)

        seen = set()
        unique_passwords = []
        
        for password in passwords:
            password_lower = password.lower()
            if password_lower not in seen:
                seen.add(password_lower)
                unique_passwords.append(password)

        return unique_passwords
    
    def remove_duplicate_passwords(self):
        unique_passwords = self.clean_passwords()
        self.write_file(password_file, "\n".join(unique_passwords) + "\n")

        self.update_list()

    def update_list(self):
        self.list_widget.clear()
        self.list_widget.addItems(self.get_passwords())
    
    def remove_password(self):
        current_item = self.list_widget.currentItem()

        if current_item:
            current_passwords: list = self.read_file(password_file)
            current_passwords.remove(current_item.text())

            all_passwords = '\n'.join(current_passwords) + '\n'
            self.write_file(password_file, all_passwords)
        
        self.update_list()

    def add_password(self):
        password = self.line_edit.text().strip()  # Assign the stripped result
        if not password:
            return
        
        self.append_file(password_file, password)
        self.line_edit.clear()

app = QApplication([])

window = MainWindow()
window.show()
app.exec()
