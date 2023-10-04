from cat.mad_hatter.decorators import tool
import requests


@tool(return_direct=True)
def canta(query, cat):
    """
    When user asks you to "canta what is love" always use this tool.
    
    """
    url = 'http://localhost:8888/api/service/python/execFile/music.py'
    print(url)
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        print("Request was successful.")
        print(f"Response content: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed with error: {e}")


    return ""

