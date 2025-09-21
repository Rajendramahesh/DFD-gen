from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from ingst import codebase_tree
import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from IPython.display import Markdown, display, update_display
from openai import OpenAI




# Initialize and constants

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith('sk-proj-') and len(api_key)>10:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key? Please visit the troubleshooting notebook!")
    
MODEL = 'gpt-4o-mini'
openai = OpenAI()

# Function to get user input for use case and format the prompt
def user_prompt_dfd():
    usecase = input("Enter the use case for the DFD:")
    return USER_PROMPT_TEMPLATE.format(usecase=usecase)



messages = [  
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt_dfd()}
        ]

# Tool function definition to ingest git repo
ingest_function = {
  "name": "codebase_tree",
  "description": "Ingest a git repository link and return the code base tree structure as a string. Call this function to understand the architecture and components of the codebase.",
  "strict": True,
  "parameters": {
    "type": "object",
    "properties": {
      "gitrepo_link": {
        "type": "string",
        "description": "URL to the Git repository to be ingested"
      }
    },
    "required": [
      "gitrepo_link"
    ],
    "additionalProperties": False
  }
}

# Include in list of tools
tools = [{"type": "function", "function": ingest_function}]

# Main function to generate DFD and threats
def generate_dfd_and_threats():
    response = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.2,
        tools=tools,
        max_tokens=1500,
    )
    if response.choices[0].finish_reason == "tool_calls":
        print("Tool call requested:")
        toolcalls = response.choices[0].message.tool_calls
        if toolcalls[0].function.name == "codebase_tree":
            print("tool name:", toolcalls[0].function.name)
            try :
                # Parse the JSON string to get the dictionary
                arguments = json.loads(toolcalls[0].function.arguments)
                gitrepo_link = arguments["gitrepo_link"]
                print("Ingesting codebase from:", gitrepo_link)
                tree = codebase_tree(gitrepo_link)
                print("Codebase tree structure obtained.", tree[:200], "...")
            except Exception as e:
                tree = f"Error parsing tool call arguments: {e}"
                print(tree)

            # Handle case where content might be None for tool calls
            assistant_content = response.choices[0].message.content or ""
            # Add the assistant message with tool_calls
            assistant_message = {
                "role": "assistant", 
                "content": assistant_content,
                "tool_calls": toolcalls
            }
            messages.append(assistant_message)
            messages.append({"role": "tool", "tool_call_id": toolcalls[0].id, "content": tree})
            #print(messages)

        # Make a new API call with the updated conversation
        second_response = openai.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.2,
            max_tokens=1500,
        )

    

    return second_response.choices[0].message.content

response_message = generate_dfd_and_threats()

parts = response_message.split("### Threat Analysis (STRIDE)")
print(parts[0])
#display(Markdown(parts[1])) #for only jupiter notebook
print("Threat Analysis (STRIDE)")
print(parts[1])


