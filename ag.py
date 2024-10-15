import math
import random
import matplotlib.pyplot as plt 

def generateGemoma(genomaSize, minRange, maxRange):
    genoma = [random.uniform(minRange, maxRange) for _ in range(genomaSize)]

    return genoma

def generatePopulation(populationSize, genomaSize, minRange, maxRange):
    population = [generateGemoma(genomaSize,minRange, maxRange) for _ in range(populationSize)]

    return population

def fitness(genoma,problem="sphere"):

    if(problem == "sphere"):
        resultado = 0
  
        for i in genoma:
            resultado += i**2
        
        return resultado
    
    if(problem == "rastrigin"):
        resultado = 0
  
        for i in genoma:
            numero = 2 * 3.1415 * i
            p = (numero/180) * math.pi
            resultado+= (i**2) - (10 * math.cos(p)) + 10
    
        return resultado
    
    if(problem == "rosenbrock"):
        resultado = 0
  
        for i in range(0,(len(genoma)-1)):
            resultado += 100*(genoma[i+1] - genoma[i]**2)**2 + (genoma[i] - 1)**2
    
        return resultado
    
def selectByFitness(population,problem):

    fitnessPopulation = [fitness(genoma,problem) for genoma in population]
   
    invertedFit = [1/fit for fit in fitnessPopulation]
    
    sumFitnessPopulation = sum(invertedFit)
    
    roulette = [fit/sumFitnessPopulation for fit in invertedFit]
    
    selection = random.choices(population,weights=roulette,k=1)[0]
   
    return selection

def selectByTournament(population,problem, k):

    tournament = random.sample(population, k)

    select = min(tournament, key= lambda genoma : fitness(genoma,problem))

    return select

def crossover(dadOne,dadTwo,slice,percentSlice=0.75):

    isSlice = random.random()
    
    if(isSlice <= percentSlice and (slice == 1 or slice == 2)):
        if(slice == 1):
           
            slicePlace = random.randint(1,len(dadOne) - 1)

            firstSon = dadOne[:slicePlace] + dadTwo[slicePlace:]
            secondSon = dadTwo[:slicePlace] + dadOne[slicePlace:]

            return firstSon, secondSon

        if(slice == 2):

            firstSlicePlace = random.randint(1,len(dadOne) - 2)
            secondSlicePlace = random.randint(firstSlicePlace,len(dadOne) - 1)

            firstSon = dadOne[:firstSlicePlace] + dadTwo[firstSlicePlace:secondSlicePlace] + dadOne[secondSlicePlace:]
            secondSon = dadTwo[:firstSlicePlace] + dadOne[firstSlicePlace:secondSlicePlace] + dadTwo[secondSlicePlace:]

            return firstSon, secondSon
    else:
        return dadOne,dadTwo

def mutation(genoma,minRange, maxRange, mutationPercent = 0.1):
    for i in range(len(genoma)):
        randomValue = random.random()
        if randomValue < mutationPercent:
            genoma[i] = random.uniform(minRange, maxRange)
    return genoma

def evolucion(population,problem,slice,minRange, maxRange, selectType="Proporcionalidade",tournamentGenomas=2,percentSlice=0.75,mutationPercent = 0.1):
    newPopulation = []
    
    selectPopulation = []

    if(selectType == "Proporcionalidade"):
        c = 0
        while c < len(population):
            selectPopulation.append(selectByFitness(population,problem))
            c = c + 1

    if(selectType == "Torneio"):
        c = 0
        while c < len(population):
            selectPopulation.append(selectByTournament(population,problem,tournamentGenomas))
            c = c + 1

    crossPopulation = []

    for i in range(0,len(selectPopulation),2):
        dadOne = selectPopulation[i]
        dadTwo = selectPopulation[i + 1] if i + 1 < len(selectPopulation) else selectPopulation[0]
        firstSon, secondSon = crossover(dadOne, dadTwo, slice,percentSlice)
        crossPopulation.extend([firstSon,secondSon])

    crossPopulation[:len(selectPopulation)]

    for i in crossPopulation:
        newPopulation.append(mutation(i,minRange, maxRange,mutationPercent))

    return newPopulation

