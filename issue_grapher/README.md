A sample command-line application providing basic argument parsing with an entrypoint in `bin/`.


### Installation:
`python3 -m venv venv`

`source venv/bin/activate`

`pip3 install -r requirements.txt`


Then, before running the dart tool: `gh auth login`.

### Running:
From the root of `issue_grapher`, run `dart run bin/issue_grapher.dart --issue=83596` (or a different number).

If all has gone well, you should see an output at `./outputs`, with the corresponding issue number.

Outputs are EXTREMELY rough at the moment. Example:

![Example output](https://github.com/gmackall/productivity-tools/blob/main/issue_grapher/sample.png)