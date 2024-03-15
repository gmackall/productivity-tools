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

# Show date for at most 10 bars on x axis
tick_step_size = round(len(df3['id']) / 10)

# plot
fig, ax = plt.subplots()
df3['id'].plot(kind="bar", stacked=True, ax=ax)
xLabels = ['']*len(df3['id'])
xLabels[::tick_step_size] = [x.strftime("%Y-%m-%d") for x in df3['id'].index[::tick_step_size]]
#ax.set_xticklabels([x.strftime("%Y-%m-%d") for x in df3['id'].index], rotation=45)
ax.set_xticklabels(xLabels, rotation=45)
plt.subplots_adjust(bottom=0.2)
plt.savefig(f'./outputs/{args.issue}.png')
print(len(df3['id']))