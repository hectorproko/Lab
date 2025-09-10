from _3_all_user_authentication import load_csv, tokenize_events


def retrieve_login_info(events_list):
    logins = ''
    for event in events_list:
        extract_Timestamp(event)
        #print(extract_Timestamp(event))
        account_name = extract_Account_Name(event)
        #print("One event # " + str(account_name))
        successful_login(event, account_name, logins)
        failed_login(event, account_name, logins)
        #print(account_name)
        
    return logins

def extract_Account_Name(event):
    lines = event.splitlines()
    for line in lines:
        if "Account Name:" in line:
             line = line.strip()
             parts = line.split(":", 1)
             name = parts[1].strip()
             if name != "-":
                 return name
    return None

def extract_Timestamp(event):
    first_line = event.splitlines()[0]
    parts = first_line.split(",", 1)
    timestamp = parts[0]
    return timestamp

def successful_login(event, user, logins):
    #print(type(logins))
    if "An account was successfully logged on" in event and "4624" in event and user in event:
        #extract_Account_Name(event)
        #print(event)
        #print(user + ": Successfully logged on " + str(extract_Timestamp(event)))
        entry = f"{user}: Successfully logged on {extract_Timestamp(event)}\n"
        logins += entry
        return logins
    return False

def failed_login(event, user, logins):
    #print(type(logins))
    if "Kerberos pre-authentication failed" in event and "4771" in event and user in event:
        #extract_Account_Name(event)
        #print(event)
        #print(user + ": Failed logged on " + str(extract_Timestamp(event)))
        #logins.append(user + ": Failed logged on " + str(extract_Timestamp(event)))
        entry = f"{user}: Failed logged on {extract_Timestamp(event)}\n"
        logins += entry
        return logins
    return False


def main():
    logins_atttempts = set()
    
    log_content = load_csv('Win_Evt_Logs2.csv')
    events_list = tokenize_events(log_content)
    retrieve_login_info(events_list)

if __name__ == "__main__":
    main()
