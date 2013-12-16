# random paketas atsitiktiniam zodziu sudeliojimui
import random

# regular expressions paketas patogiam skaidymui i tris dalis
import re

# file that contains words
wordfile = 'wordlists/EN.txt'

# number of words to produce
wordnum = 10

# calculate modified Damerau-Levenshtein distance between to given strings
# don't calculate insertion and deletion distance
# by default don't calculate transposition distance but
#   if trans == True  - calculate transposition distance
def dam_lev_dist(s1, s2, trans=False):
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
            d[(i,j)] = d[(i-1,j-1)] + cost # substitution
            if(trans == True):
                if i and j and s1[i]==s2[j-1] and s1[i-1] == s2[j]:
                    d[(i, j)] = min (d[(i, j)], d[i-2, j-2] + cost) # transposition
    return d[lenstr1-1,lenstr2-1]

allwords = [w.strip() for w in open(wordfile, "rb").readlines()]

words_subset = random.sample(allwords, wordnum*wordnum)
used_words = random.sample(words_subset, wordnum)
plaintext = " ".join(used_words)

split_text = re.findall('...?', plaintext) 
crypt_split = split_text[:]
random.shuffle(crypt_split)
crypt_text = ''.join(crypt_split) 

def unscramble(plain, crypt):
    plain = list(plain)
    crypt = list(crypt)
    lenplain = len(plain)
    lencrypt = len(crypt)

    for i in xrange(lencrypt):
        for j in xrange(lencrypt):
            before = dam_lev_dist(plain, crypt)
            if before == 0:
                return crypt
            crypt[i], crypt[j] = crypt[j], crypt[i] 
            after = dam_lev_dist(plain, crypt) 
            if after >= before:
                print 'before: ', before, ' after: ', after
                crypt[i], crypt[j] = crypt[j], crypt[i]
    return crypt

# pick only words that are possible with given sequence
def possible_words(wlist, crypt):
    poss = []
    for word in wlist:
        found = any(item in ' '+word+' ' for item in crypt)
        if found:
            poss.append(word)
    return poss
