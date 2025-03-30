import sys
import requests
import matplotlib.pyplot as plt
from io import BytesIO
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap

class InvestmentApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Automated Investment Insights")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        self.symbol_input = QLineEdit(self)
        self.symbol_input.setPlaceholderText("Enter Stock Symbol (e.g., TSLA)")
        layout.addWidget(self.symbol_input)

        self.fetch_button = QPushButton("Get Investment Insights", self)
        self.fetch_button.clicked.connect(self.fetch_data)
        layout.addWidget(self.fetch_button)

        self.result_label = QLabel("Stock data will be displayed here", self)
        layout.addWidget(self.result_label)

        self.chart_label = QLabel(self)  # Label to display the stock chart
        layout.addWidget(self.chart_label)

        self.setLayout(layout)

    def fetch_data(self):
        stock_symbol = self.symbol_input.text().strip().upper()
        if not stock_symbol:
            self.result_label.setText("Please enter a stock symbol!")
            return
        
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

    def fetchAndPlotChart(self, stock_symbol):
        try:
            url = f"http://127.0.0.1:5000/api/stock/history?symbol={stock_symbol}"
            response = requests.get(url)
            history_data = response.json()

            dates = history_data.get("dates", [])
            prices = history_data.get("prices", [])

            if dates and prices:
                plt.figure(figsize=(5, 3))
                plt.plot(dates, prices, marker='o', linestyle='-', color='b')
                plt.xlabel("Date")
                plt.ylabel("Stock Price ($)")
                plt.title(f"Stock Trend for {stock_symbol}")
                plt.xticks(rotation=45)
                plt.grid(True)

                buffer = BytesIO()
                plt.savefig(buffer, format="png")
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
