import pdb
#
import math
# random paketas atsitiktiniam zodziu sudeliojimui
import random

# regular expressions paketas patogiam skaidymui i tris dalis
import re

# itertools helps to create permutations
import itertools

deep = ''

symbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ', '.', ',', '?', '!', '(', ')', ':', ';', '-']

def triplet_permutations(syms, wordlist):
    punct = '[ .,?!\(\);:\-]'
    symperm = itertools.permutations(syms, 3)
    symlist = [''.join(p) for p in symperm]
    symdict = dict((key, []) for key in symlist)

    found = 0
    alnum = [key for key in symdict if re.match('[a-z][a-z][a-z]', key)]
    end1 = [key for key in symdict if re.match('[a-z]'+punct+punct, key)]
    end2 = [key for key in symdict if re.match('[a-z][a-z]'+punct, key)]
    beg1 = [key for key in symdict if re.match(punct+'[a-z][a-z]', key)]
    beg2 = [key for key in symdict if re.match(punct+punct+'[a-z]', key)]

    print 'all: ', len(symdict)
    print 'alnum: ', len(alnum)
    print 'end1: ', len(end1)
    print 'end2: ', len(end2)
    print 'beg1: ', len(beg1)
    print 'beg2: ', len(beg2)

    wordnum = 0
    for word in wordlist:
        wordnum += 1
        print wordnum, found
        for key in alnum:
            # if all symbols are alphanumeric
            if key in word:
                symdict[key].append(word)
                found += 1
                #print 'alnum', found
        for key in end1:
            if key[0] == word[-1]:
                symdict[key].append(word)
                found += 1
                #print 'end1', found
        for key in end2:
            if key[0:2] == word[-2:]:
                symdict[key].append(word)
                found += 1
                #print 'end2', found
        for key in beg1:
            if key[2] == word[0]:
                symdict[key].append(word)
                found += 1
                #print 'beg1', found
        for key in beg2:
            if key[1:] == word[0:2]:
                symdict[key].append(word)
                found += 1
                #print 'beg2', found
    print found

def dam_lev_dist(s1, s2, trans=False):
    """ calculate modified Damerau-Levenshtein distance between to given
    strings don't calculate insertion and deletion distance
    by default don't calculate transposition distance but
    if trans == True  - calculate transposition distance

    """

    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in xrange(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in xrange(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1

    for i in xrange(lenstr1):
        for j in xrange(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = d[(i - 1, j - 1)] + cost  # substitution
            if trans is True:
                if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                    # transposition
                    d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)
    return d[lenstr1 - 1, lenstr2 - 1]

def fit_wordset(words, tripletPool, start=''):
    global deep
    deep = deep+'  '
    LeftInPool = len(tripletPool)

    word_dict = words.copy()
    result = []
    for key in word_dict:
        #print deep, key, word_dict[key], tripletPool, start
        if start != '' and word_dict[key][0] != start:
            continue
        tripletsInPool = True

        if start != '':
            word_triplets = word_dict[key][1:]
        else:
            word_triplets = word_dict[key]

        for triplet in word_triplets:
            if triplet not in tripletPool:
                tripletsInPool = False
        if tripletsInPool is True:
            tryword = word_dict[key]
            word_dic = word_dict.copy()
            del(word_dic[key])
            newPool = [y for y in tripletPool if y not in tryword]
            all_a = re.match('[a-zA-Z][a-zA-Z][a-zA-Z]', tryword[-1])
            two_a = re.match('[a-zA-Z][a-zA-Z][ .,?!\(\);:\-]', tryword[-1])
            one_a = re.match('[a-zA-Z][ .,?!\(\);:\-][ .,?!\(\);:\-]', tryword[-1])
            if all_a or two_a or one_a:
                connecting_triplet = ''
            else:
                connecting_triplet = tryword[-1]

            arranged, pleft = fit_wordset(word_dic, newPool, connecting_triplet)

            if pleft < LeftInPool:
                result = []
                LeftInPool = pleft

            if pleft == LeftInPool:
                for item in arranged:
                    if connecting_triplet == '':
                        result.append([tryword + item[0], [key] + item[1]])
                    else:
                        result.append([tryword[:-1] + item[0], [key] + item[1]])

            if len(arranged) == 0:
                result.append([tryword, [key]])
    deep = deep[:-2]
    return result, LeftInPool


def print_keys(dictionary):
    for key in dictionary:
        print '--', key

def scramble(text):
    if len(text) % 3 == 1:
        text = text + '  '
    if len(text) % 3 == 2:
        text = text + ' '

    split = re.findall('...?', text)
    random.shuffle(split)
    return split


def used_triplets(word_dict):
    used = {}
    for key in word_dict:
        concat = ''.join(word_dict[key])
        mobj = re.search(key, concat)
        wordstart = int(math.floor(mobj.start() / 3))
        wordend = int(math.floor(mobj.end() / 3))
        if mobj.end() % 3 != 0:
            wordend += 1
        used[key] = word_dict[key][wordstart:wordend]
    return used


def smart_words(wlist, crypt, permlength=3):
    cryptset = set(crypt)
    cryptlist = list(cryptset)
    tr_length = int(math.ceil(len(crypt) / 3.0))
    print 'Triplet length of scrambled text: ', tr_length
    print 'Generating triplet permutations of length: ', permlength
    print 'Number of permutations: ', reduce(lambda x, y: x * y, list(xrange(int(math.ceil(len(crypt) / 3.0)), int(math.ceil(len(crypt) / 3 - permlength - 1)), -1)))
    permutations = [p for p in itertools.permutations(cryptlist, permlength)]
    print 'Finding words in permutations'
    perms = [''.join(p) for p in permutations]
    print 'Making a flat list of permutations'
    permarr = zip(perms, permutations)
    permwords = [[w, sublist[1]] for sublist in permarr for w in sublist[0].strip().split(' ')]
    for word in permwords:
        if word[0] == 'simple':
            print 'simple', word[1]
    print 'Generating a dict'
    permdict = dict((key, value) for [key, value] in permwords)
    print 'Permutations completed'
    print 'Number of unique permutations: ', len(permdict)
    print 'Starting search of known words'
    found = {}
    for word in wlist:
        if word in permdict:
            found[word] = permdict[word]
    print 'Found', len(found), 'words'
    return found
