from aipolabs import ACI
from aipolabs.types.functions import FunctionDefinitionFormat
from openai import OpenAI
import os
import json
class Toolbox:
    def __init__(self):
        self.aci = ACI()
        self.openai = OpenAI()

        self.LINKED_ACCOUNT_OWNER_ID = os.getenv("LINKED_ACCOUNT_OWNER_ID", "")

    def execute_tool(self, tool_response_dict: dict) -> dict:
        
        if tool_response_dict["tool"] == "calendar":
            if tool_response_dict['instructions']["action"] == "create":
                # use calender api to create a new event
                function_definition = self.aci.functions.get_definition("GOOGLE_CALENDAR__EVENTS_INSERT")
                response = self.openai.chat.completions.create(model="gpt-4o",
                                                               messages=[
                                                                    {
                                                                        "role": "system",
                                                                        "content": "You are a helpful assistant that can use the calender tool to create a new event. \
                                                                            You will be given a set of instructions on what to create, in the form of a JSON like this: \
                                                                                { \
                                                                            'action': 'create', \
                                                                            'start_time': '05/04/2025 15:00', \
                                                                            'end_time': '05/04/2025 16:00', \
                                                                            'description': 'OpenAI API payment' \
                                                                                }. \
                                                                            Use this information to create an event in your calendar. \
                                                                            Follow the function definition and the tool call format to create the event. \
                                                                            The provided date format is DD/MM/YYYY HH:MM. \
                                                                            The event should be created in the user's primary calendar. \
                                                                            The user's primary calendar is the one with the highest priority.\
                                                                            Also, infer the title of the event based on the description."
                                                                    },
                                                                    {
                                                                        "role": "user",
                                                                        "content": f"use the calender tool to schedule an event using the following information: {tool_response_dict['instructions']}",
                                                                    },
                                                                ],
                                                                tools=[function_definition],
                                                                tool_choice="required",  # force the model to generate a tool call for demo purposes
                                                                )
                #print(f"DEBUG: Response inside toolbox.py: {response}")
                tool_call = (
                    response.choices[0].message.tool_calls[0]
                    if response.choices[0].message.tool_calls
                    else None
                )
                print(f"DEBUG: Tool call inside toolbox.py: {tool_call}")
                result = self.aci.functions.execute(
                    "GOOGLE_CALENDAR__EVENTS_INSERT",
                    json.loads(tool_call.function.arguments),
                    linked_account_owner_id=self.LINKED_ACCOUNT_OWNER_ID,
                )
                #print(f"DEBUG: Tool execution result inside toolbox.py: {result}")
                return result

            elif tool_response_dict['instructions']["action"] == "view":
                function_definition = self.aci.functions.get_definition("GOOGLE_CALENDAR__EVENTS_LIST")
                response = self.openai.chat.completions.create(model="o3-mini",
                                                               messages=[
                                                                    {
                                                                        "role": "system",
                                                                        "content": "You are a helpful assistant that can use the calender tool to fetch events from the user's calendar. \
                                                                            You will be given a date, for which you need to fetch the events, in the form of a JSON like this: \
                                                                                { \
                                                                                'action': 'view', \
                                                                                'date': '05/04/2025', \
                                                                                }. \
                                                                            Use this information to fetch events from the user's calendar. \
                                                                            Follow the function definition and the tool call format to fetch the events. \
                                                                            The provided date format is DD/MM/YYYY. \
                                                                            The event should be fetched from the user's primary calendar. \
                                                                            The user's primary calendar is the one with the highest priority."                                                                    
                                                                    },
                                                                    {
                                                                        "role": "user",
                                                                        "content": f"use the calender tool to fetch events from the user's calendar using the following information: {tool_response_dict['instructions']}",
                                                                    },
                                                                ],
                                                                tools=[function_definition],
                                                                tool_choice="required",  # force the model to generate a tool call for demo purposes
                                                                )
                #print(f"DEBUG: Response inside toolbox.py: {response}")
                tool_call = (
                    response.choices[0].message.tool_calls[0]
                    if response.choices[0].message.tool_calls
                    else None
                )
                print(f"DEBUG: Tool call inside toolbox.py: {tool_call}")
                result = self.aci.functions.execute(
                    "GOOGLE_CALENDAR__EVENTS_LIST",
                    json.loads(tool_call.function.arguments),
                    linked_account_owner_id=self.LINKED_ACCOUNT_OWNER_ID,
                )
                #print(f"DEBUG: Tool execution result inside toolbox.py: {result}")
                return result
        
        elif tool_response_dict["tool"] == "email":

            if tool_response_dict['instructions']["action"] == "send":

                pass

            elif tool_response_dict['instructions']["action"] == "view":

                pass


'''
Calender:

Create event:
Tool response: {
  "tool": "calendar",
  "instructions": {
    "action": "create",
    "start_time": "05/04/2025 15:00",
    "end_time": "05/04/2025 16:00",
    "description": "OpenAI API payment",
    "location": "London"
  }
}
View event: 


------------------------
Email:

Send email:

Tool response: {
  "tool": "email",
  "instructions": {
    "action": "send",
    "to": "yash@gmail.com",
    "from": "dipayan@gmail.com",
    "subject": "Event Confirmation",
    "content": "Dear Yash,\n\nI hope this message finds you well. I wanted to confirm that I will see you at the event today. Looking forward to it!\n\nBest regards,\nDipayan"
  }
}

View emails:

'''