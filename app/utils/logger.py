import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(app):
    os.makedirs("logs", exist_ok=True)

    log_level = getattr(logging, app.config.get("LOG_LEVEL", "INFO"))

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )

    file_handler = RotatingFileHandler(
        "logs/smartmart.log", maxBytes=5 * 1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    app.logger.setLevel(log_level)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)

    app.logger.info("SmartMart logger initialized.")