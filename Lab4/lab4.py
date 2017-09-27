import re

with open("mbox-short.txt", "r") as data:
	for line in data:
		if re.findall("From", line):
			numbers = re.findall("[0-9]+",line)
			name = re.findall("(\S+)@", line)
			print (name)
			
			print (numbers)
			
			print (line)


