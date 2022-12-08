import os
import sys
import math
import csv

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

def calculateP15(trecData, relevData, queryNum):
    relevantCount = 0
    for i in range(1, min(16, len(trecData[queryNum])+1)):
        curDoc = trecData[queryNum][str(i)]["document"]
        if curDoc not in relevData[queryNum]:
            continue
        if relevData[queryNum][curDoc] == str(1):
            relevantCount += 1

    return relevantCount / 15

def calculateR20(trecData, relevData, queryNum):
    #first count all the relevant documents
    allRelv = 0
    count = 0
    # print(relevData[queryNum])
    for i in relevData[queryNum]:
        if relevData[queryNum][i] == '1':
            count += 1

    for i in range(1, min(len(trecData[queryNum]) + 1, 21)):
        curDoc = trecData[queryNum][str(i)]["document"]
        if curDoc not in relevData[queryNum]:
            continue
        if relevData[queryNum][curDoc] == str(1):
            allRelv += 1

    if count == 0:
        return 0
    return allRelv/count

def calculateF1(trecData, relevData, queryNum):
    allRelv = 0
    count = 0
    # print(relevData[queryNum])
    for i in relevData[queryNum]:
        if relevData[queryNum][i] == '1':
            count += 1

    for i in range(1, min(len(trecData[queryNum]) + 1, 26)):
        curDoc = trecData[queryNum][str(i)]["document"]
        if curDoc not in relevData[queryNum]:
            continue
        if relevData[queryNum][curDoc] == str(1):
            allRelv += 1

    if allRelv == 0:
        return 0
    return (2 * allRelv/count * allRelv/25)/((allRelv/count) + (allRelv/25))

def calculateAP(trecData, relevData, queryNum):
    recall = 0
    percision = 0
    count = 0
    for i in relevData[queryNum]:
        if relevData[queryNum][i] == '1':
            count += 1

    for i in range(1, len(trecData[queryNum])+1):
        curDoc = trecData[queryNum][str(i)]["document"]
        if curDoc not in relevData[queryNum]:
            continue
        if relevData[queryNum][curDoc] == '1':
            recall += 1
            percision += recall/i

    if count == 0:
        return 0
    return percision / count

def writeFile(outputFile, data):

    outFile = open(outputFile, "w")
    totalData = {'ndcg': 0, 'rr': 0, 'p15': 0, 'r20': 0, 'f1': 0, 'ap': 0}

    for d in data:
        totalData['ndcg'] += data[d]["ndcg"]
        totalData['rr'] += data[d]["rr"]
        totalData['p15'] += data[d]["p15"]
        totalData['r20'] += data[d]["r20"]
        totalData['f1'] += data[d]["f1"]
        totalData['ap'] += data[d]["ap"]
        outFile.write(f'NDCG@75 {d} {data[d]["ndcg"]}\n')
        outFile.write(f'RR {d} {data[d]["rr"]}\n')
        outFile.write(f'P@15 {d} {data[d]["p15"]}\n')
        outFile.write(f'R@20 {d} {data[d]["r20"]}\n')
        outFile.write(f'F1@25 {d} {data[d]["f1"]}\n')
        outFile.write(f'AP {d} {data[d]["ap"]}\n')
    

    outFile.write(f'NDCG@75 all {totalData["ndcg"]/len(data.keys())}\n')
    outFile.write(f'MRR all {totalData["rr"]/len(data.keys())}\n')
    outFile.write(f'P@15 all {totalData["p15"]/len(data.keys())}\n')
    outFile.write(f'R@20 all {totalData["r20"]/len(data.keys())}\n')
    outFile.write(f'F1@25 all {totalData["f1"]/len(data.keys())}\n')
    outFile.write(f'MAP all {totalData["ap"]/len(data.keys())}\n')

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

    data = {}

    for query in trecData:
        if query not in data:
            data[query] = {}
        data[query]['ndcg'] = calculateNDCG(trecData, relevData, query)
        data[query]['rr'] = calculateRR(trecData, relevData, query)
        data[query]['p15'] = calculateP15(trecData, relevData, query)
        data[query]['r20'] = calculateR20(trecData, relevData, query)
        data[query]['f1'] = calculateF1(trecData, relevData, query)
        data[query]['ap'] = calculateAP(trecData, relevData, query)
    
  


if __name__ == "__main__":
    main()