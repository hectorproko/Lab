from _3_all_user_authentication import load_csv, tokenize_events


def failed_logins(events_list):

    for event in events_list:
        # Check if this is a successful logon event
        if "Auditing,4771" in event:
            #print(f"\033[96m{'#' * 120}\033[0m")
            lines = event.splitlines()
            print(lines[0])
            #for line in lines:
                #if "Account Name:" in line:
                    #print(line)


def main():
    log_content = load_csv('Win_Evt_Logs.csv')
    events_list = tokenize_events(log_content)
    failed_logins(events_list)

if __name__ == "__main__":
    main()
