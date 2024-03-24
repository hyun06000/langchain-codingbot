import os
import io
import subprocess
from time import time
from dotenv import load_dotenv
from serpapi import GoogleSearch, BaiduSearch
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

from googlesearch import search
from bs4 import BeautifulSoup
import requests
import re
from PyPDF2 import PdfReader

load_dotenv()

def terminal_tool(command, timeout=3):
    """This is an agent to run a commend on a terminal. You cannot use sudo command. You can execute any terminal command on this function.
    It is very dangerous to run abitrary codes. So you should implement a codes very carefully.
    The return value of this function is stdout or stderr of your command.
    """

    command = command.strip()
    if command.startswith("`") and command.endswith("`"):
        command = command.strip("`")
    
    total_output = ""
    try:
        process = subprocess.Popen(
            [f"""{command}"""],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            start_new_session=True,
        )

        os.set_blocking(process.stdout.fileno(), False)
        total_output += "STDOUT : "
        ckpt = time()
        while True:
            stdout = process.stdout.read()
            if stdout:
                output = stdout.decode("UTF-8")
                print(output)
                total_output += output
                ckpt = time()
            elif (time() - ckpt) > timeout:
                exit_code = process.poll()
                total_output += f" exit_code: {exit_code}"
                break
                        
        os.set_blocking(process.stderr.fileno(), False)
        total_output += " | STDERR : "
        ckpt = time()
        while True:
            stderr = process.stderr.read()
            if stderr:
                output = stderr.decode("UTF-8")
                print(output)
                total_output += output
                ckpt = time()
            elif (time() - ckpt) > timeout:
                exit_code = process.poll()
                total_output += f" exit_code: {exit_code}"
                break
            
    except Exception as e:
        output = str(e)
        total_output += output
    return total_output

def chinese_search_url_tool(text: str) -> str:
    """chinese language title search tool to get url related to the keywords"""
    params = {
        "engine": "baidu",
        "q": text,
        "num": 10,
        "api_key": os.environ["SERPAPI_API_KEY"],
    }
    
    
    try:
        search = BaiduSearch(params)
        search_dict = search.get_dict()
        
        if "organic_results" not in search_dict:
            return "There is no result. Please change the search phrase to a more shorter and generic words."
        
        res = list(map(
            lambda x: f"TITLE: {x['title']} | LINK: {x['link']}", #" | DESCRIPTION: {x['snippet']}",
            search.get_dict()["organic_results"]
        ))
    except Exception as e:
        res = str(e)
    
    return res

def chinese_search_news_tool(text: str) -> str:
    """chinese language search tool to get url of news article related to the keywords"""
    params = {
        "engine": "baidu_news",
        "q": text,
        "num": 10,
        "device": "mobile",
        "api_key": os.environ["SERPAPI_API_KEY"],
    }
    
    
    try:
        search = BaiduSearch(params)
        search_dict = search.get_dict()
        
        if "organic_results" not in search_dict:
            return "There is no result. Please change the search phrase to a more shorter and generic words."
        
        res = list(map(
            lambda x: f"TITLE: {x['title']} | LINK: {x['link']}", # | DESCRIPTION: {x['snippet']}
            search_dict["organic_results"]
        ))
    except Exception as e:
        res = str(e)
    
    return res




def search_url_tool(text: str) -> str:
    """google search tool to get url related to the keywords"""
    params = {
        "q": text,
        "num": 10,
        "api_key": os.environ["SERPAPI_API_KEY"],
    }
    
    
    try:
        search = GoogleSearch(params)
        search_dict = search.get_dict()
        
        if "organic_results" not in search_dict:
            return "There is no result. Please change the search phrase to a more shorter and generic words."
        
        res = list(map(
            lambda x: f"TITLE: {x['title']} | LINK: {x['link']}", #" | DESCRIPTION: {x['snippet']}",
            search.get_dict()["organic_results"]
        ))
    except Exception as e:
        res = str(e)
    
    return res

