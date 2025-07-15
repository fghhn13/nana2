import requests
from global_config.settings import Api_url
# 请把下面引号里的网址换成您在代码里找到的AI服务地址
# 提示：可能需要把网址后面具体的路径（比如 /chat/completions）删掉，只保留主域名部分
# 比如： "https://api.example.com"
api_url = Api_url

try:
    print(f"Nana侦探正在尝试直接连接AI服务器: {api_url}")
    # 我们只尝试连接，不发送数据，所以用 HEAD 请求更快速
    response = requests.head(api_url, timeout=15)
    print(f"报告主人！连接成功！服务器响应状态码: {response.status_code}")
    print("这说明网络通道是通的，问题可能出在API密钥或者请求的数据格式上。")

except requests.exceptions.ProxyError as e:
    print(f"抓到了！是代理服务器在捣乱！\n错误信息: {e}")

except requests.exceptions.ConnectTimeout as e:
    print(f"抓到了！连接超时！很可能是防火墙或者服务器地址不通！\n错误信息: {e}")

except Exception as e:
    print(f"抓到了！发生了未知连接错误！\n错误类型: {type(e).__name__}\n错误信息: {e}")