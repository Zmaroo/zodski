import json

import autogen
from autogen.agentchat.contrib.agent_builder import AgentBuilder

config_file_or_env = "OAI_CONFIG_LIST"  # modify path
llm_config = {"temperature": 0}
config_list = autogen.config_list_from_json(config_file_or_env, filter_dict={"model": ["gpt-4-1106-preview", "gpt-4"]})


def start_task(execution_task: str, agent_list: list):
    group_chat = autogen.GroupChat(agents=agent_list, messages=[], max_round=12)
    manager = autogen.GroupChatManager(groupchat=group_chat, llm_config={"config_list": config_list, **llm_config})
    agent_list[0].initiate_chat(manager, message=execution_task)

library_path_or_json = "./Agent_Library/agentProfile.json"

building_task = "Analyze and develop preexisting Django project for producing accurate, artistic zodiac natal charts"

new_builder = AgentBuilder(
    config_file_or_env=config_file_or_env, builder_model="gpt-4-1106-preview", agent_model="gpt-4-1106-preview"
)
agent_list, _ = new_builder.build_from_library(building_task, library_path_or_json, llm_config)
start_task(
    execution_task="Access the Django project code base at C:/Users/marle/Zod/zodch on this local machine. Have appropriate agent familiarize other agents with the code base and functionality in the Charts app. Currently the project is set up for testing using selenium driver. The chart does not display corrrectly when the submit button is pushed to submit birth information on the the web browser. Develop code that will display the zodiac chart in an artistic rendering. This is a Windows 11 machine and the current directory is C:/Users/marle/Autogen",

    agent_list=agent_list,
)
new_builder.clear_all_agents()