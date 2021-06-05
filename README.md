# CDL Viewing script README:

* Project Name:  CDL LiveStream Viewer *
* Created By: Bailey Hutchings *

<b>Background Information: </b>

The CDL (Call of Duty League) hosts regular Livestreams on youtube and their own website, 
These livestreams generally cover the Professional Call of Duty tournaments that take place, 
where 12 teams compete for the top spot. Activison/Call of Duty offer an incentive for viewers 
that watch the livestreams, These incentives include: in game cosmetics, Unlockables, 
and 2x EXP Tokens. These items are unlocked at certain Milestones for watching the Live streams, 
with certian Unlockables requiring more than 10 Hours of watch time.


<b>Description: </b>

This Python Script was designed to automate the process involved with waiting, signing in, 
navigating and watching CDL Livestreams, Allowing the users to obtain the unlockable 
in game items that are rewarded for watching the CDL Live Stream events, With minimal effort.

To increase ease of use for demonstration purposes, all code for the project is contained
within one .py file/document, a production version of this code would be split up into related documents
making the code easier to manage/update.


<b>software requirements:</b>

- Must have python installed (This Script is designed for python 3.9)
	- Python 'selenium' Module (Script Created with v3.141.0)
	- As well as the Built-in Modules: (webbrowser, getpass, os, sys, time)
		- [Built-in Modules are already installed with python]

- Chromedriver WebDriver Must be installed
	- Program also requires chromedrivers directory path location 
	- (required by: users_info.txt)

- Google Chrome Must be installed
	- Program also requires chrome's directory path location 
	- (required by: users_info.txt)

<b>Using the | user_info.txt | file:</b>

- the User_info.txt file is a file used to contain the directory paths,
for: (Google Chrome & the ChromeDriver Web Driver) which are required by the script.

- Paste/type the required information required (file path) After the colon ':' inside [user_info.txt]

	  	NOTE:(script will RESET user_info.txt if it is modified/changed in any other way)

- If 'user_info.txt' is empty or does not exist, RUN the program once, and 'user_info.txt' 
will be created, once created ENTER the dirtectory paths for required items, 
then save and re-run the CDL Viewer Script

		- user_info.txt EXAMPLE:
		************************************************************************************
		*                                                                                  *
		*	chromedriver_path: C:\Program Files (x86)\chromedriver.exe                 *
		*	chrome_path: C:\Program Files (x86)\Google\Chrome\Application\chrome.exe   *
		*                                                                                  *
		************************************************************************************
	


<b>Important information:</b>

- At this point the application only works with google chrome, to recieve in game rewards,
 YouTube should be signed in on chrome (as webdriver module cannot sign in.)
  
- To recieve in game rewards, activision account must be linked to youtube account:
	- See: [ https://support.google.com/youtube/answer/9024948 ]

	 	NOTE: Therefore activision log in is optional but not essential to use script
	 	
	 	NOTE: (if siging into activision, do not set up 2 step authentication)

- PLEASE NOTE: Any Changes or updates made to the CDL Webpage can potentially break 
this script, and a patch will need to be pushed out.
			
		ALSO: When using this application the chrome / chromedriver tab 
		that is automatically opened must not be touched/used or
		the script will fail to find on screen elements.

	
<b>Future updates / Patches:</b>

- userbility Updates:
	- Additional Browsers to be added
	- Support for 2 step authentication for activision accounts

- Sercurity Updates:
	- Activision Password can be encrypted/hashed to avoid it beiong stored in plain text
