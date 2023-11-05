import pandas as pd
import random as random
from time import sleep

class Jeopardy:
    def __init__(self, csv_name):
        self.csv_name = csv_name
        self.df = self.read_csv()
        self.current_round = 0
        self.money_made = 0.0
        self.question_index = 0
        self.question_index_list = []

        self.streak = 0
        self.stats = {
            "High Score": 0,
            "Most Money" : 0.0
        }

        
    def read_csv(self):
        csv = pd.read_csv(self.csv_name)
        csv = csv.rename(columns=lambda x: x.replace(" ", ""))
        # Clean the "Value" column and try to convert to float
        def convert_value(value):
            try:
                value = value.replace("$", "").replace(",", "").strip()  # Remove "$" and commas
                return float(value) if value != "None" else 0
            except (ValueError, AttributeError):
                return 0  # Handle conversion errors

        csv["Value"] = csv["Value"].apply(convert_value)
        return csv

    def gen_index_df(self):
        self.question_index = random.randint(1, len(self.df))
        return self.question_index

    #Will need a question handler which pulls the question from the df, adds the index to the list.
    #Gets the answer, category and value from the df.
    #Will need to return the values and use that in a response handler method.

    def handle_question(self):
        while True:
            self.question_index = self.gen_index_df()
            df = self.df.iloc[self.question_index - 1]
            question = df["Question"]
            answer = df["Answer"]
            value = df["Value"]
            category = df["Category"]
            jep_val = df["Round"]
            if self.question_index in self.question_index_list:
                continue
            else:
                print(answer)
                print(self.question_index_list)
                self.current_round += 1
                print(f"Round {self.current_round}")
                user_response = input(question)
                
                if user_response.capitalize() == answer.capitalize():
                    print("Correct!")
                    print(f"You have earned ${value}")
                    self.question_index_list.append(self.question_index)
                    self.money_made += value
                    #New question
                else:
                    print("Incorrect!")
                    self.question_index_list.append(self.question_index)
                    if self.current_round > self.stats["High Score"]:
                        self.stats["High Score"] = self.current_round
                    if self.money_made >= self.stats["Most Money"]:
                        self.stats["Most Money"] = self.money_made
                    #Reset the game
                    print("Game over!")
                    break
    
    def reset_game(self):
        self.current_round = 0
        self.money_made = 0.0
        self.question_index = 0
        

    def start_game(self):
        self.reset_game()
        print("Welcome to Jeopardy! You will be given a question and you will have to answer it correctly to build your money")
        if self.question_index == 0:
            countdown = 5
            while countdown >= 0:
                print("Get ready to play Jeapordy! The game will start in {} seconds".format(countdown))   
                countdown -= 1
                sleep(1)
            self.handle_question()



    



Jep_Quiz_1 = Jeopardy("jeopardy.csv")


# print(Jep_Quiz_1.get_question_item())
Jep_Quiz_1.start_game()

print(Jep_Quiz_1.stats)




