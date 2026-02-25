

from flask import jsonify

from app.errors.exceptions import AppError


def register_error_handlers(app):


    @app.errorhandler(AppError)
    def bad_request_error(error):
        return jsonify({
            'error': error.message,
            'status': error.status_code
        }), error.status_code

    
    # Catch Flask's built-in 404 (e.g., hitting a URL that doesn't exist)
    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({
            'error': "Endpoint not found",
            'status': 404
        }), 404

    # Catch Flask's built-in 405 (e.g., GET on a POST-only route)
    @app.errorhandler(405)
    def handle_405(error):
        return jsonify({
            'error': 'Method not allowed',
            'status': 405
        }), 405

    # Catch everything else (unexpected crashes)
    @app.errorhandler(500)
    def handle_500(error):
        return jsonify({
            'error': 'Internal server error',
            'status': 500
        }), 500