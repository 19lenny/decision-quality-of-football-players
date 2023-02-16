from statsbombpy import sb
import pandas as pd
import DataManipulationAngleDistance

# save all competition and their season in a dictionary
dfComp = sb.competitions()
competitionIDs = dfComp.competition_id.values.tolist()
seasonIDs = dfComp.season_id.values.tolist()
print(competitionIDs)
print(seasonIDs)

# all data frames that are used in the for loop must be initialized
dfShotModelData = pd.DataFrame()
dfAllMatches = pd.DataFrame()
counter = 0

# go through every season in every competitition, except the one that are getting evaluated
for index in range(len(competitionIDs)):
    # lets get all the matches of all seasons, except the ones we defined for our evaluation
    # EM2020: compID: 55, seasonID: 43
    # WM2022: compID: 43, seasonID: 106

    currentCompetition = competitionIDs[index]
    currentSeason = seasonIDs[index]
    print("progress bar: ", index, "/", len(competitionIDs))
    #try:
    # too old ones dont work as well
    if (currentCompetition == 16 and currentSeason == 76):
        print("fail happened in comp: ", currentCompetition, " in season: ", currentSeason)
        continue
    elif (currentCompetition != 55 or currentSeason != 43) and (currentCompetition != 43 or currentSeason != 106):
        print("comp: ", currentCompetition, " season: ", currentSeason)
        # get all matches of the current competition / season
        dfMatches = pd.DataFrame(sb.matches(currentCompetition, currentSeason))
        # all MatchIDs of the current season
        matchIDs = dfMatches.match_id.values.tolist()

        # add this matches to a data frame, this is needed for additional information later during the join
        dfAllMatches = pd.concat([dfMatches, dfAllMatches])
        # set the key index for the join later
        dfMatches.set_index("match_id")

        # add all shot events, of every game, of every season in every competition, except the ones that are evaluated
        # here go through every event in every match
        for event in matchIDs:
            getEventsInMatch = sb.events(event)
            print("i am still working, nothing to worry")
            # only keep the necessery rows, which have something to do with shots and are not from penalties or freekicks
            getEventsInMatch = getEventsInMatch.query(
                "type == 'Shot' & shot_body_part != 'Head' & play_pattern != 'From Free Kick' & shot_type != 'Penalty'")
            # add them to the current model
            dfShotModelData = pd.concat([dfShotModelData, getEventsInMatch])

    """except AttributeError:
        counter += 1
        print("fail counter: ", counter)
        print("fail happened in comp: ", currentCompetition, " in season: ", currentSeason)"""

# join Shots and Matches
# therefore we know from every score the competition stage, the competition and additional information
dfModelData = dfShotModelData.join(dfMatches.set_index('match_id'), on='match_id')

# before we save the df, we want to add crucial information to the shot,
# with this information we can later create a better model
# therefore we calculate for every shot, the angle and the distance

# convert coordinates from list, to x and y entries
dfModelData = DataManipulationAngleDistance.coordinates(dfModelData)
# add angle
dfModelData = DataManipulationAngleDistance.angle(dfModelData)
# add distance
dfModelData = DataManipulationAngleDistance.distance(dfModelData)

# only keep the interesting columns
dfModelData = dfModelData[
    ["x_coordinate", "y_coordinate", "shot_end_location", "shot_outcome", "angle", "distance_to_goal_centre",
     "shot_statsbomb_xg", "match_id", "shot_body_part", "period",
     "minute", "shot_type", "match_date", "competition",
     "season", "home_team", "away_team", "home_score", "away_score", "competition_stage"]]

# reset the index, so a new index is created
dfModelData.reset_index(inplace=True)

# convert the dfModelData to a JSON.
# this is done for two reasons:
# 1) security: the provider can change the data all the time, in  downloading to JSON, we work on a hard copy
# 2) speed: it is way faster to work with data from a JSON file instead of always calling the API
# Therefore this code only has to be running once, the output is saved in a JSON file
dfModelData.to_json(
    'G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/JSON/allModelData.json')

print("i am finished")
