import collections
import json
import nltk

def get_words_to_learn(body):
    desired_tags = ['NOUN', 'ADJ', 'VERB']
    tagged = nltk.pos_tag(body, tagset='universal')
    #TODO: remove punctuations
    #TODO: instead of returning the word itself(t[0]), stem it
    return [t for t in tagged if t[1] in desired_tags]

def get_data_entries(text):
    # (article, word, part of speech)
    words = get_words_to_learn(text.split())
    entries = []
    for word_pos in words:
        word, pos = word_pos
        entries.append((text, word, pos))
    return entries


# Examples are written to processed_data.txt as a map containing:
#     content: the content of the article
#     word: the word in question (is it a keyword or nah? that is the question)
#     title: the title of the article
#     pos: part of speech of word
#     keyWord: -1 or 1 indicating whether the word is a keyword (1 if yes)
def process_data(num_samples=-1):
    f1 = open('raw_data.txt', 'r')
    f2 = open('processed_data.txt', 'w')

    raw_count = 0
    entry_count = 0
    while (True):
        line = f1.readline()
        if line == '' or (raw_count == num_samples and num_samples is not -1):
            break

        line_obj = json.loads(line)
        title = line_obj['title']
        content = line_obj['content']
        raw_count += 1
        print 'processing raw entry ' + str(raw_count)

        #every word in the title is assumed to be a keyword
        for word_pos in get_words_to_learn(title.split()):
            word, pos = word_pos
            entry = {'content': content, 'word': word,
                     'title': title, 'keyWord': 1, 'pos': pos}
            f2.write(str(json.dumps(entry)) + '\n')
            entry_count += 1
            if entry_count % 100 == 0:
                print 'entry ' + str(entry_count) + ' added'

        #every word not in the title is assumed to not be a keyword
        non_keywords = [w for w in content.split() if w not in title.split()]

        for word_pos in get_words_to_learn(set(non_keywords)):
            word, pos = word_pos
            entry = {'content': content, 'word': word,
                     'title': title, 'keyWord': -1, 'pos': pos}
            f2.write(str(json.dumps(entry)) + '\n')
            entry_count += 1
            if entry_count % 100 == 0:
                print 'entry ' + str(entry_count) + ' added'

    f1.close()
    f2.close()



# Reads processed_data.txt to obtain all examples and returns an array
# of example points, where each point is of the form: (article, word, part of speech) , isKeyWord
def get_data(num_samples=-1):
    f = open('processed_data.txt', 'r')
    entries = collections.defaultdict(list)
    count = 0
    while (True):
        line = f.readline()
        if line == '' or (count == num_samples and num_samples is not -1):
            break

        count += 1
        if count % 100 == 0:
            print 'processing line ' + str(count)
        line_obj = json.loads(line)

        # entry is of the form: (article, word, part of speech) , isKeyWord
        entry = ((line_obj['content'], line_obj['word'], line_obj['pos']), line_obj['keyWord'])
        entries[line_obj['title']].append(entry)
    f.close()
    return entries


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


process_data(500)
# print get_data(1000)
# print get_oracle_data(100)
