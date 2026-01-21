from fastmcp import FastMCP
from fastmcp.server.proxy import ProxyClient

try: 
    proxy = FastMCP.as_proxy(
        ProxyClient("http://127.0.0.1:8000/mcp"),
        name="Calendar MCP Server"
    )
    print("Proxy created .................")
    print(f"proxy --------> {proxy}")

    if __name__ == "__main__":
        print("Starting-----------")
        proxy.run(
            transport="http",
            host="127.0.0.1",
            port=9000
        )

except Exception as e:
    print(f"exception --------->  {e}")


