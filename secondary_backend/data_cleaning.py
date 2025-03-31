import json


with open("data.json", "r") as f:
    data = json.load(f)

convos = list()
convo = list()


for i in range(len(data)):
    if len(convo) > 1:
        convos.append(convo.copy())
        convo.clear()
    else:
        convo.append(data[i])
        

with open("user_data.json", "w") as ff:
    json.dump(convos, ff, indent=4)