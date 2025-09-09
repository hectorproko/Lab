from _3_all_user_authentication import load_csv, tokenize_events


def retrieve_login_info(events_list, user):
    workstations = set()
    source_ip = set()

    for event in events_list:
        # Check if this is a successful logon event
        if "An account was successfully logged on" in event and "4624" in event and user in event:
            #print(f"\033[96m{'#' * 120}\033[0m")
            lines = event.splitlines()
            for line in lines:
                #print(line)
                line = line.strip()
                #print(line)
                if "Source Network Address:" in line:
                    if "-" not in line:
                        #print(line)
                        parts = line.split(":", 1)
                        ip = parts[1].strip()
                        source_ip.add(ip)
                        #print(ip)
                        #print(type(ip))

                if "Workstation Name:" in line:
                        #print(line)
                        parts = line.split(":", 1)
                        workstation = parts[1].strip()
                        workstations.add(workstation)
                        #print(workstation)
                        #print(type(workstation))

    print("The list of ip addresses that Marie has logged in from: " + str(source_ip))
    print("The workstations that Marie has logged in from: " + str(workstations))

def main():
    user = "marie"
    log_content = load_csv('Win_Evt_Logs2.csv')
    events_list = tokenize_events(log_content)
    retrieve_login_info(events_list, user)


if __name__ == "__main__":
    main()


#Workstation Name:	-
#Source Network Address:	192.168.0.105