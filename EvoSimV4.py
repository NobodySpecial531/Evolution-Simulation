import random
import sys
import math
import time

# Overview:
'''
The purpose of this program is to simulate biologicsl evolution and to test how different parameters affects it.  
It first creates and stores a set of creatures and environments as requested by the user.
Each creature has a set of genes, each of which are 16 numbers between 0 and 9.  These genes 
determine the lifespan, birthrate, abd mutatation rate. 
Each environment is defined by a set of functions that determine death abd birth rates as a function of population size
The program then starts the simulation which does a check every year of which creatures are able to reproduce
and which creatures die, according to the genes and environments. Whenever a creature reproduces, it copies it's 
genes and generates mutations probsbilistically. At the end, the program prints out a list of living creatures in each
environment and how many were born.  
'''

# GENE KEY:
# the product of 16th number and first one makes lifespan
# second number divided by third number is reproduction speed in years (1/2 is half a year) if either number is zero then it cannot reproduce
# fourth number is mutation factor (9 is highest chance of mutations 0 lowest)
# the other gene numbers are for future modifications to the program.  

# IMPORTANT EXAMPLE:
''' once the program runs through all the years, it prints out for each living creatures a set of information, as described in the following key:
creatures = [  --> [GENES, BIRTH YEAR, DEATH YEAR (-1 for living creates), NUMBER OF OFFSPRING, YEAR OF LAST OFFSPRING, HOW THEY DIED (-1 if they are still living), CREATURE ID, PARENT ID, CURRENT ENVIRONMENT] 
    [23520850930, 2, -1, 0, -1, -1, 31, -1, 1]
] --> if a number is -1 that means that it is not applicable, for example, death year when the creature is alive
'''

# The function below makes a table of probabilities that each gene mutates to each possible new value. There is a higher probability that a gene mutates
# to a value near the original one.  For example, if the original gene is 5, there is a higher probability it mutates to 4 or 6.  The probability drops off 
# the more the new value differs from the original value.  
def createMutationTable(x):
    beforeVar = x # before = 4
    if x >= 4:
        beforeVar = 4
    finalList = []
    reverseBeforeVar = range(4,-1,-1)[beforeVar]
    finalList = list(range(reverseBeforeVar + 1, 5))
    finalList.append(0)
    for a in range(4, 0, -1): # [4,3,2,1]
        if len(finalList) >= 10:
            break
        finalList.append(a)


    while(True):
        if len(finalList) >= 10:
            break
        else:
            if x > 5:
                finalList.insert(0, 0) # add zeros before, works by assigning range (random/25, if the range of finalList[a] is equal to random then that is picked)
            else: 
                finalList.append(0) # add zeros to end

    return finalList

# Below is a function which creates the y value from the x of the custom death rate math function that is calculated for each environment.  
# the a and b are actually stored in the enviornment table which has a small range so that enviornments
# are slightly different from each other.  
def deathRateFunc(x, currentEnvir):
    a = envirRates[currentEnvir][3]
    b = envirRates[currentEnvir][4]
    try:
        y = 1 / (a * (1-b) ** x)
    except ZeroDivisionError:
        y = 50
    if y >= 50:
        return 50
    else:
        return y
    
# Below is a function which creates the y value from the x of the custom birth rate math function that is calculated for each environment.  
# the a and b are actually stored in the enviornment table which has a small range so that enviornments
# are slightly different from each other.  
def birthRateFunc(x, currentEnvir):
    a = envirRates[currentEnvir][1] 
    b = envirRates[currentEnvir][2] 
    try:
        y = 1 / (a * (1 - b) ** x)
    except ZeroDivisionError:
        y = 95
    if y >= 95:
        return 95
    else:
        return y
  
