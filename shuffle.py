import random
msg = "This example sentence will be shuffled"
minsize = 2
maxsize = 3

# Display starting message
print "Message to be shuffled:"
print msg

# Remove Spaces
msg = "".join(msg.split()).upper()
print "1. Remove Spaces an convert to uppercase"
print msg

# Break into Chunks
segs = []
def breakup(msg,segs,minsize,maxsize):
	if len(msg) > maxsize:
		breakPoint = random.randint(minsize,len(msg)-minsize)
		breakup(msg[0:breakPoint],segs,minsize,maxsize)
		breakup(msg[breakPoint:len(msg)],segs,minsize,maxsize)
	else:
		segs.append(msg)

breakup(msg,segs,minsize,maxsize)

# Print Broken up Message
print "2. Message Broken up as such:"
print segs

# Shuffle Text
random.shuffle(segs)
print "3. Shuffled message reads as follows:"
print segs
