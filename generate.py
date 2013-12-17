#
import math
# random paketas atsitiktiniam zodziu sudeliojimui
import random

# regular expressions paketas patogiam skaidymui i tris dalis
import re

# itertools helps to create permutations
import itertools

# file that contains words
wordfile = 'wordlists/EN.txt'

# number of words to produce
wordnum = 100 

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

words_subset = random.sample(allwords, wordnum*100)
used_words = random.sample(words_subset, wordnum)
plaintext = " ".join(used_words)
if len(plaintext) % 3 == 1:
    plaintext = plaintext+'  '

if len(plaintext) % 3 == 2:
    plaintext = plaintext+' '

split_text = re.findall('...?', plaintext) 
crypt_split = split_text[:]
random.shuffle(crypt_split)

def scramble(text):
    split = re.findall('...?', text)
    random.shuffle(split)
    return split

def smart_words(wlist, crypt):
    cryptset = set(crypt)
    cryptlist = list(cryptset)
    perms = [''.join(p).split(' ') for p in itertools.permutations(cryptlist,4)]
    permwords = [w for sublist in perms for w in sublist]
    permset = set(permwords)
    found = []
    for word in wlist:
        if word in permset:
            found.append(word)
    return found
    
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

# can word be found in scrambled text
def is_inscrambled(word, crypt):
    num = triplets_match_word(word,crypt)
    if (len(num) >= math.ceil(len(word)/3.0)):
        perms = list(itertools.permutations(num, math.ceil(len(word)/3.0))) 
        for item in perms:
            if re.match(".*"+word+".*",''.join(item)):
                return item
        return False
    else:
        return False

# ignore triplest that have a spacebar in the middle '. .'
def probable_words(wlist, crypt):
    prob = []
    cnt = 0
    for item in wlist:
        if cnt % 1000 == 0:
            print 'Words checked:', cnt, '/', len(wlist), ' Found:', len(prob)
        cnt = cnt + 1
        if is_inscrambled(item,crypt):
            prob.append(item)
    return prob

def actual_words(wlist, crypto):
    crypt = crypto[:]
    prob = probable_words(wlist, crypt)
    prob.sort(lambda x,y: cmp(len(y), len(x)))
    
    actual_words = []
    for word in prob:
        word_triplets = is_inscrambled(word, crypt)
        if word_triplets:
            actual_words.append(word)
            for o in set(word_triplets):
                if (' ' in o) == True:
                    try:
                        print 'Removing: ', o
                        crypt.remove(o)
                    except ValueError:
                        pass
    print crypt
    return actual_words

def triplets_match_word(word, crypt):
    cry = []
    for item in crypt:
        if triplet_matches_word(word,item):
            cry.append(item)
    return cry

def triplet_matches_word(word, triplet):
    if re.match(".*"+triplet+".*", word):
        return True
    if re.match(". "+word[0:1], triplet):
        return True
    if re.match(" "+word[0:2], triplet):
        return True
    if re.match(word[-2:]+" ", triplet):
        return True
    if re.match(word[-1:]+" .", triplet):
        return True
    if re.match(".*"+word+".*", triplet):
        return True
    return False
