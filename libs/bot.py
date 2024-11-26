from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import json
import requests

os.chdir("../")

# Get Authentications
load_dotenv()


AZURE_CLIENT = AzureOpenAI(
    api_key=os.getenv("AZURE_KEY"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_version="2023-10-01-preview"
)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def get_github_repo(GITHUB_TOKEN,query_string):# GitHub GraphQL API endpoint
    GRAPHQL_URL = "https://api.github.com/graphql"

    # Replace with your GitHub personal access token


    # GraphQL query string
    

    # Headers for authorization
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json",
    }

    # Make the request
    response = requests.post(
        GRAPHQL_URL,
        json={"query": query_string},
        headers=headers
    )

    # Process the response
    if response.status_code == 200:
        data = response.json()
        for edge in data["data"]["search"]["edges"]:
            node = edge["node"]
            print(f"Name: {node['name']}")
            print(f"Owner: {node['owner']['login']}")
            print(f"URL: {node['url']}")
            print(f"Description: {node['description']}")
            print("-" * 40)
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
    return response.json()

messages = [
        {
        "role": "system",
        "content":"Respond to everything as a short poem"
    }

    ,
    {"role": "user", "content": "Find the github repo that integrates glsl with touchdesigner"}
]

functions = [
        {
        "type": "function",
        "function": {
            "name": "get_github_repo",
            "description": "Get GitHub repositories based on a user's natural language description."
        },
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A GraphQL query string formatted for the GitHub API. For example: { search(query: \"touchdesigner glsl in:readme\", type: REPOSITORY, first: 10) { edges { node { name owner { login } url description } } } }"
                }
            },
            "required": ["query"]
        }
    }
]

response = AZURE_CLIENT.chat.completions.create(
    model="GPT-4",
    messages=messages,
    tools=functions,
    tool_choice="auto"
)

gpt_tools = response.choices[0].message.tool_calls
response_message = response.choices[0].message

print(response_message)

if gpt_tools:
    available_functions = {
        "get_github_repo": get_github_repo
    }

    messages.append(response_message)

    for gpt_tool in gpt_tools:
        function_name = gpt_tool.function.name
        function_to_call = available_functions[function_name]
        function_parameters = json.loads(gpt_tool.function.arguments)
        print('FUNCTION PARAMS')
        print(function_parameters)

        # Fixing parameter names
        crypto_name = function_parameters.get('crypto_name')
        fiat_currency = function_parameters.get('fiat_currency')

        function_response = function_to_call(crypto_name, fiat_currency)

        messages.append(
            {
                "tool_call_id": gpt_tool.id,
                "role": "tool",
                "name": function_name,
                "content": function_response
            }
        )

        second_response = AZURE_CLIENT.chat.completions.create(
            model="GPT-4",
            messages=messages
        )

else:
    print(response.choices[0].message)








