from ctypes import sizeof
from multiprocessing.sharedctypes import Value
from unicodedata import name
from competitor import Team, IndividualPro, IndividualCasual
from bracket import Bracket
from os.path import exists
import os
import re
import logging


# Project Goals:
# - Implement a method to assign seeds to all teams***/DONE/***
# - Implement a method to sort teams by seed***/DONE/***
# - Find a way to organize the teams so that all matchups and potential matchups can be shown***/DONE/***

'''
main method

'''
def main():
    # creat log file for this program
    logging.basicConfig(filename="tournament.log", level=logging.DEBUG, format='%(asctime)s :: %(message)s')
    
    print("*** Welcome to the Tournament Bracket Creator! ***")
    teams = []
    
    # put code inside a while loop to allow user to correct inputs
    while True:
        print("\nWhat would you like to do today?")
        print("\t1) Create a new tournament list")
        print("\t2) Edit an existing tournament list")
        print("\t3) Display a bracket from an existing tournament list")
        print("\t4) Quit")
        user_choice = int(input("\n>>> "))
        if user_choice == 4:
            break
        elif user_choice == 3:
            print("\nPlease enter a filename or filepath:")
            file = input("\n>>> ")
            b = bracketMaker(file)
            print(b)
        else:
            # load from existing file
            if user_choice == 2:
                print("\nPlease enter a filename or filepath:")
                file = input("\n>>> ")
                teams = loadTeams(file)
                while True:
                    print("\n*** YOUR TOURNAMENT ***")
                    printTeams(teams)
                    print("\nWhat would you like to do with this tournament list?")
                    print("\t1) Add a new competitor")
                    print("\t2) Remove a competitor")
                    print("\t3) Quit")
                    e_choice = input("\n>>> ")
                    if e_choice == "1":
                        # add competitor to list
                        addTeam(teams)
                    elif e_choice == "2":
                        # remove competitor
                        removeTeam(teams)
                        os.remove(file)
                    elif e_choice == "3":
                        break
                    else:
                        print("Please enter 1, 2, or 3.")
                        continue
                    saveTeams(file,teams)
                    break

            # create new file (don't overwrite existing files)
            elif user_choice == 1:
                i = 0
                if exists("data.csv"):
                    while exists("data" + str(i) + ".csv"):
                        i += 1
                    file = "data" + str(i) + ".csv"
                else:
                    file = "data.csv"
                addTeam(teams)
                saveTeams(file, teams)
            # return to beginning if erroneous input
            else:
                print("Please enter an integer")
                continue
            
        print("\nWould you like to return to the main menu?")
        print("\tY - Yes (Return to main menu)")
        print("\tN - No (Quit program)")
        c = input("\n>>> ")
        if c == 'Y' or c == 'y':
            continue
        else:
            break
    
    # nice closing message for the program
    print("*** Goodbye! Have a great day! ***")

def bracketMaker(file) -> Bracket:
    '''
    bracketMaker

    This function will produce a tournament bracket with matchups from a list of Competitors.

    Returns a bracket.

    '''

    teams = loadTeams(file)
    
    if teams[0].getSeed() == 0:
        seedTeams(teams)

    print("\nWhat is the name of this Tournament?")
    tname = str(input(">>> "))
    brack = Bracket(teams, tname)
    brack.sortTeams()
    return brack          

def seedTeams(lst_teams):
    '''
    seedTeams

    This function will assign each team or competitor in a list a seed based on how they are sorted.

    Returns None.

    '''
    print("Do you want the seeding done automatically (seeds assigned in order of entry), or would you like to set the seeds manually?\n")
    print("\t1) Auto (order of entry)")
    print("\t2) Manual")
    choice = int(input("\n>>> "))
    if choice == 1:
        for i in range(len(lst_teams)):
            lst_teams[i]._seed = i + 1
    elif choice == 2:
        for i in range(len(lst_teams)):
            while True:
                print("What seed should be assigned to", lst_teams[i].getName(), "?")
                print("\nEnter an integer:\n")
                sd = int(input(">>> "))
                if sd > len(lst_teams):
                    print("Please choose an appropriate seed for the tournament size.")
                    continue
                dup = False
                for j in range(len(lst_teams)):
                    if sd == lst_teams[j].getSeed():
                        dup = True
                        break
                if dup == True:
                    print("That seed is already in use, please choose another seed.")
                    continue
                else:
                    lst_teams[i].setSeed(sd)

