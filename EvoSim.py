import math
import time
import sys
import random

'''

KEY:
[ID, GENES, SEX, DEBT, REPRODUCTION_COOLDOWN, REPRODUCTION_TIME, CHANCE_OF_REPRODUCTION_FAILURE, HAVING_CHILD, MATURITY_TIME, MOTHER_ID]

Male: 0
Female: 1

EXAMPLE:
[4, 1234567890123456, 0, 0.1, 0.5, 1, 0.01, false, 5, -1]

ID: 0
GENES: 1
SEX: 2
DEBT: 3
REPRODUCTION_COOLDOWN: 4
REPRODUCTION_TIME: 5
CHANCE_OF_FAILURE: 6
HAVING_CHILD: 7
MATURITY_TIME: 8
BIRTH_YEAR: 9
LIFESPAN: 10
MOTHER_ID: 11
DEATH_YEAR: 12

USE OF GENES:
reproduction time = [0] * [1] / [2]
reproduction cooldown = [4] * [5] 
chance of failure = ([0] * [1] / [2]) / ([4] * 4)
maturity time = [3]
lifespan = [6] + [7] + [8]

'''



# GLOBAL VARIABLES
creatureCounter = 0
allCreatures = []
aliveCreatures = []  # contains list of INDEXES in `allCreatures`
deadCreatures = [] # contains list of INDEXES in `allCreatures`
creatureQueue = [] # contains list of creatures in the womb (that will be born soon); if the mother dies then the creature is deleted from the queue

# CONSTANTS

# --


def main():

    # request info:
    try:
        startingCreatures = int(input("How many creatures do you want the simulation to start with? Make sure to input more than 1 in order to allow reproduction. "))
        totalYears = int(input("How many years do you want it to run? "))
    except ValueError:
        print("This respone was not a number (NaN). Now exiting program, please run again.\n")
        sys.exit()


    # logic:

    for i in range(startingCreatures): # creation of starting creatures
        allCreatures.append([])
        currentCreature = allCreatures[i]
        currentCreature.append(i) # id: 0
        genes = ""
        for _ in range(16): # genes
            rand = random.randint(0,9)
            genes = genes + str(rand)
        currentCreature.append(genes) # genes: 1
        
        # gender assignment:

        gender = random.randint(0,1)
        currentCreature.append(gender) # gender: 2

        currentCreature.append(0) # debt: 3

        try:
            reproductionTimeOrig = int(genes[0]) * int(genes[1]) / int(genes[2])
        except ZeroDivisionError:
            reproductionTimeOrig = int(genes[0]) * int(genes[1]) / 1
        if (reproductionTimeOrig >= 10):
            reproductionTimeFinal = 9 / 2
        elif (reproductionTimeOrig < 1):
            reproductionTimeFinal = 1 / 2
        else:
            reproductionTimeFinal = round(reproductionTimeOrig / 2, 1)
        
        currentCreature.append(int(genes[4]) * int(genes[5])) # reproduction cooldown: 4

        currentCreature.append(reproductionTimeFinal) # reproduction time: 5
        
        if int(genes[4]) == 0:
            currentCreature.append(round(reproductionTimeFinal / (4), 2))
        else:
            currentCreature.append(round(reproductionTimeFinal / ( int(genes[4]) * 4), 2)) # reproduction chance of failure: 6

        currentCreature.append(False) # having child: 7

        currentCreature.append(int(genes[3])) # maturity time: 8

        currentCreature.append(0) # birth year: 9

        currentCreature.append(int(genes[6]) + int(genes[7]) + int(genes[8])) # lifespan: 10
        
        currentCreature.append(-1) # mother id: 11

        currentCreature.append(-1) # death year: 12

        aliveCreatures.append(currentCreature)

    global creatureCounter
    creatureCounter = startingCreatures - 1 # starting at 0 (for use in indexes for allCreatures)

    # start of sim
    for currentYear in range(totalYears):
        print("One year has passed...")
        print(f"Creatures this year: {int(len(aliveCreatures))}")
        # queue logic
        for i in range(len(creatureQueue)):
            creature = creatureQueue[0]
            queueId = creature[0]
            if creature[11] != -1:        
                clone = creatureQueue[0].copy()
                clone[3] = 0
                aliveCreatures.append(clone)

                motherIndex = findIndex(aliveCreatures, creature[11])
                aliveCreatures[motherIndex][7] = False
                creatureQueue.remove(creature)
                

        # logic
        for i in range(len(aliveCreatures)):
            if (aliveCreatures[i][2] == 0):
                mate = findMate(aliveCreatures[i][0], currentYear)
                if (mate == None):
                    continue
                childrenPerYear = findChildrenThisYear((mate[4] + mate[5]), mate[3]).children
                mate[3] = findChildrenThisYear((mate[4] + mate[5]), mate[3]).newDebt

                for _ in range(childrenPerYear): # amount of children
                    mate[7] = True
                    child = haveChild(aliveCreatures[i], mate, currentYear)
                    allCreatures.append(child)
                    creatureQueue.append(child)
                    mate[7] = False
                
