# CS 4301.001 PlantBot Project Part 1
# Reena Suh & Elizabeth Trinh
# September 24, 2018

import os


def main():
    raw_text = input("Do you want to launch Kiwi? ")
    raw_text = raw_text.lower()                                             # get user input
    if 'no' not in raw_text:                                                # check for negative reply
        launch_kiwi()


def launch_kiwi():
    print('\nHi! I\'m Kiwi!\nLet me tell you about plants and gardening!')
    print('TOPICS:\n1. garden\t\t\t\t\t2. vegetables\n3. flowers\t\t\t\t\t4. trees')
    print('5. shrubs\t\t\t\t\t6. soil\n7. fertilizer\t\t\t\t8. composting\n9. water\t\t\t\t\t10. pests')
    print('Input "stop" whenever you\'re done!')
    switch_dict = {1: 'garden', 2: 'vegetable', 3: 'flower', 4: 'tree', 5: 'shrub',
                   6: 'soil', 7: 'fertilizer', 8: 'compost', 9: 'water', 10: 'pest',}
    usertopic = input('What would you like to learn about today? ')
    facts = []
    try:
        topicnum = int(usertopic)
        if 1 <= topicnum <= 10:
            topic_key = switch_dict[topicnum]
            facts = topics[topic_key]
        else:
            print('Invalid topic number.')
            exit()
    except ValueError:
        if usertopic in topics:
            facts = topics[usertopic]
        else:
            print('Invalid topic.')
            exit()
    count = 0
    while count < len(facts):
        if 'stop' in input(facts[count]).lower():
            break
        count += 1
    print('\nI hope you learned a lot today!\nSee you next time!')


def build_kb(dir_name: str, kb: dict):
    # use sentences from manually cleaned files
    path = os.path.join(os.getcwd(), dir_name)
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:
            for line in f.readlines():
                # check for mentions of each key in each line
                for key in kb:
                    if key in line:
                        kb[key].append(line)


if __name__ == "__main__":
    knowledgeFile = 'kiwiknowledge'
    filedir = 'clean'
    # dictionary knowledge base
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
    main()