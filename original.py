
########################################################
# IMPORTS
########################################################
import json
import pandas as pd
import bokeh
from bokeh.plotting import figure, output_notebook, show, legend
output_notebook()

########################################################
# GLOBAL VARIABLES
########################################################

########################################################
# FUNCTIONS
########################################################

def load_twitter_data(tweets_data_path):
    tweets_data = []
    tweets_file = open(tweets_data_path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue
    return tweets_data

def pop_tweets(path):
    tweets_data = load_twitter_data(path)
    tweets = pd.DataFrame()
    
    tweets['text'] = list(map(lambda tweet: tweet['text'], tweets_data))
    tweets['latt'] = list(map(lambda tweet: tweet['coordinates']['coordinates'][0]
                              if tweet['coordinates'] != None else NaN, tweets_data))
                              tweets['long'] = list(map(lambda tweet: tweet['coordinates']['coordinates'][1]
                                                        if tweet['coordinates'] != None else NaN, tweets_data))
                              
    return tweets[tweets.latt.notnull()]

def pop_keys(geo_tweets, keys):
    geo_tweets['text'] = geo_tweets.text.str.lower()
    for key in keys:
        geo_tweets[key] = list(map(lambda words: key in words, geo_tweets.text.values))
    
    return geo_tweets

geo_tweets = pop_keys(pop_tweets('yall.txt'), ['python', 'javascript', 'ruby'])
geo_tweets = pd.concat([geo_tweets, yall_tweets], ignore_index=True)

print('total geo_tweets:', len(geo_tweets))
print('python', len(geo_tweets[geo_tweets['python']]))

f = figure(plot_width=1200, plot_height=900,)

f.scatter(geo_tweets[geo_tweets['python']].latt, geo_tweets[geo_tweets['python'].long, color="indianred", legend='python')
f.scatter(geo_tweets[geo_tweets['javascript']].latt, geo_tweets[geo_tweets['javascript']].long, color="indianred")
f.scatter(geo_tweets[geo_tweets['ruby']].latt, geo_tweets[geo_tweets['ruby']].long, color="blue",
          legend='ruby')

# stylistic stuff:

f.grid.grid_line_color = None
f.xaxis.axis_line_color = None

f.yaxis.axis_line_color = None
f.yaxis.major_tick_line_color = None
f.axis.major_label_standoff = 0

show(f)