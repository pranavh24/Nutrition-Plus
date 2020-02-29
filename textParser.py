from autocorrect import Speller
from math import *

NUTRITION_THRESHOLD = 0.7
NUTRITION_LABELS = {"total fat":80,"total carbohydrate":285,"protein":50,"cholesterol":300,"sodium":2286,"sugars":37,"calories":2000};
UNITS = {"total fat":" g","total carbohydrate":" g","protein":" g","cholesterol":" mg","sodium":" mg","sugars":" g","calories":" Cal"};
INGREDIENTS = [];

spell = Speller(lang = "en");

def removeMultiLines(string):
	returnString = "";
	lastChr = "\n"
	for chr in string:
		if (chr != "\n"):
			returnString += chr;
		elif (lastChr != "\n"):
			returnString += chr;	
		lastChr = chr;
	return returnString;

def normalizedKey(ky):
	maxScore = 0;
	returnString = "";
	for label in NUTRITION_LABELS.keys():
		subScore = 0;	
		for ind in range(min(len(ky),len(label))):
			if (ky[ind] == label[ind]):
				subScore+= 1;
		subScore /= max(len(ky),len(label));
		if (subScore > NUTRITION_THRESHOLD and subScore > maxScore):	
			maxScore = subScore;
			returnString = label;
	if (returnString == ""):
		return ky;
	return returnString;

def intValue(string):
	intS = "";	
	for chr in string:
		if chr.isdigit():
			intS += chr;
	if (len(intS) == 0):
		return 0;
	return int(intS);

def convertToDict(string):
	returnDict = {};
	percenDict = {};
	for ln in string.lower().split("\n"):
		data = ln.split(" ");
		if (len(data) <2):
			continue;
		ky = normalizedKey(" ".join(data[:len(data)-1]));	
		vl = intValue(data[-1]);
		if (ky in NUTRITION_LABELS.keys()):
			pcent = round(100 * int(vl)/NUTRITION_LABELS[ky])
			if (not ky in returnDict.keys()):
				returnDict[ky] = vl;
				percenDict[ky] = pcent; 
		else:
			ky = normalizedKey(data[0]);
			vl = intValue(data[1]);
			if (ky in NUTRITION_LABELS.keys() and not ky in returnDict.keys()):
				pcent = 100 * int(vl)/NUTRITION_LABELS[ky]
				returnDict[ky] = vl;
				percenDict[ky] = pcent;
	for label in NUTRITION_LABELS:
		if not label in returnDict.keys():
			returnDict[label] = 9
			percenDict[label] = 12
	return returnDict,percenDict;

def replaceChars(chars,orgString):
	returnString = "";
	for chr in orgString:
		if chr not in chars:
			returnString += chr;
	return returnString; 

def normalizeIngredients(string):
	returnString = string.lower();
	returnString = replaceChars("(){}[]:.!?$£<>''`~+=-*‘;",returnString)
	corrected = spell(returnString).split(" ", 1)[1]
	text = removeColors(corrected.replace("\n", " ").split(", "))
	return text

def containsIngredient(word,targetIngredient):
	maxMatch = 0;
	for start in range(0,max(1,len(word)-len(targetIngredient))):
		subMatch = 0;
		for i in range(start,start + len(targetIngredient)):
			x = i - start;
			if (word[i] == targetIngredient[x]):
				subMatch+= 1;
		subMatch /= len(targetIngredient); 
		if (subMatch > maxMatch):
			maxMatch = subMatch;
	return maxMatch;

def removeColors(array):
	cleanList = []
	for x in array:
		if "#" not in x:
			cleanList.append(x)
	return cleanList

