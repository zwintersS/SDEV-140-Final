# Authors: Zechariah Winters, Sam Horak
# Course: SDEV 140
# Date Started: 11/04/2024
# Date Finished: 12/11/2024
# Assignemt: Final Project
# Purpose: Allow the user to create decks of flash cards so they can practice or test their knowledge on them

# imports
import random
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog


# Classes
#Flashcards are kept in a tuple consisting of a question and answer
class Flashcard:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def to_dict(self):
        return {"question": self.question, "answer": self.answer}

    @classmethod
    def from_dict(cls, data):
        return cls(data["question"], data["answer"])

    #Decks have a name and contain a list of flashcards. 
class Deck:
    def __init__(self, name):
        self.name = name
        self.flashcards = []

    def add_flashcard(self,question,answer):
        self.flashcards.append(Flashcard(question, answer))

    def to_dict(self):
        return {"name": self.name, "flashcards": [flashcard.to_dict() for flashcard in self.flashcards]}

    @classmethod
    def from_dict(cls, data):
        deck = cls(data["name"])
        deck.flashcards = [Flashcard.from_dict(fc) for fc in data["flashcards"]]
        return deck

    #The main class that runs the whole program
class FlashcardApp:
    def __init__(self,root):
        # Initilizing the GUI
        self.root = root
        self.root.title("Flash Flow V0.1")
        #Getting a dictioary of decks and loading them (if any) from the JSON file
        self.decks = {}
        self.load_decks()
        #Creating the Menu frames
        self.main_menu = tk.Frame(self.root)
        self.deck_manager_menu = tk.Frame(self.root)
        self.practice_frame = tk.Frame(self.root)
        self.test_frame = tk.Frame(self.root)
        
        #Goes through every frame created and hides them all in the top left corner of the main application window until they are called on to be displayed
        for frame in (self.main_menu, self.deck_manager_menu, self.practice_frame, self.test_frame):
            frame.grid(row=0, column=0, sticky="nsew")
        
        #Calling the menu setup functions
        self.setup_main_menu()
        self.setup_deck_manager_menu()
        self.setup_practice_frame()
        self.setup_test_frame()

        #Displyaing the Main Menu
        self.show_frame(self.main_menu)

        #Displayes frames when they are called on
    def show_frame(self, frame):
        frame.tkraise()

        #Main Menu GUI
    def setup_main_menu(self):
        tk.Label(self.main_menu, text="Welcome to FlashFlow").pack(pady=20)
        tk.Button(self.main_menu, text = "Deck Manager", command=lambda: self.show_frame(self.deck_manager_menu)).pack(pady=10)
        tk.Button(self.main_menu, text = "Practice Mode", command=lambda: self.show_frame(self.practice_frame)).pack(pady=10)
        tk.Button(self.main_menu, text = "Test Mode", command=lambda: self.show_frame(self.test_frame)).pack(pady=10)
        tk.Button(self.main_menu, text= "Quit", command=self.quit_app).pack(pady=10)
       
        #Deck Manager GUI
    def setup_deck_manager_menu(self):
        tk.Label(self.deck_manager_menu, text="Deck Manager").pack(pady=20)
        self.deck_listbox = tk.Listbox(self.deck_manager_menu, width=50)
        self.deck_listbox.pack(pady=10)
        tk.Button (self.deck_manager_menu, text= "Create Deck", command=self.create_deck).pack(pady=10)
        tk.Button (self.deck_manager_menu, text= "Delete Deck", command=self.remove_deck).pack(pady=10)
        tk.Button(self.deck_manager_menu, text = "Add Flashcard", command=self.add_flashcard).pack(pady=10)
        tk.Button(self.deck_manager_menu, text = "Back to Main Menu", command=lambda: self.show_frame(self.main_menu)).pack(pady=10)
        self.update_deck_listbox()

        #Practice Mode GUI
    def setup_practice_frame(self):
        self.practice_label = tk.Label(self.practice_frame, text="Practice Mode. Select A Deck")
        self.practice_listbox = tk.Listbox(self.practice_frame, width=50)
        self.practice_listbox.pack(pady=10)
        self.practice_label.pack(pady=20)
        self.practice_start_button= tk.Button(self.practice_frame, text="Start", command=self.start_practice)
        self.practice_start_button.pack(pady=10)
        self.show_answer_button = tk.Button(self.practice_frame, text="Show Answer", command=self.show_answer)
        self.show_answer_button.pack(pady=10)
        tk.Button(self.practice_frame, text= "Back to Main Menu", command=lambda: self.show_frame(self.main_menu)).pack(pady=10)
        self.update_practice_listbox()

        #Test Mode GUI
    def setup_test_frame(self):
        self.test_label = tk.Label(self.test_frame, text="Test Mode")
        self.test_label.pack(pady=20)
        self.test_listbox = tk.Listbox(self.test_frame, width=50)
        self.test_listbox.pack(pady=10)
        self.update_test_listbox()
        self.test_start_button = tk.Button(self.test_frame, text="Start", command=self.start_test)
        self.test_start_button.pack(pady=10)
        self.test_entry = tk.Entry(self.test_frame)
        self.test_entry.pack(pady=10)
        self.submit_button = tk.Button(self.test_frame, text="Submit", command=self.submit_test_answer)
        self.submit_button.pack(pady=10)
        tk.Button(self.test_frame, text= "Back to Main Menu", command=lambda: self.show_frame(self.main_menu)).pack(pady=10)
        
        
        #Quit app function brings a ok cancle window to doubel check with the user
    def quit_app(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.root.destroy()

            #Deck creation function
    def create_deck(self):
        deck_name = tk.simpledialog.askstring("Create Deck", "Enter Deck name:")
        
        if not deck_name: #user cancled or enter enmpty name
            messagebox.showwarning("Warning","Deck name cannot be empty")
            return

        # checking for duplicate name
        if deck_name in self.decks:
            messagebox.showerror("Error", "Deck already exists!")
            return
        
         #Creates the deck at the given name, saves the deck to the JSON file, and updates the listbox with the new deck name    
        self.decks[deck_name] = Deck(deck_name)
        self.save_decks()
        messagebox.showinfo("Success", f"Deck {deck_name} has been added to Deck List")
        self.update_deck_listbox()
        self.update_test_listbox()
        self.update_practice_listbox()
        
        
       #Saves decks to the JSON file named decks
    def save_decks(self):
        with open("decks.json", "w") as f:
            json.dump({name: deck.to_dict() for name, deck in self.decks.items()}, f)
        
            #Deletes the elected deck and updates the JSON file and listbox
    def remove_deck(self):
        selected = self.deck_listbox.get(tk.ACTIVE)
        if selected in self.decks:
            del self.decks[selected]
            self.save_decks()
            self.update_deck_listbox()
            self.update_practice_listbox()
            self.update_test_listbox()

            #Loads decks from the JSON file, if the files doesn't it excepts the error so the prgram can keep running. 
    def load_decks(self):
        try:
            with open("decks.json", 'r') as f:
                data = json.load(f)
                self.decks = {name: Deck.from_dict(deck_data) for name, deck_data in data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            self.decks = {}

            #Updates the deck list box found on the Deck manger, practice, and test menus by clearing them and adding them all back in from the JSON file
    def update_deck_listbox(self):
        self.deck_listbox.delete(0, tk.END) # Clears list box
        for deck_name in self.decks:
            self.deck_listbox.insert(tk.END, deck_name)

            #forcing listbox redraw
            self.deck_listbox.update_idletasks()
            #Adds a flashcard to the sleceted deck 
            
    def update_test_listbox(self):
        self.test_listbox.delete(0, tk.END)
        for deck_name in self.decks:
            self.test_listbox.insert(tk.END, deck_name)
            
            self.test_listbox.update_idletasks()
            
    def update_practice_listbox(self):
        self.practice_listbox.delete(0, tk.END)
        for deck_name in self.decks:
            self.practice_listbox.insert(tk.END, deck_name)
            
            self.practice_listbox.update_idletasks()
            
    def add_flashcard(self):
        #selecting a deck
        selected = self.deck_listbox.get(tk.ACTIVE)
        if not selected:
            messagebox.showwarning("Warning", "No deck selected. Please select a deck.")
            return

        if selected in self.decks:
            while True:  # Loop to keep adding flashcards
                question = tk.simpledialog.askstring("Add Flashcard", "Enter Question:")
                if question is None:  # User canceled input
                 break

                answer = tk.simpledialog.askstring("Add Flashcard", "Enter Answer:")
                if answer is None:  # User canceled input
                 break

                if question and answer:
                    self.decks[selected].add_flashcard(question, answer)
                    self.save_decks()
                    messagebox.showinfo("Success", "Flashcard added successfully!")
                else:
                    messagebox.showerror("Error", "Invalid question or answer.")

                # Ask the user if they want to add another flashcard
                add_more = messagebox.askyesno("Add Another?", "Do you want to add another flashcard?")
                if not add_more:
                    break


    # Practice Mode Functions
    def start_practice(self):
        #selecting a deck
        selceted = self.practice_listbox.get(tk.ACTIVE)
        if not selceted:
            messagebox.showwarning("Warning","No Deck Selected. Please selcet a deck")
            return
        
        if selceted in self.decks:
            self.current_deck = self.decks[selceted]

            if not self.current_deck.flashcards:
                messagebox.showwarning("Warning", "The selected deck has no flashcards")
                return
        
        #Initializing Practice Varibles
        self.practice_flashcards = self.current_deck.flashcards[:]
        random.shuffle(self.practice_flashcards)
        self.used_flashcards = set()
        
        #Showing first card
        self.show_practice_question()
        
    def show_practice_question(self):
        #checking to see if all flashcards have been shown
        if len(self.used_flashcards)>= len(self.practice_flashcards):
            messagebox.showinfo("Practice Complete", "You have completed all the flashcards in this deck.")
            self.show_frame(self.main_menu)
            return
        #Getting the Next card
        for flashcard in self.practice_flashcards:
            if flashcard not in self.used_flashcards:
                self.current_flashcard = flashcard
                break
        #Updating the Label
        self.practice_label.config(text= f"Question: {self.current_flashcard.question}")
        self.show_answer_button.config(state="normal")
        
    def show_answer(self):
        #Showing the answer of the current card
        self.practice_label.config(text= f"Answer: {self.current_flashcard.answer}")
        self.show_answer_button.config(state="disabled")
        
        #makring it as used
        self.used_flashcards.add(self.current_flashcard)
        
        #Wait then show next question
        self.root.after(2000, self.show_practice_question)


    #Test Mode Functions
    def start_test(self):
         #selecting a deck
        selceted = self.practice_listbox.get(tk.ACTIVE)
        if not selceted:
            messagebox.showwarning("Warning","No Deck Selected. Please selcet a deck")
            return
        
        if selceted in self.decks:
            self.current_deck = self.decks[selceted]

            if not self.current_deck.flashcards:
                messagebox.showwarning("Warning", "The selected deck has no flashcards")
                return
        
        #Initilizing the Test Varibles
        self.test_flashcards =self.current_deck.flashcards[:]
        random.shuffle(self.test_flashcards)
        self.total_questions = len(self.test_flashcards)
        self.correct_answers = 0
        self.incorrect_questions = []
        self.current_question_index = 0
        
        #showing the first question
        self.show_frame(self.test_frame)
        self.show_test_question()
        
    def show_test_question(self):
        #check to see if all questions have been answered
        if self.current_question_index >= self.total_questions:
            self.show_test_results()
            return
        
        #Get the current card
        flashcard = self.test_flashcards[self.current_question_index]
        self.test_label.config(text=f"Question: {flashcard.question}")
        self.test_entry.delete(0, tk.END)
        
    def submit_test_answer(self):
        #Collecting the users answers 
        user_answer = self.test_entry.get().strip()
        flashcard =self.test_flashcards[self.current_question_index]
        
        #checking the answer
        if user_answer.lower() == flashcard.answer.lower():
            self.correct_answers += 1
        else:
            self.incorrect_questions.append((flashcard.question,flashcard.answer))
            
        #moving to next question
        self.current_question_index += 1
        self.show_test_question()
        
    def show_test_results(self):
        #Calculate the grade
        grade = (self.correct_answers/self.total_questions) * 100
        
        #display results
        results_message = (
            f"Test Completed !\n"
            f"Grade: {grade:.2f}%\n"
            f"Correct Answers: {self.correct_answers}/{self.total_questions}\n"
            )
        
        if self.incorrect_questions:
            results_message += "\nQuestions you got wrong: \n"
            for question, answer in self.incorrect_questions:
                results_message += f"Question: {question}\nCorrect Answer: {answer}\n"
        else:
            results_message += "Prefect Score!"
        
        messagebox.showinfo ("Test Results", results_message)
        self.show_frame(self.main_menu)


# Start the Program
if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()

# Due to the amount of recoding that was needed we didn't have the time to add aditional features and beautify the program. We ran into several issues along the way 
# and decided to just keep it simple.     