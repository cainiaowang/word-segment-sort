import re
from operator import itemgetter
#---------------------------------------------------------------------------------------------
#Functions


def remWord(word,words):
  for i in range(len(words)):
    if words[i] == word:
      del words[i]
      return words
  print "failed to find " + word + "in set of words"
  print words
  exit()


def addEntryTD(entry,engTD):
	# Add an entry into the Transitional Dictionary
	node = engTD
	for l in entry:
		if l not in node.keys():
			# Add empty entry
			node[l] = (False,{})
		# Proceed down Tree keeping track of past node		
		pastNode = node
		hasEnd,node = node[l]
	
	# Add word termination
	pastNode[l] = (True,node)
	return

def buildEngTD(filename):
	# Build the Transitional English Dictionary through the entries found in the dict file
	inputfile = open(filename,"r")
	lines = inputfile.readlines()
	engTD = {}
	count=0

	for line in lines:
		line = line.strip().lower()
		if re.match("^[a-z]+$",line):		
			addEntryTD(line,engTD)
			count+=1

	print "Dictionary Used:",filename
	print "Added",count,"words into the Transitional Dictionary (skipped",len(lines)-count,")"
	return engTD

def test_textEval(engTD):
	#test texts
	msg0 = "Hellothisisamessagethatiamtestingthis"
	msg1 = "Hellothisisamessagethatiamtestingthise"
	msg2 = "qwwertyuiopasdfghjklzzxcvbnmqweryuiopf"
	msg3 = "weiucuwebiqligaflewfioubualncywalveurw"
	msg4 = "URPHWAECNEYAEYREVIGSSISSITECIERKENERED"
	msg5 = "VIGENEREDECIPHERKEYISSECURITYAWARENESS"
	msg6 = "name"
	msg7 = "REURENEVIGYAWAISSECISSEYERKREDNEPHITEC"
	print "\nPreliminary Tests to ensure checks are working\n"
	for msg in [msg0,msg1,msg2,msg3,msg4,msg5,msg6,msg7]:
		msg = msg.lower()
		print "String:",msg,
		if hasTpath(msg,engTD,engTD,True,10):
			print "Valid!"#, solutions are:"
			#printTruePaths(msg+words[0],engTD,engTD,"",[])
		else:
			print "Not english"

def hasTpath(msg,engTD_root,engTD_cur,checkFinal,wordCountLeft):
	# Aim:
	# Function will proceed through the msg and the engTD tree checking to ensure has at least one 
	# valid transitional path down the tree.
	
	# (Paths may involve word ends, and then new transitions from the top
	#		thus there may be multiple valid paths down the tree.)
	
	# Algorithm: Recurse through the message from left to right, ensuring a valid
	#            path is available through the english transitional dictionary.
	#						 If through the process, the dictionary traversal encounters a word end
	#							 	then branch the search: checking both for 
	#										a new word from this point and
	#										continuing the current word
	#								return the max checkFinal value returned by both of these recursive searchs;
	#							  this will mean we return the best possible path.
	#					   If checking the last letter, and the higher function has set the 'checkFinal' flag
	#								then ensure that the last letter is both a valid transition 
	#								and that it is the end of a word.
	#						 Return the wordCountLeft figure, this will be used to check how 
	#						 many words make up this solution
	
	# Paramaters:
	#		msg: the remaining message to be checked
	#		engTD_root: the root node of the English Transitional Dictionary, 
	#								used for when starting a new word search
	#		engTD_cur: the current node in the English Transitional Dictionary,
	#							 used to progressively check whether letters can be placed in 
	#							 a valid english word words as they are read off the string
	#		checkFinal: Bool flag, T- ensure the last character read falls on the end of a word
	#								  T- Used when checking if a message which as used up all its end word 
	#									   segments matches,
	#									F- Used for checking mid string if there is a possible match (latter 
	#									   word segments still exist and are thus unknown at this stage
	#		wordCountLeft: Used to limit the total number of words that the algorithm will
	#									 accept in a solution, this has been added to filter bad solutions 
	#									 which tend to be fullof small words
	
	# Note: Function as been extended beyond the True False return to return the wordCountLeft value
	#				which will allow the higher function to be able to find the best solution,
	#				which is defined as the solution containing the least number of words


	# Ensure the msg is lower case
	msg = msg.lower()	


	# CASE: Last letter of the message
	if len(msg) == 1:
		# If has a valid transition in the Dictionary:
		if msg[0] in engTD_cur.keys():
			if checkFinal:
				# If we are in the mode that ensures the match ends on a word en:
				# if a valid word end, return the number of word counts left
				hasEnd,node = engTD_cur[msg[0]]
				if hasEnd:
					return wordCountLeft
				else:
					return 0 # 0 = No Valid Path
			else:
				# Allow a partial match (eg we still have more letters to add on the end)
				return wordCountLeft
		else:
			# Return False - no such word has this transition
			return 0

	# CASE: We are at the start or mid-message:
	if msg[0] in engTD_cur.keys() and wordCountLeft > 0:
		# If there is a valid transition in the dictionary and we havent run out of possible word mates 
		# Get current position within the TD Tree
		hasEnd,node = engTD_cur[msg[0]]
		if hasEnd and wordCountLeft >= 1:
			# If this transition could be the end of a complete word OR mid-word 
			# Fork: check both possibilities and return the best value
			return max (hasTpath(msg[1::],engTD_root,engTD_root,checkFinal,wordCountLeft-1),hasTpath(msg[1::], engTD_root,node,checkFinal,wordCountLeft))
		else:
			# If this is not a finished word, then progress through the tree with the next letter 
			# and position in the tree
			return hasTpath(msg[1::], engTD_root,node,checkFinal,wordCountLeft)
	else:
		# No such possible letter transition
		return 0


