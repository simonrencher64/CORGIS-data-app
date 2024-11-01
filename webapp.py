from flask import Flask, url_for, render_template, request
from markupsafe import Markup

import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_main():
    return render_template('home.html')

@app.route("/p1")
def render_page1():
    countries = get_country_options()
    return render_template('page1.html', country_options=countries)

@app.route("/explosionsbycountry")
def render_explosionsbycountry():
    countries = get_country_options()
    country = request.args.get("country")
    
    explosion = get_biggest_from_country(country)
    amount = get_amount_from_country(country)
    
    name = explosion["Data"]["Name"]
    if name != "Nan":
        fact1 = "The explosion with the biggest yield that was set off by " + country + " was " + name + "."
    else:
        fact1 = "The explosion with the biggest yield that was set off by " + country + " does not have a name."
    
    fact2 = "The explosion had a lower yield estimate of " + str(explosion["Data"]["Yield"]["Lower"]) + " kilotons of TNT and had an upper yield estimate of " + str(explosion["Data"]["Yield"]["Upper"]) + " kilotons of TNT."
    
    fact3 = "The amount of explosions that " + country + " has set off is " + str(amount) + "."
    return render_template('page1.html', country_options=countries, words1=fact1, words2=fact2, words3=fact3)

@app.route("/p2")
def render_page2():
    years = get_year_options()
    return render_template('page2.html', year_options=years)

@app.route("/explosionsbyyear")
def render_explosionsbyyear():
    years = get_year_options()
    year = request.args.get("year")
    
    results = get_amount_from_year(year)
    
    amount = results[0]
    biggest = results[1]
    countryMax = results[2]
    countryMaxName = results[3]
    
    fact1 = "In " + year + ", there were " + str(amount) + " nuclear bombs detonated."
    
    if biggest["Data"]["Name"] != "Nan":
        fact2 = "The biggest bomb detonated in " + year + " was named " + biggest["Data"]["Name"] + ", had an upper yield estimate of " + str(biggest["Data"]["Yield"]["Upper"]) + " kilotons, and was set off by " + get_country_name(biggest["Location"]["Country"]) + "."
    else:
        fact2 = "The biggest bomb detonated in " + year + " had an upper yield estimate of " + str(biggest["Data"]["Yield"]["Upper"]) + " kilotons and was set off by " + get_country_name(biggest["Location"]["Country"]) + "."
    
    fact3 = "The country with the most amount of bombs detonated in " + year + " is " + get_country_name(countryMaxName) + " with " + str(countryMax) + " bombs detonated."
    
    return render_template('page2.html', year_options=years, words1=fact1, words2=fact2, words3=fact3)
    
@app.route("/p3")
def render_page3():
    types = get_type_options()
    return render_template('page3.html', type_options=types)

@app.route("/explosionsbytype")
def render_explosionsbytype():
    types = get_type_options()
    type = request.args.get("type")
    
    results = get_explosions_by_type(type)
    
    amount = results[0]
    biggest = results[1]
    
    fact1 = "There were " + str(amount) + " nuclear bombs detonated that were " + type + "."
    
    if biggest["Data"]["Name"] == "Nan":
        fact2 = "The biggest bomb detonated " + type + " was detonated by " + get_country_name(biggest["Location"]["Country"]) + " and had a yield of " + str(biggest["Data"]["Yield"]["Upper"]) + " kilotons."
    else:
        fact2 = "The biggest bomb detonated " + type + " was detonated by " + get_country_name(biggest["Location"]["Country"]) + ", had a yield of " + str(biggest["Data"]["Yield"]["Upper"]) + " kilotons, and was named " + biggest["Data"]["Name"] + "."
    
    return render_template('page3.html', type_options=types, words1=fact1, words2=fact2)
    
@app.route("/p4")
def render_page4():
    graphpoints=format_dict_as_graph_points(get_explosions_by_year())
    print(graphpoints)
    
    return render_template('page4.html', points=graphpoints)




