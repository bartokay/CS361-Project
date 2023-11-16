# README
perm-server.py


<b>Only works with python 3!!</b>

You will need the Python requests and json modules:

	import requests
	import json

Running from terminal: python3 perm-server.py

## How to request:

Use this line somewhere in your code:

	url = 'http://localhost:8000/?min=1&max=10'

- You should just need to change the values to the right of the "=" sign for both min and max (currently 1 and 10) <Br> to whatever the minimum and maximum values are in the range of numbers you want a permutation for. I recommend an f-string, but <br> use whatever is comfortable to you.
- The path MUST have the structure: /?min={some number}&max={some larger number}
- The port number (8000) is currently hardcoded, if you want to use a different one you can change it in the code (8000 should be fine though).
- Run perm-server, and once you can see the "server listening on port 8000" message in the terminal, you can run your app to start requesting permutations

## How to receive:
	
	response = requests.get(url).json()
** note that url matches the variable name for the request

Then, unpack the json from the response:

	permutation = json.dumps(response, indent=4, ensure_ascii=False).encode('utf8').decode()

