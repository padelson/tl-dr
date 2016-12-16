import collections
import json
import nltk
import string
import tldrlib
import sys
import string

# given set of words, return all candidate keywords
def get_words_to_learn(body, stopWords):
    desired_tags = ['NOUN', 'ADJ', 'VERB']
    tagged = nltk.pos_tag(body, tagset='universal')
    return [(tldrlib.removePunctuation(t[0]), t[1]) for t in tagged \
        if t[1] in desired_tags and \
        tldrlib.removePunctuation(t[0]).lower() not in stopWords and \
        tldrlib.removePunctuation(t[0]) != ""]


def get_data_entries(text):
    # (article, word, part of speech)
    words = get_words_to_learn(list(set(text.split())), getStopWords())
    entries = []
    for word_pos in words:
        word, pos = word_pos
        entries.append((text, word, pos))
    return entries

def getWordCounts(data):
    wordCounts = collections.defaultdict(int)
    for k in data:
        entry = data[k][0]
        for w in entry[0][0].split():
            wordCounts[w] += 1
    return wordCounts

def getStopWords():
    f3 = open('english.stop', 'r')
    stopWords = []
    while (True):
        line = f3.readline()
        if not line:
            break
        stopWords.append(line[:-1])
    f3.close()
    return stopWords

# Examples are written to processed_data.txt as a map containing:
#     content: the content of the article
#     word: the word in question (is it a keyword or nah? that is the question)
#     title: the title of the article
#     pos: part of speech of word
#     keyWord: -1 or 1 indicating whether the word is a keyword (1 if yes)
def process_data(num_samples=-1):
    rssdata_f = open('rss_data.txt', 'r')
    processed_f = open('processed_data.txt', 'w')
    articles_f = open('articles.txt', 'w')
    stopWords = getStopWords()
    raw_count = 0
    entry_count = 0
    articles = {}
    while (True):
        line = rssdata_f.readline()
        if line == '' or (raw_count == num_samples and num_samples is not -1):
            break

        line_obj = json.loads(line)
        gold = tldrlib.preprocess(line_obj['gold'].encode('utf-8'))
        content = tldrlib.preprocess(line_obj['content'].encode('utf-8'))

        # gets list of all gold words that were found in the article
        #   working off assumption that we can build headline from only
        #   words in the article
        raw_count += 1
        print 'processing raw entry ' + str(raw_count)

        # for the gold set, get the words in the article & non stopwords
        gold = [word for word in gold.split() \
            if word in "".join(content.split()[:150]) and \
            word not in stopWords]

        # for the first 150 words in an article, get the NOUN/VERB/ADJ
        candidateKeywords = get_words_to_learn(content.split()[:150], stopWords)

        for candidate in candidateKeywords:
            word, pos = candidate
            entry = {}
            entry['content'] = content
            entry['gold'] = gold
            entry['word'] = word
            entry['keyWord'] = 1 if word in gold else 0
            entry['pos'] = str(pos)
            processed_f.write(json.dumps(entry) + '\n')
            entry_count += 1
            if entry_count % 100 == 0:
                print 'entry ' + str(entry_count) + ' added'
        #
        # gold_words_to_learn = get_words_to_learn(gold.split(), stopWords)
        # gold_words_to_learn_final = [w for w in gold_words_to_learn if w[0] in content.split()]

        articles[' '.join(gold)] = content

    articles_f.write(json.dumps(articles))

    rssdata_f.close()
    processed_f.close()
    articles_f.close()

def getArticlesDict():
    f = open('articles.txt', 'r')
    articles = collections.defaultdict(str)
    while (True):
        line = f.readline()
        if not line:
            break
        line_obj = json.loads(line)
        for k in line_obj:
            articles[k] = line_obj[k]

    return articles

def getWikiCounts():
    f = open('wikipedia_tf.txt', 'r')
    counts = collections.defaultdict(int)
    while (True):
        line = f.readline().split()
        if not line:
            break
        counts[line[0]] = int(line[1])
    return counts

# given a string that represents JSON object, return tuple of parts
# converts unicode to ascii
# returns ()
def parseJSON(s):
    obj = json.loads(s)
    return (obj['content'], obj['gold'],
        obj['word'], obj['keyWord'], obj['pos'])

# Reads processed_data.txt to obtain all examples and returns an array
# of example points, where each point is of the form: (article, word, part of speech) , isKeyWord
def get_data(num_samples=-1):
    f = open('processed_data.txt', 'r')
    entries = collections.defaultdict(list)
    wordCounts = collections.defaultdict(float)
    wikiCounts = getWikiCounts()
    count = 0
    numKeyWordEntries = 0
    while (True):
        line = f.readline()
        if line == '' or (count == num_samples and num_samples is not -1):
            break

        count += 1
        if count % 100 == 0:
            print 'processing line ' + str(count)
        #line_obj = json.loads(line)
        content, gold, word, keyWord, pos = parseJSON(line)
        wordCounts[word] += 1
        # entry is of the form: (article, word, part of speech) , isKeyWord
        entry = ((content, word, pos), keyWord)
        features = tldrlib.keywordFeatureExtractor(entry[0], wordCounts, wikiCounts)
        entries[' '.join(gold)].append(((features, word, pos), keyWord))

        if keyWord == 1:
            numKeyWordEntries += 1
            #print 'keyword'
            #print line_obj['word']
            #print features
            #if count % 100 == 0:
            #print line_obj['word']
            #print features
    f.close()
    print "number of data entries: " + str(count)
    print "number of positive entries: " + str(numKeyWordEntries)
    return entries, wordCounts, wikiCounts


# Can indicate num_samples, to choose how many raw data points
# to process

# Reads processed_data.txt to obtain all examples and returns an array
# of example points, where each point is of the form: (article, title, word) , isKeyWord
def get_oracle_data(num_samples=-1):
    f = open('processed_data.txt', 'r')
    entries = []
    count = 0
    while (True):
        line = f.readline()
        if line == '' or (count == num_samples and num_samples is not -1):
            break

        count += 1
        if count % 100 == 0:
            print 'processing line ' + str(count)
        line_obj = json.loads(line)

        # entry is of the form: (article, word) , isKeyWord
        entry = ((line_obj['content'], line_obj['title'],
                  line_obj['word']), line_obj['keyWord'])
        entries.append(entry)
    f.close()
    return entries


process_data(100)
# print get_data(1000)
# print get_oracle_data(100)
