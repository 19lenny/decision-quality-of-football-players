from SetUp import JSONtoDF, CONSTANTS, joinDF

def drop_attributes(df,attributes):
    df = df.drop(columns=attributes)
    return df

# get all testing data and only keep the columns needed

#EM20
attributes_to_drop = ["dribble_overrun", "bad_behaviour_card", "clearance_other", "goalkeeper_shot_saved_off_target",
                      "goalkeeper_shot_saved_to_post", "shot_open_goal", "shot_saved_off_target", "shot_saved_to_post", "goalkeeper_lost_in_play",
                      "ball_recovery_offensive", "goalkeeper_success_in_play", "dribble_no_touch", "goalkeeper_penalty_saved_to_post",
                      "shot_follows_dribble", "player_off_permanent", "level_0", "shot_one_on_one",
                      "50_50", "ball_receipt_outcome", "ball_recovery_recovery_failure", "block_deflection",
                      "block_offensive", "block_save_block", "carry_end_location", "clearance_aerial_won",
                      "counterpress", "dribble_outcome", "duel_outcome", "duel_type", "duration",
                      "foul_committed_card", "foul_committed_advantage",
                      "foul_committed_offensive", "foul_committed_penalty", "foul_committed_type",
                      "foul_won_advantage", "foul_won_defensive", "foul_won_penalty", "goalkeeper_body_part",
                      "goalkeeper_end_location", "goalkeeper_outcome", "goalkeeper_position",
                      "goalkeeper_technique", "goalkeeper_type",
                      "injury_stoppage_in_chain",
                      "interception_outcome", "miscontrol_aerial_won", "pass_aerial_won",
                      "pass_angle", "pass_assisted_shot_id", "pass_body_part", "pass_cross",
                      "pass_cut_back", "pass_deflected", "pass_end_location", "pass_goal_assist", "pass_height",
                      "pass_length", "pass_miscommunication",
                      "pass_outcome", "pass_recipient", "pass_shot_assist",
                      "pass_switch", "pass_technique", "pass_type", "player_id", "position", "possession",
                      "possession_team", "possession_team_id", "related_events", "second", "shot_aerial_won",
                      "shot_body_part",
                      "shot_end_location", "shot_first_time", "shot_key_pass_id",
                      "shot_technique", "shot_type", "substitution_outcome", "substitution_replacement", "tactics",
                      "timestamp", "type", "under_pressure", "dribble_nutmeg", "pass_through_ball",
                      "shot_deflected", "shot_redirect", "kick_off", "match_status", "match_status_360",
                      "last_updated", "last_updated_360", "match_week", "stadium", "referee",
                      "home_managers", "away_managers", "data_version", "shot_fidelity_version",
                      "xy_fidelity_version", 'clearance_body_part', 'clearance_head', 'clearance_left_foot',
                      'clearance_right_foot', 'goalkeeper_punched_out', 'off_camera', 'out',
                      'pass_inswinging', 'pass_no_touch', 'pass_outswinging', 'pass_straight']
dfEM20 = drop_attributes(df=JSONtoDF.createDF(CONSTANTS.JSONEM2020), attributes=attributes_to_drop)

#WM18

