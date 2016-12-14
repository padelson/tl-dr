#!/usr/bin/python
# RSS --> rss_data.txt
import feedparser, urllib2, json, nltk, string, re
from bs4 import BeautifulSoup
from PorterStemmer import PorterStemmer

def parseRSS( rss_url ):
    return feedparser.parse( rss_url )

def getLinks( rss_url ):
    links = []
    feed = parseRSS( rss_url )
    for item in feed['items']:
        links.append(item['link'])
    return links

# List of RSS feeds that we will fetch and combine
newsurls = {
    'nyt-world': 'http://rss.nytimes.com/services/xml/rss/nyt/World.xml',
    'nyt-war': 'http://atwar.blogs.nytimes.com/feed/',
    'nyt-africa': 'http://rss.nytimes.com/services/xml/rss/nyt/Africa.xml',
    'nyt-americas': 'http://rss.nytimes.com/services/xml/rss/nyt/Americas.xml',
    'nyt-asiapacific': 'http://www.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml',
    'nyt-europe': 'http://www.nytimes.com/services/xml/rss/nyt/Europe.xml',
    'nyt-middleeast': 'http://www.nytimes.com/services/xml/rss/nyt/MiddleEast.xml',
    'nyt-us': 'http://www.nytimes.com/services/xml/rss/nyt/US.xml',
    'nyt-edu': 'http://www.nytimes.com/services/xml/rss/nyt/Education.xml',
    'nyt-pol': 'http://www.nytimes.com/services/xml/rss/nyt/Politics.xml',
    'nyt-nyregion': 'http://www.nytimes.com/services/xml/rss/nyt/NYRegion.xml',
    'nyt-cityroom': 'http://cityroom.blogs.nytimes.com/feed/',
    'nyt-fortgreene': 'http://fort-greene.blogs.nytimes.com/feed',
    'nyt-eastvillage': 'http://eastvillage.thelocal.nytimes.com/feed/',
    'nyt-business': 'http://feeds.nytimes.com/nyt/rss/Business',
    'nyt-energyenvironment': 'http://www.nytimes.com/services/xml/rss/nyt/EnergyEnvironment.xml',
    'nyt-smallbusiness': 'http://www.nytimes.com/services/xml/rss/nyt/SmallBusiness.xml',
    'nyt-boss': 'http://boss.blogs.nytimes.com/feed',
    'nyt-econ': 'http://www.nytimes.com/services/xml/rss/nyt/Economy.xml',
    'nyt-deal': 'http://www.nytimes.com/services/xml/rss/nyt/Dealbook.xml',
    'nyt-media': 'http://www.nytimes.com/services/xml/rss/nyt/MediaandAdvertising.xml',
    'nyt-money': 'http://www.nytimes.com/services/xml/rss/nyt/YourMoney.xml',
    'nyt-tech': 'http://feeds.nytimes.com/nyt/rss/Technology',
    'nyt-bits': 'http://bits.blogs.nytimes.com/feed/',
    'nyt-personaltech': 'http://www.nytimes.com/services/xml/rss/nyt/PersonalTech.xml',
    'nyt-sports': 'http://www.nytimes.com/services/xml/rss/nyt/Sports.xml',
    'nyt-baseball': 'http://www.nytimes.com/services/xml/rss/nyt/Baseball.xml',
    'nyt-cbasketball': 'http://www.nytimes.com/services/xml/rss/nyt/CollegeBasketball.xml',
    'nyt-cfootball': 'http://www.nytimes.com/services/xml/rss/nyt/CollegeFootball.xml',
    'nyt-golf': 'http://www.nytimes.com/services/xml/rss/nyt/Golf.xml',
    'nyt-hockey': 'http://www.nytimes.com/services/xml/rss/nyt/Hockey.xml',
    'nyt-basketball': 'http://www.nytimes.com/services/xml/rss/nyt/ProBasketball.xml',
    'nyt-football': 'http://www.nytimes.com/services/xml/rss/nyt/ProFootball.xml',
    'nyt-soccer': 'http://www.nytimes.com/services/xml/rss/nyt/Soccer.xml',
    'nyt-tennis': 'http://www.nytimes.com/services/xml/rss/nyt/Tennis.xml',
    'nyt-gambit': 'http://gambit.blogs.nytimes.com/feed/',
    'nyt-science': 'http://www.nytimes.com/services/xml/rss/nyt/Science.xml',
    'nyt-environment': 'http://www.nytimes.com/services/xml/rss/nyt/Environment.xml',
    'nyt-space': 'http://www.nytimes.com/services/xml/rss/nyt/Space.xml',
    'nyt-health': 'http://www.nytimes.com/services/xml/rss/nyt/Health.xml',
    'nyt-wellblog': 'http://well.blogs.nytimes.com/feed/',
    'nyt-newoldage': 'http://newoldage.blogs.nytimes.com/feed/',
    'nyt-research': 'http://www.nytimes.com/services/xml/rss/nyt/Research.xml',
    'nyt-nutrition': 'http://www.nytimes.com/services/xml/rss/nyt/Nutrition.xml',
    'nyt-moneypolicy': 'http://www.nytimes.com/services/xml/rss/nyt/HealthCarePolicy.xml',
    'nyt-views': 'http://www.nytimes.com/services/xml/rss/nyt/Views.xml',
    'nyt-arts': 'http://www.nytimes.com/services/xml/rss/nyt/Arts.xml',
    'nyt-artdesign': 'http://www.nytimes.com/services/xml/rss/nyt/ArtandDesign.xml',
    'nyt-books': 'http://www.nytimes.com/services/xml/rss/nyt/Books.xml',
    'nyt-sundaybook': 'http://www.nytimes.com/services/xml/rss/nyt/SundayBookReview.xml',
    'nyt-dance': 'http://www.nytimes.com/services/xml/rss/nyt/Dance.xml',
    'nyt-movies': 'http://www.nytimes.com/services/xml/rss/nyt/Movies.xml',
    'nyt-music': 'http://www.nytimes.com/services/xml/rss/nyt/Music.xml',
    'nyt-television': 'http://www.nytimes.com/services/xml/rss/nyt/Television.xml',
    'nyt-theater': 'http://www.nytimes.com/services/xml/rss/nyt/Theater.xml',
    'nyt-artsbeat': 'http://artsbeat.blogs.nytimes.com/feed',
    'nyt-carpetbagger': 'http://carpetbagger.blogs.nytimes.com/feed',
    'nyt-fashion': 'http://www.nytimes.com/services/xml/rss/nyt/FashionandStyle.xml',
    'nyt-runway': 'http://runway.blogs.nytimes.com/feed/',
    'nyt-dining': 'http://www.nytimes.com/services/xml/rss/nyt/DiningandWine.xml',
    'nyt-home': 'http://www.nytimes.com/services/xml/rss/nyt/HomeandGarden.xml',
    'nyt-weddings': 'http://www.nytimes.com/services/xml/rss/nyt/Weddings.xml',
    'nyt-tmagazine': 'http://www.nytimes.com/services/xml/rss/nyt/tmagazine.xml',
    'nyt-motherlode': 'http://parenting.blogs.nytimes.com/feed/',
    'nyt-travel': 'http://www.nytimes.com/services/xml/rss/nyt/Travel.xml',
    'nyt-transit': 'http://intransit.blogs.nytimes.com/feed',
    'nyt-6thfloor': 'http://6thfloor.blogs.nytimes.com/feed/'
}
# shortened version for debugging
"""
newsurls = {
    'nyt-world': 'http://rss.nytimes.com/services/xml/rss/nyt/World.xml',
    'nyt-war': 'http://atwar.blogs.nytimes.com/feed/'
}
"""

