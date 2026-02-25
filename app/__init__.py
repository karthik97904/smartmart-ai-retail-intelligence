from flask import Flask
from config import get_config
from app.extensions import db, migrate, login_manager, socketio
from app.api.stress_routes import stress_bp
from app.api.risk_routes import risk_bp
from app.api.advisory_routes import advisory_bp
from app.api.simulation_routes import simulation_bp

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="../static")

    # Load configuration
    cfg = get_config()
    app.config.from_object(cfg)
    app.config["SQLALCHEMY_DATABASE_URI"] = cfg.SQLALCHEMY_DATABASE_URI

    # Initialize extensions (ONLY ONCE)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    socketio.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    # Import models for migration detection
    with app.app_context():
        from app import models

    # Register blueprints
    from app.api.auth_routes import auth_bp
    from app.api.ceo_routes import ceo_bp
    from app.api.hr_routes import hr_bp
    from app.api.health_routes import health_bp
    from app.api.market_routes import market_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(ceo_bp, url_prefix="/ceo")
    app.register_blueprint(hr_bp, url_prefix="/hr")
    app.register_blueprint(health_bp, url_prefix="/health")
    app.register_blueprint(market_bp)
    app.register_blueprint(stress_bp)
    app.register_blueprint(risk_bp, url_prefix="/ceo")
    app.register_blueprint(advisory_bp, url_prefix="/ceo")
    app.register_blueprint(simulation_bp)

    # Setup logging
    from app.utils.logger import setup_logger
    setup_logger(app)

    # Start scheduler
    from app.scheduler import start_scheduler
    start_scheduler(app)

    app.jinja_env.globals.update(enumerate=enumerate)

    return app