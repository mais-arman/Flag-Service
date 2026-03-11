from flask import jsonify
from werkzeug.exceptions import HTTPException
from app import db
from app.logger_config import logger


def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exceptions(e):

        if isinstance(e, HTTPException):
            status_code = e.code
            message = getattr(e, "description", str(e))
            error_name = getattr(e, "name", e.__class__.__name__)
        else:
            status_code = getattr(e, "code", 500)
            message = str(e)
            error_name = e.__class__.__name__

        try:
            db.session.rollback()
        except Exception:
            pass

        response = {
            "status": "error",
            "error": error_name,
            "message": message
        }

        logger.error(response, exc_info=e)
        return jsonify(response), status_code