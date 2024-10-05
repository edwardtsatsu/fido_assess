from src.controllers.transaction_controller import transaction_router


def register_routes(app):
    app.include_router(transaction_router, prefix="/transactions")
