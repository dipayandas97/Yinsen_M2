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
                response = self.openai.chat.completions.create(model="o3-mini",
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

                # use email api to send an email
                function_definition = self.aci.functions.get_definition("GMAIL__SEND_EMAIL")
                response = self.openai.chat.completions.create(model="o3-mini",
                                                               messages=[
                                                                    {
                                                                        "role": "system",
                                                                        "content": "You are a helpful assistant that can use gmail send email function to send an email on behalf of the user. \
                                                                            You will be given a set of instructions on how to create the email, in the form of a JSON like this: \
                                                                                { \
                                                                            'action': 'send', \
                                                                            'to': 'yash@gmail.com', \
                                                                            'from': 'dipayan@gmail.com', \
                                                                            'subject': 'Event Confirmation', \
                                                                            'content': 'Dear Yash,\n\nI hope this message finds you well. I wanted to confirm that I will see you at the event today. Looking forward to it!\n\nBest regards,\nDas' \
                                                                                }. \
                                                                            Use this information to send an email on behalf of the user. \
                                                                            Follow the function definition and the tool call format to send the email. \
                                                                            Any provided date and time format is DD/MM/YYYY and HH:MM."
                                                                    },
                                                                    {
                                                                        "role": "user",
                                                                        "content": f"use the email tool to send an email using the following information: {tool_response_dict['instructions']}",
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
                    "GMAIL__SEND_EMAIL",
                    json.loads(tool_call.function.arguments),
                    linked_account_owner_id=self.LINKED_ACCOUNT_OWNER_ID,
                )
                #print(f"DEBUG: Tool execution result inside toolbox.py: {result}")
                return result
            '''
            elif tool_response_dict['instructions']["action"] == "read":
                # use email api to read emails
                # 1. retrieve list of emails - in the form of IDs
                function_definition = self.aci.functions.get_definition("GMAIL__MESSAGES_LIST")
                print(f"DEBUG: Email view i inside toolbox.py: {tool_response_dict['instructions']}")
                response = self.openai.chat.completions.create(model="o3-mini",
                                                               messages=[
                                                                    {
                                                                        "role": "system",
                                                                        "content": "You are a helpful assistant that can use gmail message list function to view emails on behalf of the user. \
                                                                            You will be given a set of instructions regarding how to view the emails, in the form of a JSON. \
                                                                            The JSON can either be like:\
                                                                                { \
                                                                            'action': 'read', \
                                                                            'until_date': '29/03/2025' \
                                                                                }. \
                                                                            or like:\
                                                                                { \
                                                                            'action': 'read', \
                                                                            'last_n_emails': 10 \
                                                                                }. \
                                                                            Use this information to view the emails. \
                                                                            Follow the function definition and the tool call format to view the emails. \
                                                                            Any provided date format is DD/MM/YYYY."
                                                                    },
                                                                    {
                                                                        "role": "user",
                                                                        "content": f"use the email tool to view emails using the following information: {tool_response_dict['instructions']}",
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
                    "GMAIL__MESSAGES_LIST",
                    json.loads(tool_call.function.arguments),
                    linked_account_owner_id=self.LINKED_ACCOUNT_OWNER_ID,
                )
                print(f"DEBUG: Tool execution result inside toolbox.py: {result}")

                # here we get a list of email IDs like the following:

                #DEBUG: Tool execution result inside toolbox.py: success=True data={'messages': [{'id': '1960dfae71df3aa5', 'threadId': '1960dfae71df3aa5'}, {'id': '1960ddb5bf95d60e', 'threadId': '1960ddb5bf95d60e'}, {'id': '1960dcb8b8996882', 'threadId': '1960dcb8b8996882'}, {'id': '1960da14f79ddfbf', 'threadId': '1960da14f79ddfbf'}, {'id': '1960cc30a2a03694', 'threadId': '1960cc238ce2fa68'}, {'id': '1960cc238ce2fa68', 'threadId': '1960cc238ce2fa68'}, {'id': '19603f4130e0009c', 'threadId': '19603f4130e0009c'}, {'id': '19601a8d15b3ec9b', 'threadId': '19601a8d15b3ec9b'}, {'id': '196006191c98762f', 'threadId': '196006191c98762f'}, {'id': '195fc314e169ae21', 'threadId': '195fc314e169ae21'}], 'nextPageToken': '12565313761980251534', 'resultSizeEstimate': 201} error=None
            
                # 2. retrieve the email content
                function_definition = self.aci.functions.get_definition("GMAIL__MESSAGES_GET")
                response = self.openai.chat.completions.create(model="o3-mini",
                                                               messages=[
                                                                    {
                                                                        "role": "system",
                                                                        "content": "You are a helpful assistant that can use gmail message get function to view emails' content on behalf of the user. \
                                                                            You will be given a set of id and threadId of the emails, in the form of a JSON like the following: \
                                                                                {'messages': [{'id': '1960dfae71df3aa5', 'threadId': '1960dfae71df3aa5'}, {'id': '1960ddb5bf95d60e', 'threadId': '1960ddb5bf95d60e'}, {'id': '1960dcb8b8996882', 'threadId': '1960dcb8b8996882'}, {'id': '1960da14f79ddfbf', 'threadId': '1960da14f79ddfbf'}, {'id': '1960cc30a2a03694', 'threadId': '1960cc238ce2fa68'}, {'id': '1960cc238ce2fa68', 'threadId': '1960cc238ce2fa68'}, {'id': '19603f4130e0009c', 'threadId': '19603f4130e0009c'}, {'id': '19601a8d15b3ec9b', 'threadId': '19601a8d15b3ec9b'}, {'id': '196006191c98762f', 'threadId': '196006191c98762f'}, {'id': '195fc314e169ae21', 'threadId': '195fc314e169ae21'}], 'nextPageToken': '12565313761980251534', 'resultSizeEstimate': 201}\
                                                                            Use this information to view the content of the all the emails in the list. \
                                                                            Follow the function definition and the tool call format to view the emails. \
                                                                            Any provided date format is DD/MM/YYYY."
                                                                    },
                                                                    {
                                                                        "role": "user",
                                                                        "content": f"use the email tool to view the content of the emails using the following information: {result.data}",
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
                    "GMAIL__MESSAGES_GET",
                    json.loads(tool_call.function.arguments),
                    linked_account_owner_id=self.LINKED_ACCOUNT_OWNER_ID,
                )
                print(f"DEBUG: Tool execution result inside toolbox.py: {result}")



                return result
            '''

        elif tool_response_dict["tool"] == "expense_manager":
            
            if tool_response_dict['instructions']["action"] == "log_expense":
                # use expense manager tool to log an expense
                pass
            elif tool_response_dict['instructions']["action"] == "view_last_N_expenses":
                pass
            elif tool_response_dict['instructions']["action"] == "view_all_expenses":
                pass
            elif tool_response_dict['instructions']["action"] == "view_expenses_by_category":
                pass
            elif tool_response_dict['instructions']["action"] == "view_expenses_by_date":
                pass
            elif tool_response_dict['instructions']["action"] == "view_expenses_by_week":
                pass
            elif tool_response_dict['instructions']["action"] == "view_expenses_by_month":
                pass
            elif tool_response_dict['instructions']["action"] == "view_expenses_by_year":
                pass

        elif tool_response_dict["tool"] == "diary":
            if tool_response_dict['instructions']["action"] == "create_entry":
                pass
            elif tool_response_dict['instructions']["action"] == "view_entry":
                pass
            elif tool_response_dict['instructions']["action"] == "edit_entry":
                pass
            elif tool_response_dict['instructions']["action"] == "delete_entry":
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

{
  "tool": "email",
  "instructions": {
    "action": "read",
    "until_date": "29/03/2025",
  }
}


'''