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

#Restructure Diary, etc. file structure to be more sensible
#Rebuild to be able to remove/add food for days

#read in results from JSONs for expansion of existing diaries, etc.



client = noms.Client("aOcV0EPxHSAA0bBdFB6b6smqiThjul1LLgiHIDGf")

search_results = None
diary = Diary()

gui = tk.Tk()
gui.geometry('1200x800')
gui.title("Noms Calorie Calculator and Food Diary")


query = tk.StringVar(gui)
selection = tk.StringVar(gui)
amount = tk.StringVar(gui)

#Search Descriptor
searchfieldLabel = tk.Label(gui, text = "Find your food:")
searchfieldLabel.grid(column=1, row=1, padx=10, pady=10)

#Search Field
searchField = tk.Entry(gui, textvariable = query, width = 50)
searchField.grid(column=1, row = 2, padx=10, pady=10)

#Search Button
searchButton = tk.Button(gui, height = 1,
                 width = 5, 
                 text ="Search",
                 command = lambda:foodInput())
searchButton.grid(column=2,row=2)

#Searched items box
searchResultsBox = ttk.Combobox(gui, textvariable = "None", width = 50)
searchResultsBox.grid(column = 1, row = 3) 

#Label above amount selector
amountLabel = tk.Label(gui, text = "No food item currently selected", justify=tk.LEFT)
amountLabel.grid(column=1, row=10, padx=10, pady=10)

#Input field for amount of searched ingredient
amountField = tk.Entry(gui, textvariable = amount, width = 10)
amountField.grid(column=1, row = 11, padx=10, pady=10)

#Button to submit amount of food
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
    print("OPTION CHOSEN " + searchResultsBox.get())
    amountLabel["text"] = "How much of " + searchResultsBox.get() + "? (in grams):"


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
    
    searchResultsBox["values"] = values
    
    searchResultsBox.current(0)
    amountLabel["text"] = "How much of " + searchResultsBox.get() + "? (in grams):"
    
    query.set("")
    
    
def submitRequest():    
    new_food_data = client.get_foods({str(search_results.json["items"][searchResultsBox.current()]["fdcId"]):int(amount.get())})
            
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

searchResultsBox.bind("<<ComboboxSelected>>", chooseOption)

gui.protocol("WM_DELETE_WINDOW", save)
gui.mainloop()
    
