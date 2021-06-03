from noms.client.main import SearchResults
import noms
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
from noms.objects.food import NewMeal
from noms.objects.diary import Diary

client = noms.Client("aOcV0EPxHSAA0bBdFB6b6smqiThjul1LLgiHIDGf")

    
search_results = None
meal_list = []
diary = Diary()
gui = tk.Tk()

query = tk.StringVar(gui)
selection = tk.StringVar(gui)
amount = tk.StringVar(gui)

gui.geometry('1200x800')
gui.title("Noms Calculator")

mainLabel = tk.Label(gui, text = "Find your food:")
mainLabel.grid(column=1, row=1, padx=10, pady=10)

inputfield = tk.Entry(gui, textvariable = query, width = 40)

inputfield.grid(column=1, row = 2, padx=10, pady=10)

searchButton = tk.Button(gui, height = 1,
                 width = 5, 
                 text ="Search",
                 command = lambda:foodInput())
searchButton.grid(column=2,row=2)

comboBox = ttk.Combobox(gui, textvariable = "None", width = 50)
comboBox.grid(column = 1, row = 3) 

        
amountLabel = tk.Label(gui, text = "No food item currently selected")
amountLabel.grid(column=1, row=10, padx=10, pady=10)

numfield = tk.Entry(gui, textvariable = amount, width = 10)
numfield.grid(column=1, row = 11, padx=10, pady=10)

submitButton = tk.Button(gui, height = 1,
                 width = 5, 
                 text ="Submit",
                 command = lambda:submitRequest())
submitButton.grid(column=2,row=12)




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
    #TODO this is not pulling from search_results the overall variable
    
    new_food_data = client.get_foods({str(search_results.json["items"][comboBox.current()]["fdcId"]):int(amount.get())})
            
    new_meal = NewMeal(new_food_data, amount.get())
    new_meal.show_nutrients()
    
    diary.addMeal(new_meal)
    
def save():
    if tk.messagebox.askokcancel("Quit", "Do you want to save?"):
        out_file = open("meals.json", "w")
    
        json.dump(diary.days, out_file, indent = 6)
    
        out_file.close()
        gui.destroy()
        

comboBox.bind("<<ComboboxSelected>>", chooseOption)


gui.protocol("WM_DELETE_WINDOW", save)
gui.mainloop()
    


    # #TODO improper closure in json
        #how to save the files properly and cleanly
        #how to read back in
    
    
    #Respond to the 
    


# nutrients = client.get_foods({'167755':100})
# print(nutrients.name())

