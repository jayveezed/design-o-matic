from pathlib import Path

import pandas as pd

from functions_file import *

cwd_path = Path.cwd()

df = pd.read_csv('verbs.csv') # 9760 before duplicates removed
df_just_syns = pd.read_csv('http://www.jvzdesigns.com/get-stuff/word-lists-etc/just_syns_verbs.csv')
df_all_used_verbs = pd.read_csv('http://www.jvzdesigns.com/get-stuff/word-lists-etc/used_verbs.csv')

df.drop_duplicates(subset=['present participle (ing)'], keep='first', inplace=True)
df_just_syns.drop_duplicates(subset=['present participle (ing)'], keep='first', inplace=True)
df_all_used_verbs.drop_duplicates(subset=['present participle (ing)'], keep='first', inplace=True)

df_dups_removed = df.copy(deep=True) 
df_just_syns_dups_removed = df_just_syns.copy(deep=True) 
df_all_used_verbs_dups_removed = df_all_used_verbs.copy(deep=True)

df_dups_removed.reset_index(drop=True, inplace=True) # 9642 df to take verbs from
df_just_syns_dups_removed.reset_index(drop=True, inplace=True)
df_all_used_verbs_dups_removed.reset_index(drop=True, inplace=True) 

df_concat = pd.concat([df_all_used_verbs_dups_removed,df_just_syns_dups_removed]).drop_duplicates(subset=['present participle (ing)'], keep='first').reset_index(drop=True)
   
# duplicates = [item for item, count in Counter(listy).items() if count > 1]
for y in df_concat.index:
    if len(df_concat.loc[y, 'verb']) >= 8:
        df_concat.drop(y, inplace=True)

df_concat_list = []

for cat in df_concat['present participle (ing)']:
    df_concat_list.append(cat)    

for z in df_dups_removed.index:
    if df_dups_removed.loc[z, 'present participle (ing)'] in df_concat_list or len(df_dups_removed.loc[z, 'verb']) >= 8:
        df_dups_removed.drop(z, inplace=True)

df_dups_removed.drop_duplicates(subset=['present participle (ing)'], keep='first', inplace=True)
df_dups_removed.reset_index(drop=True, inplace=True)
