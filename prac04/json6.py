import json
x = '{"name": "Emil", "age": 30}'
y = json.loads(x)
print(y["age"])