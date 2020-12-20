#prototype for Trailmix written in python
#Authors of Prtotype.py: Marc Montesa and Sarah Cooper
#Authors of FIGMA: Matthew Deagen and Leo Galang
#Date: 12/1/2020
#class: CS 425 - Senior project part 4: prototype

import math
import time
import hashlib
from hashlib import pbkdf2_hmac
import os.path
import os
import random
import binascii
import getpass
import shutil
import ast

PATH_TO_USER = "User.txt"
PATH_TO_PREF = "Preferences.txt"

#user database: user.txt
# username, salt, password, enable_flag, connected rpreferences list (if any), logs (list)
#logs = [cats, lions, puma, tiger, ...] (what they searched)
#preferences = connected profile with the random
#database delimiter: |

#preferences database: pref.txt
# list of everyone's logs
# [cat, dog, tiger,...]


class user():
    __enable_flag = 1
    __send_data_flag = 1
    __salt = b''
    __key = b''
    def __init__(self,username,password):
        user.__salt = os.urandom(16)
        self.username = username #username
        self.logs = []
        self.preferences = []
        if password != None:
            user.__key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), user.__salt, 100000)#hashed password
            self.write_to_file(0)
        else:
            self.update_temp_profile()
    
    def logout(self):
        self.write_to_file(1)
        self.update_pref_list()
        
    def get_username(self):
        return self.username

    def show_logs(self):
        
        return self.logs

    def clear_logs(self):
        self.logs = []
        return 1
    def send_user_logs(self):
        if user.__send_data_flag == 1:
            user.__send_data_flag = 0
        else:
            user.__send_data_flag = 1
        return user.__send_data_flag

    def update_temp_profile(self):
        file = open(PATH_TO_USER,"rt")
        lines = file.readlines()
        for line in lines:
            line = line.split("|")
            if self.username == line[0]:
                user.__salt = binascii.a2b_hex(line[1][2:-1])
                user.__key = binascii.a2b_hex(line[2][2:-1])
                user.__enable_flag = int(line[3])
                user.__send_data_flag =  int(line[4])
                self.preferences = ast.literal_eval(line[5])
                self.logs = ast.literal_eval(line[6])
        file.close()

    def write_to_file(self, flag):
        if flag == 1:
            #print("Updating Changes")
            temp = open("temp", "w+")
            file = open(PATH_TO_USER,"r")
            lines = file.readlines()
            for line in lines:
                line = line.split("|") #username salt password ... --> [username,salt,password,...]
                if line[0] == self.username:
                    temp.write(self.username + "|" + str(binascii.b2a_hex(user.__salt)) + "|" + str(binascii.b2a_hex(user.__key)) + "|" + str(user.__enable_flag) +"|" + str(user.__send_data_flag) + "|" + str(self.preferences) + "|" + str(self.logs) +  "|\n")
                else:
                    temp.write(line[0] + "|" + line[1] + "|" + line[2] + "|" + line[3] + "|" + line[4] + "|" + line[5] + "|" + line[6] + "|\n")
            temp.close()
            shutil.move('temp',PATH_TO_USER)
            #check if user is in the file and then update their info.... idk how
            
        #if user is new
        if flag == 0:
            file = open(PATH_TO_USER,"a+")
            file.write(self.username + "|" + str(binascii.b2a_hex(user.__salt)) + "|" + str(binascii.b2a_hex(user.__key)) + "|" + str(user.__enable_flag)  +"|" + str(user.__send_data_flag) + "|" + str(self.preferences) + "|" + str(self.logs) + "|\n")
            file.close()

    def get_ed_flag(self):
        return user.__enable_flag

    def set_enable_disable(self):
        if user.__enable_flag == 1:
            user.__enable_flag = 0
        else:
            user.__enable_flag = 1
        return user.__enable_flag
    
    def log_system(self, logs_list):
        if len(logs_list) > 0:
            for i in logs_list:
                self.logs.append(i)
            return self.logs
        else:
            return 0

    def set_preferences(self, new_prefrenes):
        self.preferences = new_prefrenes

    def add_to_pref(self, list_new_prefs_to_add):
        if len(list_new_prefs_to_add) > 0:
            for i in list_new_prefs_to_add:
                self.preferences.append(i)
                self.logs.append(i)
            return self.preferences
        else:
            return 0

    def get_preferences(self,where):
        if where == 0:
            list_pref = []
            with open(PATH_TO_PREF,"rt") as f:
                list_pref = f.readline().split(",")
                list_pref.remove('')
                f.close()
            
            new_list_pref = random.choices(list_pref,k = 10)
            return new_list_pref
        elif where == 1:
            return self.preferences

    def refresh(self):
        self.set_preferences(self.get_preferences(0))

    def update_pref_list(self):
        total_user_logs = []
        with open(PATH_TO_USER, "r") as user_file:
            user_lines = user_file.readlines()
            for user_line in user_lines:
                user_line = user_line.split("|")
                user_logs = ast.literal_eval(user_line[6])
                if int(user_line[4]) == 1:
                    for l in user_logs:
                        total_user_logs.append(l)
            user_file.close()
        
        #print(total_user_logs)

        prefs = []
        with open(PATH_TO_PREF, "r") as pref_file:
            prefs = pref_file.readline().split(",")
            pref_file.close()
        
        #print(prefs)
        
        prefs.extend(total_user_logs)
        prefs = list(dict.fromkeys(prefs))
        
        #print(prefs)

        with open(PATH_TO_PREF,"w") as f:
            for j in prefs:
                f.write(str(j) + ",")
            f.close()
            


