#Author: Zechariah Winters
#Course: SDEV 140
#Date: 11/04/2024
#Assignemt: Final Project Consle Version 1
#Purpose: Allow the user to create decks of flash cards so they can practice or test their knowledge on them

#imports
import random
import json

# Classes
class Flashcard: 
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
       
    def to_dict(self):
        return {"question": self.question, "answer": self.answer}
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["question"], data["answer"])
        
class Deck:
    def __init__(self, name):
        self.name = name
        self.flashcards = []
   
    def add_flashcard(self):
        question = input("Enter the question: ")
        answer = input("Enter the answer: ")
        self.flashcards.append(Flashcard(question, answer))
        print("Flash Card Added to Deck")
        
    def view_flashcards(self):
        #Chcking if the deck has flashcards in it
        if not self.flashcards:
            print("No flashcards in this deck.")
            return
        for i, flashcard in enumerate(self.flashcards):
            print(f"{i + 1}. Question: {flashcard.question} | Answer: {flashcard.answer}")
    
    def remove_flashcard(self):
        #Checking to see if there are flashcards to remove
        if not self.flashcards:
            print("No flashcards available to remove.")
            return
        self.view_flashcards()
        try:
            index = int(input("Enter the number of the flashcard to remove: ")) - 1
            if 0 <= index < len(self.flashcards):
                removed_flashcard = self.flashcards.pop(index)
                print(f"Removed flashcard: {removed_flashcard.question}")
            else:
                print("Invalid Selection")
        except ValueError:
            print("Please enter a valid number.")
            
    def to_dict(self):
        return {"name": self.name, "flashcards": [flashcard.to_dict() for flashcard in self.flashcards]}
    
    @classmethod
    def from_dict(cls, data):
        deck = cls(data["name"])
        deck.flashcards = [Flashcard.from_dict(fc) for fc in data["flashcards"]]
        return deck
    

