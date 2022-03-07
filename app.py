from cgitb import reset
from re import L
from bitarray import bitarray
from bitarray.util import int2ba
import itertools
from statistics import mean

BYTE_SIZE = 8

def readBinaryFile(filePath):
    wholeBitArray = bitarray()
    with open(filePath, 'rb') as readFile:
        wholeBitArray.fromfile(readFile)
    return wholeBitArray

def toBytes(bitArray):
    return bitArray.tobytes()

def removeZeroBytes(bitArray):
    for i in range(256):
        for j in range(8):
            bitArray.pop(8*(i+1))
    return bitArray

def createFunctions(bitArray):
    arrayOfFunctions = []
    numberOfBytes = len(bitArray)//BYTE_SIZE
    for bitIndex in range(0, BYTE_SIZE):
        funct = bitarray()
        for j in range(0, numberOfBytes):
            funct.append(bitArray[j*8+bitIndex])
        arrayOfFunctions.append(funct)
    return arrayOfFunctions

def isFunctionBalanced(funct):
    numberOfZeros = funct.count(0)
    numberOfOnes = funct.count(1)
    return numberOfZeros == numberOfOnes

def getIndexCombinations(size):
    result = []
    indexArray = list(range(0, size))
    for i in range(1, size+1):
        result += list(itertools.combinations(indexArray, i))
    return result

def buildLinearFunctions():
    array = []
    for i in range(256):
        newArray = bitarray('00000000')
        num = int2ba(i)
        for j in range(len(str(num.to01()))):
            newArray.pop()
        newArray.extend(int2ba(i))
        array.append(newArray)
    
    combs = getIndexCombinations(8)
    
    resultArray = []

    for comb in combs:
        partArray = bitarray()
        for bits in array:
            xs = []
            for index in comb:
                xs.append(int(bits[7-index]))
            partResult = xs[0]
            for i in range(1, len(xs), 1):
                partResult ^= xs[i]
            partArray.append(partResult)
        resultArray.append(partArray)
    
    zeros256 = "0" * 256
    resultArray.append(bitarray(zeros256))
    return resultArray

def nonlinearity(fileFuncs, linearFuncs):
    result = []
    for fileFunc in fileFuncs:
        fileFuncResults = []
        for linearFunc in linearFuncs:
            xorResult = []
            for i in range (256):
                xorResult.append(int(fileFunc[i] ^ linearFunc[i]))
            xorSum = sum(xorResult)
            fileFuncResults.append(xorSum)
        result.append(min(fileFuncResults))
    return result

def avg(array):
    return sum(array)/len(array)

    # verify SAC
def sac(fileFuncs):
    results = []
    for fileFunc in fileFuncs: # for every file function
        fileFuncResults = []
        for i in range(8):
            newFunc = []
            power2 = 2**i
            swapPairsNum = int(256/(power2*2))
            lastIndex = 0
            for j in range(swapPairsNum): # for every swap pair
                top = []
                bot = []
                for k in range(lastIndex, lastIndex+power2):
                    bot.append(int(fileFunc[k]))
                    lastIndex += 1
                for k in range(lastIndex, lastIndex+power2):
                    bot.append(int(fileFunc[k]))
                    lastIndex += 1
                newFunc += bot
                newFunc += top
            fileFuncResults.append(newFunc)
        results.append(fileFuncResults)

    sacs = []
    for fileFunc, funcResult in zip(fileFuncs, results):
        functionSacs = []
        for result in funcResult:
            xorFunction = []
            for i in range(256):
                xorFunction.append(fileFunc [1] ^ result[1])
            functionSacs.append(sum(xorFunction))
        average = avg(functionSacs)
        percentage = average / 256
        sacs.append(percentage)
        
    totalSac = avg(sacs)

    print("--- SAC for functions ---")
    print('\n'.join(str(el) for el in sacs))
    print("=-= AVG ---")
    print(totalSac)


rawBitArray = readBinaryFile('sbox.SBX')
bitArray = removeZeroBytes(rawBitArray)
myFileFunctions = createFunctions(bitArray)

for ff in myFileFunctions:
    print('Function is balanced:')
    print(isFunctionBalanced(ff))

myLinearFunctions = buildLinearFunctions()

myNonLinearity = nonlinearity(myFileFunctions, myLinearFunctions)
sac(myFileFunctions)
# print(rawBitArray)
# result = nonlinearity
print(myNonLinearity)