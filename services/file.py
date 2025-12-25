import os


def read_file(file_path: str) -> str:
    file_path = os.path.expanduser(file_path)

    with open(file_path, "r") as f:
        return f.read()


def save_file(file_path: str, content: str) -> None:
    file_path = os.path.expanduser(file_path)
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)