from datetime import datetime;
import json;
import os;
import sys;

# Constants.
QUERY_TYPE = ['hashtag', 'username'];

# Validate command-line arguments.
args = sys.argv[1:];
if (len(args) != 3):
    print('Usage: {} <FILENAME> <{}> <QUERY>'.format(sys.argv[0], ','.join(QUERY_TYPE)));
    sys.exit(1);

filename = args[0];
search_type = args[1].lower();
query = args[2].lower();

# Check that file exists and read from it.
if (not os.path.isfile(filename)):
    print('File "{}" not found'.format(filename));
    sys.exit(1);

if (search_type not in QUERY_TYPE):
    print('Query type must be one of', QUERY_TYPE);
    sys.exit(1);

read_start = datetime.now();
with open(filename, 'r') as tweet_file:
    tweet_data = tweet_file.read();
read_end = datetime.now();
print('Read time:', read_end - read_start, 'ms');

# Parse into json.
json_start = datetime.now();
tweet_json = json.loads(tweet_data);
json_end = datetime.now();
print('JSON parse time:', json_end - json_start, 'ms');

# Conduct the query.
query_start = datetime.now();
if (search_type == 'hashtag'):
    hashtag_query = '#{}'.format(query);
    results = [t for t in tweet_json if hashtag_query in t['text']];
elif (search_type == 'username'):
    results = [t for t in tweet_json if t['from_user'].lower() == query];
else:
    print('Unimplemented query type');
    sys.exit(1);
query_end = datetime.now();
print('Query time:', query_end - query_start);

# Output the results.
print('Result count:', len(results))
print();
for t in results:
    print(t);
    print();
