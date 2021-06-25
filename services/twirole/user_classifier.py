# python Libraries

from __future__ import print_function

import warnings
warnings.filterwarnings("ignore")

# basic
import os
import glob
import re
import sys
import csv
import json
import pickle
import argparse
import importlib
import sklearn
from twarc import Twarc
from termcolor import colored
if sys.version_info[0] == 2:
    import urllib
elif sys.version_info[0] == 3:
    from urllib.request import urlretrieve

importlib.reload(sys)
#sys.setdefaultencoding('utf-8')
sys.path.append(os.path.abspath(os.path.join('..', 'twirole/Twirole')))

# NLTK
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.data.path.append('../data/lib/')
nltk.download('stopwords')
nltk.download('wordnet')

# trational Classifier
import pandas as pd
import numpy as np

# deep learning
from PIL import Image
import torch
import torch.nn as nn
from torchvision import models, transforms
from torch.autograd import Variable

# self-defined
import _cmu_tagger
import _score_calculator as sc

# Twarc Configuration
consumer_key = 'zSOrDcJVZF3Vwgrnb7snbVuwt'
consumer_secret = 'PMLDJpdrfgQXpWJ2YctUpsRNM4wyGzWbWrQWXMqNOQWvcAJ8C0'
access_token = '1050390502909124608-u1eWR4ABUikgYBOBAiCnjfJCWWATo8'
access_token_secret = 'HKV7aDEo8uVNjL0rsWHDNhYU3ZfNwoH75CCOceUPq7RDx'


class ResNet18(nn.Module):
    def __init__(self):
        super(ResNet18, self).__init__()
        self.resnet = models.resnet18(pretrained=False)

        self.resnet.fc = nn.Linear(512, 3)

    def forward(self, x):
        x = self.resnet(x)
        return x


def process_raw_tweets(tweet_raw_lines):
    tweet_text_lines = tweet_raw_lines

    # Remove Retweet Tags
    tweet_text_lines = [' '.join(re.sub("(RT @\S+)", " ", tweet_text_line).split()) for tweet_text_line in tweet_text_lines]

    # Remove Mentions
    tweet_text_lines = [' '.join(re.sub("(@\S+)", " ", tweet_text_line).split()) for tweet_text_line in tweet_text_lines]

    # Remove URLs
    tweet_text_lines = [' '.join(re.sub("(https?:\/\/t\.co\S*)", " ", tweet_text_line).split()) for tweet_text_line in tweet_text_lines]

    # Extract Taggers
    tweet_tagger_lines = _cmu_tagger.runtagger_parse(tweet_text_lines, run_tagger_cmd="java -XX:ParallelGCThreads=2 -Xmx500m -jar ark-tweet-nlp-0.3.2.jar")

    # Filter out Taggers + Remove Stopwords + Remove Keywords + Format words + Lemmatization + Lowercase
    tweet_processed = []

    stop_words = set(stopwords.words('english'))

    wordnet_lemmatizer = WordNetLemmatizer()

    for tweet_tagger_line in tweet_tagger_lines:

        tweet_tagger_processed = []

        for tweet_tagger in tweet_tagger_line:
            if tweet_tagger[1] in ['N', 'V', 'A', 'E', 'R', '#']:
                tagger = str(tweet_tagger[0]).lower().strip(string.punctuation)
                if tagger not in stop_words:
                    if tweet_tagger[1] == 'V':
                        tagger_lem = wordnet_lemmatizer.lemmatize(tagger, 'v')
                    else:
                        tagger_lem = wordnet_lemmatizer.lemmatize(tagger)
                    if len(tagger_lem) > 3:
                        tweet_tagger_processed.append(tagger_lem)

        tweet_tagger_processed = ' '.join(tweet_tagger_processed)

        tweet_processed.append(tweet_tagger_processed)

    # Remove Duplicates
    tweet_processed = list(set(tweet_processed))

    return tweet_processed


