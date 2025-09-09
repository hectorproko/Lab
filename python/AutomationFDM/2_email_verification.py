import re

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.com$'
    return re.match(pattern, email) is not None

def main():
    email = input("Enter an email address: ").strip()
    if is_valid_email(email):
        print(f"{email} is a valid email")
    else:
        print(f"{email} is an invalid email")


if __name__ == "__main__":
    main()