def loadTeams(file) -> list:
    '''
    loadTeams

    This function will load from a file into a Competitor list.

    Returns list of Competitors.

    '''
    if file[-4:] != ".csv":
        file += ".csv"
    lst_teams = []
    if not exists(file):
        return lst_teams
    else:
        with open(file,"r") as f:
            for line in f:
                txt = line.split(',')
                if txt[0] == "Team":
                    team = Team(txt[1], txt[4], txt[5], txt[3], txt[2])
                elif txt[0] == "Professional":
                    team = IndividualPro(txt[1], txt[4], txt[5], txt[3], txt[2])
                elif txt[0] == "Casual":
                    team = IndividualCasual(txt[1], txt[4], txt[5], txt[3], txt[2])
                else:
                    return lst_teams
                lst_teams.append(team)
        return lst_teams

def saveTeams(file, lst_teams):
    '''
    saveTeams

    This function will save Competitor data to data.csv

    Returns None.

    '''
    with open(file, "w") as f:
        for team in lst_teams:
            if type(team) == Team:
                f.write("Team," + team._name + "," + str(team._seed) + "," + str(team._age) + "," + team._city + "," + team._state + ",\n")
            elif type(team) == IndividualPro:
                f.write("Professional," + team._name + "," + str(team._seed) + "," + str(team._age) + "," + team._city + "," + team._state + ",\n")
            elif type(team) == IndividualCasual:
                f.write("Casual," + team._name + "," + str(team._seed) + "," + str(team._age) + "," + team._city + "," + team._state + ",\n")
            else:
                pass

def printTeams(lst_teams):
    '''
    printTeams

    This function will print all competitors in a list with their attributes

    Returns None.

    '''
    for tm in lst_teams:
        print(tm)

