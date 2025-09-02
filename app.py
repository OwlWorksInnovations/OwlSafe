from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QListWidget, QLineEdit, QMessageBox

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

        # Connect delete button
        delete_button.clicked.connect(self.delete_password)
        add_button.clicked.connect(self.add_passord)

    def delete_password(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            self.list_widget.takeItem(self.list_widget.row(selected_item))
            with open('passwords_blacklist.txt', 'a') as file:
                file.write(f"{selected_item.text()} \n")
    
    def add_passord(self):
        password = self.line_edit.text()
        if not password:
            return
        
        for i in range(self.list_widget.count()):
            if self.list_widget.item(i).text() == password:
                msg_box = QMessageBox()
                msg_box.setText("Password already exists!")
                msg_box.setWindowTitle("Error")
                msg_box.setIcon(QMessageBox.Critical)
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
                return
            
        self.list_widget.addItem(password)
        self.line_edit.clear()

        with open('passwords.txt', 'a') as file:
            file.write(password + "\n")
    
    def get_passwords(self):
        with open('passwords_blacklist.txt', 'r') as file:
            blacklist = []
            for line in file:
                clean_line = line.strip()
                blacklist.append(clean_line)

        passwords = []
        with open('passwords.txt', 'r') as file:
            for line in file:
                clean_line = line.strip()

                if clean_line not in blacklist:
                    passwords.append(clean_line)

            return passwords


app = QApplication([])

window = MainWindow()
window.show()
app.exec()
