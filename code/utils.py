import pathlib
from shutil import rmtree
from typeguard import typechecked

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

@typechecked
def vote_id_to_path(vote_id: str) -> str:
    """
    The vote id in the files has a '/' in it.
    This is an invalid character for file names.
    Convert it to a '-'

    Parameters
    ----------
    vote_id: str
        The vote id
    """
    return vote_id.replace('/', '-')

@typechecked
def vote_path_to_id(vote_path: str) -> str:
    """
    The inverse of `vote_id_to_path()`

    Parameters
    ----------
    vote_path: str
        The vote path
    """
    tmp = vote_path.split('-')
    if len(tmp) != 3:
        raise Exception(f'Bad format {vote_path}')
    return f'{tmp[0]}-{tmp[1]}/{tmp[2]}'
