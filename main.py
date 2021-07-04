from flask import Flask,jsonify,request
import requests
from collections import OrderedDict
import json
import urllib.request

app = Flask(__name__)


def get_names(res):
    lst = []
    for dic in res:
        lst.append(dic['name'])
    return lst


limit = 1500
offset = 0

flag = True
f_lst = []
while flag:
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/?limit={limit}&offset={offset}").json()
    if response['next'] == None:
        flag = False
    offset += len(response['results'])

    f_lst.extend(get_names(response['results']))

print(len(f_lst))
print(f_lst)

def get_from_list(dic_lst,kw):
    final_list = []
    for dic in dic_lst:
        final_list.append(dic[kw]['name'])
    return final_list




@app.route('/')
def pokemon_list():
    return json.dumps({'pokemon_list': f_lst})

@app.route('/pokemon_details')
def get_pokemon_details():
    poke_details_dict = OrderedDict()
    pokemon_name = request.args.get('name')
    pokemon_details = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}").json()
    poke_details_dict['id'] = pokemon_details['id']
    poke_details_dict['name'] = pokemon_name
    poke_details_dict['height'] = pokemon_details['height']
    poke_details_dict['weight'] = pokemon_details['weight']
    poke_details_dict['ability'] = get_from_list(pokemon_details['abilities'], 'ability')
    poke_details_dict['type'] = get_from_list(pokemon_details['types'], 'type')
    poke_details_dict['moves'] = get_from_list(pokemon_details['moves'], 'move')

    poke_img_url = pokemon_details['sprites']['other']['dream_world']['front_default']
    urllib.request.urlretrieve(poke_img_url, filename= pokemon_name+'.svg')
    return json.dumps(poke_details_dict)


if __name__=='__main__':
    app.run()