ps = PorterStemmer()
stop_f = open('english.stop', 'r')
stopwords = []
for line in stop_f:
    stopwords.append(line.strip())

# gets the keywords from relevant one-liner sentence
# criteria:
# noun/adj/verb
# not in stopwords
# stemmed & lowercased
def getKeywordCandidates(text):
    global stopwords
    global ps
    desired_tags = ['NOUN', 'ADJ', 'VERB']
    text = ''.join([ch.lower() for ch in text if ch.isalnum() or ch.isspace()])
    tagged = nltk.pos_tag(text.split(), tagset='universal')
    return [t[0] for t in tagged if t[1] in desired_tags and t[0] not in stopwords]

def buildDataset():
    global newsurls
    rss_data = open('rss_data.txt', 'w')
    # A list to hold all headlines
    allLinks = []
    # Iterate over the feed urls
    for key,url in newsurls.items():
        print key
        allLinks.extend(getLinks(url))

    # Iterate over the allLinks list and write data
    for link in allLinks:
        print link
        page = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(link)
        html = BeautifulSoup(page, 'html.parser')
        title = html.findAll(attrs={"name":"hdl"})
        desc = html.findAll(attrs={"name":"description"})
        if not desc or not title:
            # some links will not be articles
            continue
        entry = {}
        title = title[0]['content'].encode("utf-8")
        desc = desc[0]['content'].encode("utf-8")

        # gold is a ' ' separated list of keyword candidates
        gold = set(getKeywordCandidates(title) + getKeywordCandidates(desc))
        entry['gold'] = ' '.join(gold)

        paras = html.findAll("p", { "class" : "story-body-text" })
        article = ""
        for p in paras:
            article += "\n" + p.getText() + "\n"
        if article == "":
            # no article given
            continue
        entry['content'] = article
        rss_data.write(str(json.dumps(entry)) + '\n')

    rss_data.close()

buildDataset()
# end of code
