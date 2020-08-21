import csv
import pathlib
import progressbar as pb
import typing as t
from argparse import ArgumentParser
from collections import namedtuple
from lxml import etree
from typeguard import typechecked

Legislation = namedtuple('Legislation', 'id title sponsor cosponsors status details')

@typechecked
def process_list_of_legislation(folder_in: pathlib.Path, file_out: pathlib.Path) -> None:
    """
    Iterates over all the `HTML` files in `folder_in`, extracting the useful metadata about the role call votes and saving it to `file_out`

    Parameters
    ----------
    folder_in : pathlib.Path
        Folder containing the raw HTML files
    file_out : pathlib.Path
        CSV file containing the parsed role call votes
    """
    bar_i = 1
    widgets = [ 'Processing HTML File # ', pb.Counter(), ' ', pb.Timer(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']')]
    with pb.ProgressBar(widgets = widgets) as bar:
        with open(file_out, 'w', encoding = 'utf-8', newline = '') as file_out:
            writer = csv.writer(file_out, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)
            writer.writerow(['id', 'title', 'sponsor', 'cosponsors', 'status', 'details'])
            for file_name in folder_in.iterdir():
                if file_name.suffix == '.html' and not file_name.name.startswith('_'):
                    bar.update(bar_i)
                    bar_i = bar_i + 1
                    for leg in __parse_legislative_list(file_name):
                        writer.writerow([leg.id, leg.title, leg.sponsor, leg.cosponsors, leg.status, leg.details])

@typechecked
def __parse_legislative_list(file_name: pathlib.Path) -> t.List[Legislation]:
    """
    Transforms a single HTML file into a list of metadata about the legislation.

    Parameters
    ----------
    file_name : pathlib.Path
        The single HTML file
    """
    with open(file_name, 'r', encoding = 'utf-8') as fp:
        tree = etree.parse(fp, etree.HTMLParser())
    elms = "//div[@class='search-row']//li[@class='expanded']"
    elms = tree.xpath(elms)
    results = [__parse_legislation(elm) for elm in elms]
    return results

@typechecked
def __parse_legislation(root: etree.Element) -> Legislation:
    """
    Transforms a HTML element into Legislation

    Parameters
    ----------
    text : str
        The HTML to parse
    """
    billid = ".//span[@class='result-heading']/a"
    title = ".//span[@class='result-title']"
    sponsor = ".//span[@class='result-item'][1]/a[1]"
    cosponsors = ".//span[@class='result-item'][1]/a[2]"
    status = ".//ol[@class='stat_leg']/li"
    details = ".//span[@class='result-heading']/a"

    get_text = lambda x: x.text.strip()
    get_href = lambda x: x.attrib['href']

    billid = __value_or_none(root.xpath(billid), get_text)
    title = __value_or_none(root.xpath(title), get_text)
    sponsor = __value_or_none(root.xpath(sponsor), get_text)
    cosponsors = __value_or_none(root.xpath(cosponsors), get_text)
    status = ';'.join([e.text for e in root.xpath(status)])
    status = status if len(status) > 0 else None
    details = __value_or_none(root.xpath(details), get_href)

    return Legislation(billid, title, sponsor, cosponsors, status, details)

@typechecked
def __value_or_none(root: t.List[etree.Element], func: t.Callable) -> t.Optional[str]:
    """
    Applies a lambda function to the only element in the list
    """
    if len(root) == 0:
        return None
    elif len(root) > 1:
        raise Exception('Too many elements')
    else:
        return func(root[0])

if __name__ == '__main__':
    my_folder = pathlib.Path(__file__).parent
    parser = ArgumentParser()
    parser.add_argument(
        '-in', '--folder-in',
        help = 'Folder containing the raw HTML files',
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
    process_list_of_legislation(args.folder_in, args.file_out)
