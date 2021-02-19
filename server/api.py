##################################################
__author__ = "Rodrigo Silveira"
__version__ = "1.0.1"
__email__ = "rodrigo.silveira7@gmail.com"
__status__ = "Production"
##################################################

# Libs ############################################
import pandas as pd
import numpy as np
import re
import unicodedata
import pickle
import nltk
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

# Functions #######################################

#Generate json file to test API
def generate_jsonfile():
    TEST_PRODUCTS_PATH = os.environ['TEST_PRODUCTS_PATH']
    df_data = pd.read_csv('/usr/src/data/test_products.csv', sep=',')
    df_generate_json = pd.DataFrame(columns = ['query', 'title', 'concatenated_tags'])
    df_generate_json['query'] = df_data['query'].str.lower() 
    df_generate_json['title'] = df_data['title'].str.lower() 
    df_generate_json['concatenated_tags'] = df_data['concatenated_tags'].str.lower()
    #df_generate_json = df_generate_json.head(20)
    json =df_generate_json.to_json(orient = "records")
    json = '{"products":' + json + '}'
    f = open(TEST_PRODUCTS_PATH, "w")
    f.write(json)
    f.close()


#remove duplicate itens and especial caracters ###
def dedup_esp_caract(txt):
    x = str(txt)
    nfkd = unicodedata.normalize('NFKD', x)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    x = re.sub('[^a-zA-Z0-9 \\\]','', palavraSemAcento)
    x = x.split(' ')
    x = ' '.join([str(elem) for elem in set(x)])
    return x

#Json data #######
def predict_text(data):
    v_categories = {}
    list_categories = []
    #data = json.loads(texts)    
    for text in data['products']:        
        v_text = dedup_esp_caract(text['title'] +' '+ text['query'] +' '+ text['concatenated_tags'])        
        prediction = loaded_model.predict(np.array([v_text]))        
        output = prediction[0]        
        list_categories.append(cat_dict[int(output)])    
    v_categories["categories"] = list_categories           
    return v_categories


# 1- Model Loading ###################################
MODEL_PATH = os.environ['MODEL_PATH']
loaded_model = pickle.load(open(MODEL_PATH, 'rb'))

#Categories based on the training model/label encoder
cat_dict = {2:'Decoração', 5 :'Papel e Cia', 4 :'Outros', 0:'Bebê', 3:'Lembrancinhas', 1:'Bijuterias e Jóias'}

#Generate Json File
generate_jsonfile()

#2 - Categorization Endpoint #########################
app = Flask(__name__)
#To verify if flask is running
@app.route('/', methods=['GET', 'POST'])
def welcome():
    return "Flask is running"

#Call predictions based on the json input and return categories
@app.route('/v1/categorize', methods=['POST'])
def json_input():
    if check_request(request): #validate json/structure
        request_data = request.get_json()
        cat = predict_text(request_data)
        return jsonify(cat)        
    else:
        return "400 (Bad Request)"    

#3- Input Validation ###############################
#check if structure is valid
def validateStruct(data):
    number = 0
    try: 
        for text in data['products']:
            number +=1
            v_text = text['title'] +' '+ text['query'] +' '+ text['concatenated_tags']
            if number == 50:
                break    # break here
    except:
        return False
    return True 

#check if request is valid
def check_request(request):
    try:
        if request.headers['Content-Type'] == 'application/json':
            data = request.get_json()        
            if validateStruct(data) == False:
                return False # structure is not ok
            else:
                return True # request is ok
        else:
            return False #request is not an application/json'
    except:
        return False
