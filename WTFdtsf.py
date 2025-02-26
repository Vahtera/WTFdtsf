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
    t = 0
    if ARGUMENTS > 1:
        for l in range(1, ARGUMENTS):
            if sys.argv[l].isnumeric():
                t = int(sys.argv[l])

    if t > 0:  # Check if Number of Players is Greater than 0, otherwise Default to 5
        return t

    return 5


def set_mode():
    '''Set Program Language Mode'''
    t = "english"
    if ARGUMENTS > 1:
        for l in range(1, ARGUMENTS):
            t_str = sys.argv[l]
            if t_str in ('-f', '--finnish'):
                t = "finnish"
            elif t_str in('-h', '--help'):
                display_help()
            elif t_str in ('-r', '--rules'):
                display_rules()
    return t


# Set Program Language Mode
AS_MODE = set_mode()


def set_word_list():
    '''Set Word List'''
    t = ""
    global IS_DEFAULT_FILE
    # global AS_MODE

    if ARGUMENTS > 1:
        for l in range(1, ARGUMENTS):
            check_file = path.isfile(sys.argv[l])
            if check_file:
                t = sys.argv[l]

    if path.isfile(t):  # Check if File Exists. Otherwise, Default to "(language).lst"
        IS_DEFAULT_FILE = False
        var_file_name = t
    else:
        IS_DEFAULT_FILE = True
        var_file_name = AS_MODE + ".lst"  # Default File Name from Language Mode

    return var_file_name


FILE_NAME = set_word_list()
NUM_PLAYERS = set_players()  # Set Number of Players from Command Line (if given)

# Read Word List
AS_WORD_LIST = open_file(FILE_NAME)


# Run Game
def game_run():
    '''Main Game Loop'''
    as_len = random.choices(
        W_LENGTHS, weights=(20, 80, 60, 30, 10, 5))  # Give Weights to Random Length of Acronym
    as_length = int(as_len[0])

    # Set Status Text
    if not IS_DEFAULT_FILE:
        txt_status = (f"{BOLD}{BLACK}{TEXT['language'][AS_MODE]}: {ENDC}{BOLD}"
                      f"{TEXT['lang'][AS_MODE]}"
                      f" — {NOBOLD}{BOLD}{GREEN}{NUM_PLAYERS}{ENDC}{TEXT['players'][AS_MODE]} — "
                      f"{TEXT['wordlist'][AS_MODE]}: "
                      f"({BOLD}{YELLOW}{FILE_NAME}{ENDC})")
    else:
        txt_status = (f"{BOLD}{BLACK}{TEXT['language'][AS_MODE]}: {ENDC}{BOLD}"
                      f"{TEXT['lang'][AS_MODE]} — {NOBOLD}"
                      f"{GREEN}{BOLD}{NUM_PLAYERS}{ENDC}{TEXT['players'][AS_MODE]}")

    # Set Characters per Language
    if AS_MODE == "finnish":
        as_char = list("AEFGHIKLJMNOPRSTUVYÄÖ")
    else:
        as_char = list(string.ascii_uppercase)

    as_words = len(AS_WORD_LIST) - 1  # Word List Length
    as_location = random.randint(1, as_length)  # Location of Special Word
    as_word = AS_WORD_LIST[random.randint(1, as_words)]  # Special Word

    as_answers = []
    for l in range(NUM_PLAYERS):
        as_answers.append("")

    as_string = " "

    print("\n   ", end=" ")

    for l in range(as_length):  # Generate Random Letters and Special Word (if any)
        random.seed()
        character = random.randint(0, (len(as_char) - 1))
        if AS_SPECIAL == 1 and l == as_location:
            as_string = as_string + f"{BOLD}{BLUE}{as_word.capitalize()}{ENDC} "
        else:
            as_string = as_string + f"{BOLD}{WHITE}{as_char[character]}{ENDC} "

    clear_screen()

    for l in range(NUM_PLAYERS):  # Player Input Loop (Display Status and Acronym)
        print("\n   ", end=" ")
        print(f"{GREEN}{txt_status}{ENDC}")
        print("\n\n   ", end=" ")
        as_answers[l] = input(f"[{as_string}] - {TEXT['player'][AS_MODE]}{str(l + 1)}: ")
        clear_screen()

    print("\n\n")
    random.shuffle(as_answers)
    clear_screen()
    print("\n   ", end=" ")
    print(f"{GREEN}{txt_status}{ENDC}")
    print("\n\n   ", end=" ")
    print(f"[{as_string}]\n\n")

    for word in as_answers:  # Display Player Answers
        print(f"{BOLD}{BLACK}  * {ENDC}", end=" ")
        print(f"{RED}{BOLD}{word}{ENDC}")


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
