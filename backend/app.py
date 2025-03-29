from flask import Flask
from flask_cors import CORS
from api.routes import investment_blueprint

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Register API routes
app.register_blueprint(investment_blueprint)

@app.route("/")
def home():
    return {"message": "Investment Insights Bot API Running!"}

if __name__ == '__main__':
    app.run(debug=True)
