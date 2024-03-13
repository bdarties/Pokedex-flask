# pour lancer ce programme :
#
# export FLASK_APP=app.py
# export FLASK_ENV=development
# flask run --debug
#
# le mode debug permet de relancer automatiquement le serveur lors de changements détectés

# Contenu du fichier app.py
from flask import Flask, render_template
from flask import request
import requests

app = Flask(__name__)

tab_pokemons = [
    {"id": 1, "name": "Bulbasaur", "type": "Grass/Poison"},
    {"id": 2, "name": "Charmander", "type": "Fire"},
    {"id": 3, "name": "Squirtle", "type": "Water"},
    {"id": 4, "name": "Pikachu", "type": "Electric"},
    {"id": 5, "name": "Jigglypuff", "type": "Normal/Fairy"},
    {"id": 6, "name": "Meowth", "type": "Normal"},
    {"id": 7, "name": "Psyduck", "type": "Water"},
    {"id": 8, "name": "Geodude", "type": "Rock/Ground"},
    {"id": 9, "name": "Magikarp", "type": "Water"},
    {"id": 10, "name": "Eevee", "type": "Normal"}
]



# URL de base de l'API PokeAPI
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/"

@app.route('/')
def home():
    # Effectuer une requête pour obtenir la liste des Pokémon
    response = requests.get(POKEAPI_BASE_URL + 'pokemon/')
    print(response.json())
    tabPokemons = response.json().get('results', [])
    # Filtrer les Pokémon en fonction de la recherche
    search_term = request.args.get('search', '').lower()
    if search_term:
        tabPokemons = [pokemon for pokemon in tabPokemons if search_term in pokemon['name'].lower()]

    # Filtrer les Pokémon en fonction de la recherche
    #search_term = request.args.get('search', '').lower()
    #if search_term:
    #    pokemons = [pokemon for pokemon in pokemons if search_term in pokemon['name'].lower()]

    return render_template('index.html', pokemons=tabPokemons)

@app.route('/pokemon/<int:id>/')
def pokemon_detail(id):
    # récupération des détails d’un pokemon et rendu 
    pokemon = get_pokemon_details(id)
    return render_template('detail.html', pokemon=pokemon)

# Fonction Jinja pour extraire l'ID à partir de l'URL de l'API
@app.template_filter('extract_id')
def extract_id(url):
    print(url.split('/'))
    return int(url.split('/')[-2])

@app.template_filter('getImg')
def getImg(id) : 
  response = requests.get(POKEAPI_BASE_URL + f'pokemon/{id}')
  return response.json().get("sprites").get("front_default")


def get_pokemon_details(id):
    # Effectuer une requête pour obtenir les détails d'un Pokémon
    response = requests.get(POKEAPI_BASE_URL + f'pokemon/{id}')
    pokemon = response.json()
    return pokemon
