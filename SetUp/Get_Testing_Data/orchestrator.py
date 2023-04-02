from SetUp import JSONtoDF, CONSTANTS, joinDF


# get all testing data
dfEM20 = JSONtoDF.createDF(CONSTANTS.JSONEM2020)
dfWM18 = JSONtoDF.createDF(CONSTANTS.JSONWM2018)
dfWM22 = JSONtoDF.createDF(CONSTANTS.JSONWM2022)

# concat the testing data
dfAll = joinDF.concat([dfEM20, dfWM18, dfWM22])
dfAll.reset_index(drop=True, inplace=True)
# save it
dfAll.to_json(CONSTANTS.JSONTESTSHOTS)
