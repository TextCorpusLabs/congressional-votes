import pathlib
from shutil import rmtree
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
def ensure_empty_folder(folder_path: pathlib.Path) -> pathlib.Path:
    """
    Makes sure `folder_path` is a folder and is empty.
    If the path is a file, it will be deleted and a folder created.
    If the path is a folder, the contents will be deleted.
    
    Parameters
    ----------
    folder_path : pathlib.Path
        The path to construct/cleanup
    """
    if(folder_path.exists()):
        if folder_path.is_dir():
            rmtree(folder_path)
        else:
            folder_path.unlink()
    folder_path.mkdir(parents = True)
    return folder_path