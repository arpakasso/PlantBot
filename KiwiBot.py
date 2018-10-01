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
    print('\nHi! I\'m Kiwi!\nLet me tell you about plants and gardening!')
    print('TOPICS:\n1. garden/gardening\t\t\t2. vegetables\n3. flowers\t\t\t\t\t4. trees')
    print('5. shrubs\t\t\t\t\t6. soil\n7. fertilizer\t\t\t\t8. composting\n9. water\t\t\t\t\t10. pests')
    print('Input "stop" whenever you\'re done!')
    topic = input('What would you like to learn about today? ')
    print('\nI hope you learned a lot today!\nSee you next time!')


if __name__ == "__main__":
    main()