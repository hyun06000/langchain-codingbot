from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import StructuredTool


from custom_tools.tools import (
    terminal_tool,
    search_tool,
    readfile_tool,
    savefile_tool,
)

# In[2]:


from dotenv import load_dotenv

load_dotenv()


llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

template = """
Question:You are a senier computer programmer.
You can use a terminal command to run a code or install a package.
If there is no package to run, install it first and must check it is installed completely or not.
You can save your own code and run, debug, modify it. And also you can run a terminal command.
To run a code in safe way, you should save a code script first and run it on terminal command.
Please make up this purpose: {purpose}
"""

prompt_template = PromptTemplate(
    input_variables=["purpose"],
    template=template
)
    
tools = [
    StructuredTool.from_function(terminal_tool),
    StructuredTool.from_function(search_tool),
    StructuredTool.from_function(savefile_tool),
    StructuredTool.from_function(readfile_tool),
]

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

purpose_prompt = (            
    "please make a web page to check the current time."
    " There are buttons on screen to select on of Newyork/Seoul."
    " If user click the button, user can see the current time of the city."
    " Most of all, Make playground folder first, and save every result into the directory." 
    " If there is a existing path, then skip making folder."
    " There is no directory name as template."
    " You can run the web server on the terminal."
    " User should can select the standard between Newyork and Seoul."
    " Save a backend script and frontend script in correct path."
    " If it is necessary, You can make a directory with `mkdir` command."
    " Especially, your html codes should be in `templates` folder."
    " So before making frontend codes, please make `templates` folder."
    " Frontend should be beautiful style."
    " Backend server framework can be one of flask or fastapi."
    " And show the page on web browser."
    " If you can, you should run it with debug mode on."
    " You can use ports 60000 and 50000."
)


agent_executor.run({"input":prompt_template.format_prompt(purpose=purpose_prompt)})