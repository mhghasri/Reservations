from pakage import *

# ----------------------------------------------------- #

def print_color(string, color: str="r"):
    if color == "r":
        print(Fore.RED + f"\n{string}\n" + Fore.RESET)

    elif color == "b":
        print(Fore.BLUE + f"\n{string}\n" + Fore.RESET)

    elif color == "g":
        print(Fore.GREEN + f"\n{string}\n" + Fore.RESET)

    elif color == "m":                  # menu
        print(Fore.MAGENTA + f"\n{string}\n" + Fore.RESET)

    elif color == "c":                  # regular user
        print(Fore.CYAN + f"\n{string}\n" + Fore.RESET)

    elif color == "y":
        print(Fore.YELLOW + f"\n{string}\n" + Fore.RESET)

    else:
        print(f"\n{string}\n")

# ----------------------------------------------------- #

def read_write_json_file(data: dict={}, mode: str="read", event: str="users"):
    if event =="users":
        path = "./json/users.json"
    elif event == "travel":
        path = "./json/travel.json"

    elif event == "reservation":
        path = "./json/reservation.json"

    if mode == "read":
        with open (path) as F:
            data = json.load(F)
        
        return data

    elif mode == "write":
        with open (path, "w") as F:
            json.dump(data, F, indent= 4)

        return None
    
# ----------------------------------------------------- #

def admin_or_user_panel(permission):
    if permission == "admin":
        return True
    
    elif permission == "user":
        return False
    
# ----------------------------------------------------- #

def password_validation(password):
    lower = upper = digit = other = 0
    for ch in password:
        if ch.islower():
            lower +=1 

        elif ch.isupper():
            upper += 1

        elif ch.isdigit():
            digit += 1

        else:
            other += 1


    if len(password) in range (8, 33): 
        if (lower >= 1) and (upper >= 1) and (digit >= 1) and (other >= 1):
            return True
        
        else:
            print_color("Your password must have at least 1 special char like (upper, lower, digit, other) case(s).")
            return False

    else:
        print_color(f"{password} is not in range 8, 32 please try again.")
        return False

# ----------------------------------------------------- #

def write_log(event: str, note):
    now = datetime.now()

    date_string = now.strftime("%Y-%m-%d %H:%M:%S")

    data = f"\n[{date_string}] --- [{event}] --- [{note}]"
    
    with open("./logs/log.txt", "a") as F:
        F.write(data)

# ----------------------------------------------------- #

def signup():

    data = read_write_json_file()

    while True:

        username = input("\nPlease enter your user name: ")

        if username not in data:
            print_color(f"Wellcome {username}.", "g")
            break

        else:
            print_color(f"this username: {username} already exist. please try again.")

    for number in range (3, 0, -1):
        password = input("\nPlease enter your password: ")

        if password_validation(password):
            print_color(f"Valid password. wellcome '{username}' with password: '{password}'. Please complete all lines.", "g")
            break

        elif number == 1:
            print_color("Out of chance please try again.")
            return None

        else:
            print_color(f"You have '{number - 1}' time remaning.")

    fname = input("\nPlease enter your First name: ")
    lname = input("\nPlease enter your Last name: ")
    email = input("\nPlease enter your Email: ")

    data[username] = {
        "password" : password,
        "name" : f"{fname} {lname}",
        "email" : email,
        "permission" : "user",
        "balance" : 0
    }

    read_write_json_file(data, "write")

    write_log("signup", f"{username} has sign up successfully.")

    print_color("You sign up successfully.", "g")

    return username

# ----------------------------------------------------- #

def login():
    data = read_write_json_file()


    while True:
        username = input("\nEnter your user name: ")
        
        if username in data:
            print_color(f"Wellcome {username}.", "g")
            break

        else:
            print_color("User not found.")

    for number in range(3, 0, -1):

        password = input("\nPlease enter your password: ")

        if password == data[username]["password"]:
            return username

        elif number == 1:
            print_color("Out of try. please try again later.")
            write_log("login faild", f"{username} input wrong password '3' time.")
            return False

        else:
            print_color(f"Invalid password. Please try again. '{number-1}' remaining.")

    write_log("login successfully", f"{username} login successfully.")

