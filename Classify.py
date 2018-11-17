import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

cleanedProblems = open("Cleaned Problems.txt","w")
wordOccurrences = open("Word Ocurrences.txt","w")
commonWordProbabilities = open("Common Word Probabilities.txt","w")
problems = []
category = []
total = [0 for i in range(4)]
for line in open("Problems_FINAL.txt","r"):
    problems.append(line.lower())
for line in open("Category.txt","r"):
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
        del problems[i]
        del category[i]
        #problems.remove(problems[i])
        #category.remove(category[i])
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

TOTAL_WORDS = 200
mostCommonWords = [] # list of the 200 most common words
wordCount = 0
for w in sorted(wordsList, key=wordsList.get, reverse=True):
    if wordCount < TOTAL_WORDS:
        mostCommonWords.append(w)
    wordOccurrences.write(w+": "+str(wordsList[w])+"\n")
    wordCount += 1

# keeps track of occurences of 200 most common words in each category
numberCount = [0 for i in range(TOTAL_WORDS)]
comboCount = [0 for i in range(TOTAL_WORDS)]
algebraCount = [0 for i in range(TOTAL_WORDS)]
geometryCount = [0 for i in range(TOTAL_WORDS)]
problemCount = [[0 for i in range(TOTAL_WORDS)] for j in range(len(problems))] # counts occurences in problems

for i in range(len(cleanedList)):
    for j in range(TOTAL_WORDS):
        occur = cleanedList[i].count(mostCommonWords[j])
        problemCount[i][j] += occur
        if category[i] == "Number Theory\n":
            numberCount[j] += occur
        elif category[i] == "Combinatorics\n":
            comboCount[j] += occur
        elif category[i] == "Algebra\n":
            algebraCount[j] += occur
        elif category[i] == "Geometry\n":
            geometryCount[j] += occur
        else:
            print("RIP")

wordOccurCount = [0 for i in range(TOTAL_WORDS)]
for i in range(len(problems)):
    for j in range(TOTAL_WORDS):
        wordOccurCount[j] += problemCount[i][j]
        
probability = [total[i]/(len(problems)) for i in range(4)]
commonWordProbabilities.write("%.3f %.3f %.3f %.3f\n" %(probability[0],probability[1],probability[2],probability[3]))
wordProbabilities = [[numberCount[j]/wordOccurCount[j],comboCount[j]/wordOccurCount[j],algebraCount[j]/wordOccurCount[j],geometryCount[j]/wordOccurCount[j]] for j in range(TOTAL_WORDS)]
for i in range(TOTAL_WORDS):
    commonWordProbabilities.write(mostCommonWords[i] + "\n")
    commonWordProbabilities.write("%.3f %.3f %.3f %.3f\n" %(wordProbabilities[i][0],wordProbabilities[i][1],wordProbabilities[i][2],wordProbabilities[i][3]))

newProblems = open("New Problems.txt","w")
newCategory = open("New Category.txt","w")
for i in range(len(problems)):
    newProblems.write(problems[i])
for i in range(len(category)):
    newCategory.write(category[i])
print(total)
print(len(problems),len(category))
cleanedProblems.close()
wordOccurrences.close()
commonWordProbabilities.close()
newProblems.close()
newCategory.close()
