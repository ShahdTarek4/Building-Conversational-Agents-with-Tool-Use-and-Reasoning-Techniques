import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Get the model server type
model_server = os.getenv('MODEL_SERVER', 'GROQ').upper()  # Default to GROQ if not set

if model_server == "GROQ":
    API_KEY = os.getenv('GROQ_API_KEY')
    BASE_URL = os.getenv('GROQ_BASE_URL')
    LLM_MODEL = os.getenv('GROQ_MODEL')
    WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")  # WeatherAPI key
elif model_server == "NGU":
    API_KEY = os.getenv('NGU_API_KEY')
    BASE_URL = os.getenv('NGU_BASE_URL')
    LLM_MODEL = os.getenv('NGU_MODEL')
    WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")  # WeatherAPI key
else:
    raise ValueError(f"Unsupported MODEL_SERVER: {model_server}")

# Initialize the OpenAI client with custom base URL
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL 
)
# Weather API functions
def get_current_weather(location):
    """Get the current weather for a location."""
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}&aqi=no"
    response = requests.get(url)
    data = response.json()
    if "error" in data:
        return f"Error: {data['error']['message']}"
    weather_info = data["current"]
    return json.dumps({
        "location": data["location"]["name"],
        "temperature_c": weather_info["temp_c"],
        "temperature_f": weather_info["temp_f"],
        "condition": weather_info["condition"]["text"],
        "humidity": weather_info["humidity"],
        "wind_kph": weather_info["wind_kph"]
    })

def get_weather_forecast(location, days=3):
    """Get a weather forecast for a location for a specified number of days."""
    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&days={days}&aqi=no"
    response = requests.get(url)
    data = response.json()
    if "error" in data:
        return f"Error: {data['error']['message']}"
    forecast_days = data["forecast"]["forecastday"]
    forecast_data = []
    for day in forecast_days:
        forecast_data.append({
            "date": day["date"],
            "max_temp_c": day["day"]["maxtemp_c"],
            "min_temp_c": day["day"]["mintemp_c"],
            "condition": day["day"]["condition"]["text"],
            "chance_of_rain": day["day"]["daily_chance_of_rain"]
        })
    return json.dumps({
        "location": data["location"]["name"],
        "forecast": forecast_data
    })

# Define weather tools for Groq API
weather_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g., San Francisco, CA or country e.g., France",
                    }
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather_forecast",
            "description": "Get the weather forecast for a location for a specific number of days",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g., San Francisco, CA or country e.g., France",
                    },
                    "days": {
                        "type": "integer",
                        "description": "The number of days to forecast (1-10)",
                        "minimum": 1,
                        "maximum": 10
                    }
                },
                "required": ["location"],
            },
        },
    }
]

# Create a lookup dictionary for available functions
available_functions = {
    "get_current_weather": get_current_weather,
    "get_weather_forecast": get_weather_forecast
}

# Process messages and handle tool calls
import json

def process_messages(client, messages, tools=None, available_functions=None):
    """Process messages and invoke tools as needed."""
    tools = tools or []
    available_functions = available_functions or {}

    # Step 1: Send the messages to the model with the tool definitions
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",  # Let the model decide whether to use tools
    )
    response_message = response.choices[0].message
    messages.append({"role": "assistant", "content": response_message.content})

    # Step 2: Check if the model wants to use a tool
    if hasattr(response_message, "tool_calls") and response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions.get(function_name)

            if function_to_call:
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(**function_args)

                # Step 3: Append tool response as a properly formatted JSON string
                messages.append({
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response),  # Fix: Ensure JSON format
                })

                # Step 4: Send updated messages back to model to format tool response properly
                formatted_response = client.chat.completions.create(
                    model=LLM_MODEL,
                    messages=messages,
                ).choices[0].message

                # Step 5: Append the formatted assistant response
                messages.append({
                    "role": "assistant",
                    "content": formatted_response.content,  # Ensure properly formatted response
                })

    return messages

