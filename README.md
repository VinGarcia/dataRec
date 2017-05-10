A set of specialized Python scripts made to recovery important text files from damaged or lost file systems.

## Intro

This tool is specialized in searching for a few important text or code files.

It will search the entire HD looking for the selected patterns,
group all files found with these patterns and sort them according to how likely
it is that it is the file you are looking for.

The API is not friendly yet, but hopefully it will in future.

## Running the tool

To configure the tool use the files `js_model.json` and `json_model.json` as a model.

They contain a dictionary with the relevant arguments:

- "words": Any words whose presence is not a guanrantee that the file is relevant, but that are likely to appear multiple times on the desired file.

- "desc"/"on_it": Words that must be present on the file, e.g. the command to import some library you know you are using, or the `main()` function declaration (Note: Currently it is working as an alias for the "words" argument).

The features below are not yet implemented:

- "desc"/"off_it": List of words whose presence would disqualify the file as a possible candidate, causing it to be removed from the list.

- "regExp": a regular expression that should match one or multiple times inside the file.
