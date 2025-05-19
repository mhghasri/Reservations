from scripts import *
print_color("Dear User wellcome to Mh Flying.", "m")

end_time = 0

while True:
    print_color("1. sigup.\n2. login.\n3. exit.", "m")


    try:
        user_option = input("\nPlease enter your option: ")

        flag = True

        if user_option in "123":
            if user_option == "1":
                signup()
            
            elif user_option == "2":

                current_time = time()

                if (current_time - end_time) > 60:
                    
                    username = login()

                    user_data = read_write_json_file()

                    if not username:
                        end_time = time()
                        flag = False

                    if flag:

                        if admin_or_user_panel(user_data[username]["permission"]):
                            admin = AdminPanel(username)
                            admin.show_panel()

                        else:
                            user = BasicUserPanel(username)
                            user.show_panel()
                else:
                    time_remainig = int(60 - (current_time - end_time))

                    print_color(f"You are banned for {time_remainig} second(s). Please be pationt!")

            elif user_option == "3":
                print_color("Exiting the app. good luck.", "g")
                break

        else:
            print_color("Please enter valid number.")

    except KeyboardInterrupt:
        print_color("Exiting app by KeyboardInterrupt. good luck.", "g")
        break

    except ValueError:
        print_color("Invalid input.")

