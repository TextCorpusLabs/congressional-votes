import pathlib
from typeguard import typechecked

# makes sure our parameters are good
@typechecked
def readable_folder(folder_path: str) -> pathlib.Path:
    folder_path = pathlib.Path(folder_path).resolve()
    if not folder_path.exists():
        raise FileNotFoundError(str(folder_path))
    elif not folder_path.is_dir():
        raise NotADirectoryError(str(folder_path))
    return folder_path

@typechecked
def writable_folder(folder_path: str) -> pathlib.Path:
    folder_path = pathlib.Path(folder_path).resolve()
    if not folder_path.exists():
        folder_path.mkdir(parents = True)
    elif not folder_path.is_dir():
        raise NotADirectoryError(str(folder_path))
    return folder_path

@typechecked
def writable_file(file_path: str) -> pathlib.Path:
    file_path = pathlib.Path(file_path).resolve()
    folder_path = file_path.parent
    if not folder_path.exists():
        folder_path.mkdir(parents = True)
    elif not folder_path.is_dir():
        raise NotADirectoryError(str(folder_path))
    return file_path