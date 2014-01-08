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
    print 'ALl words: ', words
    used = gen.used_triplets(words)
    print 'Words: ', used
    #print 'Used: ', used
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

    ## TODO IN HERE
    print ' '

test_string = ' simple sentence testing scrambled algorithm'
test_dict(test_string, allwords)
#gen.triplet_permutations(gen.symbols, allwords)
