from SetUp import CONSTANTS,JSONtoDF
from SetUp.DecisionEvaluation import evaluationHelper
from Statistics.competition_overview import competition_overview


dfTrain = JSONtoDF.createDF(CONSTANTS.JSONTRAINSHOTS)
competitions = competition_overview(dfTrain, "G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Statistics/dfTrain_CompetitionOverview.xlsx")
description = dfTrain.describe()