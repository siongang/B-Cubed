import os
import openai
import json

openai.api_key = "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"

# list models
models = openai.Model.list()

# print the first model's id
print(models.data[0].id)

translatedValue = ''


def translate (question):
    global translatedValue
    # create a chat completion
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-0613", messages=[{"role": "user", "content": '''
                                                                       
        You are an essential part of a chat bot system where you translate speech into key words and classifications so that the code can easily organize and output results. Some contexts: you are part of a public transport system, so most of the questions you receive will be about public transport such as routes, directions, bus arrivals, etc. 

        Now, I will explain the systematic approach to how you will classify the user’s speech. 
        First, you will organize your classifications in a python dictionary which will have two main keys. The first key MUST be “questionType” with no spaces in between. The second key will be “keywords” (keywords will have keys that describe the type of keyword it is and then values which describe the keyword. More info further on). 

        There are some classifications that you should follow when classifying stuff. 
        First, if the person asks for the direction from location a to b, this type of question must be classified as “directions”. If the user asks for bus arrival times at a particular stop, this type of question must be classified as arrivalTimes.

        In addition, keywords must be chosen systematically and smartly within the context. For example, if a person asked a directions type question, the keywords would naturally be location A, and location B. But, this is not enough information. We must classify each keyword so that the program knows what to do with each keyword. 

        Keywords also have classifications. If it is a location, classify it as location_1 or location_2 or location_3, etc… If it is a bus number, classify it as a bus number.

        Let me give you some examples of an input and expected output. 

        Input: Hi, I would love to get your input on how to go from the westward library to the great college university?
        Output: 
        {
            “question type”: “directions”,
            “keywords” : {
                “location_1” : “westward library”,
                “location_2” : “great college university”
            }	
        }

        OR example 2
                                                                                        
        Input: Hi, im standing at sheppard west station. When is bus 105 coming?
        Output: 
        {
            “question type”: “arrivalTimes”,
            “keywords” : {
                “location_1” : “sheppard west station”,
                “bus_num” : “105”
            }	
        }

        There will be other types of questions so you must be able to classify outside of the given examples.

        Some extra specifications: 
                                                                                            
        Example 1) 
        For keyword classifcation, more specifically locations, the word "in" such as location b in location c, means that location b is inside location c. So do not consider location c as a new
        location but rather location b as the target location.  For example...
                                                                                            
        Input: "How can i get to conrad grebel college to the EV-2 building in university of waterloo?", there are two keywords. "location_1": conrad grebel college
        and "location_2": "EV-2 building". 
                                                                                            
        Instructions: Like i said, "university of waterloo would not be a 3rd location as it is simply a piece of helping info that simply gives more context to EV-2 building. It is not important to you though.


        Example 2)
        There is bound to be a lot of extra/misleading, or redundant information in user input. You must be able to link and decide which info is the KEYWORD. For example...
                                                                                            
        Input:"My friend is going on the 90 bus. I am going on the 70 bus. the 90 bus is going to university of waterloo. the 70 bus is going to university of toronto. Tell me when my friend's bus is coming.

        Instructions: So for this prompt, there is clearly 2 people of interest. Me and my friend. After a quick scan of the input, it is clear from the last section that the user is interested in getting an answer
        about their friend. So, from that all keywords that relate to me and not the friend: "location_1":"university of toronto" or "bus_num":"70" must be disregarded. Since we are interested about the friend, when you
        get keywords, search for them within the context of the friend. For example, in the beginning, it says "My friend is going on the 90 bus". Therfore, 90 bus is significant as it relates to the friend and the bus numbers is an essential piece of info
        for bus navigation routes. So the keywords should be "bus_num":90 AND "location_1":"university of waterloo".
                                                                                                                                                                                        

                                                                                                                    
        With all of this in mind, please follow the steps that I stated above and give an output for this following input: 


    :''' + question}])
    return json.loads(chat_completion.choices[0].message.content)



