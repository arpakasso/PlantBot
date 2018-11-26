import _pickle as pickle


def main():
    plantpages = open('plantpages.pkl', 'rb')
    plant_list = pickle.load(plantpages)
    plantpages.close()

    plantdb = open('plantdb.pkl', 'rb')
    plant_db = pickle.load(plantdb)
    plantdb.close()

    print(plant_list)
    print(plant_db)


if __name__ == '__main__':
    main()