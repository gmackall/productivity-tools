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

# Load the json containing the github issue data.
dictionary = json.load(open(f'./logs/{args.issue}.json', 'r'))
df = pandas.DataFrame(data=dictionary)

# Cast created_at from string to pandas date and then group by week.
# TODO: this might be offset by a week in the future.
df['created_at']=pandas.to_datetime(df['created_at'])
df3 = df.groupby([pandas.Grouper(key='created_at', freq='W')]).count()

fig, ax = plt.subplots()

# Show date for at most 10 bars on x axis
tick_step_size = round(len(df3['id']) / 10)
df3['id'].plot(kind="bar", stacked=True, ax=ax)
xLabels = ['']*len(df3['id'])
xLabels[::tick_step_size] = [x.strftime("%Y-%m-%d") for x in df3['id'].index[::tick_step_size]]
ax.set_xticklabels(xLabels, rotation=45)

# Add padding so the dates don't get cut off.
plt.subplots_adjust(bottom=0.2)

# Save to outputs folder.
plt.savefig(f'./outputs/{args.issue}.png')
