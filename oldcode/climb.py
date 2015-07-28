import itertools
from operator import itemgetter
from random import shuffle
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

def getOptions(words):
	# Get the 120 (N*N-N)/2 options that are possible from this position 

	options = []
	# Swap the entry in the [fromPos] with the entry at the [fromPos + FTdiff]
	for aPos in range(len(words)-1):
		for abDif in range(len(words)-aPos-1): #A - B location differece
			abDif+=1
			#build new list
			newWords = list(words)
			#perform swap
			temp = newWords[aPos]
			newWords[aPos] = newWords[aPos + abDif]
			newWords[aPos+abDif]=temp
			#Save to options list
			options.append(newWords)
	return options


def getBestOption(options,countDict,countDict2d):
	# Weighted (tobo) Sorted Path List
	bestVal = 0
	bestOpt=[]
	for opt in options:
		# Check each option: 
		# Val = Trival(sum of valuable trigraphs of resulting word) 
		val = evalText("".join(opt),countDict)
		
		if val > bestVal:
			bestVal = val
			bestOpt = opt
	return (bestVal,bestOpt)

def steepClimb(words,countDict,countDict2d):

	globalmax = 0
	currentVal = evalText("".join(words),countDict)
	while True:
		# Assess neighbouring options
		options = getOptions(words)

		# Find Best Option
		bestVal, bestOpt = getBestOption(options,countDict,countDict2d)

		# If better option cannot be found, we have reached the local max, check result and reset
		if bestVal <= currentVal:

			#Check if local max is higher than previous seen match			
			if bestVal > globalmax:
				# Remember and reset
				globalmax = bestVal
				print "\n",bestVal,"".join(bestOpt)
			
			# Reset: Get new starting location
			shuffle(words)
			currentVal = evalText("".join(words),countDict)
			print "-",
		else:
			#Proceed with best option
			words = bestOpt
			currentVal = bestVal

#---------------------------------------------------------------------------------------------
#Code

# our segments
words = ['RE','UR','ENE','VIG','YA','WA','ISS','ERK','EY','SS','ECI','NE','EC','PH','IT','RED']
countDict = loadDict()
countDict2d = loadDict2d()
test_textEval(countDict)
steepClimb(words,countDict,countDict2d)
