#!/usr/bin/env python3

######################################################
# This script provides a basic use case for extracting
# words from text, normalizing these words, and
# querying synonym.com for related synonyms for
# each word.
######################################################

##################################################################################
# Python imports required for basic operations
##################################################################################
from wordhoard import synonyms
from nltk.corpus import stopwords
from string import punctuation
from string import digits
import re as regex

# ASCII characters which are considered punctuation characters.
# These characters will be removed from the text
exclude_punctuation = set(punctuation)

# English stop words to remove from text.
# A stop word is a commonly used word, such
# as “the”, “a”, “an”, “in”
stop_words = set(stopwords.words('english'))


def expunge_punctuations(data):
    """
    This function is used normalized text from the submitted textual information.
    This process will lowercase all the words in the provided text.
    All common punctuations will be removed from text.
    :param data: Textual information
    :return: normalized text with punctuations removed
    """
    normalized = ''.join([i for i in data.lower() if i not in exclude_punctuation])
    return normalized


def expunge_stopwords(data):
    """
    This function is used normalized text from the submitted textual information.
    This process will lowercase all the words in the provided text.
    All English stop words will be removed from text.
    :param data: Textual information
    :return: normalized text with stopwords removed
    """
    normalized = ' '.join([i for i in regex.split('[\'| ]', ''.join(data).lower()) if i not in stop_words])
    return normalized


def expunge_numeral_characters(string_data):
    """
    This function is used to remove all numeral characters
    from the submitted textual information.
    :param string_data: Textual information
    :return: normalized text with numeral characters removed
    """
    remove_digits = str.maketrans('', '', digits)
    cleaned_data = string_data.translate(remove_digits)
    return cleaned_data


text_to_analyze ="Backgammon is one of the oldest known board games. Its history can be traced back nearly 5,000 " \
                 "years to archeological discoveries in the Middle East. it is a two player game where each player " \
                 "has fifteen checkers which move between twenty-four points according to the roll of two dice."


remove_stopwords = expunge_stopwords(text_to_analyze)
remove_punctuations = expunge_punctuations(remove_stopwords)
remove_numbers = expunge_numeral_characters(remove_punctuations)
wordlist = remove_numbers.split()

# list for word frequencies
wordfreq = []

# Count the frequencies of words within
# the normalized text
for w in wordlist:
    wordfreq.append(wordlist.count(w))

word_frequencies = (dict(zip(wordlist, wordfreq)))

# Query synonym.com for synonyms for each
# word in the dictionary word_frequencies
synonyms_dict = {}
for word in word_frequencies.keys():
    synonyms_results = synonyms.query_synonym_com(word)
    if synonyms_results is not None:
        synonyms_dict[word] = synonyms_results
    else:
        synonyms_dict[word] = 'no synonyms found'

