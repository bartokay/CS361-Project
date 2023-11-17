# README
perm-server.py

## Prerequisites:
You will need the Python requests and json modules:

```python
import requests			# pip install requests if you don't have it
import json
```

Running from terminal: 

	python perm-server.py

<b>Only works with python 3!!</b>




## How to request:

Example URL for GET request:

```python
url = 'http://localhost:8000/perm/?min=1&max=10'
```

- You should just need to change the values to the right of the "=" sign for both min and max (currently 1 and 10) <Br> to whatever the minimum and maximum values are in the range of numbers you want a permutation for. I recommend an f-string, but <br> use whatever is comfortable to you.
- The path MUST have the structure: /?min={some number}&max={some larger number}
- The port number (8000) is currently hardcoded, if you want to use a different one you can change it in the code (8000 should be fine though).
- Run perm-server, and once you can see the "server listening on port 8000" message in the terminal, you can run your app to start requesting permutations

## How to receive:
	
```python
response = requests.get(url).json()

# convert json object to prettified json string
json_obj = json.dumps(response, indent=4, ensure_ascii=False).encode('utf8').decode()
print(json_obj)

# these should be the same thing
print(json.loads(json_obj))     # load prettified thing
print(response)     			# original

# get just perm values (list)
print(response.get("perm"))
```
** note that url in `requests.get(url).json()` matches the variable name from the GET request example.

The unpacked json object saved in the variable `permutation` has the key: `perm` whose value is a list with the permutation. When printed it will look something like:

	{
		"perm": [5, 9, 7, 4, 6, 3, 1, 8, 2, 10, 11]
	}


	

## UML Sequence Diagram

![Request/Receive Sequence Diagram](/microservice/perm-uml.png)