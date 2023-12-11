import requests
import json

# local imports
from randchar import get_rand_id

def get_rand_char() -> int:
    """
    use microservice to generate random character id number, perform character search --> va search
    """
    try:
        rand_id = get_rand_id()
        return int(rand_id)
    except Exception:
        return "Please make sure random_character_gen microservice is running."


def get_va_by_search(search_str: str) -> list:
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
    vars = {
        'search': search_str,
        'page': 1,
        'perPage': 30
    }         
    
    try:
        results = contact_anilist(va_query, vars)
        filtered_staff = filter(lambda staff: 'Voice Actor' in staff['primaryOccupations'], results['data']['Page']['staff'])
        return list(filtered_staff)
    except Exception:
        return []

def get_va_chars(va_id: int) -> str:
    """
    use voice actor id to get top ten most popular characters and the anime they are from
    return formatted string: "character name (anime title)"
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

    try:
        results = contact_anilist(chars_query, vars)
        path = results['data']['Staff']['characters']['nodes']
        filtered_chars = [(char['name']['full'], char['media']['nodes'][0]['title']['english']) for char in path]
        formatted_out = ''
        for char in filtered_chars:
            formatted_out += f"{char[0]} ({char[1]}) \n"

        return formatted_out
    except Exception:
        return "Oops, looks like AniList might be down. Try again later."

def get_char_by_id(id: int) -> dict:
    """
    query anilist for character name and anime, using an id number
    returns string in "character (anime)" format
    """
    char_by_id = '''
    query ($id: Int) {
        Character(id: $id) {
        name {
            full
        }
        media (type: ANIME, sort: POPULARITY_DESC) {
            edges {
            node {
                title {
                userPreferred
                }
            }
            voiceActors (language: JAPANESE, sort: FAVOURITES_DESC) {
                id
                name {
                    full
                }
            }
            }
        }
        }
    }
    '''

    
    vars = {
        'id': id,
        'page': 1,
        'perPage': 30
    }

    try:
        results = contact_anilist(char_by_id, vars)
        path = results['data']['Character']['media']['edges'][0]
        char_info = {
            'va_id': path['voiceActors'][0]['id'],
            'va_name': path['voiceActors'][0]['name']['full'],
            'char_name': results['data']['Character']['name']['full'],
            'anime': path['node']['title']['userPreferred']
        }

        return char_info
    except Exception:
        return {}

def get_char_by_search(search_str: str) -> list:
    """
    query anilist for character name entered by user, filter results by popularity
    """
    char_search = '''
    query ($search: String, $page: Int, $perPage: Int) {
        Page(page: $page, perPage: $perPage) {
            pageInfo {
                perPage
            }
            
            characters (search: $search, sort: FAVOURITES_DESC) {
                id
                name {
                    full
                }
                media (type: ANIME) {
                    nodes {
                        title {
                            english
                        }
                    }
                }
            }
        }
    }
    '''
    vars = {
        'search': search_str,
        'page': 1,
        'perPage': 30
    }         
    
    try:
        results = contact_anilist(char_search, vars)
        filtered = list(filter(lambda x: len(x['media']['nodes']) > 0, results['data']['Page']['characters']))
        char_info = [{'char_id': char['id'], 
                    'char_name': char['name']['full'], 
                    'anime': char['media']['nodes'][0]['title']['english']} 
                    for char in filtered]
        return char_info
    except Exception:
        return []
    

def contact_anilist(query_str, vars):
    """
    beep beep boop hello, anilist?
    """
    url = 'https://graphql.anilist.co'

    # Make the HTTP Api request
    response = requests.post(url, json={'query': query_str, 'variables': vars}).json()

    return response