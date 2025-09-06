import os

from src.application.services.file_manager import File, FileManagerInterface


class FileManager(FileManagerInterface):
    def find_by_name(self, folder: str, file_name: str) -> File | None:
        for root, _, files in os.walk(folder):
            if file_name in files:
                file_path = os.path.join(root, file_name)

                with open(file_path, "rb") as f:
                    return File(name=file_name, content=f.read())

        return None

    def save(self, folder: str, file: File) -> None:
        os.makedirs(folder, exist_ok=True)

        with open(f"{folder}/{file.name}", "wb") as f:
            f.write(file.content)
