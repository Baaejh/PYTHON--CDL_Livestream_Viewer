# Call Of Duty CDL Livestream viewer
# Created by: Bailey Hutchings, 2021

# IMPORTS
from selenium import webdriver  # importing webdriver from selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import webbrowser
import time
import sys
import getpass


# Global Dictionary, stores paths required by script
# aswell as activision log in information
users_information = {
    "username": "",
    "password": "",
    "chromedriver_path": "",
    "chrome_path": "",
}


# Class Containing Instance and logic for finding Live Games
class ClassFindVideo:

    # INITIALISING instance variables
    def __init__(self, driver_instance):
        self.driver = driver_instance

    # === checks if the stream is playing ===
    def open_youtube(self):
        try:
            # assingning frame to variable
            iframe = self.driver.find_element_by_xpath(
                "//iframe[@id='yt-player']")
            # swapping the drivers focus over to the iFrame
            self.driver.switch_to.frame(iframe)
        except:
            print("Error swapping driver focus to iFrame")
            self.driver.quit()
            sys.exit()

        # checks stream (pauses if playing) and closes browser as stream should be playing in YouTube
        # NOTE: Script will finish executing after this function complete
        def check_CDL_stream_activity():
            try:
                time.sleep(5)

                # Assigning pause button to variable
                pause_button = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'ytp-play-button')))

                # gets the status of the [play/pause] button --> ('play' / 'pause')
                pause_status = pause_button.get_attribute('aria-label')

                # conditional statements to pause the stream if it is playing
                if pause_status[:4] == "Play":
                    print(pause_status)
                    print("Stream is PAUSED ... Playing in youtube")
                # check_stream()
                elif pause_status[:5] == "Pause":
                    print("Stream is PLAYING ... Pausing stream")
                    pause_button.click()
                # check_stream()
                else:
                    print("Not paused or playing:")
                    print("pause status: " + pause_status)

                # sleeps for a bit after pausing stream
                time.sleep(10)

                # Closing stream
                self.driver.quit() 

            except Exception as check_stream_exception:
                print("\nerror checking if stream is still running \n \n"
                      + str(check_stream_exception))
                print("Exiting program ... Youtube will continue to stream Live Game")
                input("Press Enter to Continue ...")
                self.driver.quit()
                sys.exit()


        # OPENS YOUTUBE IN NORMAL CHROME (NON-CHROMEDRIVER)
        def watch_in_youtube():
            try:
                real_chrome_path = users_information["chrome_path"]

                play_in_youtube_button = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH,
                        "//a[@title='Watch on youtube.com']")))
                # Grabbing Link for youtube Video
                youtube_link = play_in_youtube_button.get_attribute('href')

                print("Connecting to: " + youtube_link)

                # Note 'webbrowser' is not related to selenium, it is used to
                # open a normal instance of web browsers
                webbrowser.register('chrome', None, real_chrome_path)
                webbrowser.get('chrome')
                webbrowser.open_new(youtube_link)

            except Exception as watch_youtube_exception:
                print("\n error playing in youtube ... \n \n"
                      + str(watch_youtube_exception))
                print()
                print("Check the Google Chrome directory path in: 'users_info.txt'")
                print("Please restart application ...")
                self.driver.quit()
                sys.exit()

        # Calling Function that Opens stream in youtube (make sure youtube is logged in on Chrome)
        watch_in_youtube()  

        # Note: Script will End after: check_CDL_stream_activity() is called
        check_CDL_stream_activity()  # Pauses stream playing on CDL webpage


    # Waits 15 minutes and then runs parent function to check for a live game
    def wait_for_livestream(self):
        print("Waiting For Live Game...")
        time.sleep(900)  # Waits 15 mins
        print('wait complete...')
        self.find_live_container()

    # Finds the link within the live game container at top of CDL Webpage and clicks it
    def click_live_game(self, live_container):
        clickable_link = live_container.find_element_by_css_selector("a[href^='http']")
        clickable_link.click()  # Click Live Game Link
        time.sleep(10)
        self.find_play_button()

    # This function finds and clicks on the YT play button within the CDL Webpage
    def find_play_button(self):

        print('clicking livestream / youtube play button')

        # Waiting for element to load if it has not loaded
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((
                By.CLASS_NAME, "youtube-videostyles__Video-sc-50qh48-1")))

        play_button = self.driver.find_element_by_class_name(
            "youtube-videostyles__Video-sc-50qh48-1")

        play_button.click() # Click Play Button
        time.sleep(5)
        # *** checks if stream is playing ***
        self.open_youtube()

    # finds the container with the link to the live game (CDL Webpage) and .clicks()
    def find_live_container(self):

        live_game_counter = 0

        try:  # Attempts to open CDL Webpage With Selenium Driver Instance
            self.driver.get("https://callofdutyleague.com/en-us/")
            print("Driver.get(webpage) complete...")
        except Exception as driver_connect_exception:
            print(driver_connect_exception)
            print()
            print("Cannot Connect to webpage, driver.get()) failed --> exiting...")
            input("Press Enter to Continue ...")
            self.driver.quit()
            sys.exit()

        try:
            # Refreshes the driver (after signing in the driver must be refreshed)
            self.driver.refresh()
            time.sleep(5)
            # waits for game containers at the top to load in
            # and then Locates the live / completed game containers at the top
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((
                    By.CLASS_NAME, 'score-strip-itemstyles__ScoreStripItemContainer-sc-1502vsd-0')))

            # Locating the Live Game Containers (Top Panels) at top of Webpage
            container1 = self.driver.find_elements_by_class_name(
                'score-strip-itemstyles__ScoreStripItemContainer-sc-1502vsd-0')

            # Loop finds live game from top panels of webpage stored within (container1)
            while live_game_counter <= len(container1):

                if live_game_counter >= len(container1):  # No possibility of Live Game
                    print("No Live Games available ... ")
                    print("Exiting Script ... Check CDL Roster & Try Again Later... ")
                    self.driver.quit()
                    sys.exit()
                    break

                # reading live game container text to determine if there is a live game
                if container1[live_game_counter].text[:15] != "WATCH MATCH VOD":
                    if container1[live_game_counter].text[:21] != "TICKETS NOT AVAILABLE":  # Game Found

                        print("Live game Found: " + container1[live_game_counter].text)

                        # Passing in the Selected Container with live game link to click_live_game()
                        self.click_live_game(container1[live_game_counter])
                        break

                    else:
                        print("No Live game found ... Waiting")  # No Live Game Found Waiting...
                        self.wait_for_livestream() # Waits for 15 mins
                        break

                live_game_counter += 1  # Increment Counter to search Next Container for live Game

        except Exception as find_live_game_exception:
            print("\nerror checking for live game \n \n"
                  + str(find_live_game_exception))
            input("Please Restart Script ... Press enter to continue")
            self.driver.quit()
            sys.exit()


