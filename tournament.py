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

def main():
    '''
    main method

    '''
    # creat log file for this program
    logging.basicConfig(filename="tournament.log", level=logging.DEBUG, format='%(asctime)s :: %(message)s')
    
    # Welcome message
    print("*** Welcome to the Tournament Bracket Creator! ***")
    teams = []
    
    # put code inside a while loop to allow user to try again if they make input errors
    while True:
        # prompt user to select a mode
        print("\nWhat would you like to do today?")
        print("\t1) Create a new tournament list")
        print("\t2) Edit an existing tournament list")
        print("\t3) Display a bracket from an existing tournament list")
        print("\t4) Quit")
        user_choice = int(input("\n>>> "))
        if user_choice == 4:
            # breaks out of while loop, ends program
            break
        elif user_choice == 3:
            # creates a bracket from an existing file
            print("\nPlease enter a filename or filepath:")
            file = input("\n>>> ")
            b = bracketMaker(file)
            print(b)
        else:
            # load from existing file
            if user_choice == 2:
                print("\nPlease enter a filename or filepath:")
                file = input("\n>>> ")
                teams_load = loadTeams(file)
                while True:
                    print("\n*** YOUR TOURNAMENT ***")
                    printTeams(teams_load)
                    print("\nWhat would you like to do with this tournament list?")
                    print("\t1) Add a new competitor")
                    print("\t2) Remove a competitor")
                    print("\t3) Reseed the competitors")
                    print("\t4) Quit")
                    e_choice = input("\n>>> ")
                    if e_choice == "1":
                        # add competitor to list
                        teams = teams_load
                        addTeam(teams)
                    elif e_choice == "2":
                        # remove competitor
                        teams = removeTeam(teams_load)
                        removeFile(file)
                    elif e_choice == "3":
                        teams = seedTeams(teams_load, 1)
                        removeFile(file)
                    elif e_choice == "4":
                        break
                    else:
                        print("Please enter 1, 2, 3, or 4.")
                        continue
                    saveTeams(file,teams)
                    break

            elif user_choice == 1:
            # create new file (don't overwrite existing files)
                while True:
                    print("\nInput a filename or press return if you want a default name.\n")
                    cust = input("\n>>> ")
                    if exists(fileAdjust(cust)):
                        print("\nThat file already exists. Please choose a different name.\n")
                        continue
                    break
                if cust == "":
                    # provide default name
                    i = 0
                    if exists("data.csv"):
                        while exists("data" + str(i) + ".csv"):
                            i += 1
                        file = "data" + str(i) + ".csv"
                    else:
                        file = "data.csv"
                else:
                    file = fileAdjust(cust)
                addTeam(teams)
                print("Filename:",file)
                saveTeams(file, teams)
            # return to beginning if erroneous input
            else:
                print("Please enter an integer")
                continue
            
        print("\nWould you like to return to the main menu?")
        print("\tY - Yes (Return to main menu)")
        print("\tN - No (Quit program)")
        c = input("\n>>> ").lower()
        if c == 'yes' or c == 'y':
            continue
        else:
            break
    
    # nice closing message for the program
    print("\n*** Goodbye! Have a great day! ***\n")

def bracketMaker(fname) -> Bracket:
    '''
    bracketMaker

    This function will produce a tournament bracket with matchups from a list of Competitors.

    Returns a bracket.

    '''
    # correct for user not entering file extension
    file = fileAdjust(fname)

    teams = loadTeams(file)
    
    if len(teams) == 0:
        print("File is empty. Try again...")
        return None

    if teams[0].getSeed() == 0:
        seedTeams(teams)

    print("\nWhat is the name of this Tournament?")
    tname = str(input("\n>>> "))
    print()
    brack = Bracket(teams, tname)
    brack.sortMatchups()
    return brack          

