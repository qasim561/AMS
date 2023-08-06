import login
import student
import importlib
import login
importlib.reload(login)

def main():
    if login.main():  # If login is successful
        student.main()  # Take student


def main():
    login.main()

if __name__ == "__main__":
    main()
