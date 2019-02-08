import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

problems = []
category = []
total = [0 for i in range(4)]
cleanedProblems = open("Test Cleaned Problems.txt","w")
for line in open("Test Problems.txt","r"):
    problems.append(line.lower())
for line in open("Test Category.txt","r"):
    category.append(line)
    if line == "Number Theory\n":
        total[0] += 1
    elif line == "Combinatorics\n":
        total[1] += 1
    elif line == "Algebra\n":
        total[2] += 1
    elif line == "Geometry\n":
        total[3] += 1

print(len(problems),len(category))
puncList = string.punctuation # list of punctuation
stopWords = set(stopwords.words('english'))
stopWords.add('let') # this is an obvious choice for math problems
stopWords.add('find') # fairly decent choice for math problems
stopWords.add('compute') # this one I'm not so sure about (normally its good, but might take away from example on line below)
# the bad part about adding remainder is for purely NT problems like compute remainder when 9^{2017} is divided by 100
stopWords.add('remainder') # this is a less obvious choice, but added bc lot of problems ask for answer formatting
stopWords = list(stopWords) # to make it easier later on
# unique application here is creating a list of polygons (they're really the same for our purposes, but we dont want them deleted either)
polygons = ['triangle','quadrilateral','square','rectangle','rhombus','trapezoid','parallelogram','pentagon','hexagon','heptagon','octagan','nonagon','decagon']
wordsList = {} # dictionary of words used with number of occurences
# this gets rid of all the money problems, leaving easy data cleanup
i = 0
while i < len(problems):
    if problems[i].count("$") % 2 != 0:
        del problems[i] #problems.remove(problems[i])
        del category[i] #category.remove(category[i])
        i -= 1
    i += 1

# function which filters out all copies of polygon in problem
def cleanPolygons(problem,polygon):
    ind = problem.index(polygon)
    problem = problem[:ind]+problem[ind+1+len(polygon):]
    return "polygon " + problem # to account for the removal of the shape polygon   

print(len(problems),len(category))
# cleans the data (gets rid of ALL latex -> might not work but we'll see)
# adding polygons here too, because somethings $\triangle ABC$ might get deleted -> dont want that

for i in range(len(problems)):
    for j in range(len(polygons)):
        if j != 2:
            while problems[i].count(polygons[j]) > 0:
                problems[i] = cleanPolygons(problems[i],polygons[j])
        else:
            # 'square' should only be removed for geometry problems (double meaning with "perfect square" in NT problems)
            while problems[i].count(polygons[j]) > 0 and category[i] == "Geometry":
                problems[i] = cleanPolygons(problems[i],polygons[j])
                
    # things to add from latex: trig functions, \binom, \sum            
    while problems[i].count("$") > 0: # latex syntax requires >= 2 $ signs then
        ind1 = problems[i].index('$')
        ind2 = problems[i].index('$',ind1+1)
        latexString = problems[i][ind1+1:ind2]
        for j in range(latexString.count("\binom")):
            problems[i] = "binom " + problems[i]
        for j in range(latexString.count("\sum")):
            problems[i] = "sum " + problems[i]
        trigFuncs = ["\tan","\sin","\cos","\sec","\csc","\cot","\arcsin","\arccos","\arccot","\arctan","\arcsec","\arccsc"]
        for j in range(len(trigFuncs)):
            for k in range(latexString.count(trigFuncs[j])):
                problems[i] = "trig " + problems[i]

        ind1 = problems[i].index('$')
        ind2 = problems[i].index('$',ind1+1)        
        problems[i] = problems[i][:ind1]+problems[i][ind2+1:]

cleanedList = []
# now cleaning up the data and keeping track of the number of occurences of each word
for i in range(len(problems)):
    words = word_tokenize(problems[i])
    # this gets rid of all the words that are part of our list of stopwords
    for j in range(len(stopWords)):
        while stopWords[j] in words:
            words.remove(stopWords[j])
    # this gets rid of all the words that have punctuation in them (e.g. "'s" will get deleted too)
    for j in range(len(puncList)):
        for w in words:
            if puncList[j] in w:
                words.remove(w)
    # this gets rid of all the integers in the problem -- this shouldn't affect the content of the problem (usually)
    for w in words:
        try:
            c = int(w)
            words.remove(w)
        except:
            c = w   
    # now we can finally collect the ocurrence data
    for w in words:
        count = wordsList.get(w)
        if len(w) > 1:
            if count is None:
                wordsList[w] = 1
            else:
                wordsList[w] = wordsList.pop(w)+1
                        
    cleanedList.append(words)
    cleanedProblems.write(str(words))
    cleanedProblems.write("\n")

finalCategory = ["" for i in range(len(problems))]
probabilities = [[1 for i in range(4)] for i in range(len(problems))]
probabilityFile = open("Common Word Probabilities.txt","r")
calculatedTopic = open("Test Categories Calculated.txt","w")
answeredTopics = open("Test Categories Answered.txt","w")
commonWords = {}
topicProbs = list(map(float,probabilityFile.readline().split()))
for i in range(200):
    word = probabilityFile.readline()[:-1]
    probs = list(map(float,probabilityFile.readline().split()))
    commonWords[word] = probs

for i in range(len(problems)):
    for word in cleanedList[i]:
        probs = commonWords.get(word)
        if probs is not None:
            for j in range(4):
                probabilities[i][j] *= probs[j]
    # only for normalization
    if sum(probabilities[i]) != 0:
        for j in range(4):
            probabilities[i][j] /= sum(probabilities[i])

for i in range(len(problems)):
    maxProb = max(probabilities[i])
    if maxProb == probabilities[i][0]:
        calculatedTopic.write("Number Theory\n")
    elif maxProb == probabilities[i][1]:
        calculatedTopic.write("Combinatorics\n")
    elif maxProb == probabilities[i][2]:
        calculatedTopic.write("Algebra\n")
    elif maxProb == probabilities[i][3]:
        calculatedTopic.write("Geometry\n")
    else:
        print("RIP")#print("%.3f %.3f %.3f %.3f" %(probabilities[i][0],probabilities[i][1],probabilities[i][2],probabilities[i][3]))

for i in range(len(category)):
    answeredTopics.write(category[i])
print(topicProbs)
print(len(problems),len(category))
probabilityFile.close()
calculatedTopic.close()
answeredTopics.close()
