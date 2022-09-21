# For Wordle.py use
# Class with ability to create a random word of specified length,
#   dictionary of word lengths and words,
#   check if word is valid

import requests
from collections import defaultdict
from random import randint

class word_generator:

    def __init__(self):
        pass


    def check_word(self, word: str):
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
        r = requests.get(url)
        if r.status_code == 200:
            return True
        else:
            return False

    def check_answer(self, guess: str, answer: str):
        output = []
        for i in range(len(answer)):
            if guess[i] == answer[i]:
                output.append((guess[i],"rgb(65, 126, 52)"))
            elif guess[i] in answer:
                output.append((guess[i],"rgb(190, 163, 42)"))
            else:
                output.append((guess[i],"rgb(150, 150, 150)"))
        return output


    # Call MIT library to get a list of words

    def generate_dictionary(self):
        url = "https://www.mit.edu/~ecprice/wordlist.100000"

        response = requests.get(url)
        og_word_list = response.content.splitlines()
        decoded_word_list = []
        for i in og_word_list:
            decoded_word_list.append(i.decode("utf-8"))

        num_dict = defaultdict(list)

        for i in decoded_word_list:
            num_dict[len(i)].append(i)

        return num_dict

    def generate_random_word(self, length: int, dedupe_flag: bool):

        num_dict = self.generate_dictionary()

        #fail safe limit to loops
        counter = 0
        limit = 1000

        #check validity of word
        valid_flag = False
        while valid_flag == False:
            index = randint(0,len(num_dict[length])-1)
            word = num_dict[length][index]
            valid_flag = self.check_word(word)

        valid_flag = False
        history = []

        while dedupe_flag == True and counter < limit:

            #generate a new valid word
            while valid_flag == False:
                index = randint(0,len(num_dict[length])-1)
                word = num_dict[length][index]
                valid_flag = self.check_word(word)

            valid_flag = False

            #check for duplicate letters
            used_letters = ""
            for i in word:
                if i in used_letters:
                    break
                else:
                    used_letters += i
            if used_letters == word:
                dedupe_flag = False
            counter += 1
            history.append(word)

        if counter < limit:
            return word
        else:
            print(history)
            return "Unable to find a word, please try a lower length"
