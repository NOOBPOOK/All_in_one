import llama_index
from llama_index import VectorStoreIndex, SimpleDirectoryReader,ServiceContext
from langchain.chat_models import ChatOpenAI
import codecs

#TO DIVIDE THE INPUT FILE INTO SIX DIFFERENT PARTS
gh = []
with codecs.open("bigdata.txt", 'r', encoding='utf-8',errors='ignore') as fdata:
    gh = fdata.readlines()

li = ["CHAPTER I", "CHAPTER II", "CHAPTER III", "CHAPTER IV", "CHAPTER V", "CHAPTER VI","123456789"]
st = 0
ok = open('file.txt','w')

for i in gh:
    if li[st] in i:
        ok.close()
        ok = open(f"{li[st]}"+".txt","w")
        st += 1
    else:
        try:
            ok.write(i)
        except:
            pass
ok.close()


chp1 = SimpleDirectoryReader(input_dir="CHAPTER I.txt").load_data()
chp2 = SimpleDirectoryReader(input_dir="CHAPTER II.txt").load_data()
chp3 = SimpleDirectoryReader(input_dir="CHAPTER III.txt").load_data()
chp4 = SimpleDirectoryReader(input_dir="CHAPTER IV.txt").load_data()
chp5 = SimpleDirectoryReader(input_dir="CHAPTER V.txt").load_data()
chp6 = SimpleDirectoryReader(input_dir="CHAPTER VI.txt").load_data()

arr = [chp1,chp2,chp3,chp4,chp5,chp6]
arlm = ["0.2","0.1","0.3","0.4","0.5","0.1"]

choice = int(input("Select which chapter to choose from ...1 to 6  >>"))-1

llm = ChatOpenAI(temperature=arlm[choice],model='gpt-3.5-turbo')
service = ServiceContext.from_defaults(llm = llm)
index = VectorStoreIndex.from_documents(arr[choice])

chat_eng = index.as_chat_engine(service_context = service, chat_mode='react', verbose=True)

while True:
    question = input("Enter your Question?    >>")
    if question == "Thanks" or question=="End":
        break
    response = chat_eng.chat(question)
    print(response)
    print("\n")