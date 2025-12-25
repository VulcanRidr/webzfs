#!/usr/bin/env python

import sys
from typing import Any

import typer
import uvicorn

cli = typer.Typer()


@cli.command()
def runserver(host: str = "127.0.0.1", port: int = 8000) -> None:
    """
    Run development server
    """

    uvicorn.run("config.asgi:app", reload=True, host=host, port=port)


@cli.command()
def shell() -> None:
    """
    Enter interactive python shell
    """
    import code

    ctx: dict[str, Any] = {}

    banner = f"Python {sys.version} on {sys.platform}"
    code.interact(banner, local=ctx)


if __name__ == "__main__":
    cli()
