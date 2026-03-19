from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from core.models import db
import os

# Import Blueprints
from routes.auth import auth_bp
from routes.user import user_bp
from routes.quizzes import quizzes_bp
from routes.analytics import analytics_bp
from routes.notifications import notifications_bp

app = Flask(__name__)
# Enable CORS for all routes
CORS(app)

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'projexi.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Enable WAL mode for SQLite to handle concurrent requests better
with app.app_context():
    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        from sqlalchemy import event
        @event.listens_for(db.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA synchronous=NORMAL")
            cursor.close()

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(quizzes_bp, url_prefix='/api/quizzes')
app.register_blueprint(analytics_bp, url_prefix='/api')
app.register_blueprint(notifications_bp, url_prefix='/api/notifications')

# Specifically handle /api/search by registering the search function directly or the Blueprint again
@app.route('/api/search', methods=['GET'])
def global_search():
    from routes.quizzes import search_quizzes
    return search_quizzes()

# Special handling for search if needed at a specific level, but it's inside quizzes_bp as /api/quizzes/search
# Wait, original was /api/search. Let's adjust quizzes_bp or register it separately.
# Original /api/search was handled. Let's keep it consistent.

# Analytics had: /api/dashboard/stats and /api/analytics
# Quizzes had: /api/quizzes/upcoming, /api/quizzes/my-quizzes, /api/quizzes/<id>, /api/quizzes/<id>/submit, /api/quizzes/full, /api/quizzes (POST)
# Plus /api/search (handled in quizzes_bp)

if __name__ == '__main__':
    # Run server on port 3000
    print("Starting Projexi Backend on http://0.0.0.0:3000")
    app.run(host='0.0.0.0', port=3000, debug=True)
