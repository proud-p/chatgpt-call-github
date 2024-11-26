from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import json
import requests

# Load environment variables
load_dotenv()

# Global variables
AZURE_CLIENT = AzureOpenAI(
    api_key=os.getenv("AZURE_KEY"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_version="2023-10-01-preview"
)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


# Convert user's question into a GraphQL query string
def nlp_to_query(question):
    messages = [
        {
            "role": "system",
            "content": """Convert the user's interest or question into a GraphQL query to use with the GitHub API. Always format the response as QUERY: followed by the query string. For example:

                            QUERY:
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
                            \"""
                    """
        },
        {"role": "user", "content": question}
    ]

    response = AZURE_CLIENT.chat.completions.create(
        model="GPT-4",
        messages=messages
    )

    # Debugging response
    print("Response from Azure OpenAI:", response)

    # Extract query string from the response
    response_text = response.get("choices", [{}])[0].get("message", {}).get("content", "")
    if "QUERY:" not in response_text:
        raise ValueError("No QUERY found in the response.")

    query_string = response_text.split("QUERY:")[1].strip()
    return query_string


# Function to fetch GitHub repositories using GraphQL query
def get_github_repo(question):
    print("QUESTION")
    print(question)
    GRAPHQL_URL = "https://api.github.com/graphql"

    # Get GraphQL query from user's question
    query_string = nlp_to_query(question)

    print("Generated GraphQL Query:", query_string)

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json",
    }

    # Make the API request
    response = requests.post(
        GRAPHQL_URL,
        json={"query": query_string},
        headers=headers
    )

    # Process the API response
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


# Chat messages and functions
messages = [
    {
        "role": "system",
        "content": "Respond to everything as a short poem."
    },
    {
        "role": "user",
        "content": "Find the GitHub repo that integrates GLSL with TouchDesigner."
    }
]


functions = [
	{
		"type": "function",
		"function": {
			"name": "get_github_repo",
			"description":  "Get GitHub repositories based on a user's natural language description.",
			"parameters": {
				# lettings chat-gpt know that it's getting
				# key-value pairs
				"type": "object",
				"properties": {
					"question": {
						"type": "string",
						"description": "A user's question describing the type of repository they are looking for. For example: 'I want to create patterns on the web using GLSL shaders.'"
					},
				
				},
				"required": ["question"]
			}
		}
	}
]

# Handle GPT's response and execute functions
response = AZURE_CLIENT.chat.completions.create(
    model="GPT-4",
    messages=messages,
    tools=functions,
    tool_choice="auto"
)

gpt_tools = response.choices[0].message.tool_calls
response_message = response.choices[0].message

# Print GPT's initial response
print("GPT Response:", response_message)

if gpt_tools:
    available_functions = {
        "get_github_repo": get_github_repo
    }

    messages.append(response_message)
    print("GPT TOOLS!")
    print(gpt_tools)
    for gpt_tool in gpt_tools:
        function_name = gpt_tool.function.name
        function_to_call = available_functions[function_name]
        function_parameters = json.loads(gpt_tool.function.arguments)

        print("FUNCTION PARAMETERS:")
        print(function_parameters)

        # Extract the question parameter
        question = function_parameters.get("question")

        # Call the function
        function_response = function_to_call(question)

        # Add the function response to the messages
        messages.append(
            {
                "tool_call_id": gpt_tool.id,
                "role": "tool",
                "name": function_name,
                "content": json.dumps(function_response, indent=4)
            }
        )

        # Get a final response from GPT using the function's output
        second_response = AZURE_CLIENT.chat.completions.create(
            model="GPT-4",
            messages=messages
        )
        print("Second GPT Response:", second_response.choices[0].message)
else:
    print(response.choices[0].message)

