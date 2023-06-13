import json, csv, re

with open('data.json') as json_file:
    data = json.load(json_file)

    # Print the type of data variable
    print("Len:", len(data['data']))
    print("Type:", type(data['data']))

    count = 0
    requests = []
    responses = []
    for i in data['data']:
        print(i['title'])
        if i['title'] == 'Modern_history':
            for j in i['paragraphs']:
                for k in j['qas']:
                    count += 1
                    # print("question: ", k['question'])
                    requests.append(k['question'])
                    answers = ""
                    for m in k['answers']:
                        s = m['text']
                        answers += ('"'+s+'"')
                        print(answers)
                        # print(type(answers))
                    responses.append(answers)
                    print(responses)


    rows = zip(requests, responses)
    with open("datasets/chatbot_memory_testcases.csv", "w") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)
