#!../venv/bin/python
import json
import pandas
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(
    prog='ProgramName',
    description='What the program does',
    epilog='Text at the bottom of help')

parser.add_argument('--issue')

args = parser.parse_args()

dictionary = json.load(open(f'./logs/{args.issue}.json', 'r'))
df = pandas.DataFrame(data=dictionary)
df['created_at']=pandas.to_datetime(df['created_at'])
#df2 = df.groupby(by=df['created_at'].dt.date).count()
#print(df2)
df3 = df.groupby([pandas.Grouper(key='created_at', freq='W')]).count()
print(df3['id'])

df3['id'].plot(kind='bar').figure.savefig(f'./outputs/{args.issue}.png')
