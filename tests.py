import generate as gen
import re
import pprint

wordfile = 'wordlists/EN.txt'

allwords = [w.strip() for w in open(wordfile, "rb").readlines()]

TEST_COUNT = 0


def test_dict(plaintext, wlist):
    global TEST_COUNT
    TEST_COUNT = TEST_COUNT + 1
    print '------ TEST', TEST_COUNT, '------'
    print 'Testing string: ', plaintext
    scrambled = gen.scramble(plaintext)
    print 'Scrambled: ', ''.join(scrambled)
    words = gen.smart_words(wlist, scrambled, 4)
    print 'All words: ', words
    phrases = gen.phrases(words)
    phrase_beg = gen.phrase_beg(words)
    phrase_end = gen.phrase_end(words)
    print 'Phrase_beg: ', len(phrase_beg), phrase_beg
    print 'Phrase_end: ', len(phrase_end), phrase_end
    print 'Phrases: ', len(phrases), phrases

    phrase2_beg = gen.phrase_beg(phrases)
    phrase2_end = gen.phrase_end(phrases)
    phrases2 = gen.phrases(dict(words.items() + phrases.items()))

    possible_phrases = gen.possible_phrases(phrases, scrambled)
    possible2 = gen.phrases(dict(words.items() + possible_phrases.items()))
    possible2_phrase = gen.possible_phrases(possible2, scrambled)
    possible3 = gen.phrases(dict(words.items() + possible2_phrase.items()))
    possible3_phrase = gen.possible_phrases(possible3, scrambled)
    possible4 = gen.phrases(dict(words.items() + possible3_phrase.items()))
    possible4_phrase = gen.possible_phrases(possible4, scrambled)
    possible5 = gen.phrases(dict(words.items() + possible4_phrase.items()))
    possible5_phrase = gen.possible_phrases(possible5, scrambled)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(possible5_phrase)

    print 'Phrase2_beg: ', phrase2_beg
    print 'Phrase2_end: ', phrase2_end
    print 'Phrases2: ', phrases2
    print 'Len phrase_beg: ', len(phrase_beg)
    print 'Len phrase_end: ', len(phrase_end)
    print 'Len phrases: ', len(phrases)
    print 'Len phrase2_beg: ', len(phrase2_beg)
    print 'Len phrase2_end: ', len(phrase2_end)
    print 'Len phrases2: ', len(phrases2)
    print 'Len possible: ', len(possible_phrases)
    print 'Len with possible2: ', len(possible2)
    print 'Possible2 len: ', len(possible2_phrase)
    print 'Len with possible3: ', len(possible3)
    print 'Possible3 len: ', len(possible3_phrase)
    print 'Len with possible4: ', len(possible4)
    print 'Possible4 len: ', len(possible4_phrase)
    print 'Len with possible5: ', len(possible5)
    print 'Possible5 len: ', len(possible5_phrase)

    gen.max_phraselen(possible4_phrase)

    #phrase_phrase = gen.phrases(phrases)
    #used = gen.used_triplets(words)
    #print 'Words: ', used
    #print 'Used: ', used
    #retrieved, left = gen.fit_wordset(words, scrambled)
    ##print 'Retrieved: ', retrieved
    #sentences = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)
    #for item in retrieved:
    #    joined = ''.join(item[0])
    #    if '  ' in joined[:-2]:
    #        continue
    #    found = True
    #    for inword in item[1]:
    #        if not re.search(r'\b'+inword+r'\b', joined, re.IGNORECASE):
    #            found = False

    #    if joined != ''.join(sentences.findall(joined)):
    #        found = False

    #    if found is True:
    #        print 'String: ', joined, left
    #print 'Answers: ', len(retrieved)

    ### TODO IN HERE
    #print ' '

test_string = ' Simple sentence, testing scrambled algorithm. Another one to check again!'
test_dict(test_string, allwords)
#gen.triplet_permutations(gen.symbols, allwords)