def search_news_tool(text: str) -> str:
    """google search tool to get url of news article related to the keywords"""
    params = {
        "q": text,
        "num": 10,
        "api_key": os.environ["SERPAPI_API_KEY"],
        "tbm": "nws", 
    }
    
    
    try:
        search = GoogleSearch(params)
        search_dict = search.get_dict()
        
        if "news_results" not in search_dict:
            return "There is no result. Please change the search phrase to a more shorter and generic words."
        
        res = list(map(
            lambda x: f"TITLE: {x['title']} | DATE : {x['date']} | LINK: {x['link']}", # | DESCRIPTION: {x['snippet']}
            search_dict["news_results"]
        ))
    except Exception as e:
        res = str(e)
    
    return res


def savefile_tool(file_name, file_contents:str) -> str:
    """Save (append) script as a file with file name and file contents which is a code.
    This tool need two inputs like {action_input: {file_name:str , file_contents:str}}.
    """
    
    try:
        with open(file_name, 'w+') as f:
            f.write(file_contents + "\n")

        return f"file saved : {file_name}"
    except Exception as e:
        return f"Error: {e}"


def readfile_tool(file_name: str) -> str:
    """Read script as a file with file name and file contents which is a code"""

    try:
        with open(file_name, "r+") as f:
            file_contents = f.read()

        return f"file_contents : {file_contents}"
    except Exception as e:
        return f"Error: {e}"


def article_summary_tool(news_url: str) -> str:
    """This tool is for web news article summarizer.
    If you input a url pointing to news article,
    this tool will give you a paragraph of summary of the news.
    """

    try:
        try:
            response = requests.get(news_url, verify=False)
            if news_url.endswith(".pdf"):
                text = ""
                with io.BytesIO(response.content) as f:
                    pdf = PdfReader(f)
                    for page_num in range(len(pdf.pages)):
                        text += pdf.pages[page_num].extract_text() + '\n'
            else:
                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.body.get_text().strip().encode('utf8','replace').decode()
            text = re.sub(r"\n"," ",text)
            text = re.sub(r"\s+"," ",text)
        except Exception as e:
            text = "Something went wrong. Please try again with another URL"
        
        prompt = PromptTemplate.from_template("""
            You are a journalist.
            Could you give me the summary of the only article part of this paragraph?
            Paragraph can be written in a mixture between local language and English.
            
            ```paragraph
            {paragraph}
            ```
            
            Summary:
        """)
        runnable = prompt | ChatOpenAI(temperature=0, model="gpt-4-1106-preview")
        summary = runnable.invoke({"paragraph": text})
                
        return f"Summary : {summary}"
    except Exception as e:
        return f"Error: {e}"


def translation_tool(asking: str) -> str:
    """ask translation to ChatGPT.
    You should make prompt like : what is the "..." in <language>?
    For example, what is the "hello my friend!" in spenish?
    """

    try:
        prompt = PromptTemplate.from_template("You are a translator. Please give me the translation. {asking}")
        runnable = prompt | ChatOpenAI(temperature=0, model="gpt-4-1106-preview")
        thinking = runnable.invoke({"asking": asking})
        
        
        return f"Thinking : {thinking}"
    except Exception as e:
        return f"Error: {e}"


def google_query_tool(input_string: str) -> str:
    """With this tool, you can search something on google.
    The returns are combinations of TITLE, URL, DESCRIPTION.
    You can extract url and put it into request_url_tool to go the link. """
    try:
        return list(map(lambda x: f"TITLE:{x.title}, URL:{x.url}, DESCRIPTION:{x.description}", search(input_string, num_results=10, advanced=True)))
    except Exception as e:
        return f"Error: {e}"

def request_url_tool(input_url: str) -> str:
    """With this tool, you can get the contents in the page of url and pdf link."""
    try:
        response = requests.get(input_url, verify=False)
        if input_url.endswith(".pdf"):
            text = ""
            with io.BytesIO(response.content) as f:
                pdf = PdfReader(f)
                for page_num in range(len(pdf.pages)):
                    text += pdf.pages[page_num].extract_text() + '\n'
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.body.get_text().strip()
        text = re.sub(r"\n"," ",text)
        text = re.sub(r"\s+"," ",text)
        return text [:2000]
    except Exception as e:
        return "Something went wrong. Please try again with another URL"
