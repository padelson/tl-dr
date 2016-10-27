#!/usr/bin/python

# oracle
# predicts with perfect accuracy if a word is a keyword or not
# working on the assumption that a keyword is a word in the title
def oraclePredictor(x):
    article, title, testWord = x
    return 1 if testWord in title else -1
