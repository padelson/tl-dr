import json


def process_data(num_samples=-1):
    f1 = open('raw_data.txt', 'r')
    f2 = open('processed_data.txt', 'w')
    data = f1.read().split('\n')
    f1.close()

    raw_count = 0
    entry_count = 0
    for line in data:
        if line == '' or (raw_count == num_samples and num_samples is not -1):
            break

        line_obj = json.loads(line)
        title = line_obj['title']
        content = line_obj['content']
        raw_count += 1
        print 'processing raw entry ' + str(raw_count)
        for word in title.split():
            entry = {'content': content, 'word': word,
                     'title': title, 'keyWord': 1}
            f2.write(str(json.dumps(entry)) + '\n')
            entry_count += 1
            if entry_count % 100 == 0:
                print 'entry ' + str(entry_count) + ' added'

        non_keywords = [w for w in content.split() if w not in title.split()]

        for word in set(non_keywords):
            entry = {'content': content, 'word': word,
                     'title': title, 'keyWord': -1}
            f2.write(str(json.dumps(entry)) + '\n')
            entry_count += 1
            if entry_count % 100 == 0:
                print 'entry ' + str(entry_count) + ' added'

    f2.close()


def get_data(num_samples=-1):
    f = open('processed_data.txt', 'r')
    data = f.read().split('\n')
    entries = []
    count = 0
    for line in data:
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


def get_oracle_data(num_samples=-1):
    f = open('processed_data.txt', 'r')
    data = f.read().split('\n')
    entries = []
    count = 0
    for line in data:
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


# process_data()
# print get_data(1)
# print get_oracle_data(1)