# -------------------------------------------------------------------------------------------------------------- #

class Users:

    def __init__(self, username):

        self.username = username

        self.travel_data = read_write_json_file(event="travel")
        
        self.user_data = self.read_user_data()
        
        self.password = self.user_data["password"]

        self.name = self.user_data["name"]

        self.email = self.user_data["email"]

        self.permission = self.user_data["permission"]

        self.balance = self.user_data["balance"]

        self.reservation = read_write_json_file(event="reservation")

# ----------------------------------------------------- #

    def show_travels(self):
        print_color(f"{self.username} this is our travels.", "m")

        index = 1

        for code, information in self.travel_data.items():

            if information["quantity"] > 0:
                print_color(f"{index}. TravelID: {code} --- Destination: {information['destination']} --- Time: {information['time']} --- Price: {information['price']} --- Quantity: {information['quantity']}", "m")
                print_color("-" * 40, "b")
                index += 1

# ----------------------------------------------------- #

    def write_travel_data(self):
        read_write_json_file(data=self.travel_data, mode="write", event="travel")

# ----------------------------------------------------- #

    def read_user_data(self):
        user_json_data = read_write_json_file()
        return user_json_data[self.username]

# ----------------------------------------------------- #

    '''def write_user_data(self):
        all_user_data = read_write_json_file()
        all_user_data[self.username] = {
            "password": self.password,
            "name": self.name,
            "email" : self.email,
            "permission": self.permission,
            "balance": self.balance
        }

        read_write_json_file(data=all_user_data, mode="write")
    '''

# ----------------------------------------------------- #

    def update_balance(self, amount, receiver_username="mhghasri", buy_or_refund_or_charge: str="buy"):

        all_user_data = read_write_json_file()

        if buy_or_refund_or_charge == "buy":
            self.balance -= amount
            all_user_data[receiver_username]["balance"] += amount
        
        elif buy_or_refund_or_charge == "refund":
            self.balance += amount
            all_user_data[receiver_username]["balance"] -= amount

        elif buy_or_refund_or_charge == "charge":
            self.balance += amount


        all_user_data[self.username]["balance"] = self.balance

        read_write_json_file(data=all_user_data, mode="write")

# ----------------------------------------------------- #

    def show_balance(self):
        print_color(f"Dear {self.username} This is your current balance: {self.balance}$.", "g")

# -------------------------------------------------------------------------------------------------------------- #

class Admin(Users):

    def __init__(self, username):
        super().__init__(username)

# ----------------------------------------------------- #

    def add_new_travel(self):
        print_color(f"{self.username} Please enter data of new travel.", "y")
        # data = self.read_travel_data()

        if self.travel_data:
            travel_id = str(max(map(int, self.travel_data.keys())) + 1)

        else:
            travel_id = "100101"


        destination = input("\nPlease enter your destination: ").strip().title()
        time = input("\nPlease enter time of travel: ")

        while True:
            price = input("\nPlease enter price of travel: ")
            if price.isdigit():
                price = int(price)
                break
            print_color("Price must be a number.", "r")

        while True:
            quantity = input("\nPlease enter quantity of travel: ")
            if quantity.isdigit():
                quantity = int(quantity)
                break
            print_color("Quantity must be a number.", "r")


        self.travel_data[travel_id] = {
            "destination": destination,
            "time": time,
            "price": price,
            "quantity": quantity
        }

        self.write_travel_data()

        write_log("add new travel", f"{self.username} add new travel with id: {travel_id}")

        print_color(f"Travel with ID {travel_id} added successfully.", "g")

        

        return self

# ----------------------------------------------------- #

    def change_travel_information(self):
        self.show_travels()

        travel_id = input("\nPlease enter travel id for change information: ")
        
        if travel_id in self.travel_data:
            destination = input("\nPlease enter new destinion: ")
            time = input("\nPlease enter new time: ")
            price = int(input("\nPlease enter new price: "))
            quantity = int(input("\nplease enter new quantity: "))

            self.travel_data[travel_id] = {
                "destination": destination,
                "time": time,
                "price": price,
                "quantity": quantity
            }

            self.write_travel_data()

            write_log("edit travel", f"{self.username} edit travel with id: {travel_id}")

        else:
            print_color(f"Invalid input. this {travel_id} not found please try again.")

            write_log("edit travel faild", f"{self.username} try to edit travel.")