def printTruePaths(msg,engTD_root,engTD_cur,currentWord,goodWords):
	# proceed through engTD tree printing all possible word matches 
	msg = msg.lower()	
	
	# CASE: Last letter of the message
	if len(msg) == 1:
		# If has a valid transition in the Dictionary:
		if msg[0] in engTD_cur.keys():
			# Return as to whether this is a word end
			hasEnd,node = engTD_cur[msg[0]]
			if hasEnd:
				goodWords.append(currentWord+msg)
				print goodWords
				return 
			else:
				return
		else:
			# Otherwise return False - no such word has this transition
			return False

	# CASE: We are at the start or mid message:
	if msg[0] in engTD_cur.keys():
		# If there is a valid transition in the dictionary 
		hasEnd,node = engTD_cur[msg[0]]
		if hasEnd:
			# If this transition could be the end of a complete word, then fork to cover both 
			# the possibility of an ongoing word and a new word, if either are possible return true
			newGW= list(goodWords)
			newGW.append(currentWord+msg[0])
			return printTruePaths(msg[1::],engTD_root,engTD_root,"",newGW) or printTruePaths(msg[1::], engTD_root,node,currentWord+msg[0],goodWords)
		else:
			# If this is not a finished word, then progress through the tree with the next letter 
			# and position in the tree
			return printTruePaths(msg[1::], engTD_root,node,currentWord+msg[0],goodWords)
	else:
		# No such possible letter transition
		return False




def dictTreeSolve(msg,words,engTD,maxWordCount,solutions):
	# Aim:
	# Use the transitional dictionary to search for possible solutions, store these solutions
	# in the list solutions allong with a figure related to the minimum number of words this solution
	# is made up of (this number is used for finding the best solution of the set)

	# Algorithm:
	# Begin with an empty msg and a full set of word-segments
	# Loop through adding each word segment to the msg string,
	# 	Test each addition with the transitional dictionary to ensure the letters could make
	# 	up a valid series of english words
	# 	If the new msg (existing messange + canditate word segment) is accepted
	# 		Then use recursion to check then next set of word segments to be added
	# Return list of valid solutions, making sure to check that when the final 
	# segment is added that the final letter is at the end of a word.

	# Paramaters:
	# msg: part of string fixed at this stage
	# words: list of word segments yet to be tried to be added to the end of msg
	# engTD: English Transitional dictionary used to check that the series of letters that mages
	#				 up our solution is a valid series of english words
	# maxWordCount: max acceptable number of english words that can make up the solution 
	#								(poorer solutions tend to have larger number of words making them up, 
	#								so this is used as a filter
	# solutions: list used to store found solutions


	# If at final word, ensure final character ends on a word completion
	if len(words) == 1:
		# Check to see if there is a valid path, this function also returns the minimum word count
		# that that path generates, this figure is used to sort the solutions later
		# a zero value means no path
		minWords = hasTpath(msg+words[0],engTD,engTD,True,maxWordCount)
		if minWords > 0:
			# Solution Found, Add to solution list
			solutions.append((msg+words[0],minWords))
			return
		else:
			return

	# if there are still other word segments to be added on, check all recursively 
	#	allowing a partial match
	for word in words:
		# if there is a partial solution, progress 
		if hasTpath(msg+word,engTD,engTD,False,maxWordCount):
			# If this word has a possible partial path, proceed with it to the next stage of checks
			dictTreeSolve(msg+word,remWord(word,list(words)),engTD,maxWordCount,solutions)


#---------------------------------------------------------------------------------------------
#Code

# our segments
#words = ['RE','UR','ENE','VIG','YA','WA','ISS','ERK','EY','SS','ECI','NE','EC','PH','IT','RED']
words = ['ILL', 'ES', 'SHU', 'MPL', 'CEW', 'IS', 'EN', 'FF', 'EXA', 'TEN', 'LED', 'TH', 'BE']
# Intended Solution = "VIGENERE DECIPHER KEY IS SECURITY AWARENESS"

# Load Dictionary 
#engTD= buildEngTD("corncob_lowercase.txt")
engTD= buildEngTD("5000words.txt")

# Run Preliminary Tests
test_textEval(engTD)

# Get Possible Solutions
solutions = []
maxWordCount=7	# Filter used to disgard rubbish answeres that are made up of lots of short words
print "\nRunning search for solutions..."
print "(looking for a solution with at most",maxWordCount,"words)"
dictTreeSolve("",words,engTD,maxWordCount,solutions)

# Sort Solutions
solutions = sorted(solutions,key=itemgetter(1),reverse=True)

# Print Solutions
print "\nFound",len(solutions),"solutions:"
print "The top 10 solutions are as follows:\n"
for sol,i in solutions[0:10]:
	print "\nString:",sol
	print "Minimum Word Count:",maxWordCount-i+1
	print "Word breakdown:"
	printTruePaths(sol,engTD,engTD,"",[])

# Output full results to file
outfile = open("log.txt","w")
print "\nThe full set of results has been written to the file log.txt"
outfile.write("The following is the full list of found soluions:\n\n")

for sol,i in solutions:
	outfile.write(sol+"\n")


