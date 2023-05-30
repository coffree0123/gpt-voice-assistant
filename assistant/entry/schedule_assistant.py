# General
from dotenv import load_dotenv

import os
import pandas as pd
import json
from langchain.experimental.autonomous_agents.autogpt.agent import AutoGPT
from langchain.chat_models import ChatOpenAI

from langchain.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain.docstore.document import Document
load_dotenv()  # take environment variables from .env.



# Tools
import os
from contextlib import contextmanager
from typing import Optional
from langchain.agents import tool
from langchain.tools.file_management.read import ReadFileTool
from langchain.tools.file_management.write import WriteFileTool

ROOT_DIR = "./data/"

dates = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
def format_date(s: str):
    s = s.lower()
    if s == 'mon' or s == 'monday':
        return 'Mon'
    elif s == 'tue' or s == 'tuesday':
        return 'Tue'
    elif s == 'wed' or s =='wednesday':
        return 'Wed'
    elif s == 'thu' or s == 'thur' or s == 'thursday':
        return 'Thu'
    elif s == 'fri' or s == 'friday':
        return 'Fri'
    elif s == 'sat' or s == 'saturday':
        return 'Sat'
    elif s == 'sun' or s == 'sunday':
        return 'Sun'
    return None
class Schedule():
    def __init__(self):
        self.schedule = dict()
        self.activities = set()
        self.num_activities = 0
        for date in dates:
            self.schedule[date] = dict()
    def add_activity(self, name, date, startTime, endTime):
        if (name, date, startTime, endTime) in self.activities:
            return "The activity is already exists!"
        self.schedule[date][name] = [startTime, endTime]
        self.activities.add((name, date, startTime, endTime))
        print(self)
        self.num_activities += 1
        return f"Successfully add the activity, there are {self.num_activities} activities."
    def remove_activity(self, name, date = None):
        if date is None:
            for d in dates:
                if name in self.schedule[d].keys():
                    start, end = self.schedule[d].pop(name)
                    self.activities.remove((name, d, start, end))
        else:
            start, end = self.schedule[d].pop(name)
            self.activities.remove((name, date, start, end))
        print(self)
    def reschedule(self, name, date, startTime, endTime):
        self.remove_activity(name)
        add_activity(name, date, startTime, endTime)
    def is_available(self, date, startTime, endTime):
        for start, end in self.schedule[date].values():
            if not (start >= endTime or end <= startTime):
                return False
        return True
    def __str__(self):
        res = ""  
        for date in dates:
            res += f"{date}:\n"
            events = list(self.schedule[date].items())
            events.sort(key=lambda x: x[1][0])
            for event in events:
                name = event[0]
                startTime = event[1][0]
                endTime = event[1][1]
                res += f"{name}: {startTime}:00~{endTime}:00\n"
            res += '\n'
        return res
schedule = Schedule()

@tool
def get_schedule():
    """This function returns the schedule of the user.
    """
    return str(schedule)

@tool
def add_activity(activity: str, date: str, startTime: int, endTime: int)->str:
    """Add exactly one activity into the schedule.\
    The activity starts at 'startTime' and end at 'endTime' (in hours).\
    The 'date' can only be 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'.\
    You should add the activity one by one.
    """
    date = format_date(date)
    print(activity, startTime, endTime, date, "add")
    res = schedule.add_activity(activity, date, startTime, endTime)
    return res
@tool
def remove_activity(activity: str, date: str)->str:
    """Remove exactly one activity on a specific date from the schedule.\
    The argument 'date' represents the date of the activity that we want to remove. \
    The 'date' can only be 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'.\
    You should add the activity one by one.
    """
    date = format_date(date)
    print(activity, 'remove')
    schedule.remove_activity(activity, date)
    return "Successfully remove the activity"

@tool
def is_available(date: str, startTime: int, endTime: int)->str:
    """Check if the time slot from 'startTime' to 'endTime' on 'date' is available.\
    'startTime' and 'endTime' are in hours.\
    The 'date' can only be 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'.
    """
    date = format_date(date)
    print(date, startTime, endTime, 'available')
    if schedule.is_available(date, startTime, endTime):
        return "Available !"
    else:
        return "Not available !"
@tool
def save_schedule()->str:
    """Save the current schedule to file. You can consider to finish your job after saving the file.
    """
    # if file_name is not None:
    #     with open(os.path.join(ROOT_DIR, file_name), 'w') as f:
    #         json.dump(schedule.schedule, f)
    #     return f"Save file to {file_name}."
    if not os.path.isdir(ROOT_DIR):
        os.mkdir(ROOT_DIR)
    with open(os.path.join(ROOT_DIR, 'schedule.json'), 'w') as f:
        json.dump(schedule.schedule, f)
    return "Save file to schedule.txt."
# Memory

import faiss
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.tools.human.tool import HumanInputRun

def build_schedule_agent():
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    embeddings_model = OpenAIEmbeddings()
    embedding_size = 1536
    index = faiss.IndexFlatL2(embedding_size)
    vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

    tools = [
        add_activity,
        remove_activity,
        is_available,
        get_schedule,
        save_schedule
        # reschedule_activity,
        # HumanInputRun(), # Activate if you want the permit asking for help from the human
    ]

    agent = AutoGPT.from_llm_and_tools(
        ai_name="Tom",
        ai_role="Assistant",
        tools=tools,
        llm=llm,
        memory=vectorstore.as_retriever(search_kwargs={"k": 8}),
        # human_in_the_loop=True, # Set to True if you want to add feedback at each step.
    )
    agent.max_iterations = 3
    return agent

if __name__ == '__main__':
    agent = build_schedule_agent()
    # agent.chain.verbose = True
    print(schedule)
    agent.run(["Hi, Tom. This is my to-do list of this week:\
                1. An AI course on Monday from 13:00 to 15:00.\
                2. A statistics course on Thursday from 15:00 to 17:00.\
            Please show me the final schedule of this week and save the final schedule.\
            "])

    # agent.run(["Hi, Tom. Can you give me a 14-hour Math study plan of this week?\
    #            Please also show me the final schedule."])
    print(schedule)
                # 2. An AI final project that takes me about 7 hours and must be finished before Wednsday.\
                # 4. One of my friends ask me if I can play basketball with him on Monday afternoon.\