# review the query results
for key, values in sorted(synonyms_dict.items()):
    print(key, values)
    # NOTE: the error message related to the word twentyfour
    # synonym.com had no reference for the word twentyfour
    # Please verify that the word twentyfour is spelled correctly.
    #
    # synonyms for each word
    # according ['reported']
    # archeological ['archaeologic', 'archaeological', 'archeologic']
    # back ['body', 'body part', 'dorsal vertebra', 'dorsum', 'lat', 'latissimus dorsi', 'lumbar vertebra', 'saddle', 'small', 'thoracic vertebra', 'torso', 'trunk']
    # backgammon ['board game']
    # board ['advisory board', 'appeal board', 'appeals board', 'board member', 'board of appeals', 'board of directors', 'board of education', 'board of selectmen', 'commission', 'committee', 'director', 'directorate', 'draft board', 'federal reserve board', 'governing board', 'planning board', 'school board', 'zoning board']
    # checkers ['board game', 'checker board', 'checkerboard', 'draughts']
    # dice ['cube', 'die', 'five', 'five-spot', 'four', 'four-spot', 'one-spot', 'six', 'six-spot', 'square block']
    # discoveries ['act', 'breakthrough', 'catching', 'deed', 'detection', 'determination', 'espial', 'find', 'finding', 'human action', 'human activity', 'rediscovery', 'self-discovery', 'spotting', 'spying', 'tracing', 'uncovering']
    # east ['eastbound', 'easterly', 'eastern', 'easternmost', 'eastmost', 'eastside', 'eastward']
    # fifteen ['15', 'cardinal', 'xv']
    # game ['activity', 'athletic game', 'bowling', 'card game', 'cards', "child's game", 'curling', 'gambling game', 'game of chance', 'pall-mall', 'parlor game', 'parlour game', 'table game', 'zero-sum game']
    # games ['games-master', 'school teacher', 'schoolteacher']
    # history ['age', 'antiquity', 'dark ages', 'historic period', 'middle ages', 'past', 'past times', 'renaissance', 'renascence', 'yesteryear']
    # known ['acknowledged', 'best-known', 'better-known', 'celebrated', 'famed', 'familiar', 'famous', 'far-famed', 'glorious', 'identified', 'illustrious', 'legendary', 'notable', 'noted', 'proverbial', 'renowned', 'well-known']
    # middle ['area', 'center', 'center stage', 'central city', 'centre', 'centre stage', 'city center', 'city centre', 'country', 'eye', 'financial center', 'heart', 'hub', 'inner city', 'medical center', 'midfield', 'midstream', 'seat', 'storm center', 'storm centre']
    # move ['accompany', 'advance', 'angle', 'arise', 'ascend', 'automobile', 'back', 'bang', 'be adrift', 'beetle', 'belt along', 'betake oneself', 'billow', 'blow', 'bounce', 'breeze', 'bucket along', 'cannonball along', 'caravan', 'career', 'carry', 'cast', 'change', 'circle', 'circuit', 'circulate', 'come', 'come down', 'come up', 'continue', 'crank', 'crawl', 'creep', 'cruise', 'derail', 'descend', 'displace', 'do', 'drag', 'draw', 'draw back', 'drift', 'drive', 'ease', 'err', 'fall', 'ferry', 'float', 'flock', 'fly', 'follow', 'forge', 'get about', 'get around', 'ghost', 'glide', 'go', 'go across', 'go around', 'go by', 'go down', 'go forward', 'go on', 'go past', 'go through', 'go up', 'hasten', 'hie', 'hiss', 'hotfoot', 'hurry', 'hurtle', 'island hop', 'jounce', 'journey', 'jump', 'lance', 'lead', 'lift', 'locomote', 'lurch', 'march on', 'meander', 'motor', 'move around', 'move back', 'move on', 'move up', 'outflank', 'overfly', 'pace', 'pan', 'pass', 'pass by', 'pass on', 'pass over', 'pelt along', 'play', 'plough', 'plow', 'prance', 'precede', 'precess', 'proceed', 'progress', 'propagate', 'pull away', 'pull back', 'pursue', 'push', 'race', 'raft', 'ramble', 'range', 'recede', 'repair', 'resort', 'retire', 'retreat', 'retrograde', 'return', 'ride', 'rise', 'roam', 'roll', 'round', 'rove', 'run', 'rush', 'rush along', 'scramble', 'seek', 'shack', 'shuttle', 'sift', 'sit', 'ski', 'slice into', 'slice through', 'slide', 'slither', 'snowshoe', 'speed', 'spirt', 'spread', 'spurt', 'steam', 'steamer', 'step', 'step on it', 'stray', 'surpass', 'swan', 'swap', 'swash', 'swim', 'swing', 'take the air', 'taxi', 'thread', 'trail', 'tram', 'tramp', 'transfer', 'travel', 'travel along', 'travel by', 'travel purposefully', 'travel rapidly', 'tread', 'trundle', 'turn', 'uprise', 'vagabond', 'walk', 'wander', 'weave', 'wend', 'wheel', 'whine', 'whish', 'whisk', 'whistle', 'whoosh', 'wind', 'wing', 'withdraw', 'zigzag', 'zip', 'zoom']
    # nearly ['about', 'almost', 'most', 'near', 'nigh', 'virtually', 'well-nigh']
    # oldest ['age', 'age-old', 'antediluvian', 'antiquated', 'antique', 'archaic', 'auld', 'hand-down', 'hand-me-down', 'hoary', 'immemorial', 'long-ago', 'longtime', 'noncurrent', 'nonmodern', 'past', 'patched', 'rusty', 'secondhand', 'stale', 'sunset', 'used', 'worn', 'yellow', 'yellowed']
    # one ['1', 'ane', 'cardinal', 'i']
    # player ['ballplayer', 'baseball player', 'billiard player', 'bowler', 'card player', 'chess player', 'contestant', 'dart player', 'football player', 'footballer', 'golf player', 'golfer', 'grandmaster', 'hockey player', 'ice-hockey player', 'lacrosse player', 'linksman', 'most valuable player', 'mvp', 'participant', 'playmaker', 'pool player', 'scorer', 'seed', 'seeded player', 'server', 'shooter', 'soccer player', 'stringer', 'tennis player', 'volleyball player']
    # points ['attracter', 'attractor', 'component', 'constituent', 'element', 'factor', 'ingredient', 'intercept', 'intersection', 'intersection point', 'point of intersection']
    # roll ['revolve', 'rim', 'turn', 'turn over']
    # traced ['analyse', 'analyze', 'canvas', 'canvass', 'examine', 'follow', 'keep abreast', 'keep an eye on', 'keep up', 'observe', 'study', 'watch', 'watch over']
    # twentyfour no synonyms found
    # two ['2', 'cardinal', 'ii']
    # years ['age', 'dotage', 'eighties', 'eld', 'geezerhood', 'mid-eighties', 'mid-nineties', 'mid-seventies', 'mid-sixties', 'nineties', 'old age', 'second childhood', 'senility', 'seventies', 'sixties', 'time of life']

