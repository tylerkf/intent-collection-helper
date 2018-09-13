from tkinter import *
import argparse
import file_handler

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("intents_file", type=argparse.FileType("r+"))
	parser.add_argument("sentences_file", type=argparse.FileType("r+"))
	parser.add_argument("-r", action="store_true")
	args = parser.parse_args()

	# load intent and sentence files
	intents_file = args.intents_file
	sentences_file = args.sentences_file
	intents = file_handler.get_intents(intents_file)
	sentences = file_handler.get_sentences(sentences_file)

	root = Tk()
	app = ClassifyApp(root, intents, sentences)
	root.mainloop()

	# save intent and sentence files
	if app.current_sentence != "":
		sentences.insert(0, app.current_sentence)
	file_handler.save_intents(intents_file, app.intents)

	if args.r == True:
		file_handler.save_sentences(sentences_file, app.sentences)

	intents_file.close()
	sentences_file.close()

class ClassifyApp:
	def __init__(self, master, intents, sentences):
		self.master = master
		self.intents = intents
		self.sentences = sentences

		master.title("Intent Classification Helper")

		Grid.columnconfigure(self.master, 0, weight=1)
		Grid.columnconfigure(self.master, 1, weight=1)
		Grid.rowconfigure(self.master, 0, weight=1)

		# set up sentence text
		self.current_sentence = ""
		self.label_string = StringVar()
		self.label = Label(self.master, textvariable=self.label_string)
		self.label.grid(row=0, column=0, sticky=N+E+S+W)

		# set up entry
		self.entry_string = StringVar()
		self.entry = Entry(self.master, textvariable=self.entry_string)
		self.entry.bind("<Tab>", self.on_tab)
		self.entry.bind("<Return>", self.on_return)
		self.entry.grid(row=1, column=0, sticky=E+W)

		# set up intents list with scrollbar
		self.intents_scrollbar = Scrollbar(self.master)
		self.intents_scrollbar.grid(row=0, column=2, rowspan=2, sticky=N+S)
		self.intents_list = Listbox(self.master, yscrollcommand=self.intents_scrollbar.set)
		self.intents_list.grid(row=0, column=1, rowspan=2, columnspan=2, sticky=N+E+S+W)

		self.fill_intents_list()
		self.get_new_sentence()

	def set_sizes(self, width, height):
		print(width, height)
		self.intents_list.config(width=int(width/2), height=int(height))

	def on_tab(self, event):
		# simple autocomplete
		text = self.entry_string.get()
		text_len = len(text)

		intent_names = list(self.intents.keys())
		match = ""
		for name in intent_names:
			if name[:text_len] == text:
				if match == "":
					# first match found
					match = name
				elif match in name:
					# match includes name
					match = name
				elif name not in match:
					# get longest shared substring starting at 0
					for i in range(text_len, min(len(match), len(name))):
						if match[i] != name[i]:
							match = match[:i]
							break

		# if no match found
		if match != "":
			self.entry_string.set(match)
		self.entry.icursor(END)

		return "break"

	def on_return(self, event):
		entry = self.entry_string.get()
		if entry in self.intents:
			self.intents[entry].append(self.current_sentence)
			self.entry_string.set("")
			self.get_new_sentence()

		return "break"

	def get_new_sentence(self):
		# out of sentences
		if len(self.sentences) == 0:
			self.current_sentence = ""
			self.label_string.set("No more sentences to classify")
			return

		self.current_sentence = self.sentences.pop(0)
		self.label_string.set("\"{}\"".format(self.current_sentence))

	def fill_intents_list(self):
		self.intents_list.delete(0, END)

		intent_names = list(self.intents.keys())
		intent_names.sort()

		for name in intent_names:
			text = "{} – \"{}\"".format(name, self.intents[name][0])
			self.intents_list.insert(END, text)

if __name__ == "__main__":
	main()