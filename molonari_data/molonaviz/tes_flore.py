path_data = 'C:/Users/flore/OneDrive/Documents/mines ONE DRIVE/2A/T3/molonari/Projet Interface/git/MOLO-projet-interface/molonari_data/study_ordiFlore/Point001'
import os

class test_truc():

    def __init__(self):
        path_file = path_data + '/' + 'res_temps.csv'
        print(path_file)
        if os.path.isfile(path_file) : 
            print('coucou')
        else : 
            print("il faut compute d'abord")

test = test_truc()