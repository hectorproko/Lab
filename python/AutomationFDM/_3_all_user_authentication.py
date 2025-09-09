import csv
import re
import os

def load_csv(file_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        log_content = f.read()
    return log_content

def identify_human(log_content):
    human_users = set()
    previous_line = ""
    
    lines = [line.strip() for line in log_content.splitlines()]

    for line in lines:
        #print(line)  # Debug: Print each line to see its content
        #if line.startswith("Security ID:") and "FDM1" in line and "WIN-" not in line:
        if line.startswith("Account Name:") and "@FDM1.LOCAL" in line and "WIN-" not in line:
            #print(line)
            parts = line.split(":", 1)
            #print(parts)
            username = parts[1].strip()
            #print(username)
            name = username.split("@")[0]  # Extract the name before the domain
            #print(name)
            human_users.add(name)
    
    return sorted(human_users)

def tokenize_events(log_content):
    # Split on known event delimiter
    events_list = log_content.split("Audit Success,")
    return events_list

def successful_logins(events_list, human_users):
    users_success_login = set()
    for event in events_list:
        # Check if this is a successful logon event
        if "An account was successfully logged on" in event and "4624" in event:
            lines = event.splitlines()
            for line in lines:
                #print(line)
                line = line.strip()
                #print(line)
                #print(human_users)
                for name in human_users:
                    if name in line:
                        users_success_login.add(name)

    return users_success_login

#########################


if __name__ == "__main__": #avoid execution when imported
    log_content = load_csv('Win_Evt_Logs.csv')
    human_users = identify_human(log_content)
    #print(str(human_users))
    events_list = tokenize_events(log_content)
    #print(str(len(events_list)))
    print("Users with successful logins:")
    print(successful_logins(events_list, human_users))


# print(type(tokenize_events))

#print(identify_human(log_content))

