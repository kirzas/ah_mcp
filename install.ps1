# install uv
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/0.10.4/install.ps1 | iex"

#set venv
uv init
uv venv
.venv\Scripts\activate


python -m ensurepip --upgrade

# Install MCP Python SDK
uv add mcp

