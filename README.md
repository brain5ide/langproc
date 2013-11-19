langproc
========

langproc - natural language processing solution

Tags: dictionary search, semantic and linguisstic analysis

Task: The input data is divided into scrambled columns of three characters.
The objective is to retrieve the original text from this scrambled input.

Languages: Lithuanian(only latin alphabet), English.

  a) Use a dictionary that is freely available or personally constructed.
  b) Don't use a dictionary
  
Guidelines: 

  Dictionary part can be solved by just iteratinv over all permutations of given input
and finding the one with the best match. Of course, some words(especially the Proper noungs)
may not be in the dictionary.
  Part without dictionary will have to use a model of a generalized language, that would be
trained using dictionaries of various languages, by derviation of tasks or in any other way. 
