import nltk
import sys
import os
import string
import numpy as np

FILE_MATCHES = 1
SENTENCE_MATCHES = 3



def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), encoding='utf-8') as f:
            files[filename] = f.read()

    return files

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    document = document.lower()
    processed = nltk.word_tokenize(document)
    check_words = processed

    for word in check_words:
        if word in string.punctuation:
            processed.remove(word)
        if word in nltk.corpus.stopwords.words('english'):
            processed.remove(word)
    return processed


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()

    for document in documents:
        already_added = set()
        for word in documents[document]:
            if word not in idfs:
                idfs[word] = 1
                already_added.add(word)
            elif word not in already_added:
                idfs[word] += 1
                already_added.add(word)

    for word in idfs:
        idfs[word] = np.log( len(documents) / idfs[word] )

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfs = dict()

    for file in files:
        tfs[file] = dict()
        for word in files[file]:
            if word not in tfs[file]:
                tfs[file][word] = 1
            else:
                tfs[file][word] += 1

    tf_idfs = dict()

    for file in files:
        for word in query:
            if word in files[file]:
                if file not in tf_idfs:
                    tf_idfs[file] = tfs[file][word] * idfs[word]
                else:
                    tf_idfs[file] = tf_idfs[file] + (tfs[file][word] * idfs[word])

    matching_files = [x for (x, y) in sorted(tf_idfs.items(), key=lambda item: item[1])]

    matching_files.reverse()

    return matching_files[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    summed_idfs = dict()

    term_density = dict()

    for sentence in sentences:
        summed_idfs[sentence] = 0
        term_density[sentence] = 0

        for word in query:
            if word in sentences[sentence]:
                summed_idfs[sentence] += idfs[word]
        for word in sentences[sentence]:
            if word in query:
                term_density[sentence] += 1

        term_density[sentence] = term_density[sentence] / len(sentences[sentence])

    matching_sentences = [x for (x, y) in sorted(summed_idfs.items(), key=lambda item: item[1])]
    matching_sentences.reverse()

    first = matching_sentences[0]
    copy = matching_sentences
    for i, sentence in enumerate(copy):
        if summed_idfs[sentence] == summed_idfs[first]:
            if term_density[sentence] > term_density[first]:
                matching_sentences[0] = matching_sentences[i]
                matching_sentences[i] = first
                first = matching_sentences[0]
   
    return matching_sentences[:n]




if __name__ == "__main__":
    main()
