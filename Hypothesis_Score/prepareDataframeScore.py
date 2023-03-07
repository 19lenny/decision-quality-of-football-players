import pandas as pd
from SetUp import JSONtoDF, CONSTANTS, DataManipulation

# import all shots EM2020
dfEMScore = JSONtoDF.createDF("ScoreEM2020.json")

# throw away unnecessary shots like penalties and headers and freekicks
dfEMScore = dfEMScore.query("shot_body_part != 'Head' & play_pattern != 'From Free Kick' & shot_type != 'Penalty'")

# make the tTest on this dataframes
dfWMScore = JSONtoDF.createDF("ScoreWM2022.json")
dfWMScore = dfWMScore.query("shot_body_part != 'Head' & play_pattern != 'From Free Kick' & shot_type != 'Penalty'")
