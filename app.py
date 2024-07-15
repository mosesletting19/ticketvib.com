from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from models import db, Payment, Event
from flask_migrate import Migrate
from routes.payments import payments_bp
from routes.events import events_bp
from routes.index import index_bp
from utils.email_utils import send_email_with_qr_code

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    CORS(app)

    db.init_app(app)
    migrate = Migrate(app, db)  # Initialize Flask-Migrate

    app.register_blueprint(payments_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(index_bp)

    

    @app.route('/send_emails', methods=['POST'])
    def send_emails():
        payments = Payment.query.all()
        event = request.json
        for payment in payments:
            send_email_with_qr_code(payment.name, payment.email, event)
        return jsonify({'message': 'Emails sent successfully'}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(port=Config.PORT, debug=True)
