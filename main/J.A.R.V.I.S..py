import webbrowser
import datetime
import speech_recognition as sr
import wikipedia
import os
import pyttsx3
import socket
import requests
import speedtest
import geocoder
import pyowm

st = speedtest.Speedtest()
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

engine = pyttsx3.init('sapi5')
voices= engine.getProperty('voices') #getting details of current voice
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', 1.0)

WAKE = 'jarvis'
checkInternet = ""

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        print("Good Morning Sir!, Have A good Day!")
        speak("Good Morning Sir!, Have A good Day!")
    elif hour >= 12 and hour < 18:
        print("Good Afternoon Sir!")
        speak("Good Afternoon Sir!")
    elif hour >= 18 and hour < 20:
        print("Good Evening Sir!")
        speak("Good Evening Sir!")
    else:
        print("Good Night Sir!")
        speak("Good Night Sir!")
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"Sir, the time is {strTime} in India and {weather()} in Barasat, West Bengal")
    speak(f"Sir, the time is {strTime} in India and {weather()} in Barasat, West Bengal")

def weather():
    home = location()
    owm = pyowm.OWM('47a88494d903060bbc708e0817e0ba8c')
    mgr = owm.weather_manager()

    observation = mgr.weather_at_place(home)
    w = observation.weather
    temp = w.temperature('celsius')
    status = w.detailed_status
    answer = ("It is currently " + str(int(temp['temp'])) + " degrees celcius and " + status)
    return answer

def aboutMe():
    print('Sir I am Jarvis, simple Speech Assistant AI created by my boss Mr. Souradeep Banerjee. I can perform simple '
          'tasks like opening some common websites like google youtube excetra, and opening some other common '
          'applications like chrome excetra. But I am built to learn more! I will be developed more advanced by my '
          'boss Souradeep in the near future! I wish that everyone on this world should become well in the pandemic '
          'of COVID 19.')
    speak('Sir I am Jarvis, simple Speech Assistant AI created by my boss Mr. Souradeep Banerjee. I can perform simple '
          'tasks like opening some common websites like google youtube excetra, and opening some other common '
          'applications like chrome excetra. But I am built to learn more! I will be developed more advanced by my '
          'boss Souradeep in the near future! I wish that everyone on this world should become well in the pandemic '
          'of COVID 19.')

def shutDown():
    print('Shutting down.. Goodbye sir, have a good day!')
    speak('Shutting down.. Goodbye sir, have a good day!')

def favourite_music():
    fav_music_url = 'https://www.youtube.com/watch?v=83RUhxsfLWs&ab_channel=NEFFEX'
    webbrowser.get(chrome_path).open(fav_music_url)


def playonyt(topic):
    """Will play video on following topic, takes about 10 to 15 seconds to load"""
    url = 'https://www.youtube.com/results?q=' + topic
    count = 0
    cont = requests.get(url)
    data = cont.content
    data = str(data)
    lst = data.split('"')
    for i in lst:
        count += 1
        if i == 'WEB_PAGE_TYPE_WATCH':
            break
    if lst[count - 5] == "/results":
        raise Exception("No video found.")

    webbrowser.open("https://www.youtube.com" + lst[count - 5])
    return "https://www.youtube.com" + lst[count - 5]


def checkInternetOnOff():
    try:
        socket.create_connection(('google.com', 80))
        checkInternet = "You have an internet connection"
        return checkInternet
    except OSError:
        checkInternet = "You don't have an internet connction"
        return checkInternet

def connectionToServer():
    try:
        socket.create_connection(('google.com', 80))
        checkInternet = "Connecting to server successful. I am online and ready to be used.."
        return checkInternet
    except OSError:
        checkInternet = "Connecting to server unsuccessful. You do not have an internet connection. Pleasse connect to the internet for enjoying all services!"
        return checkInternet

def location():
    g = geocoder.ip('me')
    g = g.geojson
    g = g['features'][0]['properties']
    location = str(g['address'] + 'DIA')
    return location

