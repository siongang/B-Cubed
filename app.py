import googlemaps
import re
from datetime import datetime

import prompt

gmaps = googlemaps.Client(key='AIzaSyAO4RHdC1cwGIBcURxvavRkt--wGz3RMqU')

def removeHtmlTags(text):
    text = text.replace('<b>','')
    text = text.replace('</b>','')
    text = text.replace('<wbr>','')
    text = text.replace('<wbr/>','')
    text = text.replace('<b>','')
    return text


# parameters to find directions
mode = 'transit'
origin = 'sheppard west station'
destination = ''

directions_result = ''


# current time
now = datetime.now()

# Request directions from the API THE MOST IMPORTANT PART OF THE PROGRAM
def setDirectionsResult(start, end):
    global directions_result
    global mode
    return gmaps.directions(start, end,mode,departure_time=now)


# INITIALIZING VARIABLES
# current location
currentLocation = 'Keele St / Steeles Av'

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
    global currentLocation
    currentLocation = location

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

    # main directions result
    directions_result = setDirectionsResult(origin, destination)
    # connects to map api
    setDirectionsResult(origin,destination)
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
    directions_result = gmaps.directions(origin, destination, mode,departure_time=now)
    step = directions_result[0]['legs'][0]['steps']
    for step in steps:
        return step['html_instructions']+'\n'
            

# when the bus will come 
def getBusDeparture(shortName):
    global steps
    for step in steps:
        if step['travel_mode'] == 'TRANSIT' and step['transit_details']['line']['short_name'] == shortName:
            return step['transit_details']['departure_time']['text']
        else:
            return 'Bus departure time not found'
        


# PROMPTS

questionType = ''
keywords = ''
while True:
    print('Hi, how are you!')
    userInput = input('ask me a question!')
    translatedValue = prompt.translate(userInput)

    # if (questionType == 'directions'):
    #     origin = translatedValue['keywords']['location_1']
    #     destination = translatedValue['keywords']['location_2']
    #     constructor()
    #     locationsCounts = sum (1 for key in keywords:   
    #                             if 'location' in key:
    #                                 print('hi')

    #                         )


    



print(translate("how to go from bc to toronto"))











# Get the estimated arrival time of the bus
def getBusArrival(bus_stop):
    directions = getDirections(origin, destination)
    if directions:
        for step in directions[0]['legs'][0]['steps']:
            if step['travel_mode'] == 'TRANSIT' and step['transit_details']['arrival_stop']['name'] == bus_stop:
                return step['transit_details']['arrival_time']['text']
    return 'Bus arrival time not found.'




# PROMPTS
print('Hi, how are you!')
print('commands: directions, bus arrival, bus departure, general')
userInput = input('type the command')

if userInput == 'directions':
    constructor()
    print(f'to go from {origin} to {destination}...\n {way}')

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


print('next step'+str(nextStep()))



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