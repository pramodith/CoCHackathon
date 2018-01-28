# Make a Difference Verve

This is the backend piece of our submission for the Make a Difference Hackathon at Georgia Tech, Jan 2018

The problem that we try to address through this app is Food Wastage

This is an android application that aids in preventing wastage of food. Once you go to the grocery store all you need to do is take a photo
of your bill.
We will identify all the food items and will give you timely prompts about the expiration date of items.
To reduce wastage, the app will give you suggestions about what food you can cook using the ingredients that are about to expire.
We also give you an option to donate the food away to the needy, by finding the closes charity organizations to your work place or
home.

## Technologies Used
* [Google Cloud Vision API](https://cloud.google.com/vision/) to extract text from  images of bills
* [Edamam API](https://developer.edamam.com/) to extract the food items from the bill and provide recipes based on ingredients that the user has
* [Google Places/Maps API](https://developers.google.com/places/) to find the closest charitable organizations to the user
* [Google Firebase](https://firebase.google.com/) to send downstream notifications to clients

Server: Python Flask
Client: Android Application

## Future Prospects

* Adding a claim food feature: You often have leftovers after parties, why waste the food let your friends who live near you come
and claim the food.
* Once you are in a grocery store we will remind you of the items that you ended up throwing out, so that you'll be wary of what and how
much food you buy.

## Setup

* Install python
* Install required libraries
    ```sh
    pip install -r requirements.txt
    ```
* Run the server
    ```sh
    FLASK_APP=backend.app.py flask run --host=0.0.0.0
    ```
