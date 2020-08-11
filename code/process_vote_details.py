import csv
import pathlib
import utils
import progressbar as pb
import typing as t
from argparse import ArgumentParser
from collections import namedtuple
from typeguard import typechecked

VoteDetail = namedtuple('VoteDetail', 'id person state district vote name party')

@typechecked
def process_vote_details(folder_in: pathlib.Path, file_out: pathlib.Path) -> None:
    """
    Iterates over all the `CSV` files in `folder_in`, extracting the votes and saving them enmasse to `file_out`

    Parameters
    ----------
    folder_in : pathlib.Path
        Folder containing the raw CSV files
    file_out : pathlib.Path
        CSV file containing the aggregated data
    """
    bar_i = 1
    widgets = [ 'Aggregating CSV File # ', pb.Counter(), ' ', pb.Timer(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']')]
    with pb.ProgressBar(widgets = widgets) as bar:
        with open(file_out, 'w', encoding = 'utf-8', newline = '') as file_out:
            writer = csv.writer(file_out, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)
            writer.writerow(['id', 'person', 'state', 'district', 'vote', 'name', 'party'])
            for file_name in folder_in.iterdir():
                if file_name.suffix == '.csv' and not file_name.name.startswith('_'):
                    bar.update(bar_i)
                    bar_i = bar_i + 1
                    vote_details = __extract_vote_details(file_name)
                    for detail in vote_details:
                        writer.writerow([detail.id, detail.person, detail.state, detail.district, detail.vote, detail.name, detail.party])

@typechecked
def __extract_vote_details(file_in: pathlib.Path) -> t.Iterator[VoteDetail]:
    """
    The vote data downloaded from govtrack.us contains addtional headers.
    We want to get rid of that.

    Parameters
    ----------
    file_in : pathlib.Path
        Single vote CSV file
    """
    vote_id = utils.vote_path_to_id(file_in.stem)
    with open(file_in, 'r', encoding = 'utf-8', newline = '') as file_in:
        reader = csv.reader(file_in, delimiter = ',', quotechar = '"')
        next(reader, None)
        if __confirm_header(next(reader, None)):
            for row in reader:
                yield VoteDetail(vote_id, row[0], row[1], row[2], row[3], row[4], row[5])
        else:
            print(f'bad header: {vote_id}')

@typechecked
def __confirm_header(header: t.List[str]) -> bool:
    """
    Makes sure the header in the vote detail is in the expected order

    Parameters
    ----------
    header : list
        The header
    """
    return True \
        and len(header) == 6 \
        and header[0] == 'person' \
        and header[1] == 'state' \
        and header[2] == 'district' \
        and header[3] == 'vote' \
        and header[4] == 'name' \
        and header[5] == 'party'

if __name__ == '__main__':
    my_folder = pathlib.Path(__file__).parent
    parser = ArgumentParser()
    parser.add_argument(
        '-in', '--folder-in',
        help = 'Folder containing the raw CSV files',
        type = pathlib.Path,
        required = True)
    parser.add_argument(
        '-out', '--file-out',
        help = 'CSV file containing the aggregated data',
        type = pathlib.Path,
        required = True)
    args = parser.parse_args()    
    print(f'folder in: {args.folder_in}')
    print(f'file out: {args.file_out}')
    process_vote_details(args.folder_in, args.file_out)
