A tool to generate a graph of github likes an issue has received over time. 

Inspired by https://github.com/loic-sharma/github-insights.

### Installation:

#### Set up the venv:

`python3 -m venv venv`

`source venv/bin/activate`

`pip3 install -r requirements.txt`

#### Install the github cli and authenticate:
Install the gh cli, [instructions available here](https://github.com/gmackall/productivity-tools/tree/main/issue_grapher).

Then, before running the dart tool: `gh auth login`.

### Running:
From the root of `issue_grapher`, run `dart run bin/issue_grapher.dart --issue=83596` (or a different number).

If all has gone well, you should see an output at `./outputs`, with the corresponding issue number.

Outputs are somewhat rough at the moment. Example:

![Example output](https://github.com/gmackall/productivity-tools/blob/main/issue_grapher/sample.png)

### Things that would be nice to add:
1. Pass args to determine the time bucketing (it buckets by week currently).
2. Pass args to determine the start and end time.
3. ~~Make the x axis legible.~~ Mostly done but still room for improvement.