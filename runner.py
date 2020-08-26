from optparse import OptionParser
from pos import *
import json
import statistics

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="read text from FILE", metavar="FILE")
parser.add_option("-o", "--output", dest="output",
                  help="write report to FILE", metavar="OUTPUT_FILE")
parser.add_option("-t", "--text", dest="inputText",
                  help="process text from input")
parser.add_option("-n", "--chunksnumber", dest="chunksnumber",
                  help="split text in number of chunks")
parser.add_option("-s", "--chunksize", dest="chunksize",
                  help="split text in chunks of size")

(options, args) = parser.parse_args()
filename = vars(options)['filename']
output = vars(options)['output']
inputText = vars(options)['inputText']
chunksnumber = vars(options)['chunksnumber']
chunksize = vars(options)['chunksize']

if filename is not None:
    f = open(filename, 'r', encoding="utf-8")
    text = f.read()
    f.close()
elif inputText is not None:
    text = inputText
else:
    raise Exception('Input is not defined')
text = tokenize(text)
print (len(text))
if chunksnumber is not None:
    n = (len(text) / int(chunksnumber)) +1
elif chunksize is not None:
    n = int(chunksize)
else:
    n = len(text)
n = int(n)
print(n)

chunks = [text[i:i + n] for i in range(0, len(text), n)]
print(len(list(chunks)))
result = calculateChunksClasses(chunks)
chunksStat = calculateChunksStat(result)

row = "Section\t"
for className, stat in chunksStat.items():
    if className != "TotalWords":
        row += className + "\t"
row += "TotalWords"

print(row)
for i in range(0, len(chunks), 1):
    row = str(i) + "\t"
    for className, stat in chunksStat.items():
        if className != "TotalWords":
            row += str(chunksStat[className][i]) + "\t"
    row += str(chunksStat["TotalWords"][i])
    print(row)

row = "Section\t"
for className, stat in chunksStat.items():
    if className != "TotalWords":
        row += className + "\t"

print(row)
cnt = {}
for i in range(0, len(chunks), 1):
    row = str(i) + "\t"
    for className, stat in chunksStat.items():
        if className != "TotalWords":
            if className not in cnt:
                cnt[className] = []
            chunkClassStat = chunksStat[className][i] / float(chunksStat["TotalWords"][i])
            row += "{0:.2f}".format(chunkClassStat) + "\t"
            cnt[className].append(chunkClassStat)
    print(row)

row = "MEAN\t"
for className, stat in chunksStat.items():
    if className != "TotalWords":
        #print(cnt[className])
        row += "{0:.2f}".format(statistics.mean(cnt[className])) + "\t"
print(row)
row = "STDEV\t"
for className, stat in chunksStat.items():
    if className != "TotalWords":
        row += "{0:.2f}".format(statistics.stdev(cnt[className])) + "\t"
print(row)

if output is not None:
     f = open(output, 'w');
     f.write(json.dumps(result, indent=4, sort_keys=True))
     f.write(json.dumps(chunksStat, indent=4, sort_keys=True))
     f.close()
else:
    print(result)
    print(chunksStat)