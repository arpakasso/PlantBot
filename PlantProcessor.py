# CS 4301.001 PlantBot Project Part 1
# Reena Suh & Elizabeth Trinh
# September 24, 2018

import re
import os
import shutil
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def main():
    final_vocab = {}
    if not os.path.exists(newdir):                                          # make new dir for new files
        os.makedirs(newdir)
    for root, dirs, files in os.walk(plantdir):                             # walk through all the files in OG dir
        for filename in files:
            oldname = os.path.join(os.path.abspath(root), filename)         # old file path
            v2name = os.path.join(newdir, filename)                         # new file path
            if not os.path.exists(newdir):                                  # if folder doesn't exist, don't create
                print(newdir + ' not found')
                continue                                                    # next file
            else:
                shutil.copy(oldname, v2name)                                # copy file
                clean_text(v2name)                                          # run clean_text function
                file_vocab = extract_terms(v2name)                          # run extract_terms function
                for key in file_vocab:                                      # merge vocab from file with overall vocab
                    if key in final_vocab:
                        final_vocab[key] += file_vocab[key]
                    else:
                        final_vocab[key] = file_vocab[key]
    count = 0
    print('Top 30 Terms:')
    for k in sorted(final_vocab, key=lambda k: final_vocab[k], reverse=True):   # print top 25 entries
        print(k)
        count += 1
        if count == 30:
            break


def clean_text(filename):
    with open(filename, 'r+', encoding='utf-8') as f:                       # open file
        text = f.read()                                                     # get text
        text = re.sub(r'[\n\t\s]+', ' ', text)                              # remove newline, tabs, and spaces
        sents = sent_tokenize(text)                                         # tokenize by sentences
        f.seek(0)                                                           # return to the top of the file
        f.truncate()                                                        # clear the file
        f.write('\n'.join(sents))                                           # write cleaned text back into file


def extract_terms(filename):
    with open(filename, 'r', encoding='utf-8') as f:                        # open file
        text = f.read()
        text = text.lower()                                                 # lower text
        text = re.sub(r'[^\d\w\s]', '', text)                               # keep only alphanumeric and whitespaces
        tokens = word_tokenize(text)                                        # tokenize
        unique_tokens = set(tokens)                                         # get unique tokens
        stop_words = set(stopwords.words('english')).union(social_networks) # remove stopwords
        important_tokens = [w for w in unique_tokens if w not in stop_words]
        wnl = nltk.WordNetLemmatizer()
        token_lemmas = [wnl.lemmatize(t) for t in tokens]
        important_lemmas = [wnl.lemmatize(t) for t in important_tokens]
        important_lemmas = set(important_lemmas)

        vocab = {}
        for lemma in important_lemmas:                                      # fill vocab with token and their count
            vocab[lemma] = token_lemmas.count(lemma)
        return vocab                                                        # return the vocab dict


if __name__ == "__main__":
    social_networks = {'pinterest', 'facebook', 'instagram', 'message',
                       'google', 'email', 'twitter', 'google+', 'bookmark',
                       'wishlist', 'text'}
    plantdir = 'in'                                                         # dir that holds the og files
    newdir = 'out'

    main()