class FlashcardApp:
    def __init__(self):
        #Decks are dictionaries with a list of Flashcards 
        self.decks = {}
        self.username = self.load_username()
        self.load_decks()

    def create_deck(self):
        deck_name = input("Enter the name of the new deck: ")
        #checking for duplicate name
        if deck_name in self.decks:
            print("A deck with that name already exists.")
        else:
            self.decks[deck_name] = Deck(deck_name)
            print(f"Deck '{deck_name}' created!")
            self.save_decks()

    def remove_deck(self):
        #checking to see if any decks exist
        if not self.decks:
            print("No decks available to remove.")
            return
        deck_name = input("Enter the name of the deck to remove: ")
        if deck_name in self.decks:
            del self.decks[deck_name]
            print(f"Deck '{deck_name}' removed!")
            self.save_decks()
        else:
            print("Deck not found.")

    def select_deck(self):
        if not self.decks:
            print("No decks available. Please create a deck first.")
            return None
        deck_name = input("Enter the name of the deck: ")
        if deck_name in self.decks:
            return self.decks[deck_name]
        else:
            print("Deck not found.")
            return None

    def view_decks(self):
        if not self.decks:
            print("No decks available.")
            return
        print("Available decks:")
        for deck_name in self.decks:
            print(f"- {deck_name}")

    def save_decks(self):
        with open("decks.json", "w") as f:
            json.dump({name: deck.to_dict() for name, deck in self.decks.items()}, f)
        print("Decks saved!")

    def load_decks(self):
        try:
            with open("decks.json", 'r') as f:
                data = json.load(f)
                self.decks = {name: Deck.from_dict(deck_data) for name, deck_data in data.items()}
            print("Decks loaded!")
        except (FileNotFoundError, json.JSONDecodeError):
            print("No saved decks found or file corrupted. Starting fresh.")
    
    def save_username(self):
        with open("username.json", "w") as f:
            json.dump({"username": self.username}, f)
        print("Username Saved!")
        
    def load_username(self):
        try:
            with open("username.json", 'r') as f:
                data = json.load(f)
                print(f"Welcome back to FlashFlow, {data['username']}!")
                return data["username"]
        except (FileNotFoundError, json.JSONDecodeError):
            username = input("Welcome to FlashFlow! What's your name? ")
            self.username = username
            self.save_username()
            return username
    
    #Practice Mode User slecets a deck and then the questions are presented in a random order and then the user is shown the answer when they are ready  
    def practice_mode(self):
        deck = self.select_deck()
        if not deck:
            return
        
        if not deck.flashcards:
            print("The selected deck has not flashcards.")
            return
        
        print(f"Starting Practice Mode for deck: {deck.name}")
        flashcards = deck.flashcards[:]
        random.shuffle(flashcards)
        used_flashcards = set()
        
        while len(used_flashcards) < len(deck.flashcards):
            for flashcard in flashcards:
                if flashcard in used_flashcards:
                    continue
                print(f"Question: {flashcard.question}")
                input("Press Enter to reveal the answer...")
                print(f"Answer: {flashcard.answer}")
                used_flashcards.add(flashcard)
                print()
        print("You have completed all flashcards in this deck!")
     
        
    #Test Mode the user again selects a deck and then answers the questions this is the only section that doesn't completly function as intended
    # What needs to be Done: Random card pulling, Not telling the user they are wrong until the end of the test. Currently set the way it is for testing purposes 
    # I also want to store test scores so user can see thay are learning this may be pushed to a later iteration due to time   
    def test_mode(self):
        deck = self.select_deck()
        if not deck:
            return
        
        if not deck.flashcards:
            print("The selected deck has no flashcards.")
            return
        
        print(f"Starting test mode for deck: {deck.name}")
        total_questions = len(deck.flashcards)
        correct_answers = 0
        incorrect_questions = []
        
        for flashcard in deck.flashcards:
            print(f"Question: {flashcard.question}")
            user_answer = input("Your answer: ").strip()
            if user_answer.lower() == flashcard.answer.lower():
                print("Correct!")
                correct_answers += 1
            else:
                print(f"Inccorect! The correct answer was: {flashcard.answer}")
                incorrect_questions.append((flashcard.question, flashcard.answer))
                
        #Grading
        grade = (correct_answers / total_questions) * 100
        print("\nTest Completed!")
        print(f"Grade: {grade:.2f}%")
        print(f"Correct Answers: {correct_answers}/{total_questions}")
        if incorrect_questions:
            print("\nQuestions you got wrong:")
            for question, answer in incorrect_questions:
                print(f"Question: {question} | Correct Answer: {answer}")
        else:
            print("Perfect score! Great Job")
    
            
    #Deck Management Menu
    def deck_manager_menu(self):
        while True:
            print("\n Deck Manager Menu:")
            print("1. Create Deck")
            print("2. View Decks")
            print("3. Add Flashcard to a Deck")
            print("4. View Flashcards in a Deck")
            print("5. Remove Flashcard from a Deck")
            print("6. Remove a Deck")
            print("7. Back to Main Menu")
            choice = input("Choose and option: ")
            
            if choice == "1":
                self.create_deck()
            elif choice == "2":
                self.view_decks()
            elif choice == "3":
                deck = self.select_deck()
                if deck:
                    deck.add_flashcard()
                    self.save_decks()
            elif choice == "4":
                deck = self.select_deck()
                if deck:
                    deck.view_flashcards()
            elif choice == "5":
                deck = self.select_deck()
                if deck:
                    deck.remove_flashcard()
                    self.save_decks()
            elif choice == "6":
                self.remove_deck()
            elif choice == "7":
                break
            else:
                print("Invalid option Pleas try again.")
    
                
    # Main Menu
    def run(self):
        print(f"Hello, {self.username}! Let's learn some terms!")
        while True:
            print("\n Main Menu:")
            print("1. Deck Manager")
            print("2. Practice Mode")
            print("3. Test Mode")
            print("4. Quit")
            choice = input("Choose an option: ")
            
            if choice == "1":
                self.deck_manager_menu()
            elif choice == "2":
                self.practice_mode()
            elif choice == "3":
                deck = self.test_mode()
            elif choice == "4":
                self.save_decks()
                break
            else:
                print("Invalid option. Please try again.")


# Main Function
def main():
    
    app = FlashcardApp()
    app.run()

    print(f"Goodbye, {app.username}! Thanks for using FlashFlow.")

# Start the Program
if __name__ == "__main__":
    main()





    
