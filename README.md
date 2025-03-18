# Conversational-Agent

A conversational assistant that provides weather information using different reasoning strategies: Basic, Chain of Thought (CoT), and ReAct. The assistant interacts with users, retrieves weather data using WeatherAPI, and applies reasoning techniques to improve responses.

## **Features**
- **Weather Information**: Fetch current weather and forecasts for any location using WeatherAPI.
- **Mathematical Calculations**: Perform calculations using a built-in calculator tool.
- **Reasoning Strategies**:
  - **Basic**: Direct tool usage for simple queries.
  - **Chain of Thought (CoT)**: Step-by-step reasoning for complex queries.
  - **ReAct**: Structured reasoning and action for dynamic problem-solving.

---

## **Setup Instructions**

### **1. Prerequisites**
- Python 3.8 or higher
- A valid API key for [WeatherAPI](https://www.weatherapi.com/) (free tier available)
- A valid API key for [Groq](https://groq.com/) or [NGU](https://ngu.com/) (depending on your configuration)

### **2. Clone the Repository**

git clone https://github.com/ShahdTarek4/Conversational-Agent.git
cd Conversational-Agent

4️⃣ **Set Up Environment Variables**
Create a .env file in the project directory and add the following:

MODEL_SERVER=GROQ   # Change to NGU if using NGU API  
GROQ_API_KEY=your_groq_api_key  
GROQ_BASE_URL=your_groq_base_url  
GROQ_MODEL=your_groq_model_name  
WEATHER_API_KEY=your_weather_api_key  


5️⃣ **Run the Conversational Agent**

python conversational_agent.py

You will be prompted to choose an agent type:

1 for Basic Agent
2 for Chain of Thought (CoT) Agent
3 for ReAct Agent
