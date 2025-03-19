from flask import Blueprint, Response
from flask import current_app as app
import traceback

errors = Blueprint("errors", __name__)

@errors.app_errorhandler(Exception)
def error_handler(e):
    app.logger.error(f"An internal error occurred in the handling of the ENI message. {traceback.format_exc()}")
    return Response(f"An internal error occurred in the handling of the ENI message.", status=500)