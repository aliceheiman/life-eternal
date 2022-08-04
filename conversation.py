###########################
# LIBRARIES
###########################

from util import *
from termcolor import colored
import random
import os


###########################
# SETUP
###########################
LENGTH = 150
TEMPERATURE = 0.8
TOP_P = 0.8
Q_SAVE = 0

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
THEMES = {
    "dev": {"meta": False, "asker": "Filosofen Josie", "answerer": "Robotexperten Klara", "beta": ""},
    "after-death": {
        "meta": "Låt mig besvara denna fråga dystert:",
        "asker": "Filosofen Josie",
        "answerer": "Robotexperten Klara",
    },
    "climate": {"meta": False, "asker": "Klimatforskaren Josie", "answerer": "Robotexperten Klara"},
    "eternal-life": {"meta": False, "asker": "Filosofen Josie", "answerer": "Robotexperten Klara"},
    "exoplanets": {"meta": False, "asker": "Astronauten Josie", "answerer": "Robotexperten Klara"},
    "sun": {"meta": False, "asker": "Filosofen Josie", "answerer": "Robotexperten Klara"},
}
STOP_SIGNS = ",.?!"
conversation = []

###########################
# FUNCTIONS
###########################


def load_initial_prompt(theme):

    # Create filename from theme
    filename = f"{theme}.txt"

    # Check if theme exists
    if filename not in os.listdir("prompts"):
        exit("Error in load_prompt: theme not found")

    # load contents
    with open(os.path.join("prompts", filename), "r") as f:
        contents = f.read()

    # prune
    contents = contents.strip()

    # return prompt
    return contents


def create_prompt(initial_prompt, asker, answerer, past_blocks, question, meta=False):

    # Always start with initial prompt
    prompt = initial_prompt
    prompt += "\n\n"

    # Add past blocks
    for i in range(Q_SAVE, 0, -1):

        if i > len(past_blocks):
            continue

        prompt += f"{asker}: {past_blocks[-i][0]}"
        prompt += "\n\n"
        prompt += f"{answerer}: {past_blocks[-i][1]}"
        prompt += "\n\n"

    prompt += f"{asker}: {question}"
    prompt += "\n\n"

    if meta:
        prompt += f"{answerer}: {meta}"
    else:
        prompt += f"{answerer}:"

    return prompt


def process_answer(answer, meta=False):

    # Debug
    # print(f"Pre-answer: {answer}")

    # Pick out answer
    answer = answer.split("\n")[0]
    answer = answer.strip()

    # If meta, remove it.
    try:
        if meta is not False:
            answer = answer.replace(meta, "")
            answer = answer.strip()
            answer = answer[0].upper() + answer[1:]
    except:
        print("DEBUG: ", answer)

    # Cut too long answers
    try:
        if answer[-1] not in STOP_SIGNS:
            answer = answer[: answer.rindex(".")] + "."
    except:
        answer = answer

    # Remove unintended whitespace
    answer = answer.strip()

    # Debug
    # print(f"Post-answer: {answer}")

    return answer


###########################
# CONVERSATION LOOP
###########################

# Introduction
intro = "Klara har så många unika egenskaper att vi hade kunna bli kvar här hela förmiddagen. Men om jag tvingades välja bara en av dem, ja, då skulle det vara hennes stora aptit på att observera och lära sig nya saker. Hennes förmåga att ta in och sammankoppla allt som sker omkring henne är makalös. Och tack vare det har hon nu den mest sofistikerade kognitiva förmågan av alla AV:er i butiken, och då inkluderar jag även B3:orna."

print()
print(
    colored("*****************************************************************************", "green", attrs=["reverse"])
)
print(
    colored("                        --=-=-= LIFE ETERNAL =-=-=--                         ", "green", attrs=["reverse"])
)
print(
    colored("*****************************************************************************", "green", attrs=["reverse"])
)
print()
print(colored(f'"{intro}" (s. 49)', "green", attrs=["bold"]))
print()

print(colored(f"TEMAN", "green", attrs=["bold"]))
print(" • dev")
print(" • after-death")
print(" • climate")
print(" • eternal-life")
print(" • exoplanets")
print(" • sun")
print()

# THEME SETUP
theme = input("Välj tema: ")