# Run the conversation
def run_conversation(client, system_message="You are a helpful weather assistant."):
    """Run a conversation with the user, processing their messages and handling tool calls."""
    messages = [{"role": "system", "content": system_message}]
    print("Weather Assistant: Hello! I can help you with weather information. Ask me about the weather anywhere!")
    print("(Type 'exit' to end the conversation)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\nWeather Assistant: Goodbye! Have a great day!")
            break

        messages.append({"role": "user", "content": user_input})
        messages = process_messages(client, messages, weather_tools, available_functions)

        # Check the last message to see if it's from the assistant
        last_message = messages[-1]
        if last_message["role"] == "assistant" and last_message.get("content"):
            print(f"\nWeather Assistant: {last_message['content']}\n")

    return messages


# Calculator tool for Chain of Thought reasoning
def calculator(expression):
    """Evaluate a mathematical expression."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

# Define the calculator tool
calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "Evaluate a mathematical expression",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate, e.g., '2 + 2' or '5 * (3 + 2)'",
                }
            },
            "required": ["expression"],
        },
    }
}

# Add calculator to weather tools and available functions
cot_tools = weather_tools + [calculator_tool]
available_functions["calculator"] = calculator

# Chain of Thought system message
cot_system_message = """You are a helpful assistant that can answer questions about weather and perform calculations.

When responding to complex questions, please follow these steps:
1. Think step-by-step about what information you need
2. Break down the problem into smaller parts
3. Use the appropriate tools to gather information
4. Explain your reasoning clearly
5. Provide a clear final answer
"""

# Simplified search tool for ReAct reasoning
def web_search(query):
    """Simulate a web search for information."""
    search_results = {
        "weather forecast": "Weather forecasts predict atmospheric conditions for a specific location and time period.",
        "temperature conversion": "To convert Celsius to Fahrenheit: multiply by 9/5 and add 32.",
        "climate change": "Climate change refers to significant changes in global temperature and weather patterns.",
        "severe weather": "Severe weather includes thunderstorms, tornadoes, hurricanes, and blizzards."
    }

    # Find the closest matching key
    best_match = None
    best_match_score = 0
    for key in search_results:
        words_in_query = set(query.lower().split())
        words_in_key = set(key.lower().split())
        match_score = len(words_in_query.intersection(words_in_key))
        if match_score > best_match_score:
            best_match = key
            best_match_score = match_score

    if best_match_score > 0:
        return json.dumps({"query": query, "result": search_results[best_match]})
    else:
        return json.dumps({"query": query, "result": "No relevant information found."})

# Define the search tool
search_tool = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search for information on the web",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query",
                }
            },
            "required": ["query"],
        },
    }
}

# Create ReAct tools and available functions
react_tools = cot_tools + [search_tool]
available_functions["web_search"] = web_search

# ReAct system message
react_system_message = """You are a helpful weather and information assistant that uses the ReAct (Reasoning and Acting) approach to solve problems.

When responding to questions, follow this pattern:
1. Thought: Think about what you need to know and what steps to take
2. Action: Use a tool to gather information (weather data, search, calculator)
3. Observation: Review what you learned from the tool
4. ... (repeat the Thought, Action, Observation steps as needed)
5. Final Answer: Provide your response based on all observations
"""

#test the ReAct agent
if __name__ == "__main__":
    choice = input("Choose an agent type (1: Basic, 2: Chain of Thought, 3: ReAct): ")
    if choice == "1":
        system_message = "You are a helpful weather assistant."
        tools = weather_tools
    elif choice == "2":
        system_message = cot_system_message
        tools = cot_tools
    elif choice == "3":
        system_message = react_system_message
        tools = react_tools
    else:
        print("Invalid choice. Defaulting to Basic agent.")
        system_message = "You are a helpful weather assistant."
        tools = weather_tools

    run_conversation(client, system_message)

'''# test the Chain of Thought agent
if __name__ == "__main__":
    print("Testing Chain of Thought Agent:")
    run_conversation(client, cot_system_message)'''

'''# Main function to run the conversational agent
if __name__ == "__main__":
    run_conversation(client)'''