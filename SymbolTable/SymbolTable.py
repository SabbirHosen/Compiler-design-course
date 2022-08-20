import os

hash_table_size = 10


def clear():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


# Creating the Hash Table
hash_table = [[] for _ in range(hash_table_size)]


# Function to display hash_table
def display_hash():
    for i in range(len(hash_table)):
        print(i, end=" ")

        for j in hash_table[i]:
            print(j, end=" ")

        print()


# Hashing Function to return
# key for every value.
def hashing(name):
    return (sum((ord(x.lower()) - 97) for x in name)) % len(hash_table)


# Insert Function to add
# values to the hash table
def insert(name, type):
    hash_key = hashing(name=name)
    data_exist = False
    for s_name, s_type in hash_table[hash_key]:
        if name == s_name and type == s_type:
            data_exist = True
            break
    if data_exist:
        print(f"{name} --> Symbol or Name is exist in the table!!")
    else:
        hash_table[hash_key].append((name, type))
        print(f"{name} --> Added successfully in the table!!")


# Search function to find the element using name/symbol
def search(name):
    hash_key = hashing(name=name)
    if hash_table[hash_key]:
        flag = False
        for s_name, s_type in hash_table[hash_key]:
            if s_name == name:
                print(f'Name: {s_name} Type: {s_type}')
                flag = True
        if not flag:
            print(f"{name} --> Symbol or Name is not found in the table!!")

    else:
        print(f"{name} --> Symbol or Name is not found in the table!!")


# Delete items from the symbol table
def delete(name):
    hash_key = hashing(name=name)
    if hash_table[hash_key]:
        flag = False
        for s_name, s_type in hash_table[hash_key]:
            if s_name == name:
                hash_table[hash_key].remove((s_name, s_type))
                flag = True
        if not flag:
            print(f"{name} --> Symbol or Name is not found in the table!!")

    else:
        print(f"{name} --> Symbol or Name is not found in the table!!")


# Update the item in the symbol table
def update(name, type):
    hash_key = hashing(name=name)
    if hash_table[hash_key]:
        flag = False
        # temp = hash_table[hash_key]
        for i in range(len(hash_table[hash_key])):
            if hash_table[hash_key][i][0] == name:
                del hash_table[hash_key][i]
                hash_table[hash_key].insert(i, (name, type))
                flag = True
        if not flag:
            print(f"{name} --> Symbol or Name is not found in the table!!")

    else:
        print(f"{name} --> Symbol or Name is not found in the table!!")


if __name__ == '__main__':
    ex = True
    while ex:
        try:
            print('List of the Action: ')
            print('1:   Insert')
            print('2:   Search')
            print('3:   Delete')
            print('4:   Show')
            print('5:   Update')
            print('6:   Get Hash Value')
            print('7:   Exit')
            m = int(input("Enter the action number: "))
            if m == 1:
                name, type = input("Enter the name/symbol and type with space separate: ").split(' ', maxsplit=1)
                insert(name, type)
                print(f'Name: {name} & Type: {type} successfully added.')
            elif m == 2:
                name = input("Enter a name/ symbol to search: ")
                search(name)
            elif m == 3:
                name = input("Enter a name/ symbol to delete from the symbol table: ")
                delete(name)
            elif m == 4:
                print('-' * 100)
                print('Symbol Table')
                display_hash()
                print('-' * 100, end='\n')
            elif m == 5:
                name, new_type = input(
                    "Enter the name/symbol and new type value with space separate for update: ").split(' ', maxsplit=1)
                update(name, new_type)
            elif m == 6:
                name = input("Enter a name/ symbol to get hash value: ")
                h = hashing(name)
                print(f'{h} is the hash value of {name}')
            elif m == 7:
                ex = False
            else:
                print('Invalid Action....')
        except:
            print('Invalid Action....')
