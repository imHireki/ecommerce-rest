"""
Core's useful functions
"""
import json

def get_secret(key):
    """ Get secrets from a local JSON file """
    with open('data.json') as jsonfile:
        data = json.load(jsonfile)
        response = data.get(key)
        return response
        