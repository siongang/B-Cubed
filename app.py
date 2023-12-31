import googlemaps
import re
import os
from dotenv import load_dotenv
from datetime import datetime
import prompt
import speech

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment variable
maps_key = os.getenv("MAPS_KEY")

gmaps = googlemaps.Client(key=maps_key)

# parameters to find directions
transport = 'transit'
origin = ''
destination = ''

# the dictionary that contains all the information about the route
directions_result = ''

# current time
now = datetime.now()

# removes unnecessary tags
def removeHtmlTags(text):
    text = text.replace('<b>','')
    text = text.replace('</b>','')
    text = text.replace('<wbr>','')
    text = text.replace('<wbr/>','')
    text = text.replace('<b>','')
    return text


# Request directions from the API THE MOST IMPORTANT PART OF THE PROGRAM
def setDirectionsResult(start, end):
    global directions_result
    global transport
    return gmaps.directions(start, end,mode=transport,departure_time=now)


# INITIALIZING VARIABLES
# current location
originalBusStop = '82 Pantano Drive, Thornhill, Ontario'

# the steps of the route
way = "" 

# duration of the route
duration = ''

# estimated arival time of the route
arrivalTime = ''

# departure time
departureTime = ''

# the next step in the bus route
nextStep = ''

# steps
steps = ''

# FUNCTIONS

# different flow from the locatioin
def setCurrentLocation(location):
    global originalBusStop
    originalBusStop = location

# sets the 'way' variable to the steps 
def generalRoute (): 
    global way
    # Process the directions result
    if directions_result:
        # Access the steps of the directions
        for step in steps:
            way = way + step['html_instructions']+'\n'
    else:
        way = 'No directions found.'
    way = removeHtmlTags(way)
    


# constructor
def constructor():
    global duration
    global arrivalTime
    global departureTime
    global steps
    global directions_result 
    global way
    global now
    way = ''

    # current time
    now = datetime.now()
    
    # main directions result
    directions_result = setDirectionsResult(origin, destination)
    # connects to map api
    setDirectionsResult(origin,destination)
    # print(directions_result)
    # duration of the route
    duration = directions_result[0]['legs'][0]['duration']['text']
    # estimated arival time of the route
    arrivalTime = directions_result[0]['legs'][0]['arrival_time']['text']
    # departure time
    departureTime = directions_result[0]['legs'][0]['departure_time']['text']
    # steps
    steps = directions_result[0]['legs'][0]['steps']
    generalRoute()


def nextStep ():
        directions_result = gmaps.directions(origin, destination, mode=transport,departure_time=now)
        step = directions_result[0]['legs'][0]['steps']
        for step in steps:
            return step['html_instructions']+'\n'


   
# when the bus will come 
def getBusDeparture(shortName):
    global steps
    for step in steps:
        if step['travel_mode'] == 'TRANSIT':
            if step['transit_details']['line']['short_name'] == shortName:
                return step['transit_details']['departure_time']['text']
    return 'Bus departure time was not found'
        

# PROMPTS
keywords = ''

while True:
    # user input
    print('Hi, how are you!')
    userInput = input('ask me a question!')

    # json file type
    translatedValue = prompt.translate(userInput)
    # print(translatedValue)

    # counter of all the different locations the user is asking about
    locationCounter = 0

    # The type of question the user is asking
    questionType = translatedValue['questiontype']

    # how many locations did the user input?
    for key, value in translatedValue['keywords'].items(): 
        if 'location' in key:
            locationCounter+=1

    # If user is asking for directions
    if (questionType == 'directions'):
        origin = translatedValue['keywords']['location_1']
        destination = translatedValue['keywords']['location_2']
        constructor()
        print(way)
        speech.tts(way)

    # if user is asking for bus arrial timees             
    if questionType == "arrivalTimes":
        origin = originalBusStop
        destination = translatedValue['keywords']['location_1']
        name = translatedValue['keywords']['bus_num']
        constructor()
        print(getBusDeparture(name))
        speech.tts(getBusDeparture(name))

    # use exits
    if userInput == "exit":
        break
    