def runJarvisInMic():
    print('How can I help You?')
    speak('How can I help You?')
    query1 = takeCommand().lower()

    if 'who are you' in query1:
        aboutMe()
    elif 'wikipedia' in query1:
        print('Searching Wikipedia...')
        speak('Searching Wikipedia...')
        query1 = query1.replace("wikipedia", "")
        results = wikipedia.summary(query1, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    elif 'open youtube' in query1:
        print('Opening Youtube!')
        speak('Opening Youtube!')
        webbrowser.get(chrome_path).open("youtube.com")
    elif 'open google' in query1:
        print('Opening Google!')
        speak('Opening Google!')
        webbrowser.get(chrome_path).open("google.com")
    elif 'bye' in query1:
        shutDown()
        exit()
    elif 'shutdown' in query1:
        shutDown()
        exit()
    elif 'time' in query1:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"Sir, the time is {strTime}")
        speak(f"Sir, the time is {strTime}")
    elif 'open chrome' in query1:
        filePath = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
        os.startfile(filePath)
        print('Opening Chrome!')
        speak('Opening Chrome!')
    elif 'play' in query1:
        if 'music' in query1:
            if 'favourite' in query1:
                print("Playing your favourite music!")
                speak("Playing your favourite music!")
                favourite_music()
            else:
                print('What music do you want me to play?')
                speak('What music do you want me to play?')
                playmusic = takeCommand().lower()
                print('Playing' + playmusic)
                speak('Playing' + playmusic)
                playonyt(playmusic)
        elif 'video' in query1:
            print('What video do you want me to play?')
            speak('What video do you want me to play?')
            playvideo = takeCommand().lower()
            print('Playing' + playvideo)
            speak('Playing' + playvideo)
            playonyt(playvideo)
        elif 'favourite song' in query1:
            print("Playing your Favourite Song...")
            speak("Playing your Favourite Song")
            favourite_music()
    elif 'hey' in query1:
        print('Hi, how can I help you?')
        speak('Hi, how can I help you?')
    elif 'make a google search' in query1:
        print('What do you want to search for?')
        speak('What do you want to search for?')
        search = takeCommand().lower()
        url = 'https://www.google.com/search?q=' + search
        webbrowser.get(chrome_path).open(url)
    elif 'your name' in query1:
        print('Sir, I am Jarvis!')
        speak('Sir, I am Jarvis!')
    elif 'my name' in query1:
        print('Sir, Your Name is Souradeep Banerjee!')
        speak('Sir, Your Name is Souradeep Banerjee!')
    elif 'hi' in query1:
        print('Hi, how can I help you?')
        speak('Hi, how can I help you?')
    elif 'calculator' in query1:
        print("Opening calculator")
        speak('Opening calculator')
        calcpath = "C:\Windows\System32\calc.exe"
        os.startfile(calcpath)
    elif 'word' in query1:
        print("Opening word")
        speak('Opening word')
        wordpath = "C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.exe"
        os.startfile(wordpath)
    elif 'excel' in query1:
        print("Opening excel")
        speak('Opening excel')
        excelpath = "C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
        os.startfile(excelpath)
    elif 'change user input' in query1:
        print("Do you want to change user input to Keyboard? (Say 'Yes' if you agree or 'No' if you don't): ")
        speak("Do you want to change user input to Keyboard?")
        ask_to_change_Input = takeCommand().lower()
        if 'yes' in ask_to_change_Input:
            print('Changing user input to Keyboard...')
            speak('Changing user input to Keyboard')
            optionKeyboard()
        else:
            print("User input is not changed to Keyboard...")
            speak("User input is not changed to Keyboard")
    elif 'internet connection' in query1:
        print(checkInternetOnOff())
        speak(checkInternetOnOff())
    elif 'internet speed' in query1:
        print('This process will take around 30 seconds. Please wait.')
        speak('This process will take around 30 seconds. Please wait.')
        downspeed = str(round(st.download() / 1000000, 2)) + ' mb per second'
        upspeed = str(round(st.upload() / 1000000, 2)) + ' mb per second'
        print('Sir, your download speed is ' + downspeed + ' and your upload speed is ' + upspeed)
        speak('Sir, your download speed is ' + downspeed + 'and your upload speed is ' + upspeed)
    elif 'location' in query1:
        print(f"Sir, your current location based on your IP Address is {location()}.")
        speak(f"Sir, your current location based on your IP Address is {location()}.")
    elif 'help menu' in query1:
        help()
    elif 'hello' in query1:
        print('Hello Sir')
        speak('Hello Sir')
    elif 'how are you' in query1:
        speak("I'm fine Sir!")
        print("I'm fiine Sir!")
    elif 'you there' in query1:
        print('For you Sir, always.')
        speak('For you Sir, always.')
    elif 'weather' in query1:
        w = weather()
        print(w)
        speak(w)
    elif 'open stack overflow' in query1:
        print("Opening Stack Overflow!")
        speak('Opening Stack Overflow!')
        webbrowser.get(chrome_path).open("https://www.stackoverflow.com/")
    elif 'open git hub' in query1:
        print("Opening GitHub!")
        speak('Opening Git Hub!')
        webbrowser.get(chrome_path).open("https://www.github.com/")
    elif 'open facebook' in query1:
        print("Opening FaceBook!")
        speak('Opening Facebook!')
        webbrowser.get(chrome_path).open("https://www.facebook.com/")
    elif 'open twitter' in query1:
        print("Opening Twitter!")
        speak('Opening Twitter!')
        webbrowser.get(chrome_path).open("https://www.twitter.com/home")
    elif 'help' in query1:
        print('Showing All Commands!')
        speak('Showing all commands!')
        commands()