def addTeam(lst_teams):
    '''
    addTeam

    This function will prompt the user for input about a team/competitor to add to the team list.

    Returns None.
    
    '''
    while True:
        print("\nWill this tournament involve teams or individual competitors?")
        print("\t1) Team")
        print("\t2) Individual")
        print("\t0) Quit")
        c_type = input(">>> ")

        # check that user inputs an integer
        try:
            if c_type not in {"0", "1", "2"}:
                raise ValueError
        except ValueError as e:
            print("Please enter 1, 2, or 0.")
            continue
        
        comp_type = int(c_type)
    
        term = ""
        if comp_type == 1:
            term = "team"
        else:
            term = "person"

        break

    while True:
        while True:
            # user input determines which type of object it will be
            if comp_type == 2:
                while True:
                    print("\nPlease select the option that best applies to this tournament:")
                    print("\t2) Casual")
                    print("\t3) Professional")
                    comp_type = int(input(">>> "))
                    if comp_type == 2 or comp_type == 3:
                        break
                    else:
                        print("\nPlease selected one of the presented options (type '2', or '3').")
        
            # query is unnecessary for teams
            elif comp_type == 1:
                pass

            # break out of function if user wants to quit
            elif comp_type == 0:
                return None
            else:
                print("\nPlease selected one of the presented options (type '1', '2', or '3').")
                continue
            
        
            # Ask for name, check for commas
            while True:
                try:
                    name = input("\nEnter this " + term + "'s name:\n>>> ")
                    check = re.search(",", name)
                    if check != None:
                        raise ValueError
                except ValueError as ve:
                    print("*** ERROR: CANNOT USE COMMAS IN NAME ***")
                    logging.error("Tried to enter a comma in name, trying again...")
                else:
                    break
        
            # ask for age, check that an integer is input
            if comp_type == 1:
                age = 0
            else:
                while True:
                    print("\nHow old is this person?\nType an integer value.")
                    try:
                        age = int(input(">>> "))
                        if type(age) != int:
                            raise ValueError
                    except ValueError as ve:
                        print("**ERROR: MUST ENTER AN INTEGER VALUE!**")
                        logging.error("Tried to enter a non-integer as an age... Trying again...")
                    except Exception as e:
                        print("System ran into error.")
                    else:
                        break

            # ask for city/region, then state/country, check for commas in each
            while True:
                try:
                    city = input("\nEnter this " + term + "'s city or region:\n>>> ")
                    check = re.search(",", city)
                    if check != None:
                        raise ValueError
                except ValueError as ve:
                    print("*** ERROR: CANNOT USE COMMAS IN CITY/REGION NAME ***")
                    logging.error("Trying to enter a comma in city/region name, trying again...")
                except Exception as e:
                    print("System ran into error.")
                else:
                    break
        
            # state/region
            while True:
                try:
                    state = input("\nEnter this " + term + "'s state (U.S.A.) or country:\n>>> ")
                    check = re.search(",", state)
                    if check != None:
                        raise ValueError
                except ValueError as ve:
                    print("*** ERROR: CANNOT USE COMMAS IN STATE/COUNTRY NAME ***")
                    logging.error("Trying to enter a comma in STATE/COUNTRY NAME, trying again...")
                except Exception as e:
                    print("System ran into error.")
                else:
                    break

            # seed (if applicable)
            while True:
                print("\nHas this " + term + " been assigned a seed in the tournament?")
                print("\tYes (Y)")
                print("\tNo (N)")
                y_n = str(input(">>> "))
                if y_n == "N" or y_n == "n":
                    sd = 1
                    if len(lst_teams) == 0:
                        pass
                    else:
                        sd_set = set()
                        for tm in lst_teams:
                            sd_set.add(tm.getSeed())
                        sd_list = sorted(sd_set)
                        for elem in sd_list:
                            if elem == sd:
                                sd += 1
                            else:
                                break
                    break
                else:
                    print("\nPlease enter the seed.\nType an integer value.")
                    try:
                        sd = int(input(">>> "))
                        if type(sd) != int:
                            raise ValueError
                    except ValueError as ve:
                        print("**ERROR: MUST ENTER AN INTEGER VALUE!**")
                        logging.error("Tried to enter a non-integer as a seed... Trying again...")
                    except Exception as e:
                        print("System ran into error.")
                    else:
                        break

            if comp_type == 1:
                # Team
                comp = Team(name, city, state, age, sd)
            elif comp_type == 2:
                # Professional Individual
                comp = IndividualCasual(name, city, state, age, sd)
            else:
                # Casual Individual
                comp = IndividualPro(name, city, state, age, sd)
            break
    
        # save teams and prompt to start over
        while True:
            lst_teams.append(comp)

            for i in range(len(lst_teams)):
                print(lst_teams[i])

            # don't allow user to add more than 16 competitors
            if len(lst_teams) >= 16:
                print("Tournament is full, only up to 16 may enter.")
                return None
            else:
                break

        print("\nWould you like to add another participant?")
        print("\tYes (Y)")
        print("\tNo (N)")                
        c = input("\n>>> ")
        if c == 'Y' or c == 'y':
            continue
        else:
            return None

def removeTeam(lst_teams):
    '''
    removeTeams

    This function will remove a specified team (prompted by user input) from the tournament list.

    Returns None.

    '''
    printTeams(lst_teams)
    print("\nPlease enter the Name of the competitor you would like to remove.")
    d_tm = input("\n>>> ").lower()
    new_list = []
    for tm in lst_teams:
        if tm.getName() == d_tm:
            pass
        else:
            new_list.append(tm)
    lst_teams = new_list



if __name__ == "__main__":
    main()