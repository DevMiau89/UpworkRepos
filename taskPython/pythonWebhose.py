import webhoseio, json

webhoseio.config(token="afc23cfb-7bde-4fa9-a971-28a17969f5ae")
query_params = {
    "q": "organization:\"Apple\"",
    "sort": "crawled"
}
results = webhoseio.query("filterWebContent", query_params)

data = {}
output = []

while True:
    temp = webhoseio.get_next()
    output = output+temp['posts']
    if temp['moreResultsAvailable'] <= 0:
        break

# print('*******************************')
print (len(output))

data['output'] = output

with open('data.json','w', encoding='utf8') as outfile:
    data = json.dumps(data,
                        indent=4, sort_keys=True,
                        separators=(',', ': '), ensure_ascii=False)

    outfile.write(data)

json_list = []

with open('data.json', encoding='utf-8') as data_file:
    data = json.loads(data_file.read())
    json_list = data['output']


#prints ”title”, “text”, “url”
posts_10 = json_list[:10]

# print('*******************************')
print(len(posts_10))

for item in posts_10:
    for key, value in item.items():
        if key == 'title':
            print('Title is: ' + value + '\n')
        if key == 'text':
            print('Text is: ' + value + '\n')
        if key == "url":
            print('URL is: ' + value)

