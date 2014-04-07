import re


def validation(string):

    expr = "[A-Z]"
    expr += "(?:[^.?!]+|"
    expr += "[^a-zA-Z0-9-_]"
    expr += "(?:[a-zA-Z0-9-_].\d+\.|a\.[\s\-]?A\.)"
    expr += ")"
    expr += "{3,}[\.\?\!]+(?!\s[a-z])"

    sentences = re.findall(expr, string + ' .')
    print '\t', ' '.join(sentences)
    print '\t', string
    if ' '.join(sentences) != string:
        if len(re.findall('[!?.]', string)) == 0:
            return True
        else:
            return False
    else:
        return True

tests = []
tests.append(["This is a valid sentence.", True])
tests.append(["This sentence should be valid too!", True])
tests.append(["Is this a valid sentence?", True])
tests.append(["How is this a valid sentence? Should this one be too?", True])
tests.append(["This is a valid sentence(assuming we allow brackets).", True])
tests.append(["Why is this not a valid sentence, it it is one?", True])
tests.append(["This should not be. valid", False])
tests.append(["This. should not Be valid.", False])
tests.append(["This should. not Be valid?", False])
tests.append([". this is not a valid Sentence", False])
tests.append(["Very smart thought that should not end here...", True])
tests.append(["How about a sentence without an ending", True])
tests.append(["This is two parts: first one; and the second one.", True])
tests.append(["This \"has quotations in it\" and is very versatile.", True])
tests.append(["this starts with a small letter and is false.", False])
tests.append(["This sentence has abbr. but should be true.", True])
tests.append(["This is valid. But. this is not", False])
tests.append(["this is Not a valid sentence.", False])
tests.append(["Simple sentence testing scrambled algorithm. OK!", True])

for item in tests:
    rez = validation(item[0])
    print rez == item[1], rez, item[1], '\t\t\t', item[0]
