import requests
import json

# local imports
from randchar import get_rand_id

def get_rand_char():
    """
    use microservice to generate random character id number, perform character search --> va search
    """
    rand_id = get_rand_id()
    print(rand_id)


def get_va_by_search(search_str: str):
    """
    query anilist for va name entered by user, filter results by voice actor occupation
    """
    va_query = '''
    query ($search: String, $page: Int, $perPage: Int) {
    Page(page: $page, perPage: $perPage) {
        pageInfo {
        perPage
        }
        
        staff (search: $search, sort: FAVOURITES_DESC) {
        id
        name {
            full
        }
        primaryOccupations
        
        }
    }
    }
    '''
    # Define our query variables and values that will be used in the query request
    vars = {
        'search': search_str,
        'page': 1,
        'perPage': 30
    }         
    
    results = contact_anilist(va_query, vars)
    filtered_staff = filter(lambda staff: 'Voice Actor' in staff['primaryOccupations'], results['data']['Page']['staff'])
    return list(filtered_staff)

def get_va_chars(va_id: int):
    """
    give formatted string of the chars?
    """
    chars_query = '''
    query ($id: Int) {    
        Staff (id: $id) {
            characters(page: 1, perPage: 10, sort: FAVOURITES_DESC) {
                nodes {
                    name {
                        full
                    }
                    media (sort: FAVOURITES_DESC) {
                        nodes {
                            title {
                                english
                            }
                        }
                    }
                }
            }
        }
    }
    '''

    vars = {
        'id': va_id
    }

    results = contact_anilist(chars_query, vars)
    path = results['data']['Staff']['characters']['nodes']
    filtered_chars = [(char['name']['full'], char['media']['nodes'][0]['title']['english']) for char in path]
    formatted_out = ''
    for char in filtered_chars:
        formatted_out += f"{char[0]} ({char[1]}) \n"

    return formatted_out

def contact_anilist(query_str, vars):
    """
    beep beep boop hello, anilist?
    """
    url = 'https://graphql.anilist.co'

    # Make the HTTP Api request
    response = requests.post(url, json={'query': query_str, 'variables': vars}).json()
    # print(json.dumps(response, indent=4, ensure_ascii=False).encode('utf8').decode())

    return response