def takeCommand():

    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source)
            r.dynamic_energy_threshold = 3000
            r.pause_threshold = 1
            audio = r.listen(source, timeout=5.0)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            query = query.lower()
            print(f"You said: {query}\n")
    except Exception as e:
        pass
        return "None"
    return query

def optionMic():
    while True:
        print("Say Jarvis to wake me up... ")
        query = takeCommand().lower()
        if WAKE in query:
            runJarvisInMic()
        else:
            continue

def optionKeyboard():
    print('How can I help You?')
    speak('How can I help You?')

    while True:
        runJarvisInKeyboard()

def runJarvisInKeyboard():
    query1 = input("Enter your command: ").lower()

    if 'who are you' in query1:
        aboutMe()
    elif 'wikipedia' in query1:
        print('Searching Wikipedia...')
        speak('Searching Wikipedia...')
        query1 = query1.replace("wikipedia", "")
        results = wikipedia.summary(query1, sentences=2)
        print("According to Wikipedia...")
        speak("According to Wikipedia")
        print(results)
        speak(results)
    elif 'open youtube' in query1:
        print('Opening Youtube!')
        speak('Opening Youtube!')
        webbrowser.get(chrome_path).open("youtube.com")
    elif 'open google' in query1:
        print('Opening Google!')
        speak('Opening Google!')
        webbrowser.get(chrome_path).open("google.com")
    elif 'bye' in query1:
        shutDown()
        exit()
    elif 'shutdown' in query1:
        shutDown()
        exit()
    elif 'time' in query1:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"Sir, the time is {strTime}")
        speak(f"Sir, the time is {strTime}")
    elif 'open chrome' in query1:
        filePath = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
        os.startfile(filePath)
        print('Opening Chrome!')
        speak('Opening Chrome!')
    elif 'play' in query1:
        if 'music' in query1:
            if 'favourite' in query1:
                print("Playing your favourite music!")
                speak("Playing your favourite music!")
                favourite_music()
            else:
                print('What music do you want me to play?')
                speak('What music do you want me to play?')
                playmusic = input('Enter the name of the music:').lower()
                print('Playing' + playmusic)
                speak('Playing' + playmusic)
                playonyt(playmusic)
        elif 'video' in query1:
            print('What video do you want me to play?')
            speak('What video do you want me to play?')
            playvideo = input('Enter the name of the video:').lower()
            print('Playing' + playvideo)
            speak('Playing' + playvideo)
            playonyt(playvideo)
        elif 'favourite song' in query1:
            print("Playing your Favourite Song...")
            speak("Playing your Favourite Song")
            favourite_music()
    elif 'hey' in query1:
        print('Hi, how can I help you?')
        speak('Hi, how can I help you?')
    elif 'make a google search' in query1:
        print('What do you want to search for?')
        speak('What do you want to search for?')
        search = input('What do you want to search for? ').lower()
        url = 'https://www.google.com/search?q=' + search
        print(f"Searching {search}")
        speak(f"Searching {search}")
        webbrowser.get(chrome_path).open(url)
    elif 'your name' in query1:
        print('Sir, I am Jarvis!')
        speak('Sir, I am Jarvis!')
    elif 'my name' in query1:
        print('Sir, Your Name is Souradeep Banerjee!')
        speak('Sir, Your Name is Souradeep Banerjee!')
    elif 'hi' in query1:
        print('Hi, how can I help you?')
        speak('Hi, how can I help you?')
    elif 'calculator' in query1:
        print("Opening calculator")
        speak('Opening calculator')
        calcpath = "C:\Windows\System32\calc.exe"
        os.startfile(calcpath)
    elif 'word' in query1:
        print("Opening word")
        speak('Opening word')
        wordpath = "C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
        os.startfile(wordpath)
    elif 'excel' in query1:
        print("Opening excel")
        speak('Opening excel')
        excelpath = "C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
        os.startfile(excelpath)
    elif 'change user input' in query1:
        speak("Do you want to change user input to Mic?")
        ask_to_change_Input = input("Do you want to change user input to Mic? (Type 'Yes' if you agree or 'No' if you don't): ").lower()
        if 'yes' in ask_to_change_Input:
            print('Changing user input to Mic...')
            speak('Changing user input to Mic')
            optionMic()
        else:
            print("User input is not changed to Mic...")
            speak("User input is not changed to Mic")
    elif 'internet connection' in query1:
        print(checkInternetOnOff())
        speak(checkInternetOnOff())
    elif 'internet speed' in query1:
        print('This process will take around 30 seconds. Please wait.')
        speak('This process will take around 30 seconds. Please wait.')
        downspeed = str(round(st.download()/1000000, 2)) + ' mb per second'
        upspeed = str(round(st.upload()/1000000, 2)) + ' mb per second'
        print('Sir, your download speed is ' + downspeed + ' and your upload speed is ' + upspeed)
        speak('Sir, your download speed is ' + downspeed + 'and your upload speed is ' + upspeed)
    elif 'location' in query1:
        print(f"Sir, your current location based on your IP Address is {location()}.")
        speak(f"Sir, your current location based on your IP Address is {location()}.")
    elif 'help menu' in query1:
        help()
    elif 'hello' in query1:
        print('Hello Sir')
        speak('Hello Sir')
    elif 'how are you' in query1:
        print("I'm fine Sir!")
        speak("I'm fine Sir!")
    elif 'you there' in query1:
        print('For you Sir, always.')
        speak('For you Sir, always.')
    elif 'weather' in query1:
        w = weather()
        print(w)
        speak(w)
    elif 'open stack overflow' in query1:
        print("Opening Stack Overflow!")
        speak('Opening Stack Overflow!')
        webbrowser.get(chrome_path).open("https://www.stackoverflow.com/")
    elif 'open git hub' in query1:
        print("Opening GitHub!")
        speak('Opening Git Hub!')
        webbrowser.get(chrome_path).open("https://www.github.com/")
    elif 'open facebook' in query1:
        print("Opening FaceBook!")
        speak('Opening Facebook!')
        webbrowser.get(chrome_path).open("https://www.facebook.com/")
    elif 'open twitter' in query1:
        print("Opening Twitter!")
        speak('Opening Twitter!')
        webbrowser.get(chrome_path).open("https://www.twitter.com/home")
    elif 'help' in query1:
        print('Showing All Commands!')
        speak('Showing all commands!')
        commands()

