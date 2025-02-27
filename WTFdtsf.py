''' Acronym Game '''
#
# WTFdtsf - WTF Does That Stand For?
# A game where you have to make up a meaning for a random acronym
#

# Import
import random
import string
import sys
from os import path
from libAnna.anna import open_file, clear_screen

# Init variables
random.seed()
SELF_NAME = sys.argv[0]
SELF_NAME = SELF_NAME[SELF_NAME.rfind("\\") + 1:-3]  # Program Name
TXT_COPYRIGHT = "© Anna Vahtera 2021-2025"  # Copyright
TXT_VERSION = SELF_NAME + " 2.0.3a [02/2025] — "  # Version
IS_DEFAULT_FILE = True
AS_SPECIAL = random.randint(0, 1)  # Special Word Flag
ARGUMENTS = len(sys.argv)
GO_AGAIN = "Y"
W_LENGTHS = [2, 3, 4, 5, 6, 7]  # Acronym Lengths

# Color Definitions
WHITE = "\033[37m"  # White Text Color
BLUE = "\033[34m"  # Blue Text Color
YELLOW = "\033[33m"  # Yellow Text Color
GREEN = "\033[32m"  # Green Text Color
RED = "\033[31m"  # Red Text Color
CYAN = "\033[36m"  # Cyan Text Color
PURPLE = "\033[35m"  # Purple Text Color
BLACK = "\033[30m"  # Black Text Color
BOLD = "\033[1m"  # Bold Text
NOBOLD = "\033[22m"  # No Bold Text
ENDC = "\033[0m"  # Reset Text Color