# *** Program Start ***
# Handles grabbing user input/info from File and creating 'users_info.txt'
def retrieve_path_locations():

    # VARIABLES:
    path_template = ["chromedriver_path: \n", "chrome_path: \n"]
    directory, filename = os.path.split(os.path.abspath(sys.argv[0]))
    user_info = os.path.join(directory, 'user_info.txt')

    # Creates the blank File 'users_info.txt' for user to enter their details
    def create_credentials_file():
        users_information.clear()  # Clears Dictionary containing users info
        try:
            # Adding Content to users_input.txt File
            with open(user_info, "w") as created_file:
                for required_fields in range(len(path_template)):
                    created_file.writelines(path_template[required_fields])

        except Exception as file_creation_exception:
            print(file_creation_exception)
            print("Error creating users_info.txt File ...")
            input("Press enter to Continue")
            sys.exit()

        finally:
            print()
            print("user_info.txt has been created and reset !")
            print('locate "user_info.txt" inside the main CDL Viewer app directory, and then ')
            print("enter path locations for the required fields - after the colon ':' ")
            print('Save the file and restart this application')
            input("Press enter to Continue")
            sys.exit()   
                
    # The Following code verifys and handles user_info.txt, if all checks pass the,
    # Users input will be stored inside 'users_information' dictionary
    # if checks fail the users_input.txt file will be re-created

         # Script Logic Starts Here: 
    try:
        print('Welcome to CDL Live Stream Viewer !')
        input('Press Enter To Begin...')

        # Checks if the user_info.txt file exists
        if os.path.exists(user_info):
            with open(user_info, "r") as user_info_content: # open for reading

                for item in range(len(path_template)):
                    # Variables related to user-input.txt file
                    line_from_user_info = user_info_content.readline()
                    template_item = path_template[item]
                    colon_index = template_item.find(":")  # Finds index of ':' within the File ->
                    # As the Users input will be > the index of the colon ':'

                    # Checks if the template code within the user_info.txt file is not modified
                    if line_from_user_info[:colon_index + 1] == template_item[:colon_index + 1]:

                        # cleans and saves users input to 'users_input' variable
                        users_input = line_from_user_info[colon_index + 1:].strip()

                        # Makes sure the user enters something
                        if (users_input):
                            users_information[template_item[:colon_index]] = users_input

                        else:  # if no input detected, reset file
                            print()
                            print(path_template[item][:colon_index + 1] +
                                  " Section of the user_info.txt is blank...")
                            create_credentials_file()

                    else:  # Re-creates the credentials file because template code didn't match
                        print()
                        print("Something is not right with the users_info.txt file ")
                        create_credentials_file()
        else:
            print()
            print("No users_info.txt File Found ...")
            create_credentials_file()  # Creating New File

    except Exception as users_info_exception:
        print("\nSomething went wrong while collecting credentials ... \n \n"
              + str(users_info_exception)
              + "\n\ncheck users_info.txt and restart application.")

        input("Press Enter to Continue ...")
        sys.exit()


