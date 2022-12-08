import csv
import os

# os.remove(evaluationTable")

fileList = ["ql.eval", "bm25.eval", "sdm.eval"]
totalData = {}

for f in fileList:
    readFile = open(f, "r")
    lines = readFile.readlines()
    for l in lines:
        cond = l.split(" ")
        if cond[0] == "AP" or "MAP":
            if cond[1] not in totalData:
                totalData[cond[1]] = {}
            if f == "ql.eval":
                totalData[cond[1]]["ql"] = cond[2]
            if f == "bm25.eval":
                totalData[cond[1]]["bm25"] = cond[2]
            if f == "sdm.eval":
                totalData[cond[1]]["sdm"] = cond[2]


fi = open("evaluationTable.csv", "w")
writer = csv.writer(fi)
writer.writerow(["queryNum", "ql", "bm25", "sdm"])

for d in totalData:
    writer.writerow([d, float(totalData[d]["ql"]), float(totalData[d]['bm25']), float(totalData[d]['sdm'])])