# The below function creates a new line in the alive creatures table, copies the genes and other information, then figures out what the new genes are 
# for the ones that are getting mutated. For info on createMutationTable() see above. 
def haveChild(aliveCreatures, deadCreatures, creatureCounter, mutationFactor, parentGenes, parentID, parentEnvir):
    aliveCreatures.append([])
    newCreature = aliveCreatures[len(aliveCreatures) - 1]
    newCreature.append(parentGenes)
    # mutations:
    for a in range(16):
        if int(mutationFactor) != 0: # 0 indicates no mutations
            testMutation = random.randint(1, 100)
            if testMutation <= int(mutationFactor):
                gene_list = list(newCreature[0])  # Convert to list of characters
                # Calculating New Gene:
                mutationTable = createMutationTable(a)
                totalChances = 0
                editedMutationTable = []
                for b in range(len(mutationTable)):
                    totalChances = totalChances + mutationTable[b]
                    if b != a:
                        editedMutationTable.append(totalChances)
                randomNum = random.randint(1,totalChances)
                newMutation = None
                for b in range(len(editedMutationTable)):
                    if editedMutationTable[b] >= randomNum:
                        newMutation = b

                gene_list[a] = str(newMutation)  # Update character
                newCreature[0] = ''.join(gene_list)

    newCreature.append(currentYear)
    newCreature.append(-1)
    newCreature.append(0)
    newCreature.append(-1)
    newCreature.append(-1)
    newCreature.append(creatureCounter)
    newCreature.append(parentID)
    newCreature.append(parentEnvir)
    envirArr[parentEnvir - 1].append(newCreature[6])

    # creatureCounter += 1