def create_account():
    
    #register username and password
    file = open(PATH_TO_USER,"r")
    new_username = 0
    while new_username != 1:
        username = input("\nUSERNAME\n*Do not have any spaces\n*Do not use your name\n*Caps sensitive\n").strip(" ")
        new_username = 1
        lines = file.readlines()
        for line in lines:
            line = line.split("|")
            if line[0] == username:
                print("Username Already Registered.\n")
                new_username = 0

    confirm_pass = 0
    
    while confirm_pass != 1:        
        password = getpass.getpass('\nPASSWORD\n*Password much be 10 characters or longer\n')
        while(len(password) < 10):
            password = getpass.getpass('\nPassword does not meet the character length.\n*Password much be 10 characters or longer\n ')
            
        password_confirmation = getpass.getpass('\nPlease confirm your password.\n')
        if password_confirmation == password:
            confirm_pass = 1
        
    newUser = user(username, password)
    return 0


def signin():
    username = input("\nUsername(0 to exit back to menu): ")
    
    if username == "0":
        return 0, None
    elif username != "0":
        password = getpass.getpass('Password: ') #input("Password: ") #I want to try considering using getpass() here, to try to hide user input passwords -- not necessary just QoL stuff
        return check_user(username, password)

    
def check_user(username, password):
    file = open(PATH_TO_USER,"rt")
    lines = file.readlines()
    for line in lines:
        line = line.split("|")        

        if line[0] == username:
            new_salt = line[1].strip('\n').strip()
            new_pass = line[2].strip('\n').strip()
            new_salt = binascii.a2b_hex(new_salt[2:-1])

            verify_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), new_salt, 100000)
            if verify_key == binascii.a2b_hex(new_pass[2:-1]):
                file.close()
                print("Successfully logged in!\n")
                return 1, username
            else:
                file.close()
                print("Password does not match password for username " + username + " on file.\n")
                return 0, None
    else:
        file.close()
        print("Username: " + username + " not on file.\n")
        return 0, None

