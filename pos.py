import nltk
from nltk.stem import PorterStemmer
from nltk import word_tokenize, pos_tag, FreqDist
from nltk.tag import StanfordPOSTagger
from nltk.tokenize import StanfordTokenizer
import re
import functools

from optparse import OptionParser
from collections import Counter


import classes

def find_ngrams(input_list, n):
    return list(zip(*[input_list[i:] for i in range(n)]))

def tokenize(text):
    tokeniser = StanfordTokenizer('/Users/etulika/Downloads/stanford-corenlp-2017-04-14-build.jar')
    tokens = tokeniser.tokenize(text)
    return tokens

def prepareClasses():
    classesConfig = classes.config
    def processClassPattern(classPattern):
        if isinstance(classPattern, list):
            pattern = map('_'.join, classPattern)
            pattern = {"ngram": str(len(classPattern)), "pattern": "\s".join(pattern)}
        else:
            pattern = {"ngram": str(1), "pattern": '_'.join(classPattern) + '$'}
        return pattern

    def joinNgrams(result, pattern):
        #print(result, pattern)
        if "ngram" in result:
            firstPattern = result
            result = {firstPattern["ngram"]: [firstPattern["pattern"]]}
            # print(result)
        if pattern:
            if pattern["ngram"] not in result:
                result[pattern["ngram"]] = []
            result[pattern["ngram"]].append(pattern["pattern"])
        return result

        # '(' + ')|('.join(newClasses[className]) + ')'

    def combinePatterns(pattern):
        return "(" + ")|(".join(pattern) + ")"

    newClasses = {}

    for className, classPatterns in classesConfig.items():

        newClasses[className] = map(processClassPattern, classPatterns)
        cl = list(newClasses[className])

        if len(cl) == 1:
            newClasses[className] = joinNgrams(cl[0], None)
        else:
            newClasses[className] = functools.reduce(joinNgrams, cl)
        newClasses[className] = {k: combinePatterns(v) for k, v in newClasses[className].items()}

    compactClasses = {}
    for className, classPatterns in classesConfig.items():
        for ngramDimension, v in newClasses[className].items():
            if (ngramDimension not in compactClasses):
                compactClasses[ngramDimension] = []
            compactClasses[ngramDimension].append("(?P<" + className + ">" + v + ")")
    for ngramDimension, pattern in compactClasses.items():
        compactClasses[ngramDimension] = "|".join(compactClasses[ngramDimension])
            #map(combinePatterns, newClasses[className])
    return compactClasses

def getMappedTaggedStemmed(tokens):
    st = StanfordPOSTagger('english-bidirectional-distsim.tagger',
                           '/Users/etulika/Services/stanford-postagger-2016-10-31/stanford-postagger.jar')

    tagged = st.tag(tokens)
    newText = []
    for pair in tagged:
        newText.append(pair[0])

    porter = PorterStemmer()
    stemmed = [porter.stem(word) for word in newText]

    taggedstemmed = list(zip(list(zip(*tagged))[1], [word.lower() for word in stemmed]))
    mappedTaggedStemmed = map('_'.join, taggedstemmed)
    return list(mappedTaggedStemmed)

def calculateClasses(mappedTaggedStemmed, newClasses):

    result = {
        'chunkWords': mappedTaggedStemmed,
        'TotalWords': Counter({'words': len(list(mappedTaggedStemmed))})
    }

    for ngramDimension, patterns in newClasses.items():
        if ngramDimension == 1:
            ngrams = list(mappedTaggedStemmed)
        else:
            ngrams = find_ngrams(list(mappedTaggedStemmed), int(ngramDimension))

        r = re.compile(patterns)

        for word in ngrams:
            word = " ".join(word);
            m = r.match(word)
            if m:
                for className, value in m.groupdict().items():
                    if className not in result:
                        result[className] = Counter()
                    if value is not None:
                        result[className][word] += 1

    return result

def calculateChunksClasses(chunks):
    classesConfig = prepareClasses()
    chunkNum = 1
    result = []
    for chunk in chunks:
        taggedStemmed = getMappedTaggedStemmed(chunk)
        result.append(calculateClasses(taggedStemmed, classesConfig))
        chunkNum += 1
    return result

def calculateChunksStat(chunksClasses):
    print(chunksClasses)
    chunksStat = {}
    for className, classPattern in classes.config.items():
        chunksStat[className] = []
    chunksStat["TotalWords"] = []
    for chunkClassesCount in chunksClasses:
        for className, stat in chunksStat.items():
            if (className in chunkClassesCount):
                chunksStat[className].append(sum(chunkClassesCount[className].values()))
            else:
                chunksStat[className].append(0)
    return chunksStat