# [{'value': 7.65, 'name': 'Protein', 'unit': 'g', 'nutrient_id': 203.0}, {'value': 29.66, 'name': 'Fat', 'unit': 'g', 'nutrient_id': 204.0}, {'value': 59.4, 'name': 'Carbs', 'unit': 'g', 'nutrient_id': 205.0}, {'value': 535.0, 
# 'name': 'Calories', 'unit': 'kcal', 'nutrient_id': 208.0}, {'value': 1.5, 'name': 'Water', 'unit': 'g', 'nutrient_id': 255.0}, {'value': 20.0, 'name': 'Caffeine', 'unit': 'mg', 'nutrient_id': 262.0}, {'value': 205.0, 'name': 'Theobromine', 'unit': 'mg', 'nutrient_id': 263.0}, {'value': 51.5, 'name': 'Sugar', 'unit': 'g', 'nutrient_id': 269.0}, {'value': 3.4, 'name': 'Fiber', 'unit': 'g', 'nutrient_id': 291.0}, {'value': 189.0, 'name': 'Calcium', 'unit': 'mg', 'nutrient_id': 301.0}, {'value': 2.35, 'name': 'Iron', 'unit': 'mg', 'nutrient_id': 303.0}, {'value': 63.0, 'name': 'Magnesium', 'unit': 'mg', 'nutrient_id': 304.0}, {'value': 208.0, 'name': 'Phosphorus', 'unit': 'mg', 'nutrient_id': 305.0}, {'value': 372.0, 'name': 'Potassium', 'unit': 'mg', 'nutrient_id': 306.0}, {'value': 79.0, 'name': 'Sodium', 'unit': 'mg', 'nutrient_id': 307.0}, {'value': 2.3, 'name': 'Zinc', 'unit': 'mg', 'nutrient_id': 309.0}, {'value': 0.491, 'name': 'Copper', 'unit': 'mg', 'nutrient_id': 312.0}, {'nutrient_id': 313, 'name': 'Fluoride', 'group': 'Minerals', 'unit': 'µg', 'value': 0.0}, {'nutrient_id': 315, 'name': 'Manganese', 'group': 'Minerals', 'unit': 'mg', 'value': 0.0}, {'value': 4.5, 'name': 'Selenium', 'unit': 'µg', 'nutrient_id': 317.0}, {'nutrient_id': 318, 'name': 'Vitamin A', 'group': 'Vitamins', 'unit': 'IU', 'value': 0.0}, {'value': 0.51, 'name': 'Vitamin E', 'unit': 'mg', 'nutrient_id': 323.0}, {'nutrient_id': 324, 'name': 'Vitamin D', 'group': 'Vitamins', 'unit': 'IU', 'value': 0.0}, {'value': 0.0, 'name': 'Vitamin C', 'unit': 'mg', 'nutrient_id': 401.0}, {'value': 0.112, 'name': 'Vitamin B-1', 'unit': 'mg', 'nutrient_id': 404.0}, {'value': 0.298, 'name': 'Vitamin B-2', 'unit': 'mg', 'nutrient_id': 405.0}, {'value': 0.386, 'name': 'Vitamin B-3', 'unit': 'mg', 'nutrient_id': 406.0}, {'nutrient_id': 410, 'name': 'Vitamin B-5', 'group': 'Vitamins', 'unit': 'mg', 'value': 0.0}, {'value': 0.036, 'name': 'Vitamin B-6', 'unit': 'mg', 'nutrient_id': 415.0}, {'value': 12.0, 'name': 'Vitamin B-9', 'unit': 'µg', 'nutrient_id': 417.0}, {'value': 0.75, 'name': 'Vitamin B-12', 'unit': 'µg', 'nutrient_id': 418.0}, {'value': 46.1, 'name': 'Choline', 'unit': 'mg', 'nutrient_id': 421.0}, {'value': 5.7, 'name': 'Vitamin K', 'unit': 'µg', 'nutrient_id': 430.0}, {'value': 23.0, 'name': 'Cholesterol', 'unit': 'mg', 'nutrient_id': 601.0}, {'nutrient_id': 605, 'name': 'Trans Fat', 'group': 'Lipids', 'unit': 'g', 'value': 0.0}, {'value': 18.509, 'name': 'Saturated Fat', 
# 'unit': 'g', 'nutrient_id': 606.0}, {'value': 0.0, 'name': 'DHA', 'unit': 'g', 'nutrient_id': 621.0}, {'value': 0.0, 'name': 'EPA', 'unit': 'g', 'nutrient_id': 629.0}, {'value': 7.186, 'name': 'Monounsaturated Fat', 'unit': 'g', 'nutrient_id': 645.0}, {'value': 1.376, 'name': 'Polyunsaturated Fat', 'unit': 'g', 'nutrient_id': 646.0}, {'nutrient_id': 851, 'name': 'ALA', 'group': 'Lipids', 'unit': 'g', 'value': 0.0}]


# while query != "Exit":

#     query =  input("Find your food: ")

#     search_results = client.search_query(query)
    
#     if search_results.json:
#         values = []
#         for result in search_results.json["items"]:
#             values += [result["description"]]
        
#         mainLabel = tk.Label(gui, text = "Food results")
        
#         num_query =  int(input("Select result: "))
#         #switch to TKINTER Combobox

#         if num_query in range(1,len(search_results.json["items"])+1):
#             #TODO handle exceptions better    
#             selected_item = search_results.get_result(num_query)
            
#             value_query = input("How much? (in grams): ")
            
#             #TODO
#             #Why is this API call so slow
#             #Returns list of food objects
            
#             new_food_data = client.get_foods({str(selected_item["fdcId"]):int(value_query)})
            
#             new_meal = NewMeal(new_food_data, value_query)
#             new_meal.show_nutrients()
            
#             diary.addMeal(new_meal)

#         else:
#             print("Invalid result, returning to selection.")
    