def geneticAlgorithm(geracions,genomaSize,populationSize,minRange, maxRange,problem,slice,selectType, tournamentGenomas=2,percentSlice=0.75,mutationPercent = 0.1):

    population = generatePopulation(populationSize,genomaSize,minRange, maxRange)
    firstEvolutionGenoma = min(population, key= lambda genoma : fitness(genoma,problem))
    firstLessEvolutionGenoma = max(population, key= lambda genoma : fitness(genoma,problem))

    # print(f"Primeira população: {population}")
    # print("===================================================================================")
    # print(f"Melhor genoma com valor {fitness(firstEvolutionGenoma,problem)}")
    # print(f"Pior genoma com valor {fitness(firstLessEvolutionGenoma,problem)}")
    # print("===================================================================================")
 
    bestGenomas = []
    melhores = []
    piores = []
    c = []

    for geration in range(geracions):
        population = evolucion(population,problem,slice,minRange,maxRange,selectType,tournamentGenomas,percentSlice,mutationPercent)
        evolutionGenoma = min(population, key= lambda genoma : fitness(genoma,problem))
        lessEvolutionGenoma = max(population, key= lambda genoma : fitness(genoma,problem))

        bestGenomas.append({"geration":geration,"bestGenoma":fitness(evolutionGenoma,problem)})
 
        print(f"Geração: {geration}")
        print(f"Melhor genoma com valor {fitness(evolutionGenoma,problem)}")
        print(f"Pior genoma com valor {fitness(lessEvolutionGenoma,problem)}")
        print("===================================================================================")
        melhores.append(fitness(evolutionGenoma,problem))
        piores.append(fitness(lessEvolutionGenoma,problem))
        c.append(geration)
        
    
    # print(f"Melhores genomas: {bestGenomas}")
    betterGenoma = min(bestGenomas, key= lambda genoma: genoma["bestGenoma"])

    plt.figure(figsize=(10, 6))
    plt.plot(c, melhores, label='Melhor Genoma', color='green', marker='o')
    plt.plot(c, piores, label='Pior Genoma', color='red', marker='x')

    plt.xlabel('Geração')
    plt.ylabel('Valor de Fitness')
    plt.title('Melhor vs Pior Genoma por Geração')
    plt.legend()
    plt.grid(True)
    plt.show()
    # print("===================================================================================")
    # print(f"Melhor genoma {betterGenoma["bestGenoma"]} na geração {betterGenoma["geration"]}")
    # print("===================================================================================")

    

geneticAlgorithm(
                    geracions=100,
                    genomaSize=20,
                    populationSize=30,
                    minRange=-5.12,
                    maxRange=5.12,
                    problem="rosenbrock",
                    slice=2,
                    selectType="Proporcionalidade",
                    percentSlice=0.75,
                    mutationPercent=0.1
                ) 

# plt.plot(range(100), geneticAlgorithm, label='Melhor Fitness')
# plt.xlabel('Geração')
# plt.ylabel('Melhor Valor de Fitness')
# plt.title('Convergência do GA')
# plt.legend()
# plt.show()

# Problemas:
# - rosenbrock
# - rastrigin
# - sphere

# Seleções:
# - Torneio
# - Proporcionalidade

# Cortes:
# - 1 
# - 2

# Percentual de cruzamento padrão 0.75

# Percentual de mutação padrão 0.1

# def plotGraft(scenario1, scenario2,scenario3, execution=30):

#     executions = execution

#     scenarioConjunt = [scenario1,scenario2,scenario3]

#     data = []

#     for scenario in scenarioConjunt:
#         resultsSceanrios = [] 
#         for _ in range(executions):
#             bestValue = geneticAlgorithm(
#                     geracions=scenario["geracions"],
#                     genomaSize=scenario["genomaSize"],
#                     populationSize=scenario["populationSize"],
#                     minRange=scenario["minRange"],
#                     maxRange=scenario["maxRange"],
#                     problem=scenario["problem"],
#                     slice=scenario["slice"],
#                     selectType=scenario["selectType"],
#                     percentSlice=scenario["percentSlice"],
#                     mutationPercent =scenario["mutationPercent"]
#                 ) 
#             resultsSceanrios.append(bestValue)
    
    
#         data.append(resultsSceanrios)
    
#     # print(data)


#     plt.figure(figsize=(8, 6))
#     plt.boxplot(data, labels=[f'Cenário {index + 1}' for index, _ in enumerate(scenarioConjunt)])


#     plt.title('Boxplot dos Melhores Valores Globais em Diferentes Cenários', fontsize=14)
#     plt.xlabel('Cenários', fontsize=12)
#     plt.ylabel('Melhores Valores Globais', fontsize=12)


#     plt.show()

# scenarios1 = {"geracions":100,"genomaSize":30,"populationSize":30,"minRange":-100,"maxRange":100,"problem":"sphere","slice":2,"selectType":"Proporcionalidade","percentSlice":0.75,"mutationPercent":0.1}
# scenarios2 = {"geracions":100,"genomaSize":30,"populationSize":30,"minRange":-30,"maxRange":30,"problem":"sphere","slice":2,"selectType":"Proporcionalidade","percentSlice":0.75,"mutationPercent":0.1}
# scenarios3 = {"geracions":100,"genomaSize":30,"populationSize":30,"minRange":-5.12,"maxRange":5.12,"problem":"sphere","slice":2,"selectType":"Proporcionalidade","percentSlice":0.75,"mutationPercent":0.1}

# plotGraft(scenario1=scenarios1,
#           scenario2=scenarios2,
#           scenario3=scenarios3,
#           execution=30)

