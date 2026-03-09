import pandas as pd

df = pd.read_csv('/Users/jayvanzyl/Downloads/_vodacom_jira/Jira_Features_19Jan2024/Jira_Features-Table.csv', low_memory=False)

df.columns = df.columns.str.replace(' ', '_')
df.columns = df.columns.str.replace('.', '_')
df.columns = df.columns.str.replace('(', '_')
df.columns = df.columns.str.replace(')', '_')
df.columns = df.columns.str.replace('%', 'percent')

df = df.replace('-', '')
# df['Feature_Cost'] = pd.to_numeric(df['Feature_Cost'])
df['Feature_Cost'] = pd.to_numeric(df['Feature_Cost'], errors='coerce').round(2).fillna(0.00)
df['Feature_Count'] = pd.to_numeric(df['Feature_Count'])

df.to_csv('/Users/jayvanzyl/Downloads/_vodacom_jira/Jira_Features_19Jan2024/Jira_Features-Table1.csv', index=False)
