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
    LeftInPool = len(tripletPool)

    dset = False
    word_dict = words.copy()
    result = []
    for key in word_dict:
        for word in word_dict[key]:
            if dset is not True:
                deep = deep+'->'+key.zfill(10)
                dset = True
            print deep, key, word_dict[key], tripletPool, start
            if start != '' and word[0] != start:
                continue
            tripletsInPool = True

            if start != '':
                word_triplets = word[1:]
            else:
                word_triplets = word

            for triplet in word_triplets:
                if triplet not in tripletPool:
                    tripletsInPool = False
            if tripletsInPool is True:
                tryword = word
                word_dic = word_dict.copy()
                #del(word_dic[key])
                newPool = tripletPool[:]
                for y in tryword:
                    if y in newPool:
                        newPool.remove(y)

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
    deep = deep[:-12]
    dset = True
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
    tr_length = int(math.ceil(len(crypt)))
    print 'Triplet length of scrambled text: ', tr_length
    print 'Generating triplet permutations of length: ', permlength
    print 'Number of permutations: ', reduce(lambda x, y: x * y, list(xrange(int(math.ceil(len(crypt) / 3.0)), int(math.ceil(len(crypt) / 3 - permlength - 1)), -1)))
    if len(crypt) <= permlength:
        permutations = [p for p in itertools.permutations(cryptlist)]
    else:
        permutations = [p for p in itertools.permutations(cryptlist, permlength)]
    print 'Finding words in permutations'
    perms = [''.join(p) for p in permutations]
    print 'Perms', perms
    print 'Making a flat list of permutations'
    permarr = zip(perms, permutations)
    permwords = [[w, sublist[1]] for sublist in permarr for w in sublist[0].strip().split(' ')]
    print 'Generating a dict'
    permdict = {}
    for key, value in permwords:
        concat = ''.join(value)
        mobj = re.search(key, concat)
        wordstart = int(math.floor(mobj.start() / 3))
        wordend = int(math.floor(mobj.end() / 3))
        if mobj.end() % 3 != 0:
            wordend += 1
        cleanword = value[wordstart:wordend]
        if key in permdict:
            if cleanword not in permdict[key]:
                permdict[key] = permdict[key] + [cleanword]
        else:
            permdict[key] = [cleanword]

    #permdict = dict((key, value) for [key, value] in permwords)
    print 'Permutations completed'
    print 'Number of unique permutations: ', len(permdict)
    print 'Starting search of known words'
    found = {}
    for word in wlist:
        if word in permdict:
            found[word] = permdict[word]
    print 'Found', len(found), 'words'
    return found


