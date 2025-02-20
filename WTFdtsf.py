# WTFdtsf - WTF Does That Stand For?
# A game where you have to make up a meaning for a random acronym

# Import 
import random
import string
import sys
from os import system, name, path
from colored import fore, back, style, cprint, stylize, stylize_interactive

# Init variables
random.seed()
selfName = sys.argv[0]
selfName = selfName[selfName.rfind("\\") + 1:-3].capitalize() # Program Name
txtCopyright = "© Anna Vahtera 2021-2025" # Copyright
txtVersion = selfName + " 2.0.3a [02/2025] — " # Version
isDefaultFile = True
asSpecial = random.randint(0,1) # Special Word Flag
arguments = len(sys.argv)
goAgain = "Y"
wLengths = [2, 3, 4, 5, 6, 7] # Acronym Lengths

# Translatable strings:
text = {
  "play-again?": {
    "english": "Play another round? Y/N [Y]: ",
    "finnish": "Pelataanko uusi kierros? K/E [K]: ",
  },
  "quit": {
    "english": "Thank you for playing!",
    "finnish": "Kiitos, että pelasit!",
  },
  "players": {
    "english": " players",
    "finnish": " pelaajaa",
  },
  "player": {
    "english": " Player ",
    "finnish": " Pelaaja ",
  },
  "lang": {
    "english": "English",
    "finnish": "Suomi",
  },
  "language": {
    "english": "Language",
    "finnish": "Kieli",
  },
  "wordlist": {
    "english": "Wordlist",
    "finnish": "Sanalista",
  }
}

def displayHelp(): # Display Help Screen
    cprint("\n\nInstructions:\n", 11)
    print("Usage: "+ selfName.casefold() + " [#players] [filename] [mode]\n")
    print("Mode is any of the following:")
    print("-h, --help: this Help screen.")
    print("-r, --rules: Display rules.")
    print("-f, --finnish: Finnish mode.")
    print("\n'filename' must point to an existing file with list of words " + selfName + " can use. " + selfName + " will default to the current directory for path.\n")
    exit()
        
def displayRules(): # Display Rules Screen
    cprint("\n\nRules:\n", 11)
    print(selfName + " will give you 2 to 7 letters, with the possibility of one of the letters already replaced with a word. Your task is to form an explanation of what this 'acronym' stands for. Inflections of the given words are permitted. (eg. If the word given is 'Run', you can use 'Running'.)\n")
    print("Prepositions, articles, and punctuation do not count as words, so you can use them as much or as little as you want.\n\n")
    cprint("Examples:\n", 11)
    print("[" + stylize("T I", fore('white')) + stylize(" Head ", fore('light_blue')) + stylize("T", fore('white'))+ "]: " + stylize("The Industrial Heads of Tupperware", fore('light_red')))
    print("[" + stylize("B", fore('white')) + stylize(" Belief ", fore('light_blue')) + stylize("I", fore('white'))+ "]: " + stylize("Better Belief, Incorporated", fore('light_red')))
    print("[" + stylize("F C", fore('white')) + "]       : " + stylize("Fundamental Coconuts", fore('light_red')))
    print("[" + stylize("H Q O", fore('white')) + "]     : " + stylize("Hail the Queen of Oranges", fore('light_red')))
    print();
    exit()

def clearScreen(): # Clear Screen
    system('cls' if name == 'nt' else 'clear') # Clear Screen depending on OS

def setPlayers(): # Set Number of Players
    t = 0
    if arguments > 1:
        for l in range(1, arguments):
            if (sys.argv[l].isnumeric()):
                t = int(sys.argv[l])
    
    if t > 0: # Check if Number of Players is Greater than 0 and Return that, otherwise Default to 5
        return t
    else:
        return 5