def commands():
    print(
        "                ======================================================= - COMMANDS - =======================================================")

    print('''
                    1. who are you                                                         ----- tells about jarvis
                    2. wikipedia of <someone / something>                                  ----- finds out the wikipedia of someone or something
                    3. open youtube                                                        ----- opens youtube in chrome
                    4. open google                                                         ----- opens google in chrome
                    5. shutdown / bye                                                      ----- shutdowns the program
                    6. time                                                                ----- tells you the current time
                    7. open chrome                                                         ----- opens chrome
                    8. play --- (i) music                                                  ----- plays the music of your choice
                                (ii) favorite music                                        ----- plays your favorite music
                                (iii) video                                                ----- plays the video of your choice
                                (iv) favorite song (alternative of <favorite music>)       ----- plays your favorite music
                    9. hey                                                                 ----- jarvis will greet you
                    10. make a google search                                               ----- makes your desired search in google
                    11. your name                                                          ----- tells the name of AI
                    12. my name                                                            ----- tells your name
                    13. hi (alternative of hey)                                            ----- jarvis will greet you
                    14. calculator                                                         ----- opens calculator
                    15. word                                                               ----- opens MS Word
                    16. excel                                                              ----- opens MS Excel
                    17. change user input                                                  ----- changes user input to mic or keyboard
                    18. internet connection                                                ----- checks if you have an internet connection
                    19. internet speed                                                     ----- checks your upload and download speed
                    20. location                                                           ----- tells your current location
                    21. help menu                                                          ----- shows the help menu
                    22. hello                                                              ----- jarvis will greet you
                    23. how are you                                                        ----- will tell you how he is
                    24. are you up                                                         ----- tells the iconic dialogue given by J.A.R.V.I.S 
                    25. weather                                                            ----- tells the weather of your home
                    26. open stack overflow                                                ----- opens www.stackoverflow.com
                    27. open git hub                                                       ----- opens www.github.com
                    28. open facebook                                                      ----- opens www.facebook.com
                    29. open twitter                                                       ----- opens www.twitter.com
                    30. help                                                               ----- shows all commands
                    
                    Note: (IMPORTANT!) These are the keywords which you have to mention in your speech inorder to make jarvis work perfectly.



                ''')

