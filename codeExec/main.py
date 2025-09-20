import docker
from mcp.server.fastmcp.server import FastMCP
import os
import tempfile  

#initializing MCP server
mcp = FastMCP("codeexec", json_response=True)

#registering the tool with MCP
@mcp.tool()
async def execute_code(code: str, language: str) -> str:
    """
    Executes the provided code in a docker sandbox
    Args:
        code (str): The code to execute.
        language (str): The programming language of the code.
    Returns:
        str: The output of the code execution and a status code indicating success or fail.
    """
    #mapping languages to docker images
    image_map = {
        "python": "my-python-mcp:latest",  
        #"javascript": "node:14-slim",            
    }
    #mapping languages to execution commands
    command_map = {
        "python": "python /code/temp_code",
        #"javascript": "node /code/temp_code"
    }
    
    #selecting appropiate language
    image = image_map.get(language.lower())
    command = command_map.get(language.lower())
    if not image or not command:
        return f"Unsupported language: {language}"
    
    #creating a temporary file to hold the code
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(code.encode())
        temp_code_path = f.name

    #running the code in a docker container
    client = docker.from_env()
    container = None
    try:
        #Running the container with constraints
        container = client.containers.run(
            image,
            command=f"timeout 5s {command}",
            volumes={temp_code_path: {'bind': '/code/temp_code', 'mode': 'ro'}},
            detach=True, 
            stderr=True,
            stdout=True,
            network_disabled=True,
            mem_limit='500m',
            cpu_quota=50000,
        )
        #Waiting for the container to finish and getting the output (status and code)
        result = container.wait()
        exit_code = result.get("StatusCode", -1)
        output = container.logs(stdout=True, stderr=True, stream=False).decode()
        return f"Exit code: {exit_code}\n{output}"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
       os.remove(temp_code_path)

#Registering the tool with MCP and running the server
if __name__ == "__main__":
    mcp.run(transport="stdio")

