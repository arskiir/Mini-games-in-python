import random
import time
import os
from random_word import RandomWords
import numpy as np
import getpass
import webbrowser as web
import requests as req


def known_problems():
    """
    1. 4 in a row is under developing
    """


# do not forget to manually add new game's info into this function which acts as database
def game_info() -> dict:
    return {
        '1': ('Guess the Number', guess_number),
        '2': ('Roll a dice', roll_dice),
        '3': ('Confusing Stories', confusing_stories),
        '4': ('Rock Paper Scissors', rock_paper_scissors),
        '5': ('Hangman (requires internet connection)', hangman),
        '6': ('4 In A Row', four_in_a_row),
    }


# Every game function --------------------------------------------------------------------------------------------------

def four_in_a_row():
    print("Welcome to 4 In A Row!\n")

    # print rules
    print(
        'Rules:\n'
        "\t2 players have to take turns to choose a column to drop a coin\n"
        "\tIf whose every 4 coins align in a horizontal, diagonal or vertical line, that player wins.\n"
    )

    # table creation
    row = 6
    column = 7
    numpy_table = np.zeros((row, column), int)
    columns = [str(i + 1) for i in range(column)]
    stack_limit = column

    # game start
    print(f'columns = {columns}')
    player1_column_history = []
    player2_column_history = []
    index = 1
    player_order = (1, 2)
    players = {
        1: (player1_column_history, "1"),
        2: (player2_column_history, "2")
    }
    filled_elements = (1, 2)
    while True:

        # print table for players to see
        table_to_print = ''
        for row_to_print in numpy_table:
            table_to_print += '        |'
            for each_element in row_to_print:
                table_to_print += f' {each_element} |'
            table_to_print += '\n'
        table_to_print += f'column:   {"   ".join(columns)}'
        print(f'{table_to_print}\n')

        # coin drop
        if index == 0:
            index = 1
        else:
            index = 0
        # get player decision
        while True:
            player_choose_column = input(f'Player {player_order[index]} chooses column: ')
            if player_choose_column not in columns:
                print(f'Possible columns are {" ".join(columns)} only!\n')
            else:
                break
        players[index + 1][0].append(player_choose_column)
        print(f'player 1 {player1_column_history}')
        print(f'player 2 {player2_column_history}')
        # drop in numpy_table
        row_to_replace = row - 1
        target = numpy_table[row_to_replace][int(player_choose_column) - 1]
        while True:
            if target == 0:
                numpy_table[row_to_replace][int(player_choose_column) - 1] = players[index + 1][1]
                break
            else:
                row_to_replace -= 1
                target = numpy_table[row_to_replace][int(player_choose_column)]

        print(numpy_table)


