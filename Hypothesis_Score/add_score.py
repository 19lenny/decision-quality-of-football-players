import pandas as pd
from SetUp import JSONtoDF, CONSTANTS, DataManipulation

# import all shots EM2020
dfWMScore = JSONtoDF.createDF("ShotsEM2020.json")
dfWMScore = DataManipulation.score(dfWMScore)
dfWMScore.to_json("ScoreEM2020.json")

# import all shots EM2020
dfWMScore = JSONtoDF.createDF("ShotsWM2022.json")
dfWMScore = DataManipulation.score(dfWMScore)
dfWMScore.to_json("ScoreWM2022.json")