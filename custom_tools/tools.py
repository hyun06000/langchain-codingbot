import os
import subprocess
from langchain.serpapi import SerpAPIWrapper



def terminal_tool(command):
    """This is an agent to run a commend on a terminal. You can execute any terminal command on this function.
    It is very dangerous to run abitrary codes. So you should implement a codes very carefully.
    The return value of this function is stdout or stderr of your command.
    """

    command = command.strip()
    if command.startswith("`") and command.endswith("`"):
        command = command[1:-1]
    
    total_output = ""
    try:
        process = subprocess.Popen(
            [f"""{command}"""],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )

        os.set_blocking(process.stdout.fileno(), False)
        os.set_blocking(process.stderr.fileno(), False)
        while True:
            stdout = process.stdout.read()
            if stdout:
                output = stdout.decode("UTF-8")
                print(output)
                total_output += output

            stderr = process.stderr.read()
            if stderr:
                output = stderr.decode("UTF-8")
                print(output)
                total_output += output

            if process.poll() is not None:
                break
    
    except Exception as e:
        output = str(e)
        total_output += output
    return total_output


def search_tool(text: str) -> str:
    """web search tool"""

    try:
        search = SerpAPIWrapper()
        res = search.run(f"""{text}""")
    except Exception as e:
        res = str(e)
    
    return res

def savefile_tool(file_name: str, file_contents: str) -> str:
    """Save script as a file with file name and file contents which is a code.
    """
    
    try:
        with open(file_name, "w") as f:
            f.write(file_contents)

        return f"file saved : {file_name}"
    except Exception as e:
        return f"Error: {e}"


def readfile_tool(file_name: str) -> str:
    """Read script as a file with file name and file contents which is a code"""

    try:
        with open(file_name, "r") as f:
            file_contents = f.read()

        return f"file_contents : {file_contents}"
    except Exception as e:
        return f"Error: {e}"

