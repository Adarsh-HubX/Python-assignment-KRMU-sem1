# Task 1: Setup & Introduction:
'''
Daily Calorie Tracker CLI
Name: Adarsh Rathore
Date: 10 October 2025
Project Title: Building a Calorie Tracking Console App
'''

print("---------------------------------------------")
print(" Welcome to the Daily Calorie Tracker CLI 🍽️")
print("---------------------------------------------")
print("\nThis tool helps you log your meals and track your daily calorie intake. In this tool you can:\n"
" - Add meals with calorie values.\n" 
" - View your total calories intake for the day.\n" 
" - Compare against your personal daily limit.\n" 
" - Save your session for future reference.")


# Task 2: Input & Data Collection:
# Taking User info for calculating Calories Limit
user_name = input("\nEnter your name: ")                
age = int(input("Enter your age: "))
gender = input("Enter gender(M/F): ")
weight = float(input("Enter weight(kg): "))
height = float(input("Enter height(cm): "))
activity = float(input("Enter activity factor(1.2=sedentary, 1.375=light, 1.55=moderate, 1.725=very, 1.9=extra): "))

if gender == "M":
    bmr = 10*weight + 6.25*height - 5*age + 5
else:
    bmr = 10*weight + 6.25*height - 5*age - 161

daily_limit = round(bmr*activity)
print(f"\nDaily Calorie limit is: {daily_limit} kcal")

# Empty lists to store meals and calories
meals = []
calories = []
# Asking user for how many meals they want to enter
num_meals = int(input("How many meals do you want to log today?: "))
# Loop to collect meal names and their calorie values
for i in range(num_meals):
    meal_name = input(f"\nEnter the name of meal {i+1}: ")
    calorie_amount = float(input(f"Enter the calorie amount for {meal_name}: ")) #Convert to float
    meals.append(meal_name) # Add meal name to list
    calories.append(calorie_amount) # Add calorie amount to list
# Print the collected data
print("\nMeals logged:", meals)
print("Calories logged:", calories)

if len(calories) == 0:
    print("No meals logged. Total calories consumed today: 0 Kcal")
# Task 3: Calorie Calculation:
# Calculate total calories
else:
    total_calories = sum(calories)
# Average calories per meal
average_calories = total_calories / len(calories)
# Display total and average calories
print(f"\nTotal calories consumed today: {total_calories} kcal")
print(f"Average calories per meal: {average_calories:.2f} kcal") # rounded to 2 decimal places


# Task 4: Exceed Limit Warning system:
if total_calories > daily_limit:
    print("Warning: You have exceeded your daily calorie limit!")
elif total_calories < daily_limit:
    print("Good job! You are within your daily calorie limit.")
else:
    print("You have exactly met your daily calorie limit.")


# Task 5: Neatly Formatted Output:
print("\n=======================================")
print("           Daily Calorie Summary       ")
print("=======================================")
print("Meal Name\t\tCalories (kcal)")
print("---------------------------------------")

# Print each meal with its calories
for meal, cal in zip(meals, calories):
    print(f"{meal}\t\t\t{cal}")

# Print total and average calories
print("---------------------------------------")
print(f"Total Calories:\t\t{total_calories}")
print(f"Average Calories\t{average_calories:.2f}")
print("=======================================")


# Task 6: Save Session Log to File (Beginner-Friendly)
import datetime
import os

# Folder for saving logs
folder_name = "daily_calorie_tracker"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Take user's name
# Ask if user wants to save the report
save_choice = input("Do you want to save this session report to a file? (yes/no): ").lower()

if save_choice == "yes":
    # Current timestamp for unique filename
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"{user_name}_sample_output.txt"  # unique filename with user name

    # Full file path
    filepath = os.path.join(folder_name, filename)

    # Write session report to file
    with open(filepath, "w") as file:
        file.write("Daily Calorie Tracker Report\n")
        file.write(f"User: {user_name}\n")
        file.write(f"Date & Time: {now}\n\n")
        file.write("Meal Name\tCalories (kcal)\n")
        file.write("--------------------------------\n")
        for meal, cal in zip(meals, calories):
            file.write(f"{meal}\t{cal}\n")
        file.write("--------------------------------\n")
        file.write(f"Total Calories:\t{total_calories}\n")
        file.write(f"Average Calories:\t{average_calories:.2f}\n")

        # Limit status
        if total_calories > daily_limit:
            file.write("Status: Exceeded daily calorie limit!\n")
        elif total_calories < daily_limit:
            file.write("Status: Within daily calorie limit.\n")
        else:
            file.write("Status: Exactly met daily calorie limit.\n")

    print(f"Session report saved successfully as '{filepath}'")
else:
    print("Session report was not saved.")
