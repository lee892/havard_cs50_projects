import parser
import nltk
import sys



TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP

AP -> Adv | Adv AP | Adj | Adj AP
NP -> N | Det NP | AP NP | N PP
PP -> P NP
VP -> V | V NP | V NP PP
"""


sentence = "The dog chased the cat"


grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
Parser = nltk.ChartParser(grammar)

s = parser.preprocess(sentence)

trees = list(Parser.parse(s))

for tree in trees:
	print(tree.subtrees())