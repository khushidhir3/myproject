import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

API_URL = "http://127.0.0.1:5000/api"

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 400, 250)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.signup_button = QPushButton("Sign Up", self)
        self.signup_button.clicked.connect(self.signup)
        layout.addWidget(self.signup_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and password are required!")
            return

        response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
        data = response.json()

        if response.status_code == 200:
            QMessageBox.information(self, "Success", "Login successful!")
            self.open_dashboard(data["user_id"])
        else:
            QMessageBox.warning(self, "Login Failed", data["error"])

    def signup(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and password are required!")
            return

        response = requests.post(f"{API_URL}/signup", json={"username": username, "password": password})
        data = response.json()

        if response.status_code == 201:
            QMessageBox.information(self, "Success", "User registered successfully! Please log in.")
        else:
            QMessageBox.warning(self, "Signup Failed", data["error"])

    def open_dashboard(self, user_id):
        from main import InvestmentApp  # Import main UI
        self.close()
        self.window = InvestmentApp(user_id)
        self.window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
