import googlemaps
import re
import os
from dotenv import load_dotenv
from datetime import datetime
import prompt

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment variable
maps_key = os.getenv("MAPS_KEY")

print(maps_key)
gmaps = googlemaps.Client(key=maps_key)

def removeHtmlTags(text):
    text = text.replace('<b>','')
    text = text.replace('</b>','')
    text = text.replace('<wbr>','')
    text = text.replace('<wbr/>','')
    text = text.replace('<b>','')
    return text


# parameters to find directions
transport = 'transit'
origin = 'sheppard west station'
destination = ''

directions_result = ''


# current time
now = datetime.now()



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

# SETTER FUNCTIONS

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
    way = ''
    print("origin " + origin)
    print("destination "+ str(destination))
    # main directions result
    directions_result = setDirectionsResult(origin, destination)
    # connects to map api
    setDirectionsResult(origin,destination)

    print
    # duration of the route
    duration = directions_result[0]['legs'][0]['duration']['text']
    # estimated arival time of the route
    arrivalTime = directions_result[0]['legs'][0]['arrival_time']['text']
    # departure time
    departureTime = directions_result[0]['legs'][0]['departure_time']['text']
    # steps
    steps = directions_result[0]['legs'][0]['steps']
    generalRoute()
    # print (duration )



def nextStep ():
        directions_result = gmaps.directions(origin, destination, mode=transport,departure_time=now)
        step = directions_result[0]['legs'][0]['steps']
        for step in steps:
            return step['html_instructions']+'\n'


   
# when the bus will come 
def getBusDeparture(shortName):
    global steps
    for step in steps:
        if step['travel_mode'] == 'TRANSIT' and step['transit_details']['line']['short_name'] == shortName:
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

    print(translatedValue)

    # counter of all the different locations the user is asking about
    locationCounter = 0

    # The type of question the user is asking
    questionType = translatedValue['questiontype']

    print("question type is " + questionType)

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
                 


    if questionType == "arrivalTimes":
        print('we are in arrival time')
        origin = originalBusStop
        destination = translatedValue['keywords']['location_1']
        name = translatedValue['keywords']['bus_num']

        print("origin "+origin)
        print("destination "+destination)
        print("name "+name)

        constructor()
        print(way)
        print(getBusDeparture(name))

    if userInput == "exit":
        break
    










# # PROMPTS
# print('Hi, how are you!')
# print('commands: directions, bus arrival, bus departure, general')
# userInput = input('type the command')

# if userInput == 'directions':
#     constructor()
#     print(f'to go from {origin} to {destination}...\n {way}')

# print('I will list a series of potential question that you may want to ask so please repeat when I list the final item\n')

# print('Do you want to know how to go from location A to B?')

# if input('type Y for yes and N for no') == 'Y':
#     origin = input('where are you right now?') # technically not needed cuz each hub knows its location. just for testing purposes
#     destination = input('where are you trying to go?')
#     constructor()
#     # prints directionsY
#     print(way)


# origin = input('where are you right now?') # technically not needed cuz each hub knows its location. just for testing purposes
# destination = input('where are you trying to go?')



# print()
# print(now)
# print('origin '+origin)
# print('destination '+destination)
# print('duration '+duration)
# print('arrival time ' + arrivalTime)
# print(way)
# print()



# when will the next bus arrive to the bus stop?





# del directions_result[]
# points = directions_result[0]['legs'][0]['steps'][0]['polyline']['points']




'''
# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))



# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)

# Validate an address with address validation
addressvalidation_result =  gmaps.addressvalidation(['1600 Amphitheatre Pk'], 
                                                    regionCode='US',
                                                    locality='Mountain View', 
                                                    enableUspsCass=True)
'''