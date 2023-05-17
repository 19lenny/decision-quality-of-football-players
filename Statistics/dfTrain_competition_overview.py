from SetUp import JSONtoDF, CONSTANTS
import pandas as pd

dfTrain = JSONtoDF.createDF(CONSTANTS.JSONTRAINSHOTS)
#find out how many games are played in each season
result = pd.DataFrame()
result['number of games'] = dfTrain.groupby(['competition','season'])['competition'].count()
result.to_excel("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Statistics/dfTrain_CompetitionOverview.xlsx")

dfTest = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
#find out how many games are played in each season
result = pd.DataFrame()
result['number of games'] = dfTest.groupby(['competition','season'])['competition'].count()
result.to_excel("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Statistics/dfTest_CompetitionOverview.xlsx")