def hangman():
    print("Welcome to Hangman!")

    word_generator = RandomWords()
    number_of_words = 10

    a = '---> word length ='
    difficulty = {
        '1': (f'easy {a} 5 or 6', random.randint(5, 6)),
        '2': (f'normal {a} 7, 8 or 9', random.randint(7, 9)),
        '3': (f'hard {a} 10 or more', None),
        '4': (f'random {a} between 5 and 10', random.randint(5, 10),)
    }
    print('\nDifficulty levels: ')
    for key, value in sorted(difficulty.items()):
        print(f'{key}: {value[0]}')

    # input filter
    while True:
        chosen_difficulty = input("Choose difficulty: ")
        if chosen_difficulty not in difficulty.keys():
            print(f'\nChoose {", ".join(difficulty.keys())} only!')
        else:
            break

    # hint at final guess with 30% chance
    hint_active = False
    if random.randint(1, 10) in {1, 2}:
        hint_active = True

    # words selection
    word_length = difficulty.get(chosen_difficulty, random.randint(5, 10))[1]
    while True:
        clear_console()
        print("\nGathering words... (If this takes too long, check your internet connection.)")
        random_words = ''
        try:
            if word_length is not None:
                random_words = word_generator.get_random_words(
                    limit=number_of_words, minLength=word_length, maxLength=word_length
                )
            else:
                random_words = word_generator.get_random_words(
                    limit=number_of_words, minLength=9
                )
        except:
            print("\nConnection error detected.\nHangman needs stable internet connection.\nPlease try again later.\n")
            input("Enter to continue...")
            clear_console()
            main()

        random_words = [word.lower() for word in random_words]
        # filter any word which contains non-alphabetical out
        for word in random_words:
            remove = False
            for alphabet in word:
                if not 'a' <= alphabet <= 'z':
                    remove = True
            if remove:
                random_words.remove(word)

        print(f'The word is one of these: \n\n\t{", ".join(random_words)}\n')
        decision = input("Random a new word set ---> Enter 'x'\n"
                         "             To start ---> Press Enter!\n"
                         "(x, Enter)? : ")
        if decision != 'x':
            break
    clear_console()
    print(f'\nThe mysterious word is among these: \n\n\t{", ".join(random_words)}\n')

    full_body = {
        'hanger': '_________________\n'
                  '                |\n'
                  '                |',
        'head': '              (T_T)',
        'neck': '                |',
        'arms': '              \ | / \n'
                '               \|/ ',
        'body': '                |\n'
                '                |',
        'legs': '               / \ \n'
                '              /   \ ',
        'feet': '            __     __'
    }
    hang_order = ('hanger', 'head', 'neck', 'arms', 'body', 'legs', 'feet')

    mysterious_word = random_words[random.randint(0, len(random_words)-1)]
    mysterious_word_to_report = mysterious_word[:]
    mysterious_word = list(mysterious_word)
    length = len(mysterious_word)
    blank_spaces = list('_' * length)
    guess_limit = len(full_body.keys())
    alphabets = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split()
    you_have_guessed = []
    body = []

    # inform word's info
    print(f'This mysterious word has {length} characters.\nYou have {guess_limit} guesses.\n')
    input('Press Enter to continue...')

    # main game sequence
    hang_order_index = 0
    while True:

        clear_console()
        if guess_limit != 1:
            print(f"{guess_limit} guesses left.")
        else:
            print("DECISIVE GUESS...")
            if hint_active:
                print(f'HINT!!! (20% chance)\nThe word is one of these: \n\n\t{", ".join(random_words)}\n')
                hint_active = False
        print(f"You haven't guessed: {' '.join(alphabets)}")
        if you_have_guessed:
            print(f"You have guessed: {' '.join(you_have_guessed)}")
        print(f'\n\t\t\t\t{" ".join(blank_spaces)}')
        # body printing
        for body_part in body:
            print(body_part)

        # check whether win or lose
        if set(mysterious_word) == {''}:
            print(f"\nCongratulations! YOU WIN!!!.\nThe mysterious word is indeed '{mysterious_word_to_report}'.\n")
        else:
            if guess_limit == 0:
                print(f"\nYOU LOSE!!!\nThe mysterious word is {mysterious_word_to_report}.\n")
        if set(mysterious_word) == {''} or guess_limit == 0:
            while True:
                see_translation = input(f"Do you want to see translation in Thai for '{mysterious_word_to_report}'?\n"
                                        "(y, n)?: ").strip().lower()
                if see_translation not in 'yn':
                    print("Enter y or n.\n")
                else:
                    print()
                    break
            if see_translation == 'y':
                web.open(
                    f'https://translate.google.com/#view=home&op=translate&sl=en&tl=th&text={mysterious_word_to_report}'
                )
            break

        # guess check
        while True:
            guess = input("Your guess: ").strip().lower()
            if not 'a' <= guess <= 'z':
                print('You can guess an alphabet only!')
            else:
                if len(guess) > 1:
                    print('One character only!')
                else:
                    if guess in you_have_guessed:
                        print(f'You have already guessed "{guess}"')
                    else:
                        break

        # game mechanism
        you_have_guessed.append(guess)
        if guess in mysterious_word:
            # reform mysterious_word and black_spaces
            new_mysterious_word = []
            new_black_spaces = blank_spaces.copy()
            for index, char in enumerate(mysterious_word):
                if guess == char:
                    new_mysterious_word.append("")
                    new_black_spaces[index] = guess
                else:
                    new_mysterious_word.append(char)
                    if guess not in you_have_guessed:
                        new_black_spaces[index] = '_'
            mysterious_word = new_mysterious_word
            blank_spaces = new_black_spaces

            alphabets.remove(guess)
        else:
            alphabets.remove(guess)
            guess_limit -= 1
            body.append(full_body[hang_order[hang_order_index]])
            hang_order_index += 1


