# Mathematical-Problems-Classifier
This project was made to classify math problems (in particular, contest problems) into the four major categories (Number Theory, Combinatorics, Algebra, Geometry). The data was taken from mathleague.org's contest archives (unfortunately, this data is confidential and cannot be shared) and the classifier been tested on several hundred problems. Currently, this classifier achieves a 70% accuracy. I will be regularly improving this and also, I might add explanations about the decisions I made during this project.
Here is a brief description of what each of the files does:

Scraping Data.py -> Uses the Google Drive API to scrape the required data from Google Sheets.
Classify.py -> Uses NLTK libraries to preprocess the data and then implements a Naive Bayesian classifier (will explain this choice later)
Train.py -> Similar to Classify.py but runs the algorithm on the training document (I might make the code shorter later)
Result.py -> Calculates the results from the test data.

Currently, I've only tested the code on supervised data, will use this classifier on unsupervised data in the near future.
