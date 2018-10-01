# CS 4301.001 PlantBot Project Part 1
# Reena Suh & Elizabeth Trinh
# September 24, 2018

from nltk.tokenize import sent_tokenize
import os


def main():
    raw_text = input("Do you want to launch Kiwi? ")
    raw_text = raw_text.lower()                                             # get user input
    if 'no' not in raw_text:                                                # check for negative reply
        launch_kiwi()


def launch_kiwi():
    print('\nHi! I\'m Kiwi!\nLet me tell you more about plants and gardening!')
    print('Input "stop" whenever you\'re done!\n')
    with open(knowledgeFile, 'r', encoding="utf8") as f:                    # open knowledge base file
        text = f.read()
        sents = sent_tokenize(text)                                         # sent tokenize text
        for sent in sents:                                                  # loop through sents and print
            if 'stop' in input(sent + ' ').lower():                         # if user jnputs 'STOP' then break
                break
    print('\nI hope you learned a lot today!\nSee you next time!')


def build_kb(dir_name: str, kb: dict):
    path = os.path.join(os.getcwd(), dir_name)
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:
            for line in f.readlines():
                for key in kb:
                    if key in line:
                        kb[key].append(line)


if __name__ == "__main__":
    knowledgeFile = 'kiwiknowledge'
    filedir = 'clean'
    topics = {'vegetable': list(),
              'flower': list(),
              'tree': list(),
              'shrub': list(),
              'lawn': list(),
              'soil': list(),
              'fertilizer': list(),
              'compost': list(),
              'pest': list(),
              'garden': list(),
              'water': list()
              }
    build_kb(filedir, topics)
    print(topics)
    main()