def rock_paper_scissors():
    print("Welcome to Rock Paper Scissors!")

    rock = 'rock'
    paper = 'paper'
    scissors = 'scissors'
    possibilities = {'1': rock, '2': paper, '3': scissors}

    print('Choose "x" to return to game selection.\n')
    while True:
        inform = ''
        for key, value in sorted(possibilities.items()):
            inform += f'{key} = {value}\t'
        print(inform + ' ----------> x to stop')

        # input filter
        while True:
            you_choose = input('You choose: ').strip()
            if you_choose == 'x':
                break
            if you_choose not in possibilities.keys():
                print('Choose 1, 2 or 3.\n')
            else:
                clear_console()
                break
        if you_choose == 'x':
            break

        you_choose = possibilities[f'{you_choose}']
        computer_chooses = possibilities[f'{random.randint(1, 3)}']

        win = 'YOU WIN!'
        lose = 'YOU LOSE!'
        draw = 'DRAW!!!'
        report = f'You: {you_choose} VS Computer: {computer_chooses} ---> '
        if you_choose == computer_chooses:
            report += draw
        else:
            if you_choose == rock:
                if computer_chooses == paper:
                    report += lose
                else:
                    report += win
            elif you_choose == paper:
                if computer_chooses == scissors:
                    report += lose
                else:
                    report += win
            else:
                if computer_chooses == rock:
                    report += lose
                else:
                    report += win

        report += '\n'
        print(report)


def confusing_stories():
    print("Welcome to Confusing Stories!")

    # stories = {
    #            key: (
    #                  title,
    #                  number of required words,
    #                  required word types,
    #                  story
    #                  )
    #            }
    # Each '@' is meant to be replaced with a word that is a user input
    stories = {
        '1': (
            'Spring Cartoon!',
            10,
            'noun/s, adj, noun, noun/s, noun/s, noun, type of food, noun/s, noun, adjective',
            'Planting a vegetable garden is not only fun, it also helps save @. You will need a piece of @ '
            'land. You may need a @ to keep the @ and @ out. As soon as @ is here you can go out there with '
            'your @ and plant all kinds of @. Then in a few months, you will have corn on the @ and big, @ '
            'flowers.'
        ),
        '2': (
            'Trip to the Park!',
            14,
            'person, adj, adj, noun, adj, noun, adj, adj, verb, verb, person, verb, adj, verb',
            'Yesterday, @ and I went to the park. On our way to the @ park, we saw a @ @ on out bike. '
            'We also saw big @ balloons tied to a @. Once we got to the @ park, the sky turned @. '
            'It started to @ and @. @ and I @ all the way home. Tomorrow we will try to go to the @ '
            'park again and hope it does not @.'
        ),
        '3': (
            'Easter Hunt!',
            11,
            'adj, person, animal, plural noun, plural noun, noun, verb, noun, animal, adj, adj',
            "Today we get to hunt for @ eggs in @'s yard. The Easter @ hid them for us to find! "
            "I am hoping that there will be a basket full of @ and @. Since it's spring, there's lots of "
            "@ on the ground. When I @ through it, I hope it doesn't get on my @. I love that "
            "the Easter @ hides things for us. It makes the @ day so very @!!"
        ),
        '4': (
            'Chocolate Bunny!',
            12,
            "nouns, integer, adj, noun, a game, adj, color, liquid, noun, nouns, noun, adj",
            "Schools are closed at Easter time and all the @ get @ weeks off. The @ teachers also"
            " get a vacation. There are a lot of things to ddo on Easter vacation. Some kids hang "
            "around and watch the @. Others go outside and play @. Little kids will color @ eggs. "
            "They use a package of @ dye. They pour it in a bowl full of @. Then they dip the @ in "
            "the bowl and then rinse it off. After the @ are dried, you place them in the Easter @ "
            "along with a @ chocolate bunny!"
        )
    }

    # inform about stories
    print('\nAll available stories:')
    for key, value in sorted(stories.items()):
        print(f'{key}: {value[0]}  {value[1]} words are required.')

    # get and check input
    decision = ''
    while decision not in stories.keys():
        decision = input('\nEnter a story number: ').strip()
        if decision not in stories.keys():
            print('-----> Invalid story number.')

    # main game sequence
    clear_console()
    title, num, types, story = stories[decision]
    required_words = types.split(', ')
    user_input = []

    print(f'\n{title}')

    invalid_value = ['./,;"(|}{[]<>):', "'-=_+%$#@!^&*"]
    for i, each in enumerate(required_words, 1):
        # input filter
        chosen_word = ''
        invalid = True
        while invalid:
            identified_invalid = set()
            chosen_word = input(f'{i}/{num} Enter {each}: ').strip()
            if chosen_word == '':
                print("Enter a word!\n")
            else:
                for char in chosen_word:
                    if char in invalid_value[0] or char in invalid_value[1]:
                        identified_invalid.add(char)
                if len(identified_invalid) == 0:
                    invalid = False
                else:
                    print(f"Invalid input. Special digits '{', '.join(identified_invalid)}' are not allowed!\n")

        user_input.append(chosen_word)

    add = range(1, len(story))
    story_list = story.split('@')
    for index, word in enumerate(user_input):
        story_list.insert(index + add[index], f'"{word}"')
    completed_story = ''.join(story_list)

    clear_console()
    print(f'\nHere is your confusing story!\n')
    # print line with proper length
    proper_length = 80
    line = ''
    escape_char = '#'
    completed_story += escape_char
    count = 0
    for letter in completed_story:
        if count <= proper_length:
            line += letter
            count += 1
            if letter == escape_char:
                print(f'\t{line[:-1].strip()}\n')
        else:
            if letter == ' ':
                count = 0
                print(f'\t{line.strip()}')
                line = ''
            else:
                line += letter


