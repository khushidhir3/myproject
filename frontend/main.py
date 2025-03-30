import sys
import requests
import matplotlib.pyplot as plt
from io import BytesIO
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QProgressBar
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

class InvestmentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Automated Investment Insights")
        self.setGeometry(100, 100, 900, 500)  # 16:9 ratio
        self.setStyleSheet("background-color: #121212; color: #ffffff;")

        layout = QVBoxLayout()

        self.symbol_input = QLineEdit(self)
        self.symbol_input.setPlaceholderText("Enter Stock Symbol (e.g., TSLA)")
        self.symbol_input.setStyleSheet(
            "background-color: #1E1E1E; color: #00FFFF; border-radius: 8px; padding: 8px; font-size: 16px;"
        )
        layout.addWidget(self.symbol_input)

        self.fetch_button = QPushButton("Get Investment Insights", self)
        self.fetch_button.setStyleSheet(
            "background-color: #6200EA; color: #ffffff; border-radius: 8px; padding: 10px; font-size: 16px;"
            "border: 2px solid #3700B3;"
        )
        self.fetch_button.clicked.connect(self.fetch_data)
        layout.addWidget(self.fetch_button)

        self.result_label = QLabel("Stock data will be displayed here", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.result_label)

        # Animated Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet(
            "QProgressBar { border: 2px solid #3700B3; border-radius: 8px; background: #1E1E1E; text-align: center; color: #ffffff; }"
            "QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6200EA, stop:1 #00FFFF); }"
        )
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.chart_label = QLabel(self)  # Label to display the stock chart
        layout.addWidget(self.chart_label)

        self.setLayout(layout)

    def fetch_data(self):
        stock_symbol = self.symbol_input.text().strip().upper()
        if not stock_symbol:
            self.result_label.setText("Please enter a stock symbol!")
            return

        self.progress_bar.setValue(0)
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_timer.start(50)

        try:
            url = f"http://127.0.0.1:5000/api/stock?symbol={stock_symbol}"  # Flask API URL
            response = requests.get(url)
            data = response.json()

            if "error" in data:
                self.result_label.setText(f"Error: {data['error']}")
            else:
                display_text = (
                    f"Symbol: {data['symbol']}\n"
                    f"Current Price: ${data['current_price']}\n"
                    f"Change: {data['price_change']}\n"
                    f"Recommendation: {data['recommendation']}\n"
                    f"Volume: {data['trading_volume']}"
                )
                self.result_label.setText(display_text)

                # Fetch historical stock data and plot chart
                self.fetchAndPlotChart(stock_symbol)

        except Exception as e:
            self.result_label.setText(f"Error fetching data: {str(e)}")

    def update_progress(self):
        current_value = self.progress_bar.value()
        if current_value < 100:
            self.progress_bar.setValue(current_value + 5)
        else:
            self.progress_timer.stop()

    def fetchAndPlotChart(self, stock_symbol):
        try:
            url = f"http://127.0.0.1:5000/api/stock/history?symbol={stock_symbol}"
            response = requests.get(url)
            history_data = response.json()

            dates = history_data.get("dates", [])
            prices = history_data.get("prices", [])

            if dates and prices:
                plt.figure(figsize=(6, 4))
                plt.plot(dates, prices, marker='o', linestyle='-', color='#00FFFF')
                plt.xlabel("Date", color='white')
                plt.ylabel("Stock Price ($)", color='white')
                plt.title(f"Stock Trend for {stock_symbol}", color='white')
                plt.xticks(rotation=45, color='white')
                plt.yticks(color='white')
                plt.grid(True, color='#555555')
                plt.gca().set_facecolor('#121212')
                plt.gcf().set_facecolor('#121212')

                buffer = BytesIO()
                plt.savefig(buffer, format="png", bbox_inches='tight')
                buffer.seek(0)

                pixmap = QPixmap()
                pixmap.loadFromData(buffer.getvalue())

                self.chart_label.setPixmap(pixmap)
            else:
                QMessageBox.warning(self, "Data Error", "No historical data available.")

        except Exception as e:
            QMessageBox.warning(self, "API Error", f"Failed to fetch historical data: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InvestmentApp()
    window.show()
    sys.exit(app.exec_())
