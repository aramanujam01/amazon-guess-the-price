from flask import Flask, render_template, request
import requests
import json
import random
import sys


app = Flask(__name__)
app.url_map.strict_slashes = True

game_rules = {
    'products': [],
    'rounds': 5
}

curr_state = {
        'image': "",
        'name': "",
        'price': 0,
        'curr_round': 0,
        'score': 0
}

@app.route("/")
def home():
    return render_template('page.html')

@app.route("/results")
def results():
    global game_rules
    global curr_state    

    avg_price = round(sum([product['price'] for product in game_rules['products_static']]) / len(game_rules['products_static']), 2)


    return render_template('game-end.html', rules = game_rules, state= curr_state, avg_price = avg_price)

def initialize_products():
    global game_rules
    global curr_state

    curr_state = {
        'image': "",
        'name': "",
        'price': 0,
        'curr_round': 0,
        'score': 0
    }

    srcs = [
        "https://cdn.britannica.com/80/150980-050-84B9202C/Giant-panda-cub-branch.jpg",
        "http://photos1.blogger.com/blogger/3657/1185/1600/060124_2_meteorological_1.jpg",
        "https://www.ecmwf.int/sites/default/files/styles/default_compressed/public/Dataset-card-450x300px.jpg?itok=YM8wk9T0",
        "https://upload.wikimedia.org/wikipedia/commons/c/c2/Eagle_wing_Spread_035.jpg",
        "'https://upload.wikimedia.org/wikipedia/commons/c/ce/F-WWCF_A350_LBG_SIAE_2015_%2818953559366%29.jpg'"
    ]
    names = [
        "Giant Panda Cub",
        "Volcano",
        "Dataset Card",
        "Eagle",
        "Airbus A350"
    ]
    prices = [
        3.50,
        4.50,
        5.50,
        2.40,
        7.80
    ]

    for i in range(5):
        product = {}
        product['image_src'] = srcs.pop()
        product['image_name'] = names.pop()
        product['price'] = prices.pop()
        game_rules['products'].append(product)
    
    game_rules['products_static'] = game_rules['products'][:]
    
    



@app.route('/game')
def game():
    global game_rules
    global curr_state

    if curr_state['curr_round'] == game_rules['rounds']:
        return results()

    if len(game_rules['products']) == 0:
        initialize_products()

    product = game_rules['products'].pop()

    curr_state['image'] = product['image_src']
    curr_state['name'] = product['image_name']
    curr_state['price'] = product['price']
    curr_state['curr_round'] += 1

    return render_template('game.html', rules = game_rules, state = curr_state)

@app.route('/game-result', methods = ['GET', 'POST'])
def showResults():
    global game_rules
    global curr_state

    if request.method == 'POST':
        dig1 = request.form['guess1']
        dig2 = request.form['guess2']
        dig3 = request.form['guess3']
        dig4 = request.form['guess4']
        dig5 = request.form['guess5']
    if request.method == 'GET':
        dig1 = request.args.get('guess1')
        dig2 = request.args.get('guess2')
        dig3 = request.args.get('guess3')
        dig4 = request.args.get('guess4')
        dig5 = request.args.get('guess5')

    guess = float(dig1 + dig2 + dig3 + '.' + dig4 + dig5)
    curr_state['score'] +=  int((100  / (abs(curr_state['price'] - guess) + 1)) * 10)

    return render_template('game-results.html', rules = game_rules, state = curr_state, guess = guess)