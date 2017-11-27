import json
with open('config.js') as f:
    config = f.read()

config = '\n'.join(config.split('\n')[1:]) #chop var definition
config = json.loads(config)

print("Valid JSON for " + config['title'])
