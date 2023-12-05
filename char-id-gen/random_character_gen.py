import requests
import time
import random

print('running')
while True:
    # Read txt file every 5 seconds
    time.sleep(3)
    with open('random_character_gen.txt') as read_file:
        data = read_file.read()

    # "run" has been written in txt file
    if data == "run":
        query = '''
            query ($page: Int, $perPage: Int) {
                Page(page: $page, perPage: $perPage) {
                    pageInfo {
                        total
                        perPage
                        lastPage
                    }
                    characters (sort: FAVOURITES_DESC) { 
                        id
                        name { 
                            full
                        }
                    }
                }
            }
        '''

        variables = {
            'page': 1,
            'perPage': 500
        }

        url = 'https://graphql.anilist.co'

        # Make request to API using query
        response = requests.post(url, json={'query': query, 'variables': variables}).json()
        
        # Parse character ID numbers from json
        response = response['data']['Page']['characters']

        # Create array of character ID numbers
        id_numbers = []
        for character in response:
            id_numbers.append(character['id'])

        # Choose random ID number from array
        random_id = random.choice(id_numbers)

        with open('random_character_gen.txt','w', encoding="utf-8") as write_file:  
            write_file.write(str(random_id))