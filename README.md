# Building Conversational Agents with Tool Use and Reasoning Techniques

This project demonstrates how conversational assistants can leverage external tools and employ different reasoning strategies—Basic, Chain of Thought (CoT), and ReAct—to interact with users and deliver informative, dynamic responses. The agent fetches real-time weather information using WeatherAPI and integrates logic and arithmetic reasoning for more intelligent conversations.

---

## 🌐 Project Overview

This conversational system explores the practical use of advanced prompting and agent behavior techniques. By combining APIs and reasoning paradigms, it provides a foundation for building intelligent, tool-augmented AI systems.

Key Components:

External Tool Use: Fetching real-time data (weather info, math calculations).

Reasoning Modes:

Basic: Direct question answering with minimal logic.

Chain of Thought (CoT): Step-by-step reasoning before acting.

ReAct: Interleaving reasoning and actions for more complex tasks.


## ⚙️ Features
🔍 Weather Information

Retrieve current weather conditions and forecasts for any global location using WeatherAPI.

➗ Mathematical Calculations
Execute arithmetic operations through a built-in calculator tool.

🧠 Reasoning Strategies
Support for three distinct reasoning agents:

Basic Agent – Straightforward tool invocation.

Chain of Thought Agent (CoT) – Reasoned responses using intermediate steps.

ReAct Agent – Combines reasoning with dynamic tool execution for multi-step queries.

---

## 🛠️ Setup Instructions

**1. Prerequisites**
Ensure the following are installed:
  Python 3.8+
  pip (Python package installer)
  API Keys for:
    WeatherAPI
    Groq  API

 **2. Clone the Repository**
```bash
git clone https://github.com/ShahdTarek4/Building-Conversational-Agents-with-Tool-Use-and-Reasoning-Techniques.git
cd Building-Conversational-Agents-with-Tool-Use-and-Reasoning-Techniques
```

 **3.Set Up Environment Variables**
Create a .env file in the project directory and add the following:
 
GROQ_API_KEY=your_groq_api_key  
GROQ_BASE_URL=your_groq_base_url  
GROQ_MODEL=your_groq_model_name  
WEATHER_API_KEY=your_weather_api_key  



 **4.Run the Conversational Agent**

python conversational_agent.py

You will be prompted to choose an agent type:

-1 for Basic Agent

-2 for Chain of Thought (CoT) Agent

-3 for ReAct Agent

## 📘 Implementation Documentation

### 🧠 Agent Architectures

This project includes three distinct conversational agent types, each employing a unique reasoning methodology and toolset:

#### 🔹 Basic Agent

- Provides direct and concise answers to weather-related questions.
- Utilizes the `get_current_weather` and `get_weather_forecast` tools to retrieve real-time data.
- Best suited for simple, single-step queries.

#### 🔸 Chain of Thought (CoT) Agent

- Handles more complex questions by decomposing them into manageable steps.
- Performs explicit step-by-step reasoning before arriving at an answer.
- Leverages both weather tools and the built-in calculator tool to process multi-part or numerical queries.

#### 🔶 ReAct Agent

- Integrates reasoning and tool usage in an iterative fashion to dynamically solve problems.
- Follows the ReAct framework: **Thought → Action → Observation → Final Answer**.
- Uses all available tools, including a simulated `web_search`, for comprehensive responses that require both reasoning and information retrieval.

---

### 🧰 Integrated Tools

Each agent draws from a shared toolkit, with tools selected based on the reasoning demands of the query:

#### 🌤️ Weather Tools

- `get_current_weather`: Retrieves current weather conditions for a specified location.
- `get_weather_forecast`: Provides weather forecasts for a specific location.

#### ➕ Calculator Tool

- `calculator`: Evaluates and solves arithmetic expressions used in reasoning chains.

#### 🔍 Web Search Tool

- `web_search`: Simulates a web-based search to supplement queries with additional context or information.

---

### 🧪 Comparative Evaluation

The system supports side-by-side comparison of the different agents’ responses for the same query:

- Users can run all three agents on the same input and visually compare their outputs.
- After viewing the responses, users are prompted to rate each agent’s answer on a scale from 1 to 5.
- These ratings are recorded in a CSV file (`agent_evaluation.csv`) for further analysis or experimentation.

---

### 🚀 Running the System

Upon execution, the user is prompted to choose between two operational modes:

#### 🔹 Single-Agent Mode

- Interact with one reasoning strategy at a time.
- After selecting this mode, you'll be asked to specify which agent to use:
  - 1 - Basic Agent
  - 2 - Chain of Thought Agent
  - 3 - ReAct Agent
- The selected agent will then handle user queries using its respective reasoning approach.

#### 🔸 Comparative Evaluation Mode

- All three agents process the same query simultaneously.
- Their responses are displayed side by side.
- You’ll be asked to rate each agent’s answer on a scale from 1 to 5.
- The ratings are saved to `agent_evaluation.csv` for later inspection or evaluation.

---

### 💬 Example Conversations

#### 1️⃣ Basic Agent

**User**: What’s the weather in Paris today?  
**Agent**:  
- Temperature: 12.3°C (54.1°F)  
- Condition: Partly cloudy  
- Humidity: 65%  
- Wind Speed: 8.5 kph

#### 2️⃣ Chain of Thought (CoT) Agent

**User**: What’s the temperature difference between Tokyo and Sydney today?  
**Agent**:  
Let me calculate the temperature difference between Tokyo and Sydney.  
Fetching the current temperature for Tokyo...  
Fetching the current temperature for Sydney...  
Calculating the difference...  

- Tokyo: 5.3°C  
- Sydney: 21.2°C  

**The temperature difference is: 21.2°C - 5.3°C = 15.9°C.**  
So, the difference between Tokyo and Sydney today is **15.9°C**.

#### 3️⃣ ReAct Agent

**User**: Is it hotter in New York or London right now?  
**Agent**:  
Thought: I need to find the current temperatures in both New York and London.  
Action: Use get_current_weather for New York.  
Observation: New York is at 15.6°C.  
Thought: Now I need London's temperature.  
Action: Use get_current_weather for London.  
Observation: London is at 5.3°C.  
Thought: Now I can compare the two temperatures.  
Final Answer: **New York is hotter than London right now, with a temperature difference of 10.3°C.**

---

## 🧠 Analysis of Reasoning Strategies

### 🔹 Basic Agent

- **Strengths**: Fast, simple, and ideal for direct questions.  
- **Limitations**: Lacks the ability to handle compound or multi-step reasoning tasks.

### 🔸 Chain of Thought Agent

- **Strengths**: Excellent for multi-step problems; improves clarity by making the reasoning explicit.  
- **Limitations**: Slower due to step-by-step processing; less suitable for rapid responses.

### 🔶 ReAct Agent

- **Strengths**: Combines deep reasoning with dynamic tool use; ideal for complex or exploratory queries.  
- **Limitations**: Can be computationally heavier and may overcomplicate simple tasks.

---


## **Note on Comparative Evaluation**

Expect some delay when using the Comparative Evaluation feature—this is completely normal. Here's why:

Separate Requests: Each reasoning model (Basic, Chain-of-Thought, and ReAct) sends its own individual request to the OpenAI API.

Expanded Reasoning: The Chain-of-Thought and ReAct approaches involve more complex, step-by-step thinking, which naturally adds to the processing time.

Tool Usage: These agents may call functions such as retrieving current weather data or performing calculations, each of which takes additional time to execute.