def get_country_options():
    with open('nuclear_explosions.json') as explosion_data:
        explosions = json.load(explosion_data)
    countries=[]
    for c in explosions:
        cname = get_country_name(c["Location"]["Country"])
        if cname not in countries:
            countries.append(cname)
    options=""
    for s in countries:
        options += Markup("<option value=\"" + s + "\">" + s + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options
    
def get_country_name(country):
    if country == "USA":
        return "The USA"
    elif country == "USSR":
        return "The USSR"
    elif country == "UK":
        return "The United Kingdom"
    elif country == "FRANCE":
        return "France"
    elif country == "CHINA":
        return "China"
    elif country == "INDIA":
        return "India"
    elif country == "PAKIST":
        return "Pakistan"

def get_type_name(type):
    if type == "Tower":
        return "in a tower"
    elif type == "Airdrop":
        return "in an airdrop"
    elif type == "Uw":
        return "underwater"
    elif type == "Surface":
        return "on the surface"
    elif type == "Crater":
        return "in a crater"
    elif type == "Ship":
        return "on a ship"
    elif type == "Atmosph":
        return "in the atmosphere"
    elif type == "Barge":
        return "on a barge"
    elif type == "Balloon":
        return "from a balloon"
    elif type == "Rocket":
        return "from a deployed rocket"
    elif type == "Space":
        return "in space"
    elif type == "Ug":
        return "underground"
    elif type == "Mine":
        return "in a mine"
    elif type == "Watersur" or type == "Water Su":
        return "on the surface of a body of water"
    elif type == "Shaft" or type == "Shaft/Gr" or type == "Shaft/Lg":
        return "from a vertical shaft underground"
    elif type == "Tunnel" or type == "Gallery":
        return "in a horizontal tunnel"

def get_year_options():
    with open('nuclear_explosions.json') as explosion_data:
        explosions = json.load(explosion_data)
    years=[]
    for c in explosions:
        year = c["Date"]["Year"]
        if year not in years:
            years.append(year)
    options=""
    for s in years:
        options += Markup("<option value=\"" + str(s) + "\">" + str(s) + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options



def get_type_options():
    with open('nuclear_explosions.json') as explosion_data:
        explosions = json.load(explosion_data)
    types=[]
    for c in explosions:
        type = get_type_name(c["Data"]["Type"])
        if type not in types:
            types.append(type)
    options=""
    for s in types:
        options += Markup("<option value=\"" + s + "\">" + s + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options


def get_biggest_from_country(country):
    with open('nuclear_explosions.json') as explosion_data:
        explosions = json.load(explosion_data)
    highest=0
    explosion = ""
    for c in explosions:
        if get_country_name(c["Location"]["Country"]) == country:
            if c["Data"]["Yield"]["Upper"] > highest:
                highest = c["Data"]["Yield"]["Upper"]
                explosion = c
    return explosion

def get_amount_from_country(country):
    with open('nuclear_explosions.json') as explosion_data:
        explosions = json.load(explosion_data)
    amount = 0
    for c in explosions:
        if get_country_name(c["Location"]["Country"]) == country:
            amount+=1
    return amount
    
def get_amount_from_year(year):
    with open('nuclear_explosions.json') as explosion_data:
        explosions = json.load(explosion_data)
    
    amount = 0
    
    biggest = ""
    biggestAmount = 0
    
    counts = {}
    
    for c in explosions:
        if str(c["Date"]["Year"]) == year:
            amount+=1
            
            if c["Data"]["Yield"]["Upper"] > biggestAmount:
                biggestAmount = c["Data"]["Yield"]["Upper"]
                biggest = c
            
            if c["Location"]["Country"] in counts:
                counts[c["Location"]["Country"]] = counts[c["Location"]["Country"]] + 1
            else:
                counts[c["Location"]["Country"]] = 1
    
    max = 0
    maxName = ""
    for c in counts:
        if counts[c] > max:
            max = counts[c]
            maxName = c
    
    return [amount,biggest,max,maxName]

def get_explosions_by_type(type):
    with open('nuclear_explosions.json') as explosion_data:
        explosions = json.load(explosion_data)
    
    amount = 0
    max = 0
    biggest = ""
    
    for c in explosions:
        if get_type_name(c["Data"]["Type"]) == type:
            amount += 1
            
            if c["Data"]["Yield"]["Upper"] > max:
                max = c["Data"]["Yield"]["Upper"]
                biggest = c
    
    return [amount,biggest]


def get_explosions_by_year():
    with open('nuclear_explosions.json') as explosion_data:
        explosions = json.load(explosion_data)
    
    counts = {}
    
    for c in explosions:
        if c["Date"]["Year"] in counts:
            counts[c["Date"]["Year"]] = counts[c["Date"]["Year"]] + 1
        else:
            counts[c["Date"]["Year"]] = 1
    
    return counts

def format_dict_as_graph_points(data):
    graph_points = ""
    for key in data:
        graph_points = graph_points + Markup('{ y: ' + str(data[key]) + ', label: "' + str(key) + '" }, ')
    graph_points = graph_points[:-2]
    return graph_points
    

if __name__=="__main__":
    app.run(debug=False)
