#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet

def hangman(name):
        
    from randomwordgenerator import randomwordgenerator as rw
    word_of_the_game = rw.generate_random_words()    # generates a random English word
        
    word = word_of_the_game
    
    meaning = wordnet.synsets(word_of_the_game)     # gets the meaning of the input word to assist user
    print("\n")
    if meaning:
        print("Definition of your word: {}".format(meaning[0].definition()))
        print("\n")
    else:
        x = hangman(name)
        if x == 'Done':
            return 'finished'
        
    guess_counter = 0  # keeps a count of the number of guesses so far

    #  creating an empty string with blanks to keep track of the letters correctly guessed
    blank_word = []
    length = int(len(word_of_the_game))
    for i in range(0, length):
        blank_word.append("_")
    print(blank_word)
    print("\n")

    # looping till the user gets the word right or he has used up all his guesses

    while guess_counter <= 7:
        print("\n")
        print("Guesses Left - {}".format(7 - guess_counter))
        x = input("Take a guess: ")    # gets a guess letter from the user
        flag = word_of_the_game.find(x)     # finds the index position of the first occurence of the letter if it exists
        if flag >= 0:
            while flag >= 0:
                #blank_word_list = list(blank_word)
                blank_word[flag] = x        # replacing the position of the correctly found letter in the blank word
                if word_of_the_game.count(x) == 1:
                    print(blank_word)
                word_of_the_game = word_of_the_game.replace(x, '_', 1)  # replace it in original input string
                flag = word_of_the_game.find(x)     # recursive call in case more than one occurence of a letter is there
        else:
            guess_counter = guess_counter + 1      # if not found, increase the guess count

        if guess_counter == 7:      # if guess count reaches 7, exit the loop
            break
        if word_of_the_game.count("_") == len(word_of_the_game):    # if all letters are found, exit the loop
            break

    if guess_counter == 7:
        print("\n")
        print('The word was {}'.format(word))
        print("{} lost! Please try again".format(name))
        print("\n")
        choice = input("Do you want to play again? Yes/No ")
        if(choice == 'Yes'):
            y = hangman(name)
        return "Done"
        
    elif len(blank_word) == len(word_of_the_game) and guess_counter != 7:
        print("\n")
        print("{} wins!!".format(name))
        print(blank_word)
        print("\n")
        choice = input("Do you want to play again? Yes/No ")
        if(choice == 'Yes'):
            y = hangman(name)
        return "Done"

print("\n")

print("A Recreation of the classic Hangman Game")

print("\nRules of  the game")
print("__________________")
print("\n")
print("1. A hidden word of n letters and definition of the word is given. Player has to find out the word.")
print("2. Player has to guess the letters in the word.")
print("3. He is allowed to make upto 7 wrong guesses.")
print("4. Game ends when he finds out the word/ he makes more than 7 wrong guesses")

print("\n")

name = input("Enter your name ")
y = hangman(name)

