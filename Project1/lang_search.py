from langchain.utilities import SerpAPIWrapper
import os

os.environ['SERPAPI_API_KEY'] = '828d696b33f3825342982e6b0f7bc230d110a84001a9d70003ddda0175571063'

search = SerpAPIWrapper()
result = search.run("Who is Obama")
print(result)