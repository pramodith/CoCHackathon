import requests
import urllib.parse
import json
import pprint


class Food_Bank:

    def __init__(self):
        self.api_id_recipe = "af08e16d"
        self.api_key_recipe = "00c8c5a5d4723815822edcfd56de9dd4"
        self.api_id_food = "5140730c"
        self.api_key_food = "b5e3d17b41efb6e533827f95e9ab3151"

    def get_food(self, text):
        url_text = urllib.parse.quote_plus(text)
        response = requests.get(
            'https://api.edamam.com/api/food-database/parser?ingr==' + url_text + '&app_id=' + self.api_id_food + '&app_key=' + self.api_key_food + '&page=0')
        food = (response.json())
        pp = pprint.PrettyPrinter(width=10, compact=True)
        print("food", food)
        if (food and food['hints']):
            food_items = food['hints'][0]['food']['label']
            return food_items
        else:
            return None

    def fill_food(self, text):
        url_text = urllib.parse.quote_plus(text)
        response = requests.get(
            "https://api.edamam.com/auto-complete?q =" + url_text + "&limit=10&app_id =$" + self.api_id_food + "&app_key =$" + self.api_key_food)
        suggested = response.json()
        print(suggested)

    def get_recipe(self, food_items, preferences=None):
        recipes = []
        max_ingredients = None
        url_text = urllib.parse.quote_plus(food_items)
        url = 'https://api.edamam.com/search?q=' + url_text + '&app_id=' + self.api_id_recipe + '&app_key=' + self.api_key_recipe + '&from=0&to=3'
        if preferences:
            if "max_ingredients" in preferences:
                max_ingredients = preferences['max_ingredients']
                url += '&ingr=' + max_ingredients
            if "calories" in preferences:
                max_calories = preferences['calories']
                url += '&calories=' + urllib.parse.quote_plus('lte ') + max_calories
        response = requests.get(url)
        food = (response.json())
        food = food['hits']
        print(food[1])
        # for i in range(min(len(food),3)):
        #     recipes.append(food[i]['recipe']['label']+": ")
        #     for ingredient in food[i]['recipe']['ingredients']:
        #         recipes[i]+=ingredient['text']+", "
        # recipes[i]+="\n"+food[i]['recipe']['url']
        return list(map(lambda item: {"recipe": item["recipe"]["label"], "url": item["recipe"]["url"],
                                      "ingredients": ' '.join(list(map(lambda zz: zz["text"], item["recipe"]["ingredients"])))},
                        food))[
               :3]

# f=Food_Bank()
# print(f.get_food('hammer'))
# print(f.get_recipe("chicken,milk"))
