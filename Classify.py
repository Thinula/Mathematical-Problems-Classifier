import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
# retrives the credentials from the creds json file
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds) # authenticate with Google
problems = []
category = []
testProb = []
testCats = []

def collectData(sheetName,problems,category):
    # open the sheets
    highSchool = client.open(sheetName).worksheet('HS') 
    middSchool = client.open(sheetName).worksheet('MS')
    elemSchool = client.open(sheetName).worksheet('ES')

    oldLen = len(problems)
    # add all the problems
    problems += highSchool.col_values(8)
    problems += middSchool.col_values(8)
    problems += elemSchool.col_values(8)
    # add all the problem categories
    category += highSchool.col_values(5)
    category += middSchool.col_values(5)
    category += elemSchool.col_values(5)

    numCount = 0 # counting Number Theory problems
    comCount = 0 # counting Combinatorics problems
    algCount = 0 # counting Algebra problems
    geoCount = 0 # counting Geometry problems
    i = oldLen
    while i < len(problems):
        problems[i].replace("\n","") # replace all instances of \n with empty
        category[i].replace("\n","") # same as above
        if category[i] == '0':
            numCount += 1
        elif category[i] == '1':
            comCount += 1
        elif category[i] == '2':
            algCount += 1
        elif category[i] == '3':
            geoCount += 1
        else:
            category.remove(category[i])
            problems.remove(problems[i])
            i -= 1
        i += 1
    return problems,category
    

problems,category=collectData('118 Archive',problems,category)
problems,category=collectData('117 Archive',problems,category)
testProb,testCats=collectData('119 Archive',testProb,testCats)
print(len(category),len(problems))
# This has 1170 NT, 475 Combo, 742 Algebra, 766 Geo
problemsFile = open("Problems.txt","w")
categoryFile = open("Category.txt","w")
testProblems = open("Test Problems.txt","w")
testCategory = open("Test Category.txt","w")
for i in range(len(problems)):
    problemsFile.write(problems[i]+"\n")
    
numberCount,comboCount,algebraCount,geometryCount = 0,0,0,0
for i in range(len(category)):
    if category[i] == '0':
        categoryFile.write("Number Theory\n")
        numberCount += 1
    elif category[i] == '1':
        categoryFile.write("Combinatorics\n")
        comboCount += 1
    elif category[i] == '2':
        categoryFile.write("Algebra\n")
        algebraCount += 1
    elif category[i] == '3':
        categoryFile.write("Geometry\n")
        geometryCount += 1
    else:
        print("RIP")

for i in range(len(testProb)):
    testProblems.write(testProb[i]+"\n")
    
newNumberCount,newComboCount,newAlgebraCount,newGeometryCount = 0,0,0,0
for i in range(len(testCats)):
    if testCats[i] == '0':
        testCategory.write("Number Theory\n")
        newNumberCount += 1
    elif testCats[i] == '1':
        testCategory.write("Combinatorics\n")
        newComboCount += 1
    elif testCats[i] == '2':
        testCategory.write("Algebra\n")
        newAlgebraCount += 1
    elif testCats[i] == '3':
        testCategory.write("Geometry\n")
        newGeometryCount += 1
    else:
        print("RIP")

print(numberCount,comboCount,algebraCount,geometryCount)
print(newNumberCount,newComboCount,newAlgebraCount,newGeometryCount)
categoryFile.close()
problemsFile.close()
testProblems.close()
testCategory.close()