def roll_dice():
    print("Welcome to Roll Dice!")

    print('\nEnter now to roll 6-sided dice.\nEnter "x" to quit.\nOr enter an integer to make a custom dice\n')
    while True:
        decision = input("(Enter, integer >= 6)?: ").strip().lower()
        if decision == 'x':
            break
        elif decision == "":
            print(f'6-sided dice --------------------> {random.randint(1, 6)}')
        else:
            # check for integer
            incorrect = True
            while incorrect:
                try:
                    decision = int(decision)
                    if decision < 6:
                        raise ValueError
                    incorrect = False
                except ValueError:
                    print("The number of sides has to be >= 6.")
                    decision = input("Enter a desired integer of sides: ").strip()

            print(f'{decision}-sided dice -------------------> {random.randint(1, decision)}')


def guess_number():
    print('Welcome to Guess the Number!')

    lower = 1
    upper = 100
    mysterious_number = random.randint(lower, upper)
    limit = 7
    print(f'\nYou have {limit} available guesses.')
    print(f'The mysterious number is an integer between {lower} and {upper}.\n')

    count = 1
    guess = upper + 1
    while guess != mysterious_number and count <= limit:
        try:
            guess = int(input(f'Your guess #{count}/{limit}: '))
            if guess < mysterious_number:
                print(f"{guess} is less than the number")
            elif guess > mysterious_number:
                print(f'{guess} is more than the number')
            else:
                break
            count += 1
        except ValueError:
            print('\nYou need to input an integer!')

    if count < limit:
        print("\nCongratulations, you win!")
    else:
        if guess == mysterious_number:
            print("\nCongratulations, you win!")
        else:
            print("\nYou LOSE!")
    print(f'The mysterious number is {mysterious_number}.\n')


# Not game functions ---------------------------------------------------------------------------------------------------

def replay(game_function):
    # Games that don't need to be replayed or can be replayed by its own game function are in exception list.
    exception = [roll_dice, rock_paper_scissors]
    if game_function in exception:
        return

    final_decision = input("Enter ---> replay.\n"
                           "Enter 'x' ---> return to game selection.\n"
                           "(Enter, x)?: ").strip().lower()
    if final_decision == "":
        clear_console()
        game_function()


def clear_console():
    os.system('cls')


def get_input(all_games: dict) -> str:
    # get and check decision
    decision = ''
    while decision not in all_games.keys():
        decision = input("Enter a game number: ").strip()
        if decision == 'x':
            return decision
        if decision not in all_games.keys():
            print("-----> Invalid game number\n")
    return decision


def print_intro(all_games: dict):
    print("\nAll available games:")
    for num, (title, function) in sorted(all_games.items()):
        print(f'{num}: {title}')
    print('Enter "x" to exit.\n')


# main structure -------------------------------------------------------------------------------------------------------

def main():
    # all_games = {key: (game title, game function)}
    all_games = game_info()

    while True:

        print_intro(all_games)
        decision = get_input(all_games)
        if decision == 'x':
            break

        # call the selected game function
        clear_console()
        while True:
            game_function = all_games[decision][1]
            game_function()

            # replay?
            exception = [roll_dice, rock_paper_scissors]
            if game_function in exception:
                break
            final_decision = input("Enter ---> replay.\n"
                                   "Enter 'x' ---> return to game selection.\n"
                                   "(Enter, x)?: ").strip().lower()
            if final_decision != '':
                break

        clear_console()

    # quit entire program
    print("\nThank you for playing!\nSee you next time. xd")
    time.sleep(5)


main()
