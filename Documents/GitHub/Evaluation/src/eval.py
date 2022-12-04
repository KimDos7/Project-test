import os
import sys
import math

def calculateNDCG(trecData, relevData, queryNum):
    firstRank = trecData[queryNum]['1']["document"]
    idealRanks = []

    if firstRank not in relevData[queryNum]:
        dcg = 0
    else:
        dcg = int(relevData[queryNum][firstRank])

    for ranks in relevData[queryNum]:
        idealRanks.append(int(relevData[queryNum][ranks]))
    
    for i in range(2, min(len(trecData[queryNum]), 75)):
        curDoc = trecData[queryNum][str(i)]["document"]
        if curDoc not in relevData[queryNum]:
            relevance = 0
        else:
            relevance = relevData[queryNum][curDoc]
        dcg += int(relevance) / math.log2(i)

    idealRanks = sorted(idealRanks, reverse=True)
    idcg = idealRanks[0]
    for i in range(1, 75):
        idcg += idealRanks[i]/math.log2(i+1)

    if idcg == 0:
        return 0
    return dcg/idcg 

def calculateRR(trecData, relevData, queryNum):
    for i in range(1, len(trecData[queryNum])+1):
        curDoc = trecData[queryNum][str(i)]["document"]
        if curDoc not in relevData[queryNum]:
            continue
        if relevData[queryNum][curDoc] == str(1):
            return 1/i

    return 0

def main():
    argv_len = len(sys.argv)
    trec = sys.argv[1] if argv_len >= 2 else 'runfile.trecrun'
    queriesFile = sys.argv[2] if argv_len >= 3 else 'qrels'
    outputFile = sys.argv[3] if argv_len >= 4 else 'outputFile.eval'

#parse the trecrun file and create a hasmap based on the query number. 
#each query will have another object with the keys of the doc name, and its rank and score
    trecData = {}
    relevData = {}

    trecFile = open(trec, "r")
    trecLines = trecFile.readlines()
    for l in trecLines:
        words = l.split(" ")
        if words[0] not in trecData:
            trecData[words[0]] = {}
        trecData[words[0]][words[3]] = {"document": words[2], "score": words[4]}
    trecFile.close()

    relevFile = open(queriesFile, "r")
    relevLines = relevFile.readlines()
    for line in relevLines:
        words = line.split(" ")
        if words[0] not in relevData:
            relevData[words[0]] = {}
        relevData[words[0]][words[2]] = words[3].strip()


    for query in trecData:
        calculateNDCG(trecData, relevData, query)
        print(calculateRR(trecData, relevData, query))

if __name__ == "__main__":
    main()