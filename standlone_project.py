import os

class NameException(Exception):
    def __init__(self, message):
        self.message = message

class AgeException(Exception):
    def __init__(self, message):
        self.message = message

class Employee:
    def __init__(self):
        self.name = ""
        self.age = 0
        self.designation = ""
        self.salary = 0

    def input_data(self):
        while True:
            try:
                self.name = input("Enter name: ")
                if not self.name.isalpha():
                    raise NameException("Name must contain only alphabets.")
                break
            except NameException as e:
                print(f"Name Error: {e.message}")

        while True:
            try:
                self.age = int(input("Enter age (18-60): "))
                if self.age < 18 or self.age > 60:
                    raise AgeException("Age must be between 18 and 60.")
                break
            except AgeException as e:
                print(f"Age Error: {e.message}")
            except ValueError:
                print("Please enter a valid number for age.")

        while True:
            print("Choose designation:")
            print("1. Programmer (₹25K)")
            print("2. Manager (₹30K)")
            print("3. Tester (₹20K)")
            try:
                choice = int(input("Enter choice (1-3): "))
                if choice == 1:
                    self.designation = "Programmer"
                    self.salary = 25000
                elif choice == 2:
                    self.designation = "Manager"
                    self.salary = 30000
                elif choice == 3:
                    self.designation = "Tester"
                    self.salary = 20000
                else:
                    print("Invalid designation choice! Please try again.")
                    continue
                break
            except ValueError:
                print("Enter a valid number for designation choice.")

        with open("Emp.txt", "a") as f:
            f.write(f"{self.name},{self.age},{self.designation},{self.salary}\n")

        print("Employee is added successfully.")

    def display_all(self):
        if not os.path.exists("Emp.txt"):
            print("No employee records found.")
            return

        print("\n--- Employee Records ---")
        with open("Emp.txt", "r") as f:
            lines = f.readlines()

        if not lines:
            print("No employee data to display.")
            return

        for line in lines:
            if line.strip():
                try:
                    name, age, designation, salary = line.strip().split(",")
                    print(f"\nName: {name}")
                    print(f"Age: {age}")
                    print(f"Designation: {designation}")
                    print(f"Salary: ₹{salary}")
                except ValueError:
                    print(f"Skipping invalid line: {line.strip()}")

    def raise_salary(self):
        if not os.path.exists("Emp.txt"):
            print("No employee records to update.")
            return

        name_to_search = input("Enter employee name for raise: ").strip()
        found = False
        updated_lines = []

        with open("Emp.txt", "r") as f:
            lines = f.readlines()

        for line in lines:
            if line.strip():
                try:
                    name, age, designation, salary = line.strip().split(",")
                except ValueError:
                    updated_lines.append(line)
                    continue

                if name.lower() == name_to_search.lower() and not found:
                    found = True
                    confirm = input(f"Do you want to raise salary for {name}? (y/n): ").strip().lower()
                    if confirm != 'y':
                        print("Salary hike cancelled.")
                        updated_lines.append(line)
                        break

                    try:
                        percent = float(input("Enter hike percentage (Max 20%): "))
                        if percent > 20:
                            print("Hike more than 20% not allowed.")
                            updated_lines.append(line)
                        elif percent < 0:
                            print("Negative hike not valid.")
                            updated_lines.append(line)
                        else:
                            new_salary = float(salary) + float(salary) * (percent / 100)
                            updated_line = f"{name},{age},{designation},{new_salary:.2f}\n"
                            updated_lines.append(updated_line)
                            print(f"Salary updated for {name}: ₹{new_salary:.2f}")
                    except ValueError:
                        print("Invalid percentage value.")
                        updated_lines.append(line)
                else:
                    updated_lines.append(line)

        if not found:
            print("Employee not found.")

        with open("Emp.txt", "w") as f:
            f.writelines(updated_lines)

# Main Menu
emp = Employee()

while True:
    print("\nMenu:")
    print("1. Enter employee details")
    print("2. Display employee details")
    print("3. Raise Salary")
    print("4. Exit")
    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        confirm = input("Do you want to enter employee details? (y/n): ")
        if confirm.lower() == 'y':
            emp.input_data()
    elif choice == '2':
        emp.display_all()
    elif choice == '3':
        emp.raise_salary()
    elif choice == '4':
        print("Thank you for using the application.")
        break
    else:
        print("Invalid choice. Try again.")
