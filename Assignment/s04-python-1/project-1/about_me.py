"""Session 04 project 1: about me, a profile made of variables (topics 1-3: variables, data types, operators).

Uses ONLY what session 04 teaches before collections: variables, the basic data types (str, int,
float, bool, None), type() and id(), and simple operators, plus print().

- Your details are variables at the top: change them and run the program again
- type() shows the data type of each variable
- Arithmetic works out your age in months and days, your height in cm and your BMI
- Text works with operators too: + joins strings and * repeats them
- Comparisons and and / or / not give True or False answers, such as "Can vote?"
- None means "no value", and `is None` checks for it

There's no input() yet (session 05), so nothing is typed in. There's also no if / else and no
lists (collections are topic 4). So the program runs straight from top to bottom, and the yes / no
answers are printed as True or False.

Run it with:
    python Assignment/s04-python-1/project-1/about_me.py
"""

# ---- Your details. Change these values and run the program again. ----
first_name = "Bala"     # str: text, inside quotes
last_name = "Kumar"
age = 21                # int: a whole number
height_m = 1.75         # float: a number with a decimal point
weight_kg = 68.5
is_student = True       # bool: True or False, with a capital first letter
is_citizen = True
nickname = None         # None: no value. This person has no nickname

CURRENT_YEAR = 2026
LINE = "=" * 50         # * repeats a string: 50 "=" signs

print(LINE)
print("STEP 1: VARIABLES AND THEIR DATA TYPES")
print(LINE)
print("first_name =", first_name, type(first_name))
print("last_name  =", last_name, type(last_name))
print("age        =", age, type(age))
print("height_m   =", height_m, type(height_m))
print("weight_kg  =", weight_kg, type(weight_kg))
print("is_student =", is_student, type(is_student))
print("is_citizen =", is_citizen, type(is_citizen))
print("nickname   =", nickname, type(nickname))

print()
print(LINE)
print("STEP 2: NUMBERS (arithmetic operators)")
print(LINE)
age_in_months = age * 12
age_in_days = age * 365            # about: leap years add a few more days
birth_year = CURRENT_YEAR - age    # about: it depends on whether your birthday has passed this year
decades = age // 10                # // divides and rounds down: whole decades only
extra_years = age % 10             # % gives what's left over
height_cm = height_m * 100         # a float times an int gives a float
bmi = weight_kg / height_m ** 2    # ** runs before /, so this is weight / (height * height)

print("Age in months:", age_in_months)
print("Age in days (about):", age_in_days)
print("Born in (about):", birth_year)
print("Age in decades:", decades, "decades and", extra_years, "years")
print("Height in cm:", height_cm)
print("BMI:", bmi, "<- weight_kg / height_m ** 2: ** runs first, and / always gives a float")
print("(weight_kg / height_m) ** 2 would be", (weight_kg / height_m) ** 2, "<- brackets change the order")

print()
print(LINE)
print("STEP 3: TEXT (+ and * on strings)")
print(LINE)
full_name = first_name + " " + last_name   # + joins strings
number = 21
text = "21"                                # the quotes make it a str, even though it looks like a number

print("Full name:", full_name)
print("number + number =", number + number, "<- adds")
print("text + text     =", text + text, "<- joins")
print("text * 3        =", text * 3, "<- repeats")
# first_name + age would be an error: Python won't join a str and an int. print() shows values
# of any type side by side when you separate them with commas, so this program uses commas.

print()
print(LINE)
print("STEP 4: YES OR NO (comparison and logical operators)")
print(LINE)
is_adult = age >= 18
is_teenager = age >= 13 and age <= 19
can_vote = is_adult and is_citizen
gets_student_discount = is_student and age < 25
pays_full_price = not gets_student_discount
healthy_bmi = bmi >= 18.5 and bmi < 25
yes_count = is_adult + can_vote + gets_student_discount + healthy_bmi   # True counts as 1, False as 0

print("Adult (18 or older)?  ", is_adult)
print("Teenager (13 to 19)?  ", is_teenager)
print("Can vote?             ", can_vote)
print("Student discount?     ", gets_student_discount, "(students under 25)")
print("Pays full price?      ", pays_full_price)
print("Healthy BMI (18.5-25)?", healthy_bmi)
print("Yes answers to adult, vote, discount and BMI:", yes_count, "out of 4")

print()
print(LINE)
print("STEP 5: NONE, AND CHANGING A VARIABLE")
print(LINE)
has_nickname = nickname is not None   # check for None with is, not ==
print("Has a nickname?", has_nickname)

id_before = id(age)
age = age + 1      # a birthday! An int can't change, so Python makes a new int and age points to it
print("After a birthday, age is", age)
print("Same object as before?", id(age) == id_before, "<- ints are immutable, so the id changed")