def main():
    username = None
    flag = 0
    print("\n\nWelcome to Trailmix!\n-------------------------------------------------------")
    first_input = input("\nTrailmix Menu:\n[1]: Sign In\n[2]: Create An Account\n[3]: Exit Program\n" )
    while(first_input != "3"):
        if first_input == "1":
            flag, username = signin()
            if flag == 0:
                first_input = 0
            else:
                print("Logging In...")
                break
        elif first_input == "2":
            flag = create_account()
            if flag == 0:
                first_input = 0
        else:
            first_input = input("\nTrailmix Menu:\n[1]: Sign In\n[2]: Create An Account\n[3]: Exit Program\n" )


    time.sleep(.5)
    if flag == 1:
        temp_user = user(username, None)
        ed_flag = temp_user.get_ed_flag()
        logout_flag = 0
        next_input = input("\nTrailmix Menu:\n[1]: Enable/Disable Trailmix\n[2]: Refresh\n[3]: Preferences\n[4]: User Logs\n[5]: Settings\n[6]: Logout\n" )
        while(next_input != "6"):
            
            if next_input == "1":
                #set enable/disable flag
                ed_flag = temp_user.set_enable_disable()
                if ed_flag == 0:
                    print("-------------------\nFunctionality is Disabled\n-------------------\n")
                elif ed_flag == 1:
                    print("-------------------\nFunctionality is Enabled\n-------------------\n")
                    time.sleep(.5)
                    print("-------------------\nMixing Trail...")
                    time.sleep(.5)
                    temp_user.refresh()
                next_input = "0"
            
            elif next_input == "2":
                #Refresh
                if ed_flag == 0:
                    print("-------------------\nFunctionality has been Disabled\n-------------------\n")
                else:
                    print("-------------------\nMixing Trail...")
                    time.sleep(.5)
                    temp_user.refresh()
                    print("Current Preferences for "+ temp_user.get_username() +":\n"+str(temp_user.get_preferences(1))+ "\n-------------------\n")
                next_input = "0"
            
            elif next_input == "3":
                #preferences settings
                if ed_flag == 0:
                    print("-------------------\nfunctionality has Been Disabled\n-------------------\n")
                else:
                    inpt1 = input("\nPreferences Settings:\n[1]: Show Current Preferences\n[2]: Add Preferences\n[3]: Back\n")
                    while inpt1 != "3":
                        if inpt1 == "1":
                            print("-------------------\nCurrent Preferences for "+ temp_user.get_username() +":\n"+str(temp_user.get_preferences(1)) + "\n-------------------\n")
                            inpt1 = "0"
                        elif inpt1 == "2":
                            pref_list = []
                            pref_flag = 1
                            pref = (input("\nInput preferences followed by the enter key (0 when done):\n-->"))
                            while pref_flag != 0:
                                if pref == "0":
                                    pref_flag = 0
                                    break
                                else:
                                    pref_list.append(pref)
                                pref = (input("-->"))
                            print("\n-------------------\nUpdated Preferece List for "+ temp_user.get_username() +":\n"+str(temp_user.add_to_pref(pref_list))+"\n-------------------\n")
                            inpt1 = "0"
                        elif inpt1 == "3":
                            break
                        else:
                            time.sleep(.5)
                            inpt1 = input("\nPreferences settings:\n[1]: Show Current Preferences\n[2]: Add Preferences\n[3]: Back\n")
                        
                next_input = "0"
            
            elif next_input == "4":
                #logs
                if ed_flag == 0:
                    print("-------------------\nfunctionality has been Disabled\n-------------------\n")
                else:
                    inpt2 = input("\nUser Log Settings:\n[1]: Show Logs\n[2]: Clear Logs\n[3]: Add to Logs\n[4]: Back\n")
                    while inpt2 != "4":
                        if  inpt2 == "1":
                            print("\n-------------------\nLog File for " + temp_user.get_username() +":\n"+ str(temp_user.show_logs())+ "\n-------------------\n")
                            inpt2 = "0"
                        elif inpt2 == "2":
                            temp_user.clear_logs()
                            print("-------------------\nLogs have been Cleared\n-------------------\n")
                            inpt2 = "0"
                        elif inpt2 == "3":
                            log_list = []
                            log_flag = 1
                            #this will basically be the search history, however we cant really show how we would take their info in this prototype version so assuming this would be like if you went  on the internet and were to search things
                            logs = (input("\nGoogle Search (0 when done):\n-->"))
                            while log_flag != 0:
                                if logs == "0":
                                    log_flag = 0
                                    break
                                else:
                                    log_list.append(logs)
                                logs = (input("-->"))
                            print("\n-------------------\nUpdated User Logs for "+ temp_user.get_username() +":\n"+str(temp_user.log_system(log_list))+"\n-------------------\n")
                            inpt2 = "0"
                        elif inpt2 == "4":
                            break
                        else:
                            time.sleep(.5)
                            inpt2 = input("\nUser Log settings:\n[1]: Show Logs\n[2]: Clear Logs\n[3]: Add to Logs\n[4]: Back\n")  
                next_input = "0"
            
            elif next_input == "5":
                #settings settings
                inpt3 = input("\nSettings:\n[1]: Send/Dont Send Data\n[2]: Logout\n[3]: Back\n")

                while inpt3 != "3":
                    if  inpt3 == "1":
                        send_flag = temp_user.send_user_logs()
                        if send_flag == 0:
                            print("-------------------\nUser data logs will not be sent to Trailmix\n-------------------\n")
                        elif send_flag == 1:
                            print("-------------------\nUser data logs will be sent to Trailmix\n-------------------\n") 
                        inpt3 = "0"
                        
                    elif inpt3 == "2":
                        temp_user.logout()
                        logout_flag = 1
                        break
                    elif inpt3 == "3":
                        break
                    else:
                        time.sleep(.5)
                        inpt3 = input("\nSettings:\n[1]: Send/Dont Send Data\n[2]: Logout\n[3]: Back\n")
                
                if logout_flag == 1:
                    next_input = "6"
                else:
                    next_input = "0"
 
            else:
                time.sleep(.5)
                next_input = input("\nTrailmix Menu:\n[1]: Enable/Disable Trailmix\n[2]: Refresh\n[3]: Preferences\n[4]: User Logs\n[5]: Settings\n[6]: Logout\n" )
        
        temp_user.logout() #Consider after the prototype to change this from logout to Apply Changes
        
    time.sleep(.5)
    print("Thank You for Using Trailmix. Good Bye")
    time.sleep(1)

if __name__ == "__main__":
    main()