attributes_to_drop = [ "level_0", "bad_behaviour_card", "ball_recovery_offensive", "dribble_overrun", "index", "pass_backheel", "shot_open_goal",
                       "shot_one_on_one", "shot_follows_dribble",
                       "50_50", "ball_receipt_outcome", "ball_recovery_recovery_failure", "block_deflection",
                      "block_offensive", "block_save_block", "carry_end_location", "clearance_aerial_won",
                      "counterpress", "dribble_outcome", "duel_outcome", "duel_type", "duration",
                      "foul_committed_card", "foul_committed_advantage",
                      "foul_committed_offensive", "foul_committed_penalty", "foul_committed_type",
                      "foul_won_advantage", "foul_won_defensive", "foul_won_penalty", "goalkeeper_body_part",
                      "goalkeeper_end_location", "goalkeeper_outcome", "goalkeeper_position",
                      "goalkeeper_technique", "goalkeeper_type",
                      "injury_stoppage_in_chain",
                      "interception_outcome", "miscontrol_aerial_won", "pass_aerial_won",
                      "pass_angle", "pass_assisted_shot_id", "pass_body_part", "pass_cross",
                      "pass_cut_back", "pass_deflected", "pass_end_location", "pass_goal_assist", "pass_height",
                      "pass_length", "pass_miscommunication",
                      "pass_outcome", "pass_recipient", "pass_shot_assist",
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
dfWM18 = drop_attributes(df=JSONtoDF.createDF(CONSTANTS.JSONWM2018),attributes=attributes_to_drop)

#WM22
attributes_to_drop = ["half_start_late_video_start", "index", "dribble_overrun", "bad_behaviour_card", "clearance_other", "goalkeeper_shot_saved_off_target",
                      "goalkeeper_shot_saved_to_post", "shot_open_goal", "shot_saved_off_target", "shot_saved_to_post", "goalkeeper_lost_in_play",
                      "ball_recovery_offensive", "goalkeeper_success_in_play", "dribble_no_touch",
                      "shot_follows_dribble", "level_0", "shot_one_on_one",
                      "50_50", "ball_receipt_outcome", "ball_recovery_recovery_failure", "block_deflection",
                      "block_offensive", "block_save_block", "carry_end_location", "clearance_aerial_won",
                      "counterpress", "dribble_outcome", "duel_outcome", "duel_type", "duration",
                      "foul_committed_card", "foul_committed_advantage",
                      "foul_committed_offensive", "foul_committed_penalty", "foul_committed_type",
                      "foul_won_advantage", "foul_won_defensive", "foul_won_penalty", "goalkeeper_body_part",
                      "goalkeeper_end_location", "goalkeeper_outcome", "goalkeeper_position",
                      "goalkeeper_technique", "goalkeeper_type",
                      "injury_stoppage_in_chain",
                      "interception_outcome", "miscontrol_aerial_won", "pass_aerial_won",
                      "pass_angle", "pass_assisted_shot_id", "pass_body_part", "pass_cross",
                      "pass_cut_back", "pass_deflected", "pass_end_location", "pass_goal_assist", "pass_height",
                      "pass_length", "pass_miscommunication",
                      "pass_outcome", "pass_recipient", "pass_shot_assist",
                      "pass_switch", "pass_technique", "pass_type", "player_id", "position", "possession",
                      "possession_team", "possession_team_id", "related_events", "second", "shot_aerial_won",
                      "shot_body_part",
                      "shot_end_location", "shot_first_time", "shot_key_pass_id",
                      "shot_technique", "shot_type", "substitution_outcome", "substitution_replacement", "tactics",
                      "timestamp", "type", "under_pressure", "dribble_nutmeg", "pass_through_ball",
                      "shot_deflected", "shot_redirect", "kick_off", "match_status", "match_status_360",
                      "last_updated", "last_updated_360", "match_week", "stadium", "referee",
                      "home_managers", "away_managers", "data_version", "shot_fidelity_version",
                      "xy_fidelity_version", 'clearance_body_part', 'clearance_head', 'clearance_left_foot',
                      'clearance_right_foot', 'goalkeeper_punched_out', 'off_camera', 'out',
                      'pass_inswinging', 'pass_no_touch', 'pass_outswinging', 'pass_straight']
dfWM22 = drop_attributes(df=JSONtoDF.createDF(CONSTANTS.JSONWM2022), attributes=attributes_to_drop)

# concat the testing data
dfAll = joinDF.concat([dfEM20, dfWM18, dfWM22])
dfAll.reset_index(drop=True, inplace=True)
dfDescription = dfAll.describe()
# save it
dfAll.to_json(CONSTANTS.JSONTESTSHOTS)