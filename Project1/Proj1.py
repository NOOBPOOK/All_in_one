import guidance
from SearchPackage.Search import SerpAPIWrapper

SERPAPI_API_KEY = '828d696b33f3825342982e6b0f7bc230d110a84001a9d70003ddda0175571063'

#Contains the code for a normal Guidance llm chat bot
def gpt(ques):
    #Building a LLM with GPT3.5
    guid = guidance.llms.OpenAI("gpt-3.5-turbo")

    #Chat Dialog reference
    result = guidance('''
    {{#system~}}
    You are a helpful assistant.
    {{~/system}}

    {{#assistant~}}
    {{search query}}
    {{~/assistant}}

    
    ''',
    llm = guid)

    #USER QUERY
    ok = result(query = ques, search = search)
    print(ok)

def search(st):
    search = SerpAPIWrapper(serpapi_api_key = SERPAPI_API_KEY,search_engine="google")
    ok = search.run(st)
    return "According to Google, " + ok

question = input("Ask your Query to search Engine >>   ")
gpt(question)