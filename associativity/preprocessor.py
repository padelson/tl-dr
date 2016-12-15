#!/usr/bin/python

def replaceApostrophe(u_str):
    u_str = u_str.replace(u"\\u2018","'")
    u_str = u_str.replace(u"\\u2019","'")
    return u_str

def replaceQuotation(u_str):
    u_str = u_str.replace(u"\\u201c","\"")
    u_str = u_str.replace(u"\\u201d","\"")
    return u_str

def removeDash(u_str):
    u_str = u_str.replace(u"\\u2013","")
    u_str = u_str.replace(u"\\u2014","")
    u_str = u_str.replace(u"\\u2015","")
    return u_str

def replaceWhiteSpace(u_str):
    u_str = u_str.replace(u"\\u2009"," ")
    u_str = u_str.replace(u"\\n", " ")
    return u_str

def preprocess(body):
    u_str = unicode(body)
    u_str = replaceApostrophe(u_str)
    u_str = replaceQuotation(u_str)
    u_str = removeDash(u_str)
    u_str = replaceWhiteSpace(u_str)
    return str(u_str)

"""
def unicodeChecker(body):
    ucode = []
    for i,ch in enumerate(body):
        if body[i:i+2] == '\\u':
            if body[i:i+6] not in ucode:
                ucode.append(body[i:i+6])
    print ucode

def test():
    f = open('../articles.txt','r')
    line = f.readline()
    line = preprocess(line)
    print line[:100]
    unicodeChecker(line)

test()
"""