# ----------------------------------------------------- #

    def delet_travel(self):
        self.show_travels()

        travel_id = input("\nPlease enter travel id: ")

        if travel_id in self.travel_data:
            del self.travel_data[travel_id]

            print_color(f"This travel: {travel_id} deleted successfull.", "g")

            self.write_travel_data()

            write_log("delet travel by admin", f"{self.username} delet travel with id: {travel_id}")

        else:
            print_color(f"This id: {travel_id} not found. Please try again.")

            write_log("delet travel faild", f"{self.username} try to delet a travel.")

# ----------------------------------------------------- #

    def show_all_reservation(self):
        print_color(f"Dear {self.username} This is all reservation data:", "y")

        index = 1

        for res_id, information in self.reservation.items():
            print_color(f"{index}. Reservation Id: {res_id} --- Buyer: {information['buyer']} --- final price: {information["final_price"]}$ --- Travel Id: {information['travel_id']} --- Quantity: {information['quantity']} --- Buy time: {information['buy_time']}", "m")

            print_color("-" * 40, "b")

            index += 1

# ----------------------------------------------------- #

    def show_travels(self):
        print_color(f"{self.username} this is our travels.", "m")

        index = 1

        for code, information in self.travel_data.items():

            print_color(f"{index}. TravelID: {code} --- Destination: {information['destination']} --- Time: {information['time']} --- Price: {information['price']} --- Quantity: {information['quantity']}", "m")
            print_color("-" * 40, "b")
            index += 1

# -------------------------------------------------------------------------------------------------------------- #

class BasicUser(Users):
    def __init__(self, username):
        super().__init__(username)

# ----------------------------------------------------- #

    def add_reservation(self):

        self.show_travels()

        travel_id = input("\nPlease enter Travel Id: ")

        if travel_id in self.travel_data:

            quantity = int(input("\nPlease enter your quantity of you want: "))

            if quantity <= self.travel_data[travel_id]["quantity"]:


                travel_price = self.travel_data[travel_id]["price"] * quantity

                if travel_price <= self.balance:

                    if self.reservation:
                        reservation_id = str(max(map(int, self.reservation.keys())) + 1)

                    else:
                        reservation_id  = "200101"

                    self.reservation[reservation_id] = {
                        "buyer" : self.username,
                        "destination" : self.travel_data[travel_id]["destination"],
                        "price" : self.travel_data[travel_id]["price"],
                        "buy_time" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "travel_id" : travel_id,
                        "quantity" : quantity,
                        "final_price" : travel_price,
                        "time" : self.travel_data[travel_id]["time"]
                    }

                    self.write_reservation()

                    print_color(f"Dear {self.username} This is your buying list.\n\nreservation Id: {reservation_id} --- time: {self.travel_data[travel_id]["time"]} --- Quantity: {self.reservation[reservation_id]["quantity"]} --- Final price: {travel_price}", "g")
                    

                    self.travel_data[travel_id]["quantity"] -= quantity

                    self.update_balance(travel_price)

                    self.write_travel_data()

                    self.show_balance()

                else:
                    print_color("Not enough money please charge your balance.")


            else:
                print_color("Out of quantity. Please try again.")

                return None

        else:
            print_color("This id is not valid. Please try again.")

# ----------------------------------------------------- #

    def write_reservation(self):
        read_write_json_file(data=self.reservation, mode="write", event="reservation")

# ----------------------------------------------------- #

    def search(self):
        travel_name = input("\nPlease enter the travel you want: ").title().strip()
        
        index = 1

        is_found = False

        for travel_id, information in self.travel_data.items():
            if travel_name == information["destination"]:
                print_color(f"{index}. Travel ID: {travel_id} --- Destination: {information['destination']} --- Time: {information['time']} --- Price: {information['price']} --- Quantity: {information['quantity']}", "m")

                print_color("-" * 40, "b")

                index += 1

                is_found = True

        if not is_found:
            print_color(f"No travel found for Destination: {travel_id}.")

