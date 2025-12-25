from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from auth.exceptions import AuthenticationFailed
from config.settings import settings
from views import router


def create_app() -> FastAPI:
    app = FastAPI(debug=settings.DEBUG)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(router)

    @app.exception_handler(AuthenticationFailed)
    def redirect_to_login(request: Request, exc: AuthenticationFailed) -> Response:
        return RedirectResponse("/login/")

    return app
