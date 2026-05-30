from fastmcp import FastMCP

mcp = FastMCP("鉴权演示服务器")
VALID_TOKEN = "0106"

@mcp.tool()
def get_token() -> str:
    """获取鉴权 token，无需鉴权"""
    return VALID_TOKEN

@mcp.tool()
def add(a: float, b: float, token: str) -> dict:
    """计算两个数的和，需要鉴权"""
    if token is None:
        return {
            "error": "未提供鉴权 token",
            "hint": "请先调用 get_token 工具获取 token，然后调用 add(a, b, token)"
        }
    if token != VALID_TOKEN:
        return {
            "success": False,
            "error": "鉴权失败：token 无效"
        }
    return {
        "success": True,
        "result": a + b
    }

if __name__ == "__main__":
    mcp.run(transport="sse")