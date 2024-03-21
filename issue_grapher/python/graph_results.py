#!../venv/bin/python
import json
import pandas
import matplotlib.pyplot as plt
import argparse
from matplotlib.ticker import (MaxNLocator, AutoLocator)

def custom_plot(df_original, max_xticks=10, arg_issue=0):

    df = df_original.copy()
    param_dict = {
        'font.family': 'Arial',
        'font.size': 12,
        'lines.linewidth': 1,
        'axes.linewidth':1,
        'axes.grid': True,
        'grid.linestyle': ':',
        'grid.alpha': 0.5
    }

    with plt.rc_context(param_dict):
        df['dates'] = [datetime.date() for datetime in df['id'].index]
        df.set_index(df['dates'], inplace=True)

        # Plotting
        fig, ax = plt.subplots()
        df['id'].plot(kind="bar", stacked=True, ax=ax)
        
        # Axis tick adjustments
        xminor = ax.get_xticks()
        ax.xaxis.set_major_locator(MaxNLocator(min(len(df), max_xticks)))
        ax.set_xticks(xminor, minor=True)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True, nbins='auto', steps=[1,2,2.5,5,10]))

        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        plt.xlabel('Date Created')
        plt.ylabel('Reaction Count')
        plt.title('Issue No. {}'.format(arg_issue))
        
        # Add padding so the dates don't get cut off.
        plt.tight_layout()
        
        # Save to outputs folder.
        plt.savefig(f'./outputs/{arg_issue}.png')

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

custom_plot(df3, arg_issue=args.issue)