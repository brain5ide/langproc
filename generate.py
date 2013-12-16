# random paketas atsitiktiniam zodziu sudeliojimui
import random

# regular expressions paketas patogiam skaidymui i tris dalis
import re

# file that contains words
wordfile = 'wordlists/EN.txt'

# number of words to produce
wordnum = 10

# calculate Damerau-Levenshtein distance between to given strings
def dam_lev_dist(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in xrange(-1,lenstr1+1):
        d[(i,-1)] = i+1
    for j in xrange(-1,lenstr2+1):
        d[(-1, j)] = j+1

    for i in xrange(lenstr1):
        for j in xrange(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i,j)] = min(
                            d[(i-1,j)] + 1, # deletion
                            d[(i,j-1)] + 1, # insertion
                            d[(i-1,j-1)] + cost, # substitution
                          )
            if i and j and s1[i]==s2[j-1] and s1[i-1] == s2[j]:
                d[(i, j)] = min (d[(i, j)], d[i-2, j-2] + cost) # transposition
    return d[lenstr1-1,lenstr2-1]

allwords = [w.strip() for w in open(wordfile, "rb").readlines()]

used_words = random.sample(allwords, wordnum)
plaintext = " ".join(used_words)

split_text = re.findall('...?', plaintext) 
crypt_split = split_text[:]
random.shuffle(crypt_split)
crypt_text = ''.join(crypt_split) 


