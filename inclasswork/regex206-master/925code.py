import re
values = []
values2 = []
with open("mbox-short.txt", "r") as data:
	for line in data:
		if re.findall("X-DSPAM-Confidence: ", line):
			values.append((re.findall(":(.\S+)", line)))


print ("Number of Values: " + str(len(values)))
print ("Maximum: "+ str(max(values)[0]))
print ("Minimum: "+ str(min(values)[0]))
print ("Average: " + str(sum(values)/ len(values)))