import const
import pathlib
import time
import requests
import protego
import utils
import progressbar as pb
from argparse import ArgumentParser
from lxml import etree
from typeguard import typechecked

@typechecked
def get_list_of_legislation(folder_out: pathlib.Path, congress: int) -> None:
    """
    Get the list of legislation from a specified Congress.

    Parameters
    ----------
    folder_out : pathlib.Path
        Folder to contain the downloaded documents
    congress : int
        The Congress in question
    """
    with requests.Session() as session:
        session.headers['User-Agent'] = const.USER_AGENT

        print("Complying with robots.txt...")
        rtxt = __setup_robots_txt(session)

        print('Retrieving page 1...')
        if rtxt.can_fetch(const.USER_AGENT, const.URL_VOTE_LIST):
            page_1_file = __download_page(session, congress, 1, folder_out)
            total_pages = __get_total_pages(page_1_file)

            widgets = [ 'Retrieving Page # ', pb.Counter(), ' ', pb.Bar(marker = '.', left = '[', right = ']'), ' ', pb.ETA()]
            with pb.ProgressBar(widgets = widgets, max_value = total_pages) as bar:
                for page in range(2, total_pages + 1):
                    bar.update(page)
                    time.sleep(max(.5, rtxt.crawl_delay(const.USER_AGENT)))
                    __download_page(session, congress, page, folder_out)
        else:
            print(f'robots.txt forbids url: {const.URL_VOTE_LIST}')

@typechecked
def __setup_robots_txt(session: requests.Session) -> protego.Protego:
    """
    Gets the robots.txt from Congress and makes our parser

    Parameters
    ----------
    session: requests.Session
        The browser session
    """
    with session.get(const.ROBOTS) as response:
        rtxt = protego.Protego.parse(response.text)
    return rtxt

@typechecked
def __get_total_pages(page_path: pathlib.Path) -> int:
    """
    Pulls out the total number of pages for a single Congress

    Parameters
    ----------
    page_path : pathlib.Path
        The path to page 1
    """
    with open(page_path, 'r', encoding = 'utf-8') as fp:
        tree = etree.parse(fp, etree.HTMLParser())
    node = tree.find("//div[@class='pagination']/span[@class='results-number']")
    text = node.text.strip()
    return int(text.split()[1])    

@typechecked
def __download_page(session: requests.Session, congress: int, page: int, folder_out: pathlib.Path) -> pathlib.Path:
    """
    Get a single page worth of bills.

    Parameters
    ----------
    session: requests.Session
        The browser session
    congress : int
        The Congress in question
    page : int
        The Congress in question
    folder_out : pathlib.Path
        Folder to contain the downloaded documents
    """

    params = {
        'congresses' : congress,
        'pageSize' : 250,
        'page' : page,        
        'q' : '{"type":"bills"}',
        'submitted' : 'Submitted'
    }
    result_path = folder_out.joinpath(f'./bill_list.{congress}.{page}.html')
    with session.get(const.URL_VOTE_LIST, params = params) as response:
        if response.status_code == 200:
            with open(result_path, 'w', encoding = 'utf-8') as fp:
                fp.write(response.text)
            return result_path
        else:
            print(f'could not open ({response.status_code}) url: {page_url}')

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-out', '--folder-out',
        help = 'Folder to contain the downloaded documents',
        type = pathlib.Path,
        required = True)
    parser.add_argument(
        '-c', '--congress',
        help = 'The Congress in question',
        type = int,
        required = True)
    args = parser.parse_args()
    print(f'folder out: {args.folder_out}')
    print(f'congress start: {args.congress}')
    get_list_of_legislation(args.folder_out, args.congress)

