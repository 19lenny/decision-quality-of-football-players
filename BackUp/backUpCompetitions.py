from statsbombpy import sb
# save all competition and their season in a dictionary
dfComp = sb.competitions()
dfComp.to_json(
    'G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/JSON/BackUp/dfBackUpComp.json')