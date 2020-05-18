import pandas as pd
import pickle
path=''

unstrucdf=pd.read_pickle('./AugmentedFiles/Augmented_Dataset.pkl')
unstrucdf = unstrucdf[unstrucdf.FundamentalAtT != 'StructuredDataNotFound']
##Adding structured
strucdf=pd.read_csv('./AugmentedFiles/Augmented_Dataset_Revenue.csv')
temp = np.array([])
final_df = pd.DataFrame(columns=['x', 'y'])
strucdf.dropna(inplace=True)
unstrucdf.dropna(inplace=True)
for i, r in unstrucdf.iterrows():
    for ind, row in strucdf.iterrows():

        if (r['year']) == str(int(row['year'])) and r['Company'] == row['Company']:

            temp = np.concatenate(
                [r['t-1embedding1a'], r['t-2embedding1a'], r['t-1embedding7b'], r['t-2embedding7b'], row['t-1Revenue'],
                 row['t-2Revenue']], axis=None)

        if temp.shape == (3074,):
            final_df = final_df.append(pd.Series([temp, row['Revenue']], index=final_df.columns), ignore_index=True)

final_df.to_pickle('./FinalMerged/Final_FinRobertaMax.pkl')
