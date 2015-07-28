import itertools
from operator import itemgetter
#---------------------------------------------------------------------------------------------
#Functions

# Read in our 3 letter counts
def loadDict():
	inputfile = open("count-3l.txt","r")
	countDict = {}
	lines = inputfile.readlines()

	for line in lines:
		key,value = line.split()
		countDict[key]=int(value)

	print "[3d] Read in ",len(countDict.keys())," entries"
	return countDict

def loadDict2d():
	inputfile = open("count-2l.txt","r")
	countDict2d = {}
	lines = inputfile.readlines()

	for line in lines:
		key,value = line.split()
		countDict2d[key]=int(value)

	print "[2d] Read in ",len(countDict.keys())," entries"
	return countDict2d


#Get tupples
def getTupples(text):
	tList = []
	for i in range(len(text)-2):
		tList.append(text[i:i+3:1])
	return tList

#Evaluate possible text
def evalText(text,countDict):
	tList = getTupples(text.lower())
	total =0
	for t in tList:
		if t in countDict.keys():
			total += countDict[t]
	return total

def test_textEval(countDict):
	#test 3 texts
	msg1 = "Hellothisisamessagethatiamtestingthise"
	msg2 = "qwwertyuiopasdfghjklzzxcvbnmqweryuiopf"
	msg3 = "weiucuwebiqligaflewfioubualncywalveurw"
	msg4 = "URPHWAECNEYAEYREVIGSSISSITECIERKENERED"
	msg5 = "VIGENEREDECIPHERKEYISSECURITYAWARENESS"

	for msg in [msg1,msg2,msg3,msg4,msg5]:
		msg = msg.lower()
		print msg
		print evalText(msg,countDict)

#test Get tupples
def test_tupple():
	msg = "heythisismy"
	print getTupples(msg)

def printList(best5,progress):
	print "----------------------"
	print "Progress: ",progress
	for msg,val in best5:
		print msg,val

def addUpdateList(entry,best5,lowest,progress):
	msg,val = entry
	if val < lowest:
		return lowest
	else:
		# Add entry
		best5.append(entry)
	
		#Cull lowest entry if list too big
		if len(best5) > 5:
			#initial vals
			lowVal = best5[0]
			lowI =0
			for i in range(len(best5)): 
				msg,val =best5[i]
				if val < lowVal:
					lowVal = val
					lowI =i
			del best5[lowI]
			printList(best5,progress)
			return lowVal
		else:
			return lowest



def bruteForceSolve(words):
	combinations = itertools.permutations(words)
	countDict = loadDict()
	best5 = []
	lowest= 100000000000
	checkNo =0
	maxCheck =20922789888000

	for c in combinations:
		text= "".join(c)
		val =  evalText(text,countDict)
	
		lowest = addUpdateList([text,val],best5,lowest,float(checkNo)/float(maxCheck))
		checkNo += 1
		if checkNo % (maxCheck /100) == 0:
			print checkNo/maxCheck

	for msg,val in best5:
		print msg,")",val



def smartTraverse(msg,words,countDict,countDict2):
	if len(words) == 0:
		#Hit bottom
		return (msg,evalText(msg,countDict)) 

	elif len(words) == 1:
		#Last Choice
		msg = msg + words[0]
		return (msg,evalText(msg,countDict)) 

	elif len(words) > 1:
		#Smart Choice: pick transition with the highest touple value
		highVal = -1
		highWord ="boo"
		for word in words:
			pair = (msg[-1]+word[0]).lower()
			val = 0
			if pair in countDict2.keys():
				val = countDict2[pair]
			if val > highVal:
				highVal = val
				highWord = word
		return smartTraverse(msg+highWord,remWord(highWord,list(words)),countDict,countDict2)



# Alway pick first word
def dumbTraverse(msg,words,countDict):
	msg = msg + "".join(words)
	return (msg,evalText(msg,countDict))
	
def remWord(word,words):
	for i in range(len(words)):
		if words[i] == word:
			del words[i]
			return words
	print "failed to find " + word + "in set of words"
	print words
	exit()


def sortPaths(paths,i):
	#Sort based on the value field in the thingy
	return sorted(paths,key=itemgetter(i))


def recTreeSolve(msg,words,countDict,countDict2d,best):
	
	bestMsg,bestVal = best
	
	#Evaluate possible choices
	paths = []
	
	for word in words:
		# Check each path
		newWords = remWord(word,list(words))	# possible options if we take this path	
		#(guessMsg,val) = dumbTraverse(msg+word,newWords,countDict) # simple traverse of path
		(guessMsg,val) = smartTraverse(msg+word,newWords,countDict,countDict2d) # simple traverse of path
		paths.append((word,guessMsg,val,newWords)) # Save results
	
	# Sort to evaluate most promising paths first
	paths=sortPaths(pathsi,2)	

	# Evaluate paths from most likely to least
	for i in range(len(paths)):
		# Retrieve calculated info above
		word,guessMsg,val,newWords = paths[i]

		# if one of these represents our best path found thus far, display to user
		if val > bestVal:
			bestMsg = guessMsg
			bestVal = val
			print bestVal,bestMsg
		
		# Recursively follow paths from best to worst
		bestMsg,bestVal = recTreeSolve(msg+word,newWords,countDict,countDict2d,(bestMsg,bestVal))

	return (bestMsg,bestVal)

def getBestNPaths(msg,words,countDict,countDict2d,N):
	# Weighted (tobo) Sorted Path List
	paths = []
	
	for word in words:
		# Check each path: 
		# Val = Trival(sum of valuable trigraphs of resulting word) 
		#			  * DiVal (value of resulting digraph by adding this individual node)
		TriVal = evalText(msg+word,countDict)
		DiVal = 1
		if msg:	# (MSG is not present for root node)
			pair = (msg[-1]+word[0]).lower()
			if pair in countDict2d.keys():
					DiVal = countDict2d[pair]
		
		paths.append((word,TriVal*DiVal)) # Save results
	
	# Sort to evaluate most promising paths first
	paths=sortPaths(paths,1)	

	# Return to N paths for evaluation (more than 2 takes over 160 min)
	return paths[0:N]	

def cutTreeSolve(msg,words,countDict,countDict2d,best):
	bestMsg,bestVal = best
	
	N=2
	#print ("["+msg+"]",words)
	#Evaluate best possible paths
	paths = getBestNPaths(msg,words,countDict,countDict2d,N)
	
	# Recurse through paths from best to worst
	for i in range(len(paths)):
		# Retrieve calculated info above
		word,val = paths[i]
		newWords = remWord(word,list(words))
	
		# if one of these represents our best path found thus far, display to user
		if val > bestVal:
			bestMsg = msg+word
			bestVal = val
			print bestVal,bestMsg,newWords
		
		# Recursively follow paths from best to worst
		bestMsg,bestVal = cutTreeSolve(msg+word,newWords,countDict,countDict2d,(bestMsg,bestVal))

	return (bestMsg,bestVal)



#---------------------------------------------------------------------------------------------
#Code

# our segments
words = ['RE','UR','ENE','VIG','YA','WA','ISS','ERK','EY','SS','ECI','NE','EC','PH','IT','RED']
countDict = loadDict()
countDict2d = loadDict2d()
#test_textEval(countDict)
cutTreeSolve("",words,countDict,countDict2d,("yomama",0))
