from tkinter import Tk, Label, Button, Entry, StringVar, IntVar, END, W, E
import re
import pandas as pd

# read data from file
df = pd.read_csv('DxMxLR.csv', index_col=0)

def parse(txt):
    """
    separate text entry by commas and note whether positive or negative
    """
    try:
        # eliminate white space throughout string
        # ensure all upper case
        # separate by commas into list
        txt_list = [x.strip().upper() for x in txt.split(',')]
        return txt_list

    except:
        return "Unable to parse."


def make_diff(Mx_list, simple_output=True):
    """
    Creates differential diagnosis list, ranked in descending order of post-test probability.
    Originally authored by Sarah
    Input: list of manifestations
    Output: list of strings in descending order 
    """
    #Mx_list = ['+HEPATOMEGALY PRESENT', '-JAUNDICE FAMILY HX', '-ABDOMEN PAIN COLICKY']
    Dx_list = pd.DataFrame(columns=['Rank', 'Dx', 'Score', 'Importance_List'])
    Dx_list['Dx']=pd.Series((list(set(df['Dx Name']))))
    Dx_list['Importance_List']=pd.Series( [ [] for i in range(10) ])

    for i,r in Dx_list.iterrows():
        #r['Dx'] = disease
        #print(r['Dx'])
        score = 1
        for mx in Mx_list: 
            if re.match('[+]', mx): 
                mx = mx.strip('+')
                q = df.loc[df['Dx Name'] == r['Dx']]
                q = q.loc[df['Mx Name'] == mx]
                im = q['Import'].values
                if im > 4:
                    Dx_list.loc[i, 'Dx'] = str(Dx_list.loc[i, 'Dx'] + '*')
                p = q['LR (+)'].values
                #print(p)
                if p.size == 0: continue #don't count NAs
                else:
                    score = score * p
                    Dx_list.loc[i,'Importance_List'].append(float(im))
            elif re.match('[-]', mx): 
                mx = mx.strip('-')
                s = df.loc[df['Dx Name'] == r['Dx']]
                s = s.loc[df['Mx Name'] == mx]
                im = s['Import'].values
                #if im > 4:
                #    Dx_list.loc[i, 'Dx'] = str(Dx_list.loc[i, 'Dx'] + '*')
                m = s['LR (-)'].values
                #print(m)
                if m.size == 0: continue #don't count NAs
                else: 
                    score = score * m
                    Dx_list.loc[i,'Importance_List'].append(float(im))
            else: 
                #print("Mx ", mx, "is not positive or negative. Please indicate presence or absence of mx.")
                return "Mx " + str(mx) +  " is not positive or negative. Please indicate presence or absence of mx."
        if not Dx_list.loc[i,'Importance_List']: 
            Dx_list.loc[i, 'Score'] = 0
        else:
            Dx_list.loc[i, 'Score'] = float(score)

    Dx_list = Dx_list.sort_values(by="Score", ascending= False)

    rank = 1
    for i,r in Dx_list.iterrows():
        Dx_list.loc[i, 'Rank'] = rank
        rank = rank + 1
    Dx_list.set_index('Rank', inplace=True)
    
    # for production, only list diagnoses (i.e., not scores & other info used in testing)
    if simple_output:
        # coerce from pandas series to list
        # and attach a line break for readability
        return '\n'.join(map(str, Dx_list['Dx'].tolist()))
            
    return Dx_list


class BayesGUI:
    def __init__(self, master):
        self.master = master
        master.title("Bayes' Rule for Differential Diagnosis")

        # instructions
        self.label = Label(master, text="Enter manifestations below with\n\
        positive findings preceded by a plus sign (+)\n\
        and pertinent negative findings preceded by a minus sign (-).")
        self.label.config(font=("Courier", 24))
        self.label.pack()

        # text entry box
        self.txt = Entry(master, width=150)
        self.txt.config(font=("Courier", 24))
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
        self.differential_list.config(font=("Courier", 24))
        self.differential_list.pack()

        # quit program
        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()


    def rank_order(self):        
        mx_list = parse(self.txt.get())
        dx_diff = make_diff(mx_list)
        
        self.differential_list_text.set(dx_diff)


root = Tk()
my_gui = BayesGUI(root)
root.mainloop()