import requests
import streamlit as st

url = ['http://localhost:8000/predictions','http://localhost:9000/predictions']
# Fonction pour envoyer la requête POST à l'API
def predict_client_classification(data):
    response = requests.post(url[0], json=data)
    if response.ok:
        result = response.json()
        return result['prediction']
    else:
        st.error('Erreur lors de la prédiction.')

def predict_client_classification_no_corr(data):
    response = requests.post(url[1], json=data)
    if response.ok:
        result = response.json()
        return result['prediction']
    else:
        st.error('Erreur lors de la prédiction.')