def seedTeams(lst_teams, mode=0):
    '''
    seedTeams

    This function will assign each team or competitor in a list a seed based on how they are sorted.

    Returns None.

    '''
    if mode == 0:
        for i in range(len(lst_teams)):
            lst_teams[i]._seed = i + 1
    else:
        while True:
            in_use = set()
            print("What seed should be assigned to", lst_teams[0].getName(), "?")
            print("\nEnter an integer:\n")
            inp = input(">>> ")

            intlist = set()
            for i in range(len(lst_teams)):
                intlist.add(str(i+1))

            # check that user inputs an integer
            try:
                if inp not in intlist:
                    raise ValueError
            except ValueError as e:
                print("Please enter a valid integer.")
                continue

            sd = int(inp)

            if sd > len(lst_teams):
                print("Please choose an appropriate seed for the tournament size.")
                continue

            lst_teams[0].setSeed(sd)
            in_use.add(sd)
            break

        for i in range(1, len(lst_teams)):
            while True:
                print("What seed should be assigned to", lst_teams[i].getName(), "?")
                print("\nEnter an integer:\n")
                inp = input(">>> ")

                # check that user inputs an integer
                try:
                    if inp not in intlist:
                        raise ValueError
                except ValueError as e:
                    print("Please enter a valid integer.")
                    continue

                sd = int(inp)

                if sd > len(lst_teams):
                    print("Please choose an appropriate seed for the tournament size.")
                    continue
                if sd in in_use:
                    print("That seed is already in use, please choose another seed.")
                    continue
                else:
                    lst_teams[i].setSeed(sd)
                    in_use.add(sd)
                    break
    return lst_teams

def loadTeams(fname) -> list:
    '''
    loadTeams

    This function will load from a file into a Competitor list.

    Returns list of Competitors.

    '''
    file = fileAdjust(fname)
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

def fileAdjust(fname) -> str:
    '''
    fileAdjust
    
    This function adjusts the filename if no file extension is given

    Returns a string
    
    '''
    if fname[-4:] != ".csv":
        return fname + ".csv"
    else:
        return fname

def saveTeams(fname, lst_teams):
    '''
    saveTeams

    This function will save Competitor data to data.csv

    Returns None.

    '''
    file = fileAdjust(fname)
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

def removeFile(fname):
    '''
    removeFile
    
    This function removes a designated file
    
    Returns None
    
    '''
    file = fileAdjust(fname)
    os.remove(file)

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
    print("\n***NOTE: Teams are seeded by order of entry into list.***\n")
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

        # user input determines which type of object it will be
        if comp_type == 2:
            while True:
                print("\nPlease select the option that best applies to this tournament:")
                print("\t2) Casual")
                print("\t3) Professional")
                c_type = input(">>> ")

            # check that user inputs an integer
                try:
                    if c_type not in {"2", "3"}:
                        raise ValueError
                except ValueError as e:
                    print("Please enter 2 or 3.")
                    continue
                
                comp_type = int(c_type)

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
            print("\nPlease selected one of the presented options (type '1', '2', or '0').")
            continue
        break

    while True:
        while True:
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
                if comp_type == 2:
                    city = ""
                    break
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
                if comp_type == 2:
                    state = ""
                    break
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

            if comp_type == 1:
                # Team
                comp = Team(name, city, state, age, sd)
            elif comp_type == 2:
                # Casual Individual
                comp = IndividualCasual(name, city, state, age, sd)
            elif comp_type == 3:
                # Professional Individual
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
        c = input("\n>>> ").lower()
        if c == 'yes' or c == 'y':
            continue
        else:
            return None

def sortTeams(lst_teams) -> list:
    '''
    sortTeams

    This function sorts a team list.

    Returns list.

    '''
    new_lst = []
    for i in range(len(lst_teams)):
        for t in lst_teams:
            if t.getSeed() == i + 1:
                tm = t
                break
        new_lst.append(tm)
    return new_lst

def removeTeam(lst_teams) -> list:
    '''
    removeTeams

    This function will remove a specified team (prompted by user input) from the tournament list.

    Returns list.

    '''
    lst_tms = sortTeams(lst_teams)
    printTeams(lst_tms)
    print("\nPlease enter the Name of the competitor you would like to remove.")
    d_tm = input("\n>>> ").lower()
    new_list = []
    for tm in lst_tms:
        if tm.getName().lower() == d_tm:
            pass
        else:
            new_list.append(tm)
    seedTeams(new_list)
    return new_list

if __name__ == "__main__":
    main()