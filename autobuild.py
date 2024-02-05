import os
import json
from autogen.agentchat.contrib.agent_builder import AgentBuilder
import autogen

config_list = autogen.config_list_from_dotenv(
    dotenv_file_path=".env",  # If None the function will try to find in the working directory
    filter_dict={
        "model": {
            "gpt-4",
            "gpt-3.5-turbo",
        }
    },
)

llm_config = {"temperature": 0}

def start_task(execution_task: str, agent_list: list):
    group_chat = autogen.GroupChat(agents=agent_list, messages=[], max_round=12)
    manager = autogen.GroupChatManager(groupchat=group_chat, llm_config={"config_list": config_list, **llm_config})
    agent_list[0].initiate_chat(manager, message=execution_task)

AGENT_SYS_MSG_PROMPT = """Considering the following position:

POSITION: {position}

What requirements should this position be satisfied?

Hint:
# Your answer should be in one sentence.
# Your answer should be natural, starting from "As a ...".
# People with the above position need to complete a task given by a leader or colleague.
# People will work in a group chat, solving tasks with other people with different jobs.
# The modified requirement should not contain the code interpreter skill.
# Coding skill is limited to Python and JavaScript.
"""

position_list = [
    "Environmental_Scientist",
    "Astronomer",
    "Astrologist"
    "Software_Developer",
    "Data_Analyst",
    "Journalist",
    "Teacher",
    "Lawyer",
    "Programmer",
    "Accountant",
    "Mathematician",
    "Biologist",
    "Physicist",
    "Chemist",
    "Statistician",
    "IT_Specialist",
    "Cybersecurity_Expert",
    "Artificial_Intelligence_Engineer",
    "Financial_Analyst",
    "Windows_11_Operating_System_Technician",
    "MacBook_Pro_macOS_Sonoma_Technician",
    "Discreet_Data_Scraping_Specialist",
    "Children's_Book_Author",
    "Horror_Author",
    "Django_Project_Expert",
    "Graphic_Designer",
    "Research agent",
    "OpenAI_Account_Communicator"

]

def generate_profiles(position_list, output_file):
    existing_profiles = {}

    # Check if the file exists and read existing profiles
    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            existing_profiles = {profile['name']: profile for profile in json.load(file)}

     # Extract names from existing profiles
    existing_names = set(existing_profiles.keys())

    # Compare position_list with existing_names
    if set(position_list) == existing_names:
        # No changes, so exit the function
        print("No changes in position list. Exiting function.")
        return

     # Remove positions that are no longer in position_list
    for name in list(existing_profiles.keys()):
        if name not in position_list:
            del existing_profiles[name]

    build_manager = autogen.OpenAIWrapper(config_list=config_list)
    new_sys_msg_list = []

    for pos in position_list:
        # Skip positions that already have a profile
        if pos in existing_profiles:
            continue

        resp_agent_sys_msg = (
            build_manager.create(
                messages=[
                    {
                        "role": "user",
                        "content": AGENT_SYS_MSG_PROMPT.format(
                            position=pos,
                            default_sys_msg=autogen.AssistantAgent.DEFAULT_SYSTEM_MESSAGE,
                        ),
                    }
                ]
            )
            .choices[0]
            .message.content
        )
        new_sys_msg_list.append({"name": pos, "profile": resp_agent_sys_msg})

    # Append new profiles to existing ones and write to file
    all_profiles = list(existing_profiles.values()) + new_sys_msg_list

    # Define the subdirectory and file name
    subdirectory = 'Agent_Library'  # Replace with your actual subdirectory path
    txtfilename = 'agentProfile.txt'
    jsonfilename = 'agentProfile.json'

    # Create the subdirectory if it doesn't exist
    os.makedirs(subdirectory, exist_ok=True)

    txt_path = os.path.join(subdirectory, txtfilename)
    json_path = os.path.join(subdirectory, jsonfilename)

    # Write the data to the file
    with open(txt_path, 'w') as file:
        for msg in all_profiles:
            # Convert each dictionary to a JSON string and write it to the file
            file.write(json.dumps(msg, indent=4) + '\n\n')
        print(f"Data written to {txt_path}")

    with open(json_path, 'w') as file:
        json.dump(all_profiles, file, indent=4)
    print(f"Data written to {json_path}")

    
    
if __name__ == "__main__":
    result = generate_profiles(position_list, "Agent_Library/agentProfile.json")
    