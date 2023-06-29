from SetUp import CONSTANTS,JSONtoDF
from SetUp.DecisionEvaluation import evaluationHelper
from Statistics.competition_overview import competition_overview


dfTrain = JSONtoDF.createDF(CONSTANTS.JSONTRAINSHOTS)
dfTrain = dfTrain.dropna(subset=['log_angle', 'distance_to_goal_centre', 'delta_distance_GK_to_optimal_line'])
dfTrain.reset_index(drop=True, inplace=True)
#dfTrain.to_csv("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/SPSS/dfTrain/dfTrain.csv")
#competitions_train = competition_overview(dfTrain, "G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Statistics/dfTrain_CompetitionOverview.xlsx")
descriptionTrain = dfTrain.describe()

dfTest = JSONtoDF.createDF(CONSTANTS.JSONTESTSHOTS)
dfTest = dfTest.dropna(subset=['log_angle', 'distance_to_goal_centre', 'delta_distance_GK_to_optimal_line'])
dfTest.reset_index(drop=True, inplace=True)
#overview_test = competition_overview(dfTest, "G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Statistics/dfTest_CompetitionOverview.xlsx")
#dfTest.to_csv("G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/SPSS/dfTest/dfTest.csv")
#dfTest = dfTest[dfTest['shot_decision_correct']==False]
descriptionTest = dfTest.describe()