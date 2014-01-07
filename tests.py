import generate as gen
import re

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
    used = gen.used_triplets(words)
    print 'Words: ', used
    #print 'Used: ', used
    #phrases = gen.phrases(used)
    retrieved, left = gen.fit_wordset(used, scrambled)
    #print 'Retrieved: ', retrieved
    for item in retrieved:
        joined = ''.join(item[0])
        if '  ' in joined[:-2]:
            continue
        found = True
        for inword in item[1]:
            if not re.search(r'\b'+inword+r'\b', joined):
                found = False

        if found is True:
            print 'String: ', joined, left
    print 'Answers: ', len(retrieved)

   #print 'Phrases: '
    #print_phrase(phrases)
    #phrases = gen.phrases(phrases)
    #print 'Phrases: '
    #print_phrase(phrases)
    ## TODO IN HERE
    print ' '


def print_phrase(word_dict):
    #for key in word_dict:
    #    print 'Phrase: ', key, word_dict[key]
    print '# of phrases: ', len(word_dict), len(set(word_dict))

test_string = 'simple sentence testing scrambled algorithm'
test_dict(test_string, allwords)
