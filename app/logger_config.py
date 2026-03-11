import logging
import json
from flask import request, has_request_context

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if has_request_context():
            log_record["path"] = request.path
            log_record["method"] = request.method
            log_record["remote_addr"] = request.remote_addr

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_record)

logger = logging.getLogger("app")
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)