import pathlib
import time
import progressbar as pb
import urllib.request
import urllib.robotparser

# setup main variables
domain = 'govtrack.us'
data_path = '/congress/votes?session={session}&faceting=false&do_search=1'
session_start = 274 # 1990
session_end = 304 # 2020
download_root = pathlib.Path(__file__).parent.joinpath('../data/raw/list_of_votes')
user_agent = 'MindMimicLabs/1.0'

# make sure our folder exists
download_root.mkdir(parents = True, exist_ok = True)

# honor robots.txt protocal
rp = urllib.robotparser.RobotFileParser()
rp.set_url(f'https://{domain}/robots.txt')
rp.read()

# go over all the sessions that are in-scope
for session in range(session_start, session_end + 1):

    # make the url + download path for this session
    data_url = f'https://{domain}{data_path}'.format(session = session)
    download_path = download_root.joinpath(f'./{session}.json')

    if rp.can_fetch(user_agent, data_url):

        # dont crawl too fast
        delay = rp.crawl_delay(user_agent)
        time.sleep(delay)

        # make the request
        req = urllib.request.Request(data_url, headers = {'User-Agent': user_agent})
        try:
            # get the data
            response = urllib.request.urlopen(req)
            response_code = response.getcode()

            # if the request is good save it
            if response_code == 200:
                content = response.read()
                with open(download_path, 'wb') as download_path:
                    download_path.write(content)
                response.close()
            else:
                print(f'could not open [{response_code}] url: {data_url}')

        except urllib.error.HTTPError as e:
            print(f'could not open [{response_code}] url: {data_url}')
        except urllib.error.URLError as e:
            print(f'could not open [{e.reason}] url: {data_url}')
    else:
        print(f'cannot scrap usl: {data_url}')