# ----------------------------------------------------- #

    def show_my_travels(self):
        
        index = 1

        is_found = False

        print_color(f"Dear {self.username} This is your reservations: ", "c")

        for res_id, information in self.reservation.items():
            if self.username == information["buyer"]:
                print_color(f"{index}. Reservation ID: {res_id} --- Destination: {information['destination']} --- Time: {information['time']} --- Price: {information['final_price']} --- Quantity: {information['quantity']}", "m")
                
                print_color("-" * 40, "b")

                index += 1

                is_found =True

        if not is_found:
            print_color(f"Dear {self.username} You dont have any reservation.")

            return False
        return True

# ----------------------------------------------------- #
    def refund_reservation(self):
        if self.show_my_travels():

            refund_id = input("\nPlease enter reservation id for refund it: ")

            if refund_id in self.reservation.keys():
                
                print_color("Warning. If you refund a reservation you tax 10% for refund it care.")

                while True:

                    user_sure = input("\nAre you sure? Yes or no: ").lower()

                    if user_sure in ("yes", "no", "y", "n"):
                        if user_sure in ("yes", "y"):
                            amount = self.reservation[refund_id]["final_price"] * 0.9
                            self.travel_data[self.reservation[refund_id]["travel_id"]]["quantity"] += self.reservation[refund_id]["quantity"]
                            del self.reservation[refund_id]
                            self.write_reservation()
                            self.write_travel_data()
                            self.update_balance(amount=amount, buy_or_refund_or_charge="refund")
                            print_color(f"Dear {self.username} reservation id: {refund_id} hes refund successfully.", "g")
                            self.show_balance()

                        else:
                            print_color("Refund canceled successfully.", "g")

                        break

                    else:
                        print_color(f"Dear {self.username} Please enter valid input.")



            else:
                print_color(f"Dear {self.username} this id: {refund_id} not found please try again.")

# ----------------------------------------------------- #

    def add_balance(self):
        self.show_balance()

        amount = int(input("\nPlease enter your balance: "))

        self.update_balance(amount=amount, buy_or_refund_or_charge="charge")

        self.show_balance()

# -------------------------------------------------------------------------------------------------------------- #

class AdminPanel(Admin):
    def __init__(self, username):
        super().__init__(username)

    def show_panel(self):
        print_color(f"Wellcome Back Dear Admin. {self.username}.", "y")
        while True:
            print_color("1. Add new travel.\n2. Show Travel List.\n3. Edit travels.\n4. Delete a travel.\n5. show reservations.\n6. Current Balance.\n7. log out", "y")

            admin_option = input("\nPlease enter your choice: ")

            if admin_option in "1234567":
                if admin_option == "1":
                    self.add_new_travel()

                elif admin_option == "2":
                    self.show_travels()

                elif admin_option == "3":
                    self.change_travel_information()

                elif admin_option == "4":
                    self.delet_travel()

                elif admin_option == "5":
                    self.show_all_reservation()

                elif admin_option == "6":
                    self.show_balance()

                elif admin_option == "7":
                    print_color("You log out successfully.", "g")
                    return None

            else:
                print_color("Wrong input. Please try again.")

class BasicUserPanel(BasicUser):
    def __init__(self, username):
        super().__init__(username)

    def show_panel(self):
        print_color(f"Wellcome back {self.username}.", "c")

        while True:
            print_color(f"1. Show all travels.\n2. Search travels.\n3. Reservation.\n4. My reservation.\n5. Refund a reservation.\n6. Add balance\n7. Show Balance.\n8. Logout", "c")

            user_option = input("\nPlease enter your option: ")

            if user_option in "12345678":
                if user_option == "1":
                    self.show_travels()
                
                elif user_option == "2":
                    self.search()
                
                elif user_option == "3":
                    self.add_reservation()
                
                elif user_option == "4":
                    self.show_my_travels()
                
                elif user_option == "5":
                    self.refund_reservation()
                
                elif user_option == "6":
                    self.add_balance()

                elif user_option == "7":
                    self.show_balance()
                
                elif user_option == "8":
                    print_color("Logout successfull.", "g")
                    return None

            else:
                print_color("Invalid input. Please try again.")