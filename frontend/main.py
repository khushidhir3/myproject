import sys
import requests
import matplotlib.pyplot as plt
from io import BytesIO
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QProgressBar, QFrame
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

class InvestmentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Automated Investment Insights")
        self.setGeometry(50, 50, 1200, 600)
        self.setStyleSheet("background-color: #1A1A2E; color: #E0E0E0;")

        main_layout = QHBoxLayout()

        # Left section for insights
        left_layout = QVBoxLayout()

        self.symbol_input = QLineEdit(self)
        self.symbol_input.setPlaceholderText("Enter Stock Symbol (e.g., TSLA)")
        self.symbol_input.setStyleSheet(
            "background-color: #0F3460; color: #E94560; border-radius: 8px; padding: 8px; font-size: 16px;"
        )
        left_layout.addWidget(self.symbol_input)

        self.fetch_button = QPushButton("Get Investment Insights", self)
        self.fetch_button.setStyleSheet(
            "background-color: #E94560; color: #ffffff; border-radius: 8px; padding: 10px; font-size: 16px;"
            "border: 2px solid #D72323;"
        )
        self.fetch_button.clicked.connect(self.fetch_data)
        left_layout.addWidget(self.fetch_button)

        self.result_label = QLabel("Stock data will be displayed here", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.result_label.setStyleSheet(
            "background-color: #16213E; padding: 15px; border-radius: 10px; border: 2px solid #E94560; font-size: 16px;"
        )
        left_layout.addWidget(self.result_label)

        # Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet(
            "QProgressBar { border: 2px solid #E94560; border-radius: 8px; background: #0F3460; text-align: center; color: #ffffff; }"
            "QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #E94560, stop:1 #F08A5D); }"
        )
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setValue(0)
        left_layout.addWidget(self.progress_bar)

        # Right section for the chart
        right_layout = QVBoxLayout()

        self.chart_label = QLabel(self)
        self.chart_label.setStyleSheet("background-color: #16213E; padding: 10px; border-radius: 10px; border: 2px solid #E94560;")
        right_layout.addWidget(self.chart_label)

        # Adding sections to the main layout
        main_layout.addLayout(left_layout, 3)
        main_layout.addLayout(right_layout, 2)

        self.setLayout(main_layout)

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
            url = f"http://127.0.0.1:5000/api/stock?symbol={stock_symbol}"
            response = requests.get(url)
            data = response.json()

            if "error" in data:
                self.result_label.setText(f"Error: {data['error']}")
            else:
                display_text = (
                    f"<b>Symbol:</b> {data['symbol']}<br>"
                    f"<b>Current Price:</b> ${data['current_price']}<br>"
                    f"<b>Change:</b> {data['price_change']}<br>"
                    f"<b>Recommendation:</b> {data['recommendation']}<br>"
                    f"<b>Volume:</b> {data['trading_volume']}"
                )
                self.result_label.setText(display_text)
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
                plt.plot(dates, prices, marker='o', linestyle='-', color='#E94560')
                plt.xlabel("Date", color='white')
                plt.ylabel("Stock Price ($)", color='white')
                plt.title(f"Stock Trend for {stock_symbol}", color='white')
                plt.xticks(rotation=45, color='white')
                plt.yticks(color='white')
                plt.grid(True, color='#555555')
                plt.gca().set_facecolor('#1A1A2E')
                plt.gcf().set_facecolor('#1A1A2E')

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
