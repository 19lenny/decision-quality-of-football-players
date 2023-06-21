from SetUp import JSONtoDF, CONSTANTS
import pandas as pd

def competition_overview(df, saving_path):
    # Group by 'competition' and 'season' and count the occurrences
    grouped_df = df.groupby(['competition', 'season']).size().reset_index(name='shot_count')

    # Group by 'competition' and 'season' and count the distinct 'match_id'
    unique_matches_df = df.groupby(['competition', 'season'])['match_id'].nunique().reset_index(name='match_count')

    # Merge the two DataFrames
    result_df = grouped_df.merge(unique_matches_df, on=['competition', 'season'])

    # Set index starting from 1 and assign a name to the index
    result_df.index = result_df.index + 1
    result_df.index.name = 'number of seasons'

    # Calculate the sum of the number of events and the sum of the number of games
    event_count_sum = result_df['shot_count'].sum()
    unique_matches_count_sum = result_df['match_count'].sum()

    # Create a row with the sums
    sum_row = pd.DataFrame({'shot_count': [event_count_sum], 'match_count': [unique_matches_count_sum]})
    sum_row.index = ['Total']
    result_df = result_df.append(sum_row)

    # Save the DataFrame as an Excel file
    #result_df.to_excel(saving_path)
    return result_df

dfTrain = JSONtoDF.createDF(CONSTANTS.JSONTRAINSHOTS)
overview = competition_overview(dfTrain, "G:/Meine Ablage/a_uni 10. Semester - Masterarbeit/Masterarbeit/Thesis/thesis/Statistics/dfTrain_CompetitionOverview.xlsx")



