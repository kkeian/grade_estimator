#!/usr/bin/env python3
import os
from ClassGrade import ClassGrade
from GradeCategory import GradeCategory
import re
import json
from colorama import Fore, Style

classDir = "classes/"
for f in os.listdir(classDir):
    if f.endswith("json"):
        print(f.strip('.json'))

classToEval = input('\nWhich class: ')

# Get class info
with open(classDir + classToEval + ".json", "r") as read_file:
    swengClass = json.load(read_file)

categories = swengClass['GradeCategories']

cats = {}
for cat in categories:
    name = cat['Name']
    weight = cat['Weight']
    currPoints = cat['CurrPoints']
    pointsPossible = cat['PossiblePoints']
    category = GradeCategory(name, weight, currPoints, pointsPossible)
    cats[name] = category

classG = ClassGrade(swengClass['ClassName'], cats)

def generateAllCombos(cats: dict[GradeCategory], gradeCats: list[str]):
    catWeights = {}
    for catName, category in cats.items():
        if catName in gradeCats:
            category.createPointMatrix()
            weight = category.getWeight()
            catWeights[catName] = weight
    return catWeights


def getMaxCatAndWeight(cats: dict[str], gradeCats: list[str]):
    maxCatAndWeight = ("",0)

    for cat, weight in cats.items():
        if cat not in gradeCats:
            continue
        if weight > maxCatAndWeight[1]:
            maxCatAndWeight = (cat, weight)
    
    return maxCatAndWeight


def stringifyCombos(passingCombos: list[dict]) -> str:
    comboLines = []
    comboLen = len(passingCombos)
    for i in range(comboLen, 0, -1):

        comboHeadline = f'Combo {comboLen-i}:\n'
        comboLines.append(comboHeadline)

        combo = passingCombos[i-1]
        maxCat = max([len(cat) for cat in combo.keys()])
        for cat, score in combo.items():
            catLen = len(cat)
            pad = maxCat - catLen+2
            comboLines.append(f'{cat}:'.ljust(catLen + pad) + f'{score} points\n')
        lastEntry = len(comboLines)-1
        comboLines[lastEntry] += "\n"
    comboStr = ' '.join(comboLines)
    return comboStr


def getHighestAndLowestCombos(passingCombos: list[dict]) -> list[dict]:
    lowestAndHighest = []
    comboLen = len(passingCombos)
    lowestCombo = passingCombos[comboLen-1]
    highestCombo = passingCombos[0]

    lowestAndHighest.append(highestCombo)
    lowestAndHighest.append(lowestCombo)
    return lowestAndHighest




simulateExam = input('\nSimulate Grade Category(s)? (Y/N): ')

yes = re.compile('yes|y|ye|ye*|y*', re.IGNORECASE)
no = re.compile('no.*|n.*|no*|(no)*', re.IGNORECASE)
Eexam = re.compile('.*exam.*', re.IGNORECASE)
# Output categories to choose from
if (yes.match(simulateExam) != None):
    print("\nCategories:")
    categories = classG.getCategories()
    for cat in categories.keys():
        #if (exam.match(cat) != None):
        print(f"\t-{cat}")
    gradeCats = []
    e = ''
    while (e != "1"):
        e = input('Which Exam? "1" to stop: ')
        if e not in categories.keys():
            continue
        gradeCats.append(e)
        

    # Setup base ClassGrade categories
    deepCopyCategories = {}
    for k, v in categories.items():
        deepCopyCategories[k] = v
    simulatedClassRes = ClassGrade(classG.getName(), deepCopyCategories)
    for exam in gradeCats:
        existingExam = categories[exam]
        simulatedExam = GradeCategory(existingExam.getName(),
                        existingExam.getWeight(),
                        existingExam.getPointsReceived(),
                        existingExam.getPointsPossible())

    # Get current class state and objective
    currGrade = round(classG.calcGrade(), 2)
    toPass = round(72 - currGrade, 2)

    # Store all class categories
    simulatedClassCategories = simulatedClassRes.getCategories()
    # Mark category to explore first
    combos = generateAllCombos(simulatedClassCategories, gradeCats)
    maxCatAndWeight = getMaxCatAndWeight(combos, gradeCats)

    print(f'\nCurrent grade {currGrade}%\tPercent required to pass: {toPass}%\n')

    # Get percentages possible for gradeCats
    catPercentsAdded = {}
    for catName in gradeCats:
        catObj = simulatedClassCategories[catName]
        cat = catObj.getName()
        percents = catObj.getPossPercentsAdded()
        
        catPercentsAdded[cat] = percents

    # Create list of passing score combos
    passingScoreCombos = []
    startingCat, weight = maxCatAndWeight
    otherGradeCats = [exam for exam in gradeCats if exam != startingCat]
    numOtherExams = len(otherGradeCats)
    end = False
    for i in range(len(catPercentsAdded[startingCat])-1, 0, -1):
        passingCombo = {}
        if end:
            break
        percent = catPercentsAdded[startingCat][i]
        passingCombo = {startingCat: i}
        if percent > toPass:
            # Current exam grade sufficient to pass
            # with no points earned on other exams
            for exam in otherGradeCats:
                passingCombo[exam] = 0.0
            passingScoreCombos.append(passingCombo)
        elif numOtherExams > 0:
            foundCombo = False
            requiredExtraPercent = toPass - percent
            for i in range(numOtherExams):
                otherExam = otherGradeCats[i]
                otherPercents = catPercentsAdded[otherExam]
                otherWeight = int(otherPercents[len(otherPercents)-1])
                if otherWeight < requiredExtraPercent:
                    # No more possible combos
                    end = True
                    break
                else:
                    for j in range(len(otherPercents)):
                        otherPercent = otherPercents[j]
                        if otherPercent >= requiredExtraPercent:
                            passingCombo[otherExam] = j
                            foundCombo = True
                            break # stop searching this other category
                    continue
            if foundCombo == True:         
                passingScoreCombos.append(passingCombo)
                            
        else:
            end = True

    comboStr = ''
    comboLen = len(passingScoreCombos)
    if numOtherExams == 0:
        minScore = passingScoreCombos[comboLen-1][startingCat]
        comboStr = f'Min Score needed: {minScore}'

    else:
        # Gets a list of all possible generates combos
        comboStr = stringifyCombos(passingScoreCombos)
        #comboToStringify = getHighestAndLowestCombos(passingScoreCombos)
        #comboStr = stringifyCombos(comboToStringify)
                
    textColor = Fore.GREEN
    print(textColor, f'{comboStr}')