# Translatable strings:
TEXT = {
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


def display_help():
    '''Display Help Screen'''
    print(f"\n\n{GREEN}Instructions:{ENDC}\n")
    print(f"Usage: {SELF_NAME} [#players] [filename] [mode]\n")
    print("Mode is any of the following:")
    print("-h, --help: this Help screen.")
    print("-r, --rules: Display rules.")
    print("-f, --finnish: Finnish mode.")
    print(f"\n'filename' must point to an existing file with list of words {SELF_NAME} can use. "
          f"{SELF_NAME} will default to the current directory for path.\n")
    sys.exit()


def display_rules():
    '''Display Rules Screen'''
    print(f"\n\n{GREEN}Rules:{ENDC}\n")
    print(f"{SELF_NAME} will give you 2 to 7 letters, with the possibility of one of the letters "
          f"replaced with a word. Your task is to form an explanation of what this 'acronym' "
          f"stands for. Inflections of the given words are permitted. (eg. If the word given is "
          f"'Run', you can use 'Running'.)\n")
    print("Prepositions, articles, and punctuation do not count as words, so you can use them as "
          "much or as little as you want.\n\n")
    print(f"{GREEN}Examples:{ENDC}\n")
    print(f"{BOLD}[{WHITE}T I{BOLD}{BLUE} Head {BOLD}{WHITE}T{ENDC}]: {BOLD}{RED}The Industrial "
          f"Heads of Tupperware{ENDC}")
    print(f"{BOLD}[{WHITE}B{BOLD}{BLUE} Belief {BOLD}{WHITE}I{ENDC}]: {BOLD}{RED}Better Belief,"
          f" Incorporated{ENDC}")
    print(f"{BOLD}[{WHITE}F C{ENDC}]       : {BOLD}{RED}Fundamental Coconuts{ENDC}")
    print(f"{BOLD}[{WHITE}H Q O{ENDC}]     : {BOLD}{RED}Hail the Queen of Oranges{ENDC}")
    print()
    sys.exit()


def set_players():
    '''Set Number of Players'''
    T = 0
    if ARGUMENTS > 1:
        for L in range(1, ARGUMENTS):
            if sys.argv[L].isnumeric():
                T = int(sys.argv[L])

    if T > 0:  # Check if Number of Players is Greater than 0, otherwise Default to 5
        return T

    return 5


def set_mode():
    '''Set Program Language Mode'''
    T = "english"
    if ARGUMENTS > 1:
        for L in range(1, ARGUMENTS):
            T_STR = sys.argv[L]
            if T_STR in ('-f', '--finnish'):
                T = "finnish"
            elif T_STR in('-h', '--help'):
                display_help()
            elif T_STR in ('-r', '--rules'):
                display_rules()
    return T


# Set Program Language Mode
AS_MODE = set_mode()


def set_word_list():
    '''Set Word List'''
    T = ""
    global IS_DEFAULT_FILE
    # global AS_MODE

    if ARGUMENTS > 1:
        for L in range(1, ARGUMENTS):
            CHECK_FILE = path.isfile(sys.argv[L])
            if CHECK_FILE:
                T = sys.argv[L]

    if path.isfile(T):  # Check if File Exists. Otherwise, Default to "(language).lst"
        IS_DEFAULT_FILE = False
        VAR_FILE_NAME = T
    else:
        IS_DEFAULT_FILE = True
        VAR_FILE_NAME = AS_MODE + ".lst"  # Default File Name from Language Mode

    return VAR_FILE_NAME


FILE_NAME = set_word_list()
NUM_PLAYERS = set_players()  # Set Number of Players from Command Line (if given)

# Read Word List
AS_WORD_LIST = open_file(FILE_NAME)


# Run Game
def game_run():
    '''Main Game Loop'''
    AS_LEN = random.choices(
        W_LENGTHS, weights=(20, 80, 60, 30, 10, 5))  # Give Weights to Random Length of Acronym
    AS_LENGTH = int(AS_LEN[0])

    # Set Status Text
    if not IS_DEFAULT_FILE:
        TXT_STATUS = (f"{BOLD}{BLACK}{TEXT['language'][AS_MODE]}: {ENDC}{BOLD}"
                      f"{TEXT['lang'][AS_MODE]}"
                      f" — {NOBOLD}{BOLD}{GREEN}{NUM_PLAYERS}{ENDC}{TEXT['players'][AS_MODE]} — "
                      f"{TEXT['wordlist'][AS_MODE]}: "
                      f"({BOLD}{YELLOW}{FILE_NAME}{ENDC})")
    else:
        TXT_STATUS = (f"{BOLD}{BLACK}{TEXT['language'][AS_MODE]}: {ENDC}{BOLD}"
                      f"{TEXT['lang'][AS_MODE]} — {NOBOLD}"
                      f"{GREEN}{BOLD}{NUM_PLAYERS}{ENDC}{TEXT['players'][AS_MODE]}")

    # Set Characters per Language
    if AS_MODE == "finnish":
        AS_CHAR = list("AEFGHIKLJMNOPRSTUVYÄÖ")
    else:
        AS_CHAR = list(string.ascii_uppercase)

    AS_WORDS = len(AS_WORD_LIST) - 1  # Word List Length
    AS_LOCATION = random.randint(1, AS_LENGTH)  # Location of Special Word
    AS_WORD = AS_WORD_LIST[random.randint(1, AS_WORDS)]  # Special Word

    AS_ANSWERS = []
    for L in range(NUM_PLAYERS):
        AS_ANSWERS.append("")

    AS_STRING = " "

    print("\n   ", end=" ")

    for L in range(AS_LENGTH):  # Generate Random Letters and Special Word (if any)
        random.seed()
        CHARACTER = random.randint(0, (len(AS_CHAR) - 1))
        if AS_SPECIAL == 1 and L == AS_LOCATION:
            AS_STRING = AS_STRING + f"{BOLD}{BLUE}{AS_WORD.capitalize()}{ENDC} "
        else:
            AS_STRING = AS_STRING + f"{BOLD}{WHITE}{AS_CHAR[CHARACTER]}{ENDC} "

    clear_screen()

    for L in range(NUM_PLAYERS):  # Player Input Loop (Display Status and Acronym)
        print("\n   ", end=" ")
        print(f"{GREEN}{TXT_STATUS}{ENDC}")
        print("\n\n   ", end=" ")
        AS_ANSWERS[L] = input(f"[{AS_STRING}] - {TEXT['player'][AS_MODE]}{str(L + 1)}: ")
        clear_screen()

    print("\n\n")
    random.shuffle(AS_ANSWERS)
    clear_screen()
    print("\n   ", end=" ")
    print(f"{GREEN}{TXT_STATUS}{ENDC}")
    print("\n\n   ", end=" ")
    print(f"[{AS_STRING}]\n\n")

    for WORD in AS_ANSWERS:  # Display Player Answers
        print(f"{BOLD}{BLACK}  * {ENDC}", end=" ")
        print(f"{RED}{BOLD}{WORD}{ENDC}")


# Main Loop, Loop until user quits
while GO_AGAIN.capitalize() in ("Y", "K"):
    game_run()
    print("\n\n   ", end=" ")
    GO_AGAIN = input(f"{WHITE}{TEXT['play-again?'][AS_MODE]}{ENDC}") or "Y"
    print("\n\n")

# Version and Copyright Info
print("\n   ", end=" ")
print(f"{GREEN}{TEXT['quit'][AS_MODE]}{ENDC}")
print("\n   ", end=" ")
print(f"{TXT_VERSION}{TXT_COPYRIGHT}{ENDC}")
print()
