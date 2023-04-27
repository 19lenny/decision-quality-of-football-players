from statsbombpy import sb
import pandas as pd
from SetUp import CONSTANTS


# save all competition and their season in a dictionary
dfComp = sb.competitions()
competitionIDs = dfComp.competition_id.values.tolist()
seasonIDs = dfComp.season_id.values.tolist()
print(competitionIDs)
print(seasonIDs)

# all data frames that are used in the for loop must be initialized
dfAllEvents = pd.DataFrame()
dfAllMatches = pd.DataFrame()
counter = 0

# go through every season in every competitition, except the one that are getting evaluated
for index in range(len(competitionIDs)):
    # lets get all the matches of all seasons
    currentCompetition = competitionIDs[index]
    currentSeason = seasonIDs[index]
    print("progress bar: ", index, "/", len(competitionIDs))
    try:
        print("comp: ", currentCompetition, " season: ", currentSeason)
        # get all matches of the current competition / season
        dfMatches = pd.DataFrame(sb.matches(currentCompetition, currentSeason))
        # all MatchIDs of the current season
        matchIDs = dfMatches.match_id.values.tolist()

        # add this matches to a data frame, this is needed to make a backup of all matches
        dfAllMatches = pd.concat([dfMatches, dfAllMatches])
        # set the key index
        dfMatches.set_index("match_id")

        # add all events, of every game, of every season in every competition
        # here go through every event in every match
        for event in matchIDs:
            getEventsInMatch = sb.events(event)
            print("i am still working, nothing to worry")
            # add them to the current dataframe
            dfAllEvents = pd.concat([dfAllEvents, getEventsInMatch])

    except AttributeError:
        counter += 1
        print("fail counter: ", counter)
        print("fail happened in comp: ", currentCompetition, " in season: ", currentSeason)


# reset the index, so a new index is created
dfAllEvents.reset_index(drop=True, inplace=True)

# convert the dfModelData to a JSON.
# this is done for two reasons:
# 1) security: the provider can change the data all the time, in  downloading to JSON, we work on a hard copy
# 2) speed: it is way faster to work with data from a JSON file instead of always calling the API
# Therefore this code only has to be running once, the output is saved in a JSON file
filename = "ScoreCalculationShots.json"
dfAllEvents.to_json("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/JSON/BackUp/ScoreCalculationShots.json")
filename = "ScoreCalculationMatches.json"
dfAllMatches.to_json("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/JSON/BackUp/ScoreCalculationMatches.json")

print("i am finished")