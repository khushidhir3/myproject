import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox

class InvestmentBot(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Investment Insights Bot')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Select your financial goal:')
        layout.addWidget(self.label)

        self.combo = QComboBox()
        self.combo.addItems(["short-term", "long-term", "retirement", "high-risk"])
        layout.addWidget(self.combo)

        self.btn = QPushButton('Get Investment Advice')
        self.btn.clicked.connect(self.fetch_recommendations)
        layout.addWidget(self.btn)

        self.result_label = QLabel('')
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def fetch_recommendations(self):
        goal = self.combo.currentText()
        response = requests.post('http://127.0.0.1:5000/recommend', json={"goal": goal})
        if response.status_code == 200:
            data = response.json()
            investments = ', '.join(data["suggested_investments"])
            self.result_label.setText(f"Suggested: {investments}")
        else:
            self.result_label.setText("Error fetching data")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    bot = InvestmentBot()
    bot.show()
    sys.exit(app.exec_())