# Prompts the user if they want to log into the activison site
    # Note Logging in is not Mandatory
def log_in_optional():
    try:
        while True: # Loops untill required input is entered by user
            print()
            login_response = input("do you wish to log in to the Activison Webpage ... ( Y / N ): ")

            # Code Block Makes sure a user enters information and saves the users input
            if (login_response):
                login_response = login_response.strip() # Removes spaces surrounding input
                login_response = login_response.lower() # Converts input to lowerCase

                if (login_response == 'y' or login_response == 'n'): # User must enter 'y' or 'n'

                    if (login_response == 'y'):
                        input("Log In Selected ... Press Any key to Continue ...")

                        collect_user_input() # collects the log in credentials

                        create_instances(1) # creates selenium driver & main class instances
                        # Activision Log In Requested (1)
                        break

                    if (login_response == 'n'):
                        input("No Log In Selected ... Press Any key to Continue ...")

                        create_instances(0) # creates selenium driver & main class instances
                        # No Activision Log In (0)
                        break
                else:
                    print("Please enter 'y' or 'n'")  # No y or n entered
                    continue
            else:
                print("No input detected")  # No Input Detected
                continue
    except Exception as optional_log_in_exception:
        print("\nError while prompting user for input ...\n\n")
        print(optional_log_in_exception)
        print("\n\nPlease restart script ...")
        sys.exit()


# This function collects users Activision Log In info/input & assigns it to the users_information DICT
def collect_user_input():
    # VARIABLES
    global users_information # Links to global variable

    try:
        while True:
            username_input = input("Enter Username: ")
            password_input = getpass.getpass("Enter Password: ")

            # if the user enters something, add it to users_information dictionary:
            if (username_input and password_input):
                # Removing Spaces from around the users input
                username_clean = username_input.strip()
                password_clean = password_input.strip()

                print("Saving Username and Password")

                # Storing Users Input to credential Storage Dictionary 
                users_information["username"] = username_clean
                users_information["password"] = password_clean
            else:
                print("Error with credentials, make sure to fill in both fields")
                continue
            break
    except:
        print("\nError collecting user / pass ...\n")
        print("Please restart program and re-enter credentials ...\n")
        input("Press Enter to Continue ...")
        sys.exit()


