# tl-dr
Stanford University CS221 Project: generating summaries for bodies of text

Run tldr.py

# How To Use
-   run `pip install -r requirements.txt` to make sure you have the necessary libraries
-   unzip rss_data.txt and put it in this directory (or run `python rss.py`, which takes around 10 minutes)
-   run `python tldr.py`

# tldr.py command line options
*   -n:  number of articles you want to learn on
*   -a:  action type {key, sum, base, ora} for {key extraction, summary generation, baseline, oracle}
*   -f:  filepath (available for key extraction and summary generation) to text file
*   key extraction and summary generation work using a cached weight vector learned from 1549 articles for convenience.  You can simply create a file for the text you would like to extract keys from / summarize.
*   ex: `python tldr.py -a sum -f final.txt`
*   command line functionality was built for exploration of the different aspects, and not for robustness

# TODOS (remove this before submitting):
-   EVALUATE GENERATED SUMMARIES SOMEHOW.
-   get search working
-   stop caching latest weight vector and just staticly store a good one for TAs to use
-   zip everything up properly for submission

## Approach
The general problem we are trying to solve is **article => headline**.

We simplify this first to **article => keywords**.  We can construct a headline from
significant words using NLP techniques.

We can break down the problem even further to **(article, word) => [-1,1\]** indicating
whether word is a keyword in article.

We have chosen to run logistic on the simplest form of the problem.
Once learned, we can identify keywords by iterating over each word in the article
and scoring it.  

We then take the top scoring words and run them through our MDP to generate headlines.

Dataset is a series of NY Times articles scraped via RSS.