def startup():
    print("""
           __       ___        ____     _    __       ____      _____
          / /      /   |      / __ \   | |  / /      /  _/     / ___/
     __  / /      / /| |     / /_/ /   | | / /       / /       \__ \ 
    / /_/ /   _  / ___ | _  / _, _/  _ | |/ /   _  _/ /    _  ___/ / 
    \____/   (_)/_/  |_|(_)/_/ |_|  (_)|___/   (_)/___/   (_)/____/  
                                                                     """)
    print('=============== - Coded by Souradeep Banerjee - ===============')

    print('========================== - MENU - ===========================')
    print("""
                 1. About Us
                 2. Speak Through Mic 
                 3. Type In Keyboard 
                 4. Help
                 5. Features
                 6. Skills
                 7. Exit

                 Note: 1. Make sure to remember the correct keyword to make J.A.R.V.I.S understand your query.
                       2. If you have forgotten the keywords please review the commands (keywords) by going to
                          "Help > All Commands".
                       3. To wake J.A.R.V.I.S up, speak "Jarvis" when he is listening to you.(Only Applicable in
                          "Speak Through Mic Option".
                       4. If you want to change user input, type or speak to J.A.R.V.I.S by giving him the 
                          command "Change User Input" and continue.
                       5. To use a choice from the above menu, please enter your choice by typing the 
                          serial numbers of the desired function.
                       """)
    speak('Preparing startup protocols. Connecting to the Server.')
    speak(connectionToServer())
    wishMe()
    speak("Please choose your desired choice from the above menu.")


    while True:
        choice = int(input('Enter your Choice: '))

        if choice == 1:
            about()
        elif choice == 2:
            print('Initiating input via Speak Through Mic!')
            speak('Initiating input via Speak Through Mic')
            optionMic()
        elif choice == 3:
            print('Initiating input via Type In Keyboard!')
            speak('Initiating input via Type In Keyboard')
            optionKeyboard()
        elif choice == 4:
            print('Help at your service!')
            speak('Help at your service')
            help()
        elif choice == 5:
            print('Showing my features!')
            speak('Showing my features')
            features()
        elif choice == 6:
            print('Showing what I can do!')
            speak('Showing what I can do')
            skills()
        elif choice == 7:
            print('Thank you for spending your precious time with me. I hope you will come again.')
            speak('Thank you for spending your precious time with me. I hope you will come again.')
            exit()
        else:
            print('Wrong input.. Try Again!')
            speak('Wrong input, try again')



