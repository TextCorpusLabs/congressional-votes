import const
import csv
import pathlib
import time
import urllib.request
import urllib.robotparser
import utils
import progressbar as pb
from argparse import ArgumentParser
from typeguard import typechecked

@typechecked
def get_vote_details(file_in: pathlib.Path, folder_out: pathlib.Path) -> None:
    """
    Get the details of each vote

    Parameters
    ----------
    file_in : pathlib.Path
        File containing the list of vote
    folder_out : pathlib.Path
        Folder to contain the downloaded vote details
    """
    utils.ensure_empty_folder(folder_out)

    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(const.ROBOTS_GOVTRACK)
    rp.read()

    bar_i = 1
    widgets = [ 'Retrieving Details # ', pb.Counter(), ' ', pb.Timer(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']')]
    with pb.ProgressBar(widgets = widgets) as bar:
        with open(file_in, 'r', encoding = 'utf-8', newline = '') as file_in:
            reader = csv.reader(file_in, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)
            next(reader, None)
            for row in reader:
                bar.update(bar_i)
                bar_i = bar_i + 1
                url = const.URL_VOTE_DETAILS.format(vote_id = row[0])
                if rp.can_fetch(const.USER_AGENT, url):
                    time.sleep(rp.crawl_delay(const.USER_AGENT))
                    __download_vote_details(folder_out, row[0])
                else:
                    print(f'robots.txt forbids url: {url}')

@typechecked
def __download_vote_details(folder_out : pathlib.Path, vote_id: str) -> None:
    """
    Get the csv export of the vote details from a single vote.

    Parameters
    ----------
    folder_out : pathlib.Path
        Folder to contain the downloaded documents
    vote_id : str
        The vote's id, {congress}-{year}/{vote #}
    """
    detail_url = const.URL_VOTE_DETAILS.format(vote_id = vote_id)
    detail_path = folder_out.joinpath(f'./{utils.vote_id_to_path(vote_id)}.csv')
    req = urllib.request.Request(detail_url, headers = {'User-Agent': const.USER_AGENT})
    try:
        with urllib.request.urlopen(req) as response:
            response_code = response.getcode()
            if response_code == 200:
                content = response.read()
                with open(detail_path, 'wb') as detail_path:
                    detail_path.write(content)
            else:
                print(f'could not open ({response_code}) url: {detail_url}')
    except urllib.error.HTTPError as e:
        print(f'could not open ({e.reason}) url: {detail_url}')
    except urllib.error.URLError as e:
        print(f'could not open ({e.reason}) url: {detail_url}')

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-in', '--file-in',
        help = 'File containing the list of votes',
        type = pathlib.Path,
        required = True)
    parser.add_argument(
        '-out', '--folder-out',
        help = 'Folder to contain the downloaded vote details',
        type = pathlib.Path,
        required = True)
    args = parser.parse_args()
    print(f'file in: {args.file_in}')
    print(f'folder out: {args.folder_out}')
    get_vote_details(args.file_in, args.folder_out)
