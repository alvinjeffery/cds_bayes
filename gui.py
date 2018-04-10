from tkinter import Tk, Label, Button, Entry, StringVar, IntVar, END, W, E
import re

def parse(txt):
    """
    separate text entry by commas and note whether positive or negative
    """
    try:
        # eliminate white space throughout string
        # separate by commas into list
        txt_list = [x.strip() for x in txt.split(',')]

        ### add positive/negative designation here? 
        
        return txt_list

    except:
        return "Unable to parse."

def map_mx_id(txt_list):
    """
    Map each text item of a list to its unique MX identifier
    """
    try:
        return empty_var
    except:
        return txt_list


class BayesGUI:
    def __init__(self, master):
        self.master = master
        master.title("Bayes' Rule for Differential Diagnosis")

        # instructions
        self.label = Label(master, text="Enter manifestations below with\n\
        positive findings preceded by a plus sign (+)\n\
        and pertinent negative findings preceded by a minus sign (-).")
        self.label.pack()

        # text entry box
        self.txt = Entry(master, width=150)
        self.txt.pack()

        # execute core functionality
        self.greet_button = Button(master, 
                                   text="$Provide Differential Diagnosis List", 
                                   command=self.rank_order)
        self.greet_button.pack()

        # display differential list
        self.diagnoses = "No data entered"
        self.differential_list_text = StringVar()
        self.differential_list_text.set(self.diagnoses)
        self.differential_list = Label(master, textvariable=self.differential_list_text)
        self.differential_list.pack()

        # quit program
        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()


    def rank_order(self):
        ### here is where we can replace with our CDS function
        ### to return a string (with line breaks '\n') with an 
        ### ordered list of diagnoses
        
        mx_list = parse(self.txt.get())
        mx_list_id = map_mx_id(mx_list)

        self.differential_list_text.set(mx_list_id)


root = Tk()
my_gui = BayesGUI(root)
root.mainloop()