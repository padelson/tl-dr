import json

def processData():
    f1 = open('raw_data.txt', 'r')
    f2 = open('processed_data.txt', 'w')
    data = f1.read().split('\n')
    f1.close()

    rawCount = 0
    entryCount = 0
    for line in data:
        if line == '':
            break

        lineObj = json.loads(line)
        title = lineObj['title']
        content = lineObj['content']
        rawCount += 1
        print 'processing raw entry ' + str(rawCount)
        for word in title.split():
            entry = {'content': content, 'word': word}
            f2.write(str(json.dumps(entry)) + '\n')
            entryCount += 1
            print 'entry ' + str(entryCount) + ' added'

    f2.close()

def getData():
    f = open('processed_data.txt', 'r')
    data = f.read().split('\n')
    entries = []
    count = 0
    for line in data:
        if line == '':
            break

        count += 1
        print 'processing line ' + str(count)
        lineObj = json.loads(line)
        #entry is of the form: (article, word) , isKeyWord
        entry = ((lineObj['content'], lineObj['word']), 1)
        entries.append(entry)
    f.close()
    return entries
processData()
entries = getData()