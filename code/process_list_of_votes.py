import csv
import json
import pathlib
import progressbar as pb
import typing as t
from argparse import ArgumentParser
from collections import namedtuple
from lxml import etree
from typeguard import typechecked

RoleCallVote = namedtuple('RoleCallVote', 'id chamber number time result name')

@typechecked
def process_list_of_votes(folder_in: pathlib.Path, file_out: pathlib.Path) -> None:
    """
    Iterates over all the `JSON` files in `folder_in`, extracting the useful metadata about the role call votes and saving it to `file_out`

    Parameters
    ----------
    folder_in : pathlib.Path
        Folder containing the raw JSON files
    file_out : pathlib.Path
        CSV file containing the parsed role call votes
    """
    bar_i = 1
    widgets = [ 'Processing JSON File # ', pb.Counter(), ' ', pb.Timer(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']')]
    with pb.ProgressBar(widgets = widgets) as bar:
        with open(file_out, 'w', encoding = 'utf-8', newline = '') as file_out:
            writer = csv.writer(file_out, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)
            writer.writerow(['id', 'chamber', 'number', 'time', 'result', 'name'])
            for file_name in folder_in.iterdir():
                if file_name.suffix == '.json' and not file_name.name.startswith('_'):
                    bar.update(bar_i)
                    bar_i = bar_i + 1
                    role_call_votes = __parse_role_call_votes(file_name)
                    for rcv in role_call_votes:
                        writer.writerow([rcv.id, rcv.chamber, rcv.number, rcv.time, rcv.result, rcv.name])

@typechecked
def __parse_role_call_votes(file_name: pathlib.Path) -> t.List[RoleCallVote]:
    """
    Transforms a single JSON file into a list of metadata about role call votes.
    The JSON file contains a collextion of HTML elements.
    Each one of those HTML emements describes a single role call vote.

    Parameters
    ----------
    file_name : pathlib.Path
        The single JSON file
    """
    with open(file_name, 'r') as tmp:
        data = json.load(tmp)
    results = [__parse_role_call_vote(result) for result in data['results']]
    return results

@typechecked
def __parse_role_call_vote(text: str) -> RoleCallVote:
    """
    Transforms a HTML element into a RoleCallVote

    Parameters
    ----------
    text : str
        The HTML to parse
    """
    root = etree.fromstring(text)
    elm1 = "./div[2]/div[1]/div[1]/div[1]/a[1]"
    elm2 = "./div[2]/div[1]/div[2]/div[1]/div[1]/span[1]"
    elm3 = "./div[2]/div[1]/div[2]/div[1]/div[2]/span[1]"
    elm4 = "./div[2]/div[1]/div[2]/div[2]/div[1]/span[1]"    
    elm1 = root.find(elm1)
    elm2 = root.find(elm2)
    elm3 = root.find(elm3)
    elm4 = root.find(elm4)

    id = '/'.join(elm1.attrib['href'].split('/')[3:])
    chamber = elm2.tail.split('#')[0].strip().split(' ')[0]
    number = elm2.tail.split('#')[1].strip()
    time = elm3.tail.strip()
    result = elm4.tail.strip()
    name = elm1.text.strip().replace('\n', ' ')

    return RoleCallVote(id, chamber, number, time, result, name)

if __name__ == '__main__':
    my_folder = pathlib.Path(__file__).parent
    parser = ArgumentParser()
    parser.add_argument(
        '-in', '--folder-in',
        help = 'Folder containing the raw JSON files',
        type = pathlib.Path,
        required = True)
    parser.add_argument(
        '-out', '--file-out',
        help = 'CSV file containing the parsed role call votes',
        type = pathlib.Path,
        required = True)
    args = parser.parse_args()    
    print(f'folder in: {args.folder_in}')
    print(f'file out: {args.file_out}')
    process_list_of_votes(args.folder_in, args.file_out)