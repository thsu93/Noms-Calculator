from noms.client.main import SearchResults
import noms
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
from noms.objects.food import NewMeal
from noms.objects.diary import Diary

#TODO

#more robust display of nutritional data
#Rounding on values
#Clean up presentation of table
#Should use "Always Contain" values (Cal, Fat,s, Chol, Sod, Carbs, Prot, Vit ACDE) 
# and then Sometimes (if above % RDA? what metric)


#Remove repetitions on calculations, storage, etc. due to reuse/rejigger of code

#read in results from JSONs for expansion of existing diaries, etc.

    


client = noms.Client("aOcV0EPxHSAA0bBdFB6b6smqiThjul1LLgiHIDGf")

search_results = None
diary = Diary()

gui = tk.Tk()
gui.geometry('1200x800')
gui.title("Noms Calculator")


query = tk.StringVar(gui)
selection = tk.StringVar(gui)
amount = tk.StringVar(gui)


mainLabel = tk.Label(gui, text = "Find your food:")
mainLabel.grid(column=1, row=1, padx=10, pady=10)

inputfield = tk.Entry(gui, textvariable = query, width = 50)
inputfield.grid(column=1, row = 2, padx=10, pady=10)

searchButton = tk.Button(gui, height = 1,
                 width = 5, 
                 text ="Search",
                 command = lambda:foodInput())
searchButton.grid(column=2,row=2)

comboBox = ttk.Combobox(gui, textvariable = "None", width = 50)
comboBox.grid(column = 1, row = 3) 

amountLabel = tk.Label(gui, text = "No food item currently selected", justify=tk.LEFT)
amountLabel.grid(column=1, row=10, padx=10, pady=10)

numfield = tk.Entry(gui, textvariable = amount, width = 10)
numfield.grid(column=1, row = 11, padx=10, pady=10)

submitButton = tk.Button(gui, height = 1,
                 width = 5, 
                 text ="Submit",
                 command = lambda:submitRequest())
submitButton.grid(column=2,row=12)

foodsLabel = tk.Label(gui, text="No foods entered yet", width =50, height = 30,
                      justify = tk.LEFT,
                      wraplength=300)
foodsLabel.grid(column=1, row=1, padx=10, pady=10)

nutrientsLabel = tk.Label(gui, text="No foods entered yet", width =50, height = 30, 
                          justify= tk.LEFT,
                          wraplength=300)
nutrientsLabel.grid(column=3, row=1, padx=10, pady=10)


def chooseOption(event):
    print("OPTION CHOSEN " + comboBox.get())
    amountLabel["text"] = "How much of " + comboBox.get() + "? (in grams):"


def foodInput():
    print("Searching for " + query.get())
    
    global search_results
    search_results = client.search_query(query.get())
    
    if not search_results.json:
        return
    
    values = []
    for result in search_results.json["items"]:
        print(result["description"])
        values += [result["description"]]
    
    comboBox["values"] = values
    
    comboBox.current(0)
    
    query.set("")    
    
    
def submitRequest():    
    new_food_data = client.get_foods({str(search_results.json["items"][comboBox.current()]["fdcId"]):int(amount.get())})
            
    new_meal = NewMeal(new_food_data, int(amount.get()))
    new_meal.show_nutrients()
    
    diary.addMeal(new_meal)
    
    meals = ""
    for meal in list(new_meal.food_dict):
        meals += meal + ", " + str(new_meal.food_dict[meal]) + "gs \n"
    
    foodsLabel["text"] = meals
    nutrientsLabel["text"] = diary.printNutrients()
    
def save():
    if tk.messagebox.askokcancel("Quit", "Do you want to save?"):
        out_file = open("meals.json", "w")
    
        json.dump(diary.days, out_file, indent = 6)
    
        out_file.close()
    gui.destroy()

comboBox.bind("<<ComboboxSelected>>", chooseOption)

gui.protocol("WM_DELETE_WINDOW", save)
gui.mainloop()
    
