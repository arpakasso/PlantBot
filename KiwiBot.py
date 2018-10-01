# CS 4301.001 PlantBot Project Part 1
# Reena Suh & Elizabeth Trinh
# September 24, 2018

from nltk.tokenize import sent_tokenize


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


if __name__ == "__main__":
    knowledgeFile = 'kiwiknowledge'
    main()