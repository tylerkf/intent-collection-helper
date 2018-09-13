# intent-collection-helper
Program to make hand classifying language intent easier and quicker.

### Usage
```
python3 classify.py intents_path new_data_path -r
```
```intents_path``` is the path of your intents file.
```new_data_path``` is the path of your file of sentences to be classified.
The ```-r``` flag enables rewrite mode which deletes sentences from your ```new_data_path``` file once they are classified.

### File Formats
The intents file should be in Rasa NLU markdown format (see http://rasa.com/docs/nlu/master/dataformat/). The sentences file should contain sentences separated by new lines.