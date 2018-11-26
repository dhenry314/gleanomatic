import sys
import os

volMount = '/var/lib/docker/volumes/gleanomatic_rs-static/_data/'

if len(sys.argv) < 3:
    print("USAGE: dumpSource.py {sourceName} {targetPath}")
    exit()

sourceName = sys.argv[1]
targetPath = sys.argv[2]
sourceDir = str(volMount) + str(sourceName) + '/'

f = open(targetPath,"w+")
f.write('[')

#print(sourceDir)

nsPaths = []

try:
    for file in os.listdir(sourceDir):
        if os.path.isdir(str(sourceDir) + str(file)):
            nsPaths.append(str(sourceDir) + str(file))
except Exception as e:
    print(e)
    exit()

n = 0

for nsPath in nsPaths:
    #debug
    print(nsPath)
    dumpDirs = []
    try:
        for tsFile in os.listdir(nsPath):
            if os.path.isdir(str(nsPath) + "/" + str(tsFile)):
                dumpDir = int(tsFile)
                dumpDirs.append(dumpDir)
    except Exception as e:
        print(e)
        exit()
    #iterate through each dumpDir starting with the latest 
    ids = []
    dumpDirs.sort()
    dumpDirs.reverse()
    for dumpDir in dumpDirs:
        manifestPath = str(nsPath) + "/" + str(dumpDir) + "/manifest"
        with open(manifestPath) as fp:  
            line = fp.readline()
            cnt = 1
            while line:
                if '><' not in line:
                   break
                parts = line.split('><')
                subParts = parts[1].split("/")
                fName = subParts[-1]
                hashID = fName.replace('.json','')
                if hashID in ids:
                    line = fp.readline()
                    continue
                docPath = str(nsPath) + "/" + str(dumpDir) + "/" + str(parts[1])
                cf = open(docPath,"r")
                contents = cf.read()
                if n > 0:
                    f.write(',')
                n = n + 1
                f.write(contents)
                ids.append(hashID)
                print(n)
                try:
                    line = fp.readline()
                except:
                    line = None
        fp.close()

f.write(']')
f.close()
