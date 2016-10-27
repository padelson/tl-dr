import json


# Can indicate num_samples, to choose how many raw data points
# to process

# Reads raw_data.txt and outputs a file processed_data.txt,
# which can later be read to obtain all examples

# Examples are written to processed_data.txt as a map containing:
#     content: the content of the article
#     word: the word in question (is it a keyword or nah? that is the question)
#     title: the title of the article
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
        for word in title.split():
            entry = {'content': content, 'word': word,
                     'title': title, 'keyWord': 1}
            f2.write(str(json.dumps(entry)) + '\n')
            entry_count += 1
            if entry_count % 100 == 0:
                print 'entry ' + str(entry_count) + ' added'

        #every word not in the title is assumed to not be a keyword
        non_keywords = [w for w in content.split() if w not in title.split()]

        for word in set(non_keywords):
            entry = {'content': content, 'word': word,
                     'title': title, 'keyWord': -1}
            f2.write(str(json.dumps(entry)) + '\n')
            entry_count += 1
            if entry_count % 100 == 0:
                print 'entry ' + str(entry_count) + ' added'

    f1.close()
    f2.close()


# Can indicate num_samples, to choose how many raw data points
# to process

# Reads processed_data.txt to obtain all examples and returns an array
# of example points, where each point is of the form: (article, word) , isKeyWord
def get_data(num_samples=-1):
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
        entry = ((line_obj['content'], line_obj['word']), line_obj['keyWord'])
        entries.append(entry)
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


# process_data(10)
# print get_data(1000)
# print get_oracle_data(100)