# This Function Creates an instance of the ClassFindFVideo() Class
# if user does not wish to log in stream_instance.find_live_container() is called
def create_instances(option):
    # global driver
    global stream_instance # making instance of stream global

    # Creating Instance of Selenium Driver and Instance of the ClassFindVideo() CLASS
    try:
        driver = webdriver.Chrome(users_information['chromedriver_path']) # Driver Instance
        stream_instance = ClassFindVideo(driver) # Class instance
    except:
        print("Error creating Instances")
        print()
        print("Check the chromedriver Path inside 'user_info.txt' ...")
        input("Press Enter to Continue ...")
        sys.exit()

    # Calls Log in Function if the Users Wishes to Log In
    if option == 1:
        log_in(driver) # Logs in
    else:
        stream_instance.find_live_container() # starts searching for live game


# Logs into activison site, once succesfull -> stream_instance.find_live_container() is called
def log_in(driver_arg):  # | Logs in |
    driver = driver_arg

    try:
        driver.get("https://callofdutyleague.com/en-us/")
        print("Driver.get(webpage) complete...")

    except Exception as retrieve_webpage_exception:
        print("\nCannot Connect to webpage  \n \n"
              + str(retrieve_webpage_exception)
              + "\n\nplease restart application...")

        input("Press Enter to Continue ...")
        driver.quit()
        sys.exit()


    try:  # Locates login button, and enters credentials, and skips the 2FA Screen
        # NOTE: IF 2 Step Authentication is set up, this code program will not work

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME,
                "signin-signoutstyles__Container-sc-6rp3r5-0")))

        # assigns sign / log in button to a variable
        sign_in_icon = driver.find_elements_by_class_name(
            "signin-signoutstyles__Container-sc-6rp3r5-0")

        # Locates and Clicks log in button (Appears twice in webpage hence loop)
        for item in sign_in_icon:
            if item.text == "LOGIN":
                item.click()  # clicks link to login page
                time.sleep(5)
                print('Entering login page')
                break
            else:
                continue

        # VARIABLES FOR LOG IN FIELD ELEMENTS
        email_field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'username')))

        # Locates the Password login field
        password_field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'password')))

        # Locates the Submit Button
        submit_button = driver.find_element(By.ID, 'login-button')

        # ENTERING USERNAME
        email_field.send_keys(users_information["username"])

        # ENTERING PASSWORD
        password_field.send_keys(users_information["password"])

        # SUBMITTING CREDENTIALS
        submit_button.click()

        # VARIABLE FOR: skip 2 step authentication
        skip_2_factor = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'skip-tfa')))

        # *** SUCCESSFUL LOG IN ***
        # if skip 2 step auth link is found, then log in was succesfull
        if skip_2_factor:
            skip_2_factor.click() # Clicking Link to continue back to home page

            print('Succesfully Logged In !')
            time.sleep(5)

            # calling method of class instance to start searching for live games
            stream_instance.find_live_container()
        else:
            print("Unable to sign in ... Check Log in credentials")
            print('Script exiting.')
            input("Press Enter to Continue ...")
            driver.quit()
            sys.exit()

    except Exception as sign_in_exception:
        print("\nError Signing-in ...  \n\n"
                + str(sign_in_exception)
                + "\n\ncheck credentials (Username & Password) and restart application.")

        input("Press Enter to Continue ...")
        driver.quit()
        sys.exit()


# === Calling Functions / Classes ===
# retrieves the path locations for chromedriver and Chrome
retrieve_path_locations()

# asks user if they wish to log into the activision page
# driver & ClassFindVideo instance will be created within this function
# the script will begin searching for a livestream via: ClassFindVideo.find_live_container()
log_in_optional()

print()
print('Script Finished ... Stream playing in youtube')
input("Press Enter to Quit ...")

sys.exit()