def help():
    while(True):
        print("""********** HELP MENU **********
                
                VERSION - 1.0
                
                1. About Us
                2. All Commands
                3. Exit to Main Menu
              """)
        ch = int(input('Enter Choice: '))
        if ch < 0 and ch > 3:
            print('Please enter your choice between the range of 1 to 3')
            speak('Please enter your choice between the range of 1 to 3')
        else:

            if ch == 1:
                about()
            elif ch == 2:
                commands()
            else:
                startup()

def about():
    print("            ======================================================= - ABOUT - =======================================================")
    print("""
            Hey there, I am J.A.R.V.I.S., your personal A.I. Speech Assistant. I was developed by Souradeep Banerjee in between the years 2020 – 2021. 
            I am developed to solve simple problems asked by the user. 
            I will be developed more advanced by my developer Souradeep in the near future. 
            For now, I am just a speech assistant used on terminal of Windows Operating System. 
            I am able to run in other operating systems as well but some of my abilities won’t work in their interface. 
            Thank you!

            Contact Developer: 
                Name: Souradeep Banerjee
                Email: rishibanerjee1101@gmail.com
                Employment: Student
             
            By Developer: I am thankful and grateful to CodeWithHarry (YouTube Channel: https://www.youtube.com/channel/UCeVMnSShP_Iviwkknt83cww), 
                          who inspired me in developing this wonderful project and modifying it according to my wish.
        """)
    while (True):
        ch = input("Type <y> to exit to Main Menu: ")
        if ch != 'y':
            print("Please enter <y> in order to exit to Main Menu.")
        else:
            startup()
def features():
    print("          ======================================================= - FEATURES - =======================================================")
    print("""
          1. Supports two different user input modes (text or speech), user can write or speak in the mic.
          2. Change input mode on run time.
          3. Gives both Vocal and Text Response.
    """)
    while (True):
        ch = input("Type <y> to exit to Main Menu: ")
        if ch != 'y':
            print("Please enter <y> in order to exit to Main Menu.")
        else:
            startup()
def skills():
    print("          ======================================================= - SKILLS - =======================================================")
    print("""
          1. Can open common websites like Youtube, Google, etc.
          2. Can show the wikipedia of someone / something.
          3. Can tell the Time.
          4. Can open Google Chrome as the default Web browser.
          5. Can make a Google Search.
          6. Can open Calculator, MS Excel and MS Word.
          7. Can Change User Input from Mic to Keyboard and Vice-Versa.
          8. Can tell if the user has an Internet Connection or not.
          9. Can tell the Weather and User's current Location.
          10. Can tell the Internet Speed.
    """)
    while(True):
        ch = input("Type <y> to exit to Main Menu: ")
        if ch != 'y':
            print("Please enter <y> in order to exit to Main Menu.")
        else:
            startup()


if __name__ == "__main__":
    startup()



