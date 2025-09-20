## Overview

This is a basic MCP tool for providing code execution as a tool for an AI model, accepting a request from an AI app containing code, executing it, and then returning the output back to the AI. This server was built on STDIO transport, which means it will be running on your very own machine, so feel free to experiment, extend, and use it locally for safe and private code execution.

## Building the necessary docker image

After cloning this repo, be sure do build a docker image like so:

```sh
docker build -t my-python-mcp:latest .
```

This will create a docker image named `my-python-mcp:latest` with numpy and pandas, libraries specified in the Dockerfile. Feel free to add any other library after installing it on your machine for your desired LLM to use it on the image! No need to install anything else inside the container.  You can change the name of the build my modifying the name on the dockerfile and in the build command provided above

For now, python image is the only completed one, but other languages can also be added. 

## Adding the MCP to Claude

In order to add this MCP to Claude (the chosen platform in this case), just open the settings tab, select developer and input the following code in the `claude_desktop_config.json` as so:

```sh
{
  "mcpServers": {
    "codeexec": {
      "command": "C:\\Users\\YOUR USER\\.local\\bin\\uv.EXE",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "C:\\THE\\PATH\\WHERE\\MAIN.PY\\LIES\\main.py"
      ]
    }
  }
}
```
Any MCP should be added inside the big mcpServers object (featuring the command, arguments to be ran in the the terminal and the server location). Also, be sure to have uv on your machine. Revise this link for more information:
[UV Link](https://docs.astral.sh/uv/getting-started/installation/)


## Downloading the necessary requirements (windows) - just in case:
Given the lastest python installation (3.13.7), run the following command provided in the official MCP Python SDK:

´´´sh
pip install "mcp[cli]"
´´´ 
or alternatively be sure you download the requirements.txt like so:

´´´sh
pip install "mcp[cli]"
´´´

## General information

For general information regarding the python SDK and the MCP in general, follow these links:
1) https://modelcontextprotocol.io/docs/getting-started/intro
2) https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#installation