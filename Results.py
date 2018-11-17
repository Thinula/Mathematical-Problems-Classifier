answers = open("Test Categories Answered.txt","r")
compute = open("Test Categories Calculated.txt","r")
cleaned = open("Test Cleaned Problems.txt","r")

catAnswers = []
catCompute = []
for line in answers:
    catAnswers.append(line)
for line in compute:
    catCompute.append(line)
#for line 

correct = 0
total = 0
numberWrong,comboWrong,algebraWrong,geoWrong = 0,0,0,0
print(len(catAnswers),len(catCompute))
for i in range(len(catAnswers)):
    if catAnswers[i] == catCompute[i]:
        correct += 1
    elif catCompute[i] == "Number Theory\n":
        numberWrong += 1
    elif catCompute[i] == "Combinatorics\n":
        comboWrong += 1
    elif catCompute[i] == "Algebra\n":
        algebraWrong += 1
    elif catCompute[i] == "Geometry\n":
        geoWrong += 1
    total += 1

print(total,correct,numberWrong,comboWrong,algebraWrong,geoWrong)
