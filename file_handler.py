INTENT_FLAG = "##"
EXAMPLE_FLAG = "-"
INTENT_LABEL = "intent:"

def get_intents(file):
	intent_flag_len = len(INTENT_FLAG)
	example_flag_len = len(EXAMPLE_FLAG)
	intent_label_len = len(INTENT_LABEL)

	intents = {}
	intent_name = ""
	intent_examples = []

	for line in file.readlines():
		if line[:intent_flag_len] == INTENT_FLAG:
			# save last intent info
			if intent_name != "":
				intents[intent_name] = intent_examples
			# get new intent name
			intent_name = line[intent_flag_len:].strip()
			# removes intent label
			if intent_name[:intent_label_len] == INTENT_LABEL:
				intent_name = intent_name[intent_label_len:]
			# reset
			intent_examples = []
		elif line[:example_flag_len] == EXAMPLE_FLAG:
			# add new example
			example = line[example_flag_len:].strip()
			intent_examples.append(example)

	if intent_name != "":
		intents[intent_name] = intent_examples

	return intents

def save_intents(file, intents):
	file.seek(0)
	file.truncate()

	new_text = ""
	for name in intents:
		# add intent name
		if new_text != "":
			new_text += "\n\n"
		new_text += INTENT_FLAG + " " + name
		# add examples
		for example in intents[name]:
			new_text += "\n" + EXAMPLE_FLAG + " " + example

	file.write(new_text)

def get_sentences(file):
	sentences = []
	for line in file.readlines():
		sentence = line.strip()
		# check isn't empty line
		if len(sentence) != 0:
			sentences.append(sentence)

	return sentences

def save_sentences(file, sentences):
	file.seek(0)
	file.truncate()

	new_text = ""
	for sentence in sentences:
		if new_text != "":
			new_text += "\n"
		new_text += sentence

	file.write(new_text)


