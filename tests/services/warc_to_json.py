import json
import utils
import sys

from warcio.archiveiterator import ArchiveIterator

URI_LIST = ('https://api.twitter.com/1.1/statuses/user_timeline.json',
    'https://api.twitter.com/1.1/search/tweets.json',
    'https://stream.twitter.com/1.1/statuses/filter.json')

def service_handler(input_filename, output_filename):
    tweets_list = []
    with open(input_filename, 'rb') as stream:
        for record in ArchiveIterator(stream):
            target_URI = record.rec_headers.get_header('WARC-Target-URI')
            if record.rec_type == 'response' and target_URI.startswith(URI_LIST):
                content = record.content_stream().read()
                content_json = json.loads(content)
                tweets_list += content_json

    with open(output_filename, 'w') as output_file:
        output_file.write(json.dumps(tweets_list))


print('warc_to_json.py starting...')
if __name__ == '__main__':
    input_filename = utils.get_input()
    output_filename = utils.get_output()
    service_handler(input_filename, output_filename)
