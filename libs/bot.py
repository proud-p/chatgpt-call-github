from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import json
import requests

os.chdir("../")

# Get Authentications
load_dotenv()


global AZURE_CLIENT, GITHUB_TOKEN
AZURE_CLIENT = AzureOpenAI(
        api_key=os.getenv("AZURE_KEY"),
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_version="2023-10-01-preview"
    )

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# -----------


def nlp_to_query(question):
    messages = [
        {
            "role": "system",
            "content": """Convert the user's interest or question into a GraphQL query to use with the GitHub API. For example:
                                    
                            User Input: "I want to create a water-like texture procedurally in TouchDesigner so I can VJ."
                            System Response: "To look at this, you can explore repositories integrating GLSL into TouchDesigner. QUERY:
                            query_string = \"""
                            {
                            search(query: "glsl touchdesigner in:readme", type: REPOSITORY, first: 10) {
                                edges {
                                node {
                                    name
                                    owner {
                                    login
                                    }
                                    url
                                    description
                                }
                                }
                            }
                            }
                            \"\"\"

                            or

                            For example: { search(query: \"touchdesigner glsl in:readme\", type: REPOSITORY, first: 10) { edges { node { name owner { login } url description } } } }

                        Always format your response with the QUERY after 'QUERY:' so it can be parsed later."""
                    },
                    {"role": "user", "content": question}
                ]

    response = AZURE_CLIENT.chat.completions.create(
    model="GPT-4",
    messages=messages
    )


def get_github_repo(question):# GitHub GraphQL API endpoint
    # Get GraphQL query string from question using chatgpt

    # -------- deal with getting github repo-------

    GRAPHQL_URL = "https://api.github.com/graphql"
    response_and_query = nlp_to_query(question)
    print(response_and_query)

    query_string = response_and_query.split("QUERY:")[1]
    

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
                "question": {
                    "type": "string",
                    "description": "Question user is interested in asking, for example, I want to create patterns on the web can be translated to using p5.js or using glsl shaders for the web. "
                }
            },
            "required": ["question"]
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








