import collections
import json
import nltk
import string
import tldrlib

def removePunc(text):
    return text.translate(None, string.punctuation)

def get_words_to_learn(body, stopWords):
    desired_tags = ['NOUN', 'ADJ', 'VERB']
    tagged = nltk.pos_tag(body, tagset='universal')
    #TODO: remove punctuations
    #TODO: instead of returning the word itself(t[0]), stem it
    return [t for t in tagged if t[1] in desired_tags and t[0].lower() not in stopWords]

def get_data_entries(text):
    # (article, word, part of speech)
    words = get_words_to_learn(text.split(), getStopWords())
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
    f1 = open('raw_data.txt', 'r')
    f2 = open('processed_data.txt', 'w')
    f3 = open('articles.txt', 'w')
    stopWords = getStopWords()
    raw_count = 0
    entry_count = 0
    articles = {}
    while (True):
        line = f1.readline()
        if line == '' or (raw_count == num_samples and num_samples is not -1):
            break

        line_obj = json.loads(line)
        title = line_obj['title']
        content = line_obj['content']
        raw_count += 1
        print 'processing raw entry ' + str(raw_count)

        title_words_to_learn = get_words_to_learn(title.split(), stopWords)
        title_words_to_learn_final = [w for w in title_words_to_learn if w[0] in content.split()]
        #every word in the title is assumed to be a keyword
        for word_pos in title_words_to_learn_final:
            word, pos = word_pos
            entry = {'content': content, 'word': word,
                     'title': title, 'keyWord': 1, 'pos': pos}
            f2.write(str(json.dumps(entry)) + '\n')
            entry_count += 1
            if entry_count % 100 == 0:
                print 'entry ' + str(entry_count) + ' added'

        #every word not in the title is assumed to not be a keyword
        non_keywords = [w for w in content.split()[:150] if w.lower() not in title.lower().split()]

        for word_pos in get_words_to_learn(set(non_keywords), stopWords):
            word, pos = word_pos
            entry = {'content': content, 'word': word,
                     'title': title, 'keyWord': 0, 'pos': pos}
            f2.write(str(json.dumps(entry)) + '\n')
            entry_count += 1
            if entry_count % 100 == 0:
                print 'entry ' + str(entry_count) + ' added'

        articles[title] = content

    f3.write(str(json.dumps(articles)))

    f1.close()
    f2.close()
    f3.close()

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
        line_obj = json.loads(line)
        wordCounts[line_obj['word']] += 1
        # entry is of the form: (article, word, part of speech) , isKeyWord
        entry = ((line_obj['content'], line_obj['word'], line_obj['pos']), line_obj['keyWord'])
        features = tldrlib.keywordFeatureExtractor(entry[0], wordCounts, wikiCounts)
        entries[line_obj['title']].append(((features, line_obj['word'], line_obj['pos']), line_obj['keyWord']))

        if line_obj['keyWord'] == 1:
            numKeyWordEntries += 1
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


process_data(10)
# print get_data(1000)
# print get_oracle_data(100)
