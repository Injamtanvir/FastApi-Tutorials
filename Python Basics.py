# InjamTanvir(INJAM UL HAQUE)

# The print() Function is used to display output to the console.
print("Hello World!" )


# The input() function is used to take input from the user.
inp = input("Enter your name: ")
print(type(inp)) # The type() function is used to check the data type of a variable. In this case, it will return <class 'str'> because the input always returns as string.
print("Hello " + inp + "! Welcome to the program.")

# conditional statements(If/elif/else) are used to perform different actions based on different conditions.
inp_number = int(input("Enter a number: ")) # The int() function is used to convert the input string to an integer.
if (inp_number % 2 == 0):       # The % operator is used to find the remainder of a division operation. If the remainder is 0, then the number is even.
    print("Even")
else:
    print("Odd")


# List 
my_list = [1, 2, 3, 4, 5] # A list is a collection of items that are ordered and changeable. In this case, the list contains integers.
print(my_list) # This will print the entire list.




# Dictionary
my_dict = {"name": "Injam", "age": 22, "city": "Dhaka"} # A dictionary is a collection of key-value pairs. In this case, the dictionary contains information about a person.
print(my_dict) # This will print the entire dictionary.


# Fuction