def setMode(): # Set Program Language Mode
    t = "english"
    if arguments > 1:
        for l in range(1, arguments):
            tStr = sys.argv[l]
            if tStr == "-f" or tStr == "--finnish":
                t = "finnish"
            elif tStr == "-h" or tStr == "--help":
                displayHelp()
            elif tStr == "-r" or tStr == "--rules":
                displayRules()
    return t

# Set Program Language Mode
asMode = setMode()

def setWordList(): # Set Word List
    t = ""
    global isDefaultFile
    global asMode
    
    if arguments > 1:
        for l in range(1, arguments):
            checkFile = path.isfile(sys.argv[l])
            if checkFile:
                t = sys.argv[l]

    if path.isfile(t): # Check if File Exists, and Set File Name. Otherwise, Default to "(language).lst"
        isDefaultFile = False
        varFileName = t
    else:
        isDefaultFile = True
        varFileName = asMode + ".lst" # Default File Name from Language Mode
    
    return varFileName

fileName = setWordList()
numPlayers = setPlayers() # Set Number of Players from Command Line (if given)

# Read Word List
with open(fileName, "r", encoding="utf-8") as f:
    asWordList = [line.strip() for line in f]

# Run Game
def gameRun():
    asLen = random.choices(
        wLengths, weights=(20, 80, 60, 30, 10, 5)) # Give Weights to Random Length of Acronym
    asLength = int(asLen[0])
    
    # Set Status Text
    if not isDefaultFile:
        txtStatus = text["language"][asMode] + ": " + stylize(text["lang"][asMode] + " — ", style(3)) + str(numPlayers) + stylize(text["players"][asMode], fore('dark_gray')) + " — " + stylize(text["wordlist"][asMode], fore('white')) + ": (" + stylize(fileName, fore('light_yellow')) + ")"
    else:    
        txtStatus = text["language"][asMode] + ": " + stylize(text["lang"][asMode] + " — ", style(3)) + str(numPlayers) + stylize(text["players"][asMode], fore('dark_gray'))
    
    # Set Characters per Language
    if asMode == "finnish":
        asChar = list("AEFGHIKLJMNOPRSTUVYÄÖ")
    else:
        asChar = list(string.ascii_uppercase)

    asWords = len(asWordList) - 1 # Word List Length
    asLocation = random.randint(1, asLength) # Location of Special Word
    asWord = asWordList[random.randint(1,asWords)] # Special Word
    
    asAnswers = []
    for l in range(numPlayers):
        asAnswers.append("")

    asString = " "
    print("\n   ", end=" "),
    for l in range(asLength): # Generate Random Letters and Special Word (if any)
        random.seed()
        character = random.randint(0, (len(asChar)-1))
        if (asSpecial == 1) and (l == asLocation):
            asString = asString + stylize(asWord.capitalize(), fore('cyan')) + " "
        else:
            asString = asString + stylize(asChar[character], fore('white')) + " "
        
    clearScreen()

    for l in range(numPlayers): # Player Input Loop (Display Status and Acronym)
        print("\n   ", end=" ")
        cprint(txtStatus, 8)
        print("\n\n   ", end=" ")
        asAnswers[l] = input("[" + asString + "] - " + text["player"][asMode] + str(l+1) + ": ")
        clearScreen()
        
    print("\n\n")
    random.shuffle(asAnswers)
    clearScreen()
    print("\n   ", end=" ")
    cprint(txtStatus, 8)
    print("\n\n   ", end=" ")
    print("[" + asString + "]\n\n")

    for word in asAnswers: # Display Player Answers
        print("  * ", end=" "),
        cprint(word, 9)

# Main Loop, Loop until user quits
while goAgain.capitalize() in ("Y", "K"):
    gameRun()
    print("\n\n   ", end=" ")
    goAgain = input(stylize_interactive(text["play-again?"][asMode], fore('light_gray'))) or "Y"
    print("\n\n")
    
# Version and Copyright Info
print("\n   ", end=" ")
cprint(text["quit"][asMode], 2)
print("\n   ", end=" ")
cprint(txtVersion + txtCopyright, 175)
print()