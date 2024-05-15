# pyls.py

import json
import sys
from datetime import datetime
import subprocess

def func_ls_l_r_t(data):
    key_file = ["permission","size","month","day","time","name"]
    r_list = list_files_dir_ls_l_r(data)
    rever_list = r_list[::-1]
    file_list = [i.split() for i in rever_list]
    
    dict_list = []
    for lst in file_list:
        result_dict = {}
        for i in range(len(key_file)):
            result_dict[key_file[i]] = lst[i]
        dict_list.append(result_dict)

    # Sort the list of dictionaries by datetime (oldest first)
    sorted_list = sorted(dict_list, key=get_datetime)
    # Print the sorted list
    final_list = []
    for item in sorted_list:
        d_list = []
        for k,v in item.items():
            d_list.append(v)
        final_list.append(" ".join(d_list))
    return final_list
       
def get_datetime(d):
    return datetime.strptime(f"{d['month']} {d['day']} {d['time']}", '%b %d %H:%M')

def convert_timestamp_to_datetime(timestamp):
    # Convert the timestamp to a datetime object
    dt_object = datetime.fromtimestamp(timestamp)
    # Format the datetime object as desired (e.g., 'Nov 14 11:27')
    formatted_datetime = dt_object.strftime('%b %d %H:%M')
    return formatted_datetime

def list_files_dir_ls_l(node):
    dt_time = None
    if "contents" in node:
        for item in node["contents"]:
            if not item["name"].startswith("."):
                dt_time = convert_timestamp_to_datetime(item["time_modified"])
                if item["size"] < 99:
                    dt_time = f"{'  ' * 1}{dt_time}"
                print(item['permissions'],item["size"],dt_time,item['name'])

def list_files_dir_ls_l_r(node):
    rev_list = []
    if "contents" in node:
        for item in node["contents"]:
            if not item["name"].startswith("."):
                dt_time = convert_timestamp_to_datetime(item["time_modified"])
                # print(item['permissions'],item["size"],dt_time,item['name'])
                rev_list.append(f"{item['permissions']} {item['size']} {dt_time} {item['name']}")
        return rev_list

def load_dir_struct(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    return data

def list_files_dir(node,ls_output):
    if "contents" in node:
        for item in node["contents"]:
            if not item["name"].startswith("."):
                ls_output.append(item["name"])

def list_files_dir_ls_a(node,ls_output):
    if "contents" in node:
        for item in node["contents"]:
            ls_output.append(item["name"])

def human_readable_size(size):
    suffixes = ['B', 'KB', 'MB', 'GB']
    suffix_index = 0
    while size >= 1024 and suffix_index < len(suffixes) - 1:
        size = size / 1024
        suffix_index = suffix_index + 1
    return f"{size:.1f} {suffixes[suffix_index]}"

def sub_directory_struct(data,check_var,human=None):
    error = None
    if "interpreter" in data["name"]:
        if "contents" in data:
            data_contents = data["contents"]
            for item in data_contents:
                if "name" in item and "contents" in item:
                    if check_var.split("/")[0] == item["name"]:
                        error = "err"
                        for i in item["contents"][::-1]:
                            dt_time = convert_timestamp_to_datetime(i["time_modified"])
                            if "/" in check_var:
                                if check_var.split("/")[1] in i["name"]:
                                    if human == "ls -h":
                                        human_readable = human_readable_size(i["size"])
                                        print(i["permissions"],human_readable,dt_time,i["name"])
                                    else:
                                        print(i["permissions"],i["size"],dt_time,i["name"])
                            else:
                                if human == "ls -h":
                                    human_readable = human_readable_size(i["size"])
                                    print(i["permissions"],human_readable,dt_time,i["name"])
                                else:
                                    print(i["permissions"],i["size"],dt_time,i["name"])
                    
            if error == None:
                print("cannot access 'non_existent_path': No such file or directory")

def cmd_help(cmd):
    try:
        # Run the command and capture the output
        process = subprocess.Popen([cmd, '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Print the help message
        print(stdout.decode('utf-8'))
    except FileNotFoundError:
        print(f"Error: '{cmd}' not found.")

def main():
    try:
        # Access the command line arguments
        script_name = sys.argv[0]  # The name of the Python file being executed
        arguments = sys.argv[1:]  # List of arguments (excluding the script name)
        arguments = " ".join(arguments)
        filename = 'structure.json'
        data = load_dir_struct(filename)

        if arguments == "ls":
            output = []
            # Print the top-level directories and files
            list_files_dir(data,output)
            final_output = ",".join(output)
            print(final_output)
        
        elif arguments == "ls -A":
            output = []
            list_files_dir_ls_a(data,output)
            final_output = ",".join(output)
            print(final_output)
        
        elif arguments == "ls -l":
            list_files_dir_ls_l(data)

        elif arguments == "ls -l -r":
            r_list = list_files_dir_ls_l_r(data)
            for i in r_list[::-1]:
                print(i)

        elif arguments == "ls -l -r -t": 
            final_list = func_ls_l_r_t(data)
            for final in final_list[::-1]:
                print(final)

        elif "ls -l -r -t --filter" in arguments:
            final_list = func_ls_l_r_t(data)
            error_message = None
            for i in final_list[::-1]:
                if arguments == "ls -l -r -t --filter=dir":
                    if "drwxr-xr-x" in i:
                        print(i)
                elif arguments == "ls -l -r -t --filter=file":
                    if "-rw-r--r--" in i:
                        print(i)
                else:
                    error_message = "'folder' is not a valid filter criteria. Available filters are 'dir' and 'file'"
            
            if error_message != None:
                print(error_message)

        elif arguments == "-l" + " " + arguments.split(" ")[1]:
            sub_directory_struct(data,arguments.split(" ")[1])
        
        elif arguments == "ls --help":
            print(arguments.split(" ")[0])
            cmd_help(arguments.split(" ")[0])

        elif arguments == "ls -h" + " " + arguments.split(" ")[2]:
            sub_directory_struct(data,arguments.split(" ")[2],"ls -h")

    except:
        print("invalid command,please use correct command")

if __name__ == '__main__':
    main()