'''
def findChildrenPerYear(rate: float, remainder: float):

    childrenThisYear = (1 + remainder) / rate
    newRemainder = childrenThisYear - math.floor(childrenThisYear)

    return [childrenThisYear, newRemainder]
'''
'''
class findChildrenPerYear: # time 1.5, debt, 0.9 (repeated)
    def __init__(self, time: float, debt: float):
        if debt >= 1:
            debt = debt - 1
            self.children = 0
        elif debt >= 0:
            rate = (1) / (time - debt)
            roundedRate = math.ceil(rate)
            self.newDebt = roundedRate - rate
            self.children = roundedRate
'''

class findChildrenThisYear: # time 1.5, debt, 0.9 (repeated)
    def __init__(self, time: float, debt: float):
        if debt >= 1:
            debt = debt - 1
            self.children = 0
        else:
            remainingTime = 1 - debt
            rate = remainingTime / time
            roundedRate = math.ceil(rate)
            self.newDebt = roundedRate - rate
            self.children = roundedRate


def findMate(creatureID: int, currentYear: int):
    
    currentCreature = aliveCreatures[findIndex(aliveCreatures, creatureID)]
    gender = currentCreature[2]
    for i in range(len(aliveCreatures)):
        if ((currentCreature != aliveCreatures[i]) & (aliveCreatures[i][2] != gender)):
            age = currentYear - currentCreature[9]
            if (currentCreature[7] == True or aliveCreatures[i][7] == True):
                continue
            elif (age <= currentCreature[8]):
                print(currentCreature[8])
                print(age)
                continue
            return aliveCreatures[i]
    return None

def findIndex(table: list, desired_id: int):

    for i in range(len(table)):

        if (table[i][0] == desired_id):
            return i

def find(table: list, desired_value):

    for i in range(len(table)):

        if (table[i] == desired_value):
            return i

def scrambleList(table: list):
    newList = []
    for i in range(len(table)):
        randomValue = random.choice(table)
        table.remove(randomValue)
        newList.append(randomValue)

        finalList = int(''.join(str(x) for x in newList))
        
    return finalList


def haveChild(father: list, mother: list, year: int):

    randomIndexes = []
    takingList = list(range(16))
    for _ in range(8):
        randomNum = random.choice(takingList)
        if not find(randomIndexes, randomNum):
            randomIndexes.append(randomNum)
            takingList.remove(randomNum)

    maleIndex = randomIndexes
    femaleIndex = takingList
    maleGenes = father[1]
    femaleGenes = mother[1]
    Genes = []

    for i in range(8):
        Genes.append(maleGenes[maleIndex[i]])

    for i in range(8):
        Genes.append(femaleGenes[femaleIndex[i]])

    finalGenes = str(scrambleList(Genes))


    currentCreature = []
    currentCreature.append(len(allCreatures) + 1) # id
    currentCreature.append(finalGenes) # genes
    currentCreature.append(random.randint(0,1)) # gender
    currentCreature.append(0) # debt

    if int(finalGenes[2]) == 0:
        reproductionTimeOrig = 1
    else:
        reproductionTimeOrig = int(finalGenes[0]) * int(finalGenes[1]) / int(finalGenes[2])
    if (reproductionTimeOrig >= 10):
        reproductionTimeFinal = 9 / 2
    elif (reproductionTimeOrig < 1):
        reproductionTimeFinal = 1 / 2
    else:
        reproductionTimeFinal = round(reproductionTimeOrig / 2, 1)
        
    currentCreature.append(int(finalGenes[4]) * int(finalGenes[5])) # reproduction cooldown

    currentCreature.append(reproductionTimeFinal) # reproduction time

    if not int(finalGenes[4]) == 0:
        currentCreature.append(round(reproductionTimeFinal / ( int(finalGenes[4]) * 4), 2)) # reproduction chance of failure
    else:
        currentCreature.append(3)

    currentCreature.append(False) # having child

    currentCreature.append(int(finalGenes[3])) # maturity time

    currentCreature.append(year + mother[5]) # birth year

    currentCreature.append(int(finalGenes[6]) + int(finalGenes[7]) + int(finalGenes[8])) # lifespan

    currentCreature.append(mother[0]) # mother id
    
    currentCreature.append(-1) # death year
    global creatureCounter    
    creatureCounter += 1

    return currentCreature
main()

for x in range(len(allCreatures)):
    print(allCreatures[x])
