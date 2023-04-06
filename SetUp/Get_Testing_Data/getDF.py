from statsbombpy import sb
import pandas as pd
from SetUp import DataManipulation, CONSTANTS
from Model import model_info
from SetUp.DecisionEvaluation import evaluate_decision
from SetUp import TM_values

def getDF(competition_id, season_id, competition, save_path):
    df_matches = pd.DataFrame(sb.matches(competition_id, season_id))

    # all matchID's of the current competition
    match_ids = df_matches.match_id.values.tolist()

    # initialize df
    df_shots = pd.DataFrame()
    # this must be done for every event in every game,
    # then we have a dataframe with all shots from every game from the current competition
    counter = 0
    for event in match_ids:
        get_all_events_of_this_match = sb.events(event)
        # only keep the shots, in the rest we are not interested
        get_all_events_of_this_match = get_all_events_of_this_match.query("type == 'Shot'")
        df_shots = pd.concat([df_shots, get_all_events_of_this_match])
        counter += 1
        print("nothing to worry - still working")
        print("progress bar to get all events at ", competition,": ", counter, " / ", len(match_ids))

    # set the key index for the join later
    df_matches.set_index("match_id")

    # join Shots and Matches, therefore we know from every score the competition stage,
    # the competition and additional information
    df_return = df_shots.join(df_matches.set_index('match_id'), on='match_id')
    df_return.reset_index(drop=True, inplace=True)

    # before we save the df, we want to add crucial information to the shot,
    # with this information we can later calculate the xG
    # therefore we calculate for every shot, the angle and the distance

    # convert coordinates from list, to x and y entries
    df_return = DataManipulation.coordinates(df_return)
    # add angle
    df_return = DataManipulation.angle(df_return)
    # add angle in rad
    df_return = DataManipulation.angleInRadian(df_return)
    # add distance
    df_return = DataManipulation.distancePlayerToGoal(df_return)
    # add goal
    df_return = DataManipulation.addGoalBinary(df_return)
    # add xGoal, calculated by me
    df_return = model_info.prediction(df_return)

    # add the current score of this competition
    df_return = DataManipulation.score(df_return)
    print("score is done")

    # only keep the necessery rows, which have something to do with shots and are not from penalties or freekicks
    # this way some time is saved in the next call
    df_return = df_return.query(
        "type == 'Shot' & shot_body_part != 'Head' & play_pattern != 'From Free Kick' & shot_type != 'Penalty'")
    df_return.reset_index(drop=True, inplace=True)

    # add the transfer value of every shooting player
    df_return = TM_values.transfermarketValue(dfCompetition=df_return, competition=competition)
    print("TM Value is added")

    # calculates
    # - the xG of the best alternative
    # - the x and y coordinate of the best alternative
    # - the difference of the shooting players decision and the decision of the best alternative
    # - if the shooting player made the best decision
    # - the xP of the pass that would be needed to go to the best alternative
    df_return = evaluate_decision.decisionEvaluation(df_return, competition)

    # save only the needed columns
    attributes_to_drop = ["50_50", "ball_receipt_outcome", "ball_recovery_recovery_failure", "block_deflection",
                          "block_offensive", "block_save_block", "carry_end_location", "clearance_aerial_won",
                          "clearance_body_part", "clearance_head", "clearance_left_foot", "clearance_right_foot",
                          "counterpress", "dribble_outcome", "duel_outcome", "duel_type", "duration",
                          "foul_committed_card", "foul_committed_advantage",
                          "foul_committed_offensive", "foul_committed_penalty", "foul_committed_type",
                          "foul_won_advantage", "foul_won_defensive", "foul_won_penalty", "goalkeeper_body_part",
                          "goalkeeper_end_location", "goalkeeper_outcome", "goalkeeper_position",
                          "goalkeeper_punched_out", "goalkeeper_technique", "goalkeeper_type",
                          "injury_stoppage_in_chain",
                          "interception_outcome", "miscontrol_aerial_won", "off_camera", "out", "pass_aerial_won",
                          "pass_angle", "pass_assisted_shot_id", "pass_body_part", "pass_cross",
                          "pass_cut_back", "pass_deflected", "pass_end_location", "pass_goal_assist", "pass_height",
                          "pass_inswinging", "pass_length", "pass_miscommunication", "pass_no_touch",
                          "pass_outcome", "pass_outswinging", "pass_recipient", "pass_shot_assist", "pass_straight",
                          "pass_switch", "pass_technique", "pass_type", "player_id", "position", "possession",
                          "possession_team", "possession_team_id", "related_events", "second", "shot_aerial_won",
                          "shot_body_part",
                          "shot_end_location", "shot_first_time", "shot_key_pass_id",
                          "shot_technique", "shot_type", "substitution_outcome", "substitution_replacement", "tactics",
                          "timestamp", "type", "under_pressure", "dribble_nutmeg", "pass_through_ball",
                          "shot_deflected", "shot_redirect", "kick_off", "match_status", "match_status_360",
                          "last_updated", "last_updated_360", "match_week", "stadium", "referee",
                          "home_managers", "away_managers", "data_version", "shot_fidelity_version",
                          "xy_fidelity_version"]
    df_return = df_return.drop(columns=attributes_to_drop)

    # todo: these tasks
    # other file, add all analyzing files to one file
    # on the hypothesis folder only the hypothesis should happen and bedingungen für hypothesis
    # DEBUG SCORE, CHECK IF THE SCORES ARE TRUE
    # EXCEPTIONS MV 16, 18
    # UPDATE ALLMODELDATA.JSON

    # reset the index, so a new index is created
    df_return.reset_index(drop=True, inplace=True)

    # convert the df_return to a JSON.
    # this is done for two reasons:
    # 1) security: the provider can change the data all the time, in  downloading to JSON, we work on a hard copy
    # 2) speed: it is way faster to work with data from a JSON file instead of always calling the API
    # Therefore this code only has to be running once, the output is saved in a JSON file
    #TODO: UNCOMMENT HERE
    df_return.to_json(save_path)

    print("i am finished with competition: ", competition)

#get EM20
getDF(competition_id=55, season_id=43, competition="EM20", save_path=CONSTANTS.JSONEM2020)

#get WM18
getDF(competition_id=43, season_id=3, competition="WM18", save_path=CONSTANTS.JSONWM2018)

#getWM22
getDF(competition_id=43, season_id=106, competition="WM22", save_path=CONSTANTS.JSONWM2022)
