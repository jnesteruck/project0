from tokenize import Single
from competitor import Team
from bracket import Bracket, Matchup
import tournament as tn

teams_load = tn.loadTeams("data0.csv")
teams = []
half = int(len(teams_load) / 2)
for elem in teams_load:
    teams.append(elem)

# tourn = Bracket(teams_load, "Cool Tournament")
# tourn.sortTeams()
# # tourn.printTeams()

# print(tourn)

tn.removeTeam(teams_load)