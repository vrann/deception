from pos import *

# chunks = [
#    ['helped', 'to', 'see'],
#    ["helped", "the", "young", "lady", "to", "see"],
#    ["stopped", "him", "going"],

#   ["try", "to", "eat"],
#   ["tell", "him", "to", "go"],
#   ["tell", "my", "friend", "to", "go"],
#   ["avoid", "eating"],
#   ["stop", "him", "eating"],
#   ["prevent", "him", "from", "eating"],
#   ["I", "believe", "that"],
#   ["said", "he", "went"],
#   ["I", "me", "myself", "my", "of", "mine"],
#   ["us", "ours", "ourselves", "ours"],
#   ["you", "your", "yours", "yourself"]
# ]

#import re
#r = re.compile("((((?!is)|(?!wa)|(?!do)|(?!have)).)*)")

#r = re.compile("^((?!.*(bar|mitzva)).*)$")
#m = r.match("brometer")
#print(m.groups())

chunks = [
        #["he", "him", "his", "himself", "it", "its", "itself", "them", "theirs", "their", "they", "themselves", "one",
        # "ones"],
        #tokenize("Now she does but one might not later"),
        #tokenize("It is better to use one's own money"),
        #tokenize("anyone anything something someone whenever whatever whichever wherever whoever")
        #tokenize("not do don't neither never no nobody none nope nor nothing nowhere without only unless hardly bare")
        #tokenize("all another both each either every half many much some such them these that this those")
        #tokenize("all an another any both del each either every half la many much nary neither no some such that the them these this those"),
        #tokenize("I saw many of them")
        #tokenize("help to develop"),
        #tokenize("is to confirm"),
        #tokenize("help them to improve"),
        tokenize("am are is was were be been being will"),
        tokenize("here I am"),
        tokenize("being has had")
    ]
result = calculateChunksClasses(chunks)
chunksStat = calculateChunksStat(result)

print(result)
print(chunksStat)