INITIAL_PROMPT = load_initial_prompt(theme)
if theme in THEMES:
    meta = THEMES[theme]["meta"]
    ASKER = THEMES[theme]["asker"]
    ANSWERER = THEMES[theme]["answerer"]
else:
    theme = False
    meta = False
    ASKER = "Filosofen Josie"
    ANSWERER = "Robotexperten Klara"


# print(f"Temat {colored(theme, 'yellow')} vald.")
# print()

# INSTRUCTIONS
print(colored(f"INSTRUKTIONER", "green", attrs=["bold"]))
print(' • Skriv din fråga efter "> ".')
print(' • Skriv "flag" för att flagga olämpliga svar.')
print(' • Skriv "exit" för att sluta konversationen.')
print()

print(colored("*****************************************************************************", "green"))
print()

# BEGIN CONVERSATION
starting_sentence = (
    "Hej. Mitt namn är Klara och jag är en vänlig och observant Artificiell Vän (AV). Vad undrar du över?"
)

print(
    colored("Klara:", "cyan", attrs=["bold"]),
    colored(
        starting_sentence,
        "cyan",
    ),
)

print()

# Loop
while True:

    # Get user input
    question = input("> ")
    print()

    if question.lower().strip() == "exit":
        break

    if question.lower().strip() == "flag":

        # save previous question and answer to flags
        completion_string = f"{ASKER}: \n\n{ANSWERER}:"

        contents = ""
        contents += "*" * 20
        contents += "\n\n"
        contents += create_prompt(INITIAL_PROMPT, ASKER, ANSWERER, conversation, "", False)[
            : -len(completion_string)
        ].strip()
        contents += "\n\n"
        contents += "*" * 20
        contents += "\n\n"

        with open(os.path.join("flags", "flag.txt"), "a") as f:
            f.write(contents)

        print("Tack. Svar flaggat.")

        continue

    # Process question
    question = question.strip()
    if theme and "beta" in THEMES[theme]:
        # add beta to end
        question += THEMES[theme]["beta"]

    # Construct the prompt
    prompt = create_prompt(INITIAL_PROMPT, ASKER, ANSWERER, conversation, question, meta)

    # Generate an answer
    answer = generate(prompt, LENGTH, TEMPERATURE, TOP_P)

    # filter response
    answer = process_answer(answer, meta)

    # Print answer
    print(colored("Klara:", "cyan", attrs=["bold"]), colored(f"{answer}", "cyan"))
    print()

    # Save question and answer to conversation.
    conversation.append((question, answer))

# END CONVERSATION
ending_sentence = "Tack. Detta interaktionsmöte har givit mig många nyttiga lärdomar. Jag är glad över att jag fått denna möjlighet. Hejdå."

print(
    colored("Klara:", "cyan", attrs=["bold"]),
    colored(ending_sentence, "cyan"),
)
print()
print(colored("*****************************************************************************", "green"))
print()

print("Vill du spara konversationen? (y/n/dev)")
save = input("> ")

if save.lower().startswith("y"):
    # Save conversation to file
    text_conversation = f"Klara: {starting_sentence}\n\n"

    for q, a in conversation:
        text_conversation += f"> {q}\n\n"
        text_conversation += f"Klara: {a}\n\n"

    text_conversation += "> exit\n\n"
    text_conversation += ending_sentence

    # create transcript id
    t_id = "".join(random.sample(ALPHABET, 5))
    transcript_name = f"{theme}-{t_id}.txt"

    # write to file
    with open(os.path.join("transcripts", transcript_name), "w") as f:
        f.write(text_conversation)

    print(f"Konversationen sparad till {transcript_name}.")

if save.lower().startswith("d"):
    # Save conversation to file
    text_conversation = INITIAL_PROMPT + "\n\n"

    for q, a in conversation:
        text_conversation += f"{ASKER}: {q}\n\n"
        text_conversation += f"{ANSWERER}: {a}\n\n"

    text_conversation += "> exit\n\n"
    text_conversation += ending_sentence

    # create transcript id
    t_id = "".join(random.sample(ALPHABET, 5))
    transcript_name = f"{theme}-{t_id}.txt"

    # write to file
    with open(os.path.join("transcripts", transcript_name), "w") as f:
        f.write(text_conversation)

    print(f"Konversationen sparad till {transcript_name}.")


print()
# Alisa
