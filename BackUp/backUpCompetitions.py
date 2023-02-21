from statsbombpy import sb
from SetUp import CONSTANTS
# save all competition and their season in a dictionary
dfComp = sb.competitions()
filename = "dfBackUpComp.json"
dfComp.to_json(CONSTANTS.JSONBACKUPFOLDER + filename)
