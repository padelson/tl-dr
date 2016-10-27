# tl-dr
Stanford University CS221 Project: generating summaries for bodies of text

## Approach
The general problem we are trying to solve is article => headline.

We simplify this first to article => keywords.  We can construct a headline from 
significant words using NLP techniques.

We can break down the problem even further to (article, word) => [-1,1] indicating
whether word is a keyword in article.

We have chosen to run linear classification on the simplest form of the problem.
Once learned, we can identify keywords by iterating over each word in the article
and classifying it.

Initial dataset is the first 10,000 data entries from the Signal Media One-million news articles dataset