# Explanation in the function:
def main():
    # asks the user the values needed to start the simulation: years to run it, starting creatures, number of environments
    totalYears = int(input("How many years do you want to run this simulation? \n"))
    currentCreatureNumber = int(input("How many starting creatures? \n"))
    envirNum = int(input("How many environments? \n"))

    # creates the arrays:
    # aliveCreates stores all alive creatures and their information
    global aliveCreatures
    aliveCreatures = []
    # deadCreatures stores all the creatures that died
    global deadCreatures
    deadCreatures = [] # all dead creatures
    # creatureCounter stores all the creatures that ever lived
    creatureCounter = 0
    # stores each creature in each environment
    global envirArr
    envirArr = []
    # stores the environment rates (the custom parts of the birth and death rate function)
    global envirRates
    envirRates = []

    for a in range(envirNum): # assigns every environment id
        envirArr.append([(a + 1) * -1]) # to account for zeros AND for creature IDs interfering

    for a in range(envirNum): # creates and assigns all the rates (random)
        envirRates.append([(a + 1) * -1])
        # birth rate:
        envirRates[a].append(random.uniform(2, 4))
        envirRates[a].append(random.uniform(0.006, 0.01))
        # death rate
        envirRates[a].append(random.uniform(0.4, 1))
        envirRates[a].append(random.uniform(0.006, 0.01))

    for a in range(currentCreatureNumber): # creates an empty slot for every create in the aliveCreatures list
        aliveCreatures.append([])

        aliveCreatures[a].append("") # initiazes creatures[a][0] with a value of nothing to then have the genes put into it
        for b in range(16): # loop to put all genes into creatures[a][0]
            aliveCreatures[a][0] += str(random.randint(0, 9))
        
        environment = random.randint(1, envirNum) # picks a random environment to be placed into
        aliveCreatures[a].append(random.randrange(-5, 1, 1)) # generates random number between -5 and 0 (it excludes the 1 making it 0) all numbers multiple of 1
        aliveCreatures[a].append(-1) # death year                      ^^ birth year ^^
        aliveCreatures[a].append(0) # number of offspring
        aliveCreatures[a].append(-1) # year of last offspring
        aliveCreatures[a].append(-1) # how they died
        aliveCreatures[a].append(creatureCounter) # creature numeral
        aliveCreatures[a].append(-1) # parent id
        aliveCreatures[a].append(environment)
        envirArr[environment - 1].append(aliveCreatures[a][6]) # aliveCreatures[a][6] is current creature's id
        creatureCounter += 1

    # SIMULATION:
    global currentYear
    for currentYear in range(totalYears): # years
        for a in range(len(aliveCreatures)): # checks every creature
            currentCreature = aliveCreatures[a]
            currentEnvir = currentCreature[8] - 1
            populationOfCurrentEnvir = len(envirArr[currentEnvir]) - 1
            if int(currentCreature[0][1]) == 0 or int(currentCreature[0][2]) == 0: # cannot reproduce
                reproductionSpeed = -1
            else:
                reproductionSpeed = int(currentCreature[0][1]) / int(currentCreature[0][2])
            if currentCreature[4] == -1: # if it is -1 it means they never had a child hence always being able to have one
                randNum = random.random()
                if randNum * 100 > birthRateFunc(populationOfCurrentEnvir, currentEnvir):
                        if reproductionSpeed < 1:
                            amountOfOffspring = 2
                        elif reproductionSpeed < 0.5:
                            amountOfOffspring = 3
                        elif reproductionSpeed < 0.2:
                            amountOfOffspring = 4
                        elif reproductionSpeed < 0.1:
                            amountOfOffspring = 5
                        else:
                            amountOfOffspring = 1
                        for b in range(amountOfOffspring):
                            haveChild(aliveCreatures, deadCreatures, creatureCounter, currentCreature[0][3], currentCreature[0], currentCreature[6], currentCreature[8])
                        creatureCounter += amountOfOffspring
                        currentCreature[3] += amountOfOffspring
                        currentCreature[4] = currentYear
            else:
                if currentYear - currentCreature[4] >= reproductionSpeed and reproductionSpeed != -1:
                    randNum = random.random()
                    if randNum * 100 > birthRateFunc(populationOfCurrentEnvir, currentEnvir):
                        if reproductionSpeed < 1:
                            amountOfOffspring = 2
                        elif reproductionSpeed < 0.5:
                            amountOfOffspring = 3
                        elif reproductionSpeed < 0.2:
                            amountOfOffspring = 4
                        elif reproductionSpeed < 0.1:
                            amountOfOffspring = 5
                        for b in range(amountOfOffspring):
                            haveChild(aliveCreatures, deadCreatures, creatureCounter, currentCreature[0][3], currentCreature[0], currentCreature[6], currentCreature[8])
                        creatureCounter += amountOfOffspring
                        currentCreature[3] += amountOfOffspring
                        currentCreature[4] = currentYear

        creaturesToKill = [] # makes a list that determines what creatures need to die
        for a in range(len(aliveCreatures)):
            currentCreature = aliveCreatures[a]
            age = currentYear - currentCreature[1] 
            lifespan = int(currentCreature[0][0]) * int(currentCreature[0][-1])
            if age >= lifespan:
                currentCreature[2] = currentYear # death year
                currentCreature[5] = 1 # how they died
                creaturesToKill.append(currentCreature)
                for sublist in envirArr:
                    if currentCreature[6] in sublist: # removes creatures from their environments
                        sublist.remove(currentCreature[6]) 
        for a in range(len(creaturesToKill)):
            aliveCreatures.remove(creaturesToKill[0]) # removes creatures from alive and adds to dead
            deadCreatures.append(creaturesToKill[0]) # starts at zero and removes everything from zero
            creaturesToKill.remove(creaturesToKill[0]) # removes from creatures to kill
        
        creaturesToKill = [] # deals with creatures that die of overpopulation
        for a in range(len(aliveCreatures)):
            currentCreature = aliveCreatures[a]
            randNum = random.random()
            currentEnvir = currentCreature[8] - 1
            populationOfCurrentEnvir = len(envirArr[currentEnvir])
            if randNum * 100 < deathRateFunc(populationOfCurrentEnvir, currentEnvir): # calculates the current deathRate for the enviroment
                currentCreature[2] = currentYear
                currentCreature[5] = 2
                creaturesToKill.append(currentCreature)
                for sublist in envirArr:
                    if currentCreature[6] in sublist:
                        sublist.remove(currentCreature[6])
        for a in range(len(creaturesToKill)):
            aliveCreatures.remove(creaturesToKill[0])
            deadCreatures.append(creaturesToKill[0])
            creaturesToKill.remove(creaturesToKill[0])


    for a in range(len(aliveCreatures)):
        print(aliveCreatures[a])
    print("\n") # makes 2 spaces

    print("Key: [GENES, BIRTH YEAR, DEATH YEAR, NUMBER OF OFFSPRING, YEAR OF LAST OFFSPRING, HOW THEY DIED, CREATURE NUMERAL, PARENT ID, CURRENT ENVIRONMENT] \n")
    print(f"A total of {len(aliveCreatures)} were alive when the simulation ended.")
    print(f"A total of {creatureCounter} creatures were born. (Including starting creatures)")

    for a in range(len(envirArr)):
        print(f"There are {len(envirArr[a]) - 1} creatures in environment {envirArr[a][0] * -1}")
main()
