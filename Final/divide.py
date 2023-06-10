import codecs
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
