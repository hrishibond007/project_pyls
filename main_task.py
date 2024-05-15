import json
list_count = 0
length = 0
count = 0
def print_directory_structure(data, indent=0):
    global count
    global list_count
    global length
    if 'name' in data:
        # Print the current directory or file name
        # print('  ' * indent + data['name'], data['permissions'])
        if count == 0:
            print(f"{'  ' * indent}{data['name']}")
            count = count + 1
        else:
            if "name" in data and "contents" in data:
                print(f"|--{'  ' * indent}{data['name']}")
                list_count = list_count + 1
                length = len(data['contents'])
            else:
                if list_count > 0:
                    if length == 0:
                        print(f"|--{'  ' * indent}{data['name']}")
                        list_count = 0
                    else:
                        print(f"|   |--{'  ' * 1}{data['name']}")
                        length = length - 1
                else:
                    print(f"|--{'  ' * indent}{data['name']}")
                            
    if 'contents' in data:
        # Recursively print the contents of subdirectories
        for item in data['contents']:
            print_directory_structure(item, indent + 1)

def main():
    # Read the JSON file
    with open('structure.json', 'r') as file:
        json_data = json.load(file)

    # Print the directory structure
    print_directory_structure(json_data)

if __name__ == '__main__':
    main()

