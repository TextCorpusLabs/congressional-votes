import csv
import json
import pathlib
import progressbar as pb
import utils as u
from argparse import ArgumentParser
from collections import namedtuple
from lxml import etree
from typeguard import typechecked

# declare all the named tuples up front
MetaVote = namedtuple('MetaVote', 'id chamber number time result name')

# Iterates over all the files in `folder_in`, extracting the useful metadata about the votes and saving it to `file_out`
@typechecked
def process_list_of_votes(folder_in: pathlib.Path, file_out: pathlib.Path) -> None:
    i = 1
    widgets = [ 'Processing File # ', pb.Counter(), ' ', pb.Timer(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']')]
    with pb.ProgressBar(widgets = widgets) as bar:
        with file_out.open('w', encoding = 'utf-8', newline = '') as file_out:
            writer = csv.writer(file_out, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)
            writer.writerow(['id', 'chamber', 'number', 'time', 'result', 'name'])
            for file_name in folder_in.iterdir():
                if file_name.suffix == '.json' and not file_name.name.startswith('_'):
                    bar.update(i)
                    i = i + 1
                    metavotes = __extract_metavotes(file_name)
                    for mv in metavotes:
                        writer.writerow([mv.id, mv.chamber, mv.number, mv.time, mv.result, mv.name])

# Transforms a single document by removing punction
@typechecked
def __extract_metavotes(file_name: pathlib.Path) -> list:
    with file_name.open('r') as tmp:
        data = json.load(tmp)
    results = [__extract_metavote(result) for result in data['results']]
    return results

# Transforms a element into a MetaVote
@typechecked
def __extract_metavote(text: str) -> MetaVote:
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

    return MetaVote(id, chamber, number, time, result, name)

if __name__ == '__main__':
    my_folder = pathlib.Path(__file__).parent
    parser = ArgumentParser()
    parser.add_argument(
        '-in', '--folder-in',
        help = 'Folder containing the raw files',
        type = u.readable_folder,
        default = str(my_folder.joinpath('../data/raw/list_of_votes')))
    parser.add_argument(
        '-out', '--file-out',
        help = 'List of role call votes',
        type = u.writable_file,
        default = str(my_folder.joinpath('../data/list_of_votes.csv')))
    args = parser.parse_args()    
    print(f'folder in: {args.folder_in}')
    print(f'file out: {args.file_out}')
    process_list_of_votes(args.folder_in, args.file_out)