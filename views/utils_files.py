from typing import Annotated, Any, List, Dict
import os
from pathlib import Path

from fastapi import APIRouter, Depends, Form, Request

from auth.dependencies import get_current_user
from config.templates import templates
from services.file import read_file, save_file
from services.audit_logger import audit_logger

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("utils/files/index.jinja", {"request": request})


@router.post("/list")
def list_files(request: Request, directory: Annotated[str, Form()], current_user: str = Depends(get_current_user)):
    try:
        directory_path = Path(os.path.expanduser(directory))
        if not directory_path.exists() or not directory_path.is_dir():
            audit_logger.log_directory_list(user=current_user, directory_path=directory, success=False, error="Directory does not exist or is not a directory")
            return templates.TemplateResponse(
                "partials/error.jinja", 
                {"request": request, "error": f"Directory {directory} does not exist or is not a directory"}
            )
        
        files = []
        for item in directory_path.iterdir():
            try:
                # Skip broken symlinks and inaccessible files
                is_dir = item.is_dir()
                if is_dir:
                    size = 0
                    modified = item.stat().st_mtime
                else:
                    stat_info = item.stat()
                    size = stat_info.st_size
                    modified = stat_info.st_mtime
                
                files.append({
                    "name": item.name,
                    "path": str(item),
                    "is_dir": is_dir,
                    "size": size,
                    "modified": modified
                })
            except (OSError, PermissionError):
                # Skip files we can't access (broken symlinks, permission denied, etc.)
                continue
        
        audit_logger.log_directory_list(user=current_user, directory_path=directory)
        return templates.TemplateResponse(
            "utils/files/list.jinja",
            {"request": request, "files": files, "directory": directory}
        )
    except Exception as exc:
        audit_logger.log_directory_list(user=current_user, directory_path=directory, success=False, error=str(exc))
        return templates.TemplateResponse(
            "partials/error.jinja", {"request": request, "error": str(exc)}
        )


@router.post("/read")
def read(request: Request, file_path: Annotated[str, Form()], current_user: str = Depends(get_current_user)):
    try:
        content = read_file(file_path)
        audit_logger.log_file_read(user=current_user, file_path=file_path)
    except Exception as exc:
        audit_logger.log_file_read(user=current_user, file_path=file_path, success=False, error=str(exc))
        return templates.TemplateResponse(
            "partials/error.jinja", {"request": request, "error": str(exc)}
        )

    return templates.TemplateResponse(
        "utils/files/edit.jinja",
        {"request": request, "content": content, "file_path": file_path},
    )


@router.post("/save")
def save(
    request: Request, file_path: Annotated[str, Form()], content: Annotated[str, Form()],
    current_user: str = Depends(get_current_user)
):
    context: dict[str, Any] = {"content": content, "file_path": file_path}

    try:
        save_file(file_path, content)
        audit_logger.log_file_write(user=current_user, file_path=file_path)
    except Exception as exc:
        audit_logger.log_file_write(user=current_user, file_path=file_path, success=False, error=str(exc))
        context["error"] = str(exc)
    else:
        context["success"] = True

    return templates.TemplateResponse(
        "utils/files/edit.jinja", {"request": request, **context}
    )
