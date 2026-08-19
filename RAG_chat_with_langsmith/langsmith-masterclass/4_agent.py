from langchain_groq import ChatGroq
from langchain_core.tools import tool
import requests
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_agent
from ddgs import DDGS
from dotenv import load_dotenv
import os
os.environ["LANGSMITH_PROJECT"]="Agent project"
load_dotenv()

search_tool = DuckDuckGoSearchRun()

@tool
def get_weather_data(city: str) -> str:
  """
  This function fetches the current weather data for a given city
  """
  url = f'https://api.weatherstack.com/current?access_key=f07d9636974c4120025fadf60678771b&query={city}'

  response = requests.get(url)

  return response.json()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    max_tokens=500
)


# Step 3: Create the ReAct agent manually with the pulled prompt
agent = create_agent(
    model=llm,
    tools=[search_tool,get_weather_data],
    system_prompt="You are a helpful assistant."
)

response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "Identify the birthplace city of Kalpana Chawla (search) and give its current temperature?"
        }
    ]
})
print(response["messages"][-1].content)