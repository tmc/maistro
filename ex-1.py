import multion
from multion import MultionToolSpec
from langchain.llms.openai import OpenAI
from langchain.agents import initialize_agent, AgentType

from langchain.tools import StructuredTool

multion_toolkit = MultionToolSpec(use_api=True, mode="auto")
browser = StructuredTool.from_function(multion_toolkit.browse)

multion.login()
multion.set_remote(False)
#multion.login(true, multion_api_key="01e57befda43447fafce549a5333f876")

llm = OpenAI(temperature=0)


agent = initialize_agent(
    tools=[browser],
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)


MAESTRO_URL = "http://localhost:9999/interact"
# pass the image to GPT to generate a list of example features to test?

PROMPT1 = f"""
You are an AI Agent whose job is to use the search bar to enumerate all possible click actions. Here is the link to start from: {MAESTRO_URL}. DO NOT guess or make up any user information, instead ask user to provide any missing info. Do not use any placeholders.

Here are the high-level steps:
1. Go to {MAESTRO_URL}
2. Given the left side screenshot, create high level goals to test for
3. Input the high level goals into the search bar starting with typing in " "
4. Print the output on screen
"""

PROMPT2 = f"""
You are an AI Agent whose job is to write high level UI automation tests using the Maestro framework. Here is the link to start from: {MAESTRO_URL}. Do not use any placeholders.

Here are the high-level steps:
1. Go to {MAESTRO_URL}
2. Add steps to describe new interactions.
"""

response = agent(inputs={
    'input': PROMPT2,
})
