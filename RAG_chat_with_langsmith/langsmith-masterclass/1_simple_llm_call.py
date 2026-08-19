from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
load_dotenv()
os.environ["LANGSMITH_PROJECT"]="First project"
# Simple one-line prompt
prompt = PromptTemplate.from_template("{question}")

model=ChatGroq(
    model="groq/compound-mini",
    api_key=os.getenv("GROQ_API_KEY"),
)
parser = StrOutputParser()

# Chain: prompt → model → parser
chain = prompt | model | parser

# Run it
result = chain.invoke({"question": "What is the capital of Peru?"})
print(result)
