# calculates and returns an x value where the offside line has to be drawn
def offsideLine(shooting_player_x, dataframe_all_other_players):
    # rule: two have to be behind the ball
    # goal: find second last opponent player, which defines the offside rule
    # or when the ball is closer than the second last opponent, then the ball defines the offside line

    # find second last opponent
    # for this only the x value is relevant

    # helper variables, the value describes the x value
    second_last_opponent = 0
    last_opponent = 0

    for row in range(len(dataframe_all_other_players)):
        # player has to be opponent
        if not dataframe_all_other_players['teammate'][row]:
            # check if the current opponent player is closer to the goal than the last one that was closest
            if dataframe_all_other_players['x_coordinate'][row] > last_opponent:
                # the last opponent is the new second last opponent
                second_last_opponent = last_opponent
                last_opponent = dataframe_all_other_players['x_coordinate'][row]

            # if its not the last opponent, maybe its the second last opponent
            elif dataframe_all_other_players['x_coordinate'][row] > second_last_opponent:
                # the last opponent is not changed in here only the second last opponent
                second_last_opponent = dataframe_all_other_players['x_coordinate'][row]

    # the opponent with the highest x value and the opponent with the second highest x value has be found
    # now this is compared to the shooter. If its x value is bigger than the one from the second last opponent,
    # then the shooter sets the offside line
    if shooting_player_x > second_last_opponent:
        return shooting_player_x
    else:
        return second_last_opponent


# check which players in a dataframe are offside
# update the given dataframe with a row which states if the player is offside or not
def isOffside(offsideLine, dataframePlayers):
    # to be offside, the player has to be a teammate, otherwise the player is not offside
    offside = []
    for row in range(len(dataframePlayers)):
        if dataframePlayers['teammate'][row]:
            # if it is a teammate, check if the x value is bigger than the offside line, if so, the player is offside
            if dataframePlayers['x_coordinate'][row] > offsideLine:
                offside.append(True)
            else:
                offside.append(False)
        else:
            offside.append(False)

    dataframePlayers['isOffside'] = offside
    return dataframePlayers