def user_info_crawler(screen_name, user_dir, user_profile_f, user_profileimg_f, user_tweets_f,user_clean_tweets_f):
    try:
            # crawl user profile
            #sys.stdout.write('Get user profile >> ')
            # sys.stdout.flush()
        t = None

        if not os.path.exists(os.path.join(user_dir, user_profile_f)):

            t = Twarc(consumer_key, consumer_secret, access_token, access_token_secret)

            user_profile_data = t.user_lookup(ids=[screen_name], id_type="screen_name")

            for user_profile in user_profile_data:
                with open(os.path.join(user_dir, user_profile_f), 'w') as outfile:
                    json.dump(user_profile, outfile)

        # crawl user profile image
        #sys.stdout.write('Get user profile image >> ')
        # sys.stdout.flush()
        with open(os.path.join(user_dir, user_profile_f), 'r') as rf:

            user_profile_json = json.load(rf)

            if not os.path.exists(os.path.join(user_dir, user_profileimg_f)):

                # extract user profile image url
                user_profileimg_url = user_profile_json['profile_image_url']

                def image_converter(user_profileimg_url):
                    tmp_file = '/mnt/camelot-cs5604/twt/user/tmp' + user_profileimg_url[-4:]
                    if sys.version_info[0] == 2:
                        urlretrieve(user_profileimg_url, tmp_file)
                    elif sys.version_info[0] == 3:
                        urlretrieve(user_profileimg_url, tmp_file)
                    from PIL import Image
                    im = Image.open(tmp_file)
                    rgb_im = im.convert('RGB')
                    rgb_im.save(os.path.join(user_dir, user_profileimg_f))
                    os.remove(tmp_file)

                if user_profileimg_url:
                    user_profileimg_url = user_profileimg_url.replace('_normal', '_bigger')

                image_converter(user_profileimg_url)

        # crawl user tweets
        # sys.stdout.write('Get user tweets >> ')
        # sys.stdout.flush()
        if not os.path.exists(os.path.join(user_dir, user_tweets_f)):
            t = Twarc(consumer_key, consumer_secret, access_token, access_token_secret)
            user_timeline_data = t.timeline(screen_name=screen_name)
            with open(os.path.join(user_dir, user_tweets_f), 'a') as outfile:
                for user_timeline in user_timeline_data:
                    json.dump(user_timeline, outfile)
                    outfile.write('\n')

        # clean user tweets
        #sys.stdout.write('Clean user tweets \n')
        # sys.stdout.flush()
        if not os.path.exists(os.path.join(user_dir, user_clean_tweets_f)):
            tweet_raw_lines = []
            with open(os.path.join(user_dir, user_tweets_f), 'r') as rf:
                for line in rf:
                    tweet_raw_lines.append(json.loads(line)['full_text'])

            clean_tweets = process_raw_tweets(tweet_raw_lines)

            with open(os.path.join(user_dir, user_clean_tweets_f), 'w') as wf:
                for tweet in clean_tweets:
                    if len(tweet) > 0:
                        wf.write(tweet + '\n')
            wf.close()

        return user_profile_json

    except Exception as e:
        #print(e)
        print("Could not predict user's role. Check account info, few tweets, incorrect image format...")
        #sys.exit(1)


def role_classifier(screen_name):
    try:

        user_dir = '/mnt/camelot-cs5604/twt/user'

        user_profile_f = screen_name + '.json'
        user_profileimg_f = screen_name + '.jpg'
        user_tweets_f = screen_name + '_tweets.json'
        user_clean_tweets_f = screen_name + '.csv'

        # If user does not exist, run crawler to get user info; Otherwise, use local data
        user_profile_json = user_info_crawler(screen_name, user_dir, user_profile_f, user_profileimg_f, user_tweets_f, user_clean_tweets_f)

        # create a one row dataframe
        user_df = pd.DataFrame(columns=['name', 'screen_name', 'desc', 'follower', 'following'])

        user_df.loc[-1] = [user_profile_json['name'], user_profile_json['screen_name'], user_profile_json['description'], user_profile_json['followers_count'], user_profile_json['friends_count']]

        # ============================================
        # basic feature calculation and prediction
        # ============================================

        name_score = sc.name_score(user_df.name)
        screen_name_score = sc.screen_name_score(user_df.screen_name)
        desc_score, desc_words = sc.desc_score(user_df.desc)
        network_score = sc.network_score(user_df.follower, user_df.following)
        _, _, prof_img_v_score = sc.prof_img_score(user_df.screen_name, user_dir)
        first_score, inter_score, emo_score = sc.first_inter_emo_score(user_df.screen_name, user_dir, "All")

        TML_1_testing = pd.DataFrame()
        TML_1_testing['user'] = user_df.screen_name
        TML_1_testing['name_score'] = name_score
        TML_1_testing['screen_name_score'] = screen_name_score
        TML_1_testing['desc_score'] = desc_score
        TML_1_testing['desc_words'] = desc_words
        TML_1_testing['network_score'] = network_score
        TML_1_testing['prof_img_score'] = prof_img_v_score
        TML_1_testing['first_score'] = first_score
        TML_1_testing['inter_score'] = inter_score
        TML_1_testing['emo_score'] = emo_score
          
        with open('classifier_1.pkl', 'rb') as mr:
            classifier_1 = pickle.load(mr, fix_imports=True, encoding="latin1")         # For Python 3
        classifier_1_predict = classifier_1.predict_proba(TML_1_testing[list(TML_1_testing)[1:]])

        output_1 = classifier_1_predict[0] * 100.0
        #print('Classifier_1: \t', end='')
        #print('[Brand: %.2f%%, Female: %.2f%%, Male: %.2f%%]' % (output_1[0], output_1[1], output_1[2]))

        return output_1

    except Exception as e:
        #print(e)
        print("Could not predict user's role. Check account info, few tweets, incorrect image format...")


def main(args, args1):
    screen_name_file = args #inputfile username csv
    username_database = args1 #distinct username df

    dict_classification = {}
    type_arr = { 0:"Brand", 1:"Female", 2:"Male" }

    with open(screen_name_file, 'r') as rf:
        screen_name_list = list(csv.reader(rf))

    for idx, screen_name in enumerate(screen_name_list):
        #sys.stdout.write("Task %4d: %-15s  =>  " % (idx + 1, screen_name[0]))
        sys.stdout.flush()

        found = username_database.index[username_database['username'] == screen_name[0]].tolist()
        if len(found) > 0: 
            if username_database['twirole'].iloc[found[0]] == "": # classification not previously found
                arr = role_classifier(screen_name[0])
                if isinstance(arr, np.ndarray) and arr.size > 1:
                    arr = list(map(int, arr.tolist()))
                    username_database['twirole'].iloc[found[0]] = type_arr[arr.index(max(arr))]
                else:
                    username_database['twirole'].iloc[found[0]] = "Could not predict user's role."

        files = glob.glob('/mnt/camelot-cs5604/twt/user/*')
        for f in files:
            os.remove(f)
    
    return username_database
