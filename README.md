# tl-dr
Stanford University CS221 Project: generating summaries for bodies of text

Run tldr.py

SEE output.txt FOR RESULTS OF MOST RECENT UPDATE

# TODOS:
-   figure out how to process data efficiently so we can run this on a big data set
-   try different classifiers
-   try different loss functions
-   switch from util.py to sklearn?  so that we can host this code publicly
-   figure out how to rate generated summaries
-   implement remaining features
-   do better on summary generation.  the plan now is to turn it into a search problem.
-   EVALUATE GENERATED SUMMARIES SOMEHOW.
-   add command line functionality to tldr.py, key_ex.py, and sum_gen.py  

## Approach
The general problem we are trying to solve is **article => headline**.

We simplify this first to **article => keywords**.  We can construct a headline from
significant words using NLP techniques.

We can break down the problem even further to **(article, word) => [-1,1\]** indicating
whether word is a keyword in article.

We have chosen to run linear classification on the simplest form of the problem.
Once learned, we can identify keywords by iterating over each word in the article
and classifying it.

Initial dataset is the first 10,000 data entries from the *Signal Media One-million news articles* dataset
