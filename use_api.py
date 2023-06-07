import requests

url = 'http://localhost:8000/predictions'
# Fonction pour envoyer la requête POST à l'API


def predict_client_classification(data):
    response = requests.post(url[0], json=data)
    if response.ok:
        result = response.json()
        return result['prediction']
