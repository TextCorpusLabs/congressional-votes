import const
import pathlib
import time
import urllib.request
import urllib.robotparser
import utils
import progressbar as pb
from argparse import ArgumentParser
from typeguard import typechecked

@typechecked
def get_list_of_votes(folder_out: pathlib.Path, session_start: int, session_end: int) -> None:
    """
    Get the list of votes from govtrack.us for the requested sessions (inclusive).

    Parameters
    ----------
    folder_out : pathlib.Path
        Folder to contain the downloaded documents
    session_start : int
        The session of Congress used to start the collection of information
    session_end : int
        The session of Congress used to end the collection of information
    """
    utils.ensure_empty_folder(folder_out)

    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(const.ROBOTS_GOVTRACK)
    rp.read()

    widgets = [ 'Retrieving Session # ', pb.Counter(), ' ', pb.Timer(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']')]
    with pb.ProgressBar(widgets = widgets) as bar:
        for session in range(session_start, session_end + 1):
            bar.update(session)
            url = const.URL_VOTE_LIST.format(session = session)
            if rp.can_fetch(const.USER_AGENT, url):
                time.sleep(rp.crawl_delay(const.USER_AGENT))
                __download_session(folder_out, session)
            else:
                print(f'robots.txt forbids url: {url}')

@typechecked
def __download_session(folder_out: pathlib.Path, session: int) -> None:
    """
    Get the list of votes from a single session.

    Parameters
    ----------
    folder_out : pathlib.Path
        Folder to contain the downloaded documents
    session : int
        The session in question
    """
    session_url = const.URL_VOTE_LIST.format(session = session)
    session_path = folder_out.joinpath(f'./{session}.json')
    req = urllib.request.Request(session_url, headers = {'User-Agent': const.USER_AGENT})
    try:
        with urllib.request.urlopen(req) as response:
            response_code = response.getcode()
            if response_code == 200:
                content = response.read()
                with open(session_path, 'wb') as session_path:
                    session_path.write(content)
            else:
                print(f'could not open ({response_code}) url: {session_url}')
    except urllib.error.HTTPError as e:
        print(f'could not open ({e.reason}) url: {session_url}')
    except urllib.error.URLError as e:
        print(f'could not open ({e.reason}) url: {session_url}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-out', '--folder-out',
        help = 'Folder to contain the downloaded documents',
        type = pathlib.Path,
        required = True)
    parser.add_argument(
        '-s', '--session-start',
        help = 'The session of Congress used to start the collection of information',
        type = int,
        required = True)
    parser.add_argument(
        '-e', '--session-end',
        help = 'The session of Congress used to end (inclusive) the collection of information',
        type = int,
        required = True)
    args = parser.parse_args()
    print(f'folder out: {args.folder_out}')
    print(f'session start: {args.session_start}')
    print(f'session end: {args.session_end}')
    get_list_of_votes(args.folder_out, args.session_start, args.session_end)
