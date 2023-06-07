from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid
import pandas as pd
import joblib

model_corr = joblib.load("ml_models\RandomForest_One_Vs_All_No_Corr.pkl")
model_no_corr = joblib.load("ml_models\RandomForest_One_Vs_All.pkl")
class User:

  def start_session(self, user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    return jsonify(user), 200

  def signup(self):
    # Create the user object
    user = {
      "_id": uuid.uuid4().hex,
      "name": request.form.get('name'),
      "email": request.form.get('email'),
      "password": request.form.get('password')
    }

    # Encrypt the password
    user['password'] = pbkdf2_sha256.encrypt(user['password'])

    # Check for existing email address
    if db.users.find_one({ "email": user['email'] }):
      return jsonify({ "error": "Adresse Email déjà utilisée!" }), 400

    if db.users.insert_one(user):
      return self.start_session(user)

    return jsonify({ "error": "Création de compte échouée!" }), 400
  
  def signout(self):
    session.clear()
    return redirect('/')
  
  def login(self):

    user = db.users.find_one({
      "email": request.form.get('email')
    })

    if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
      return self.start_session(user)
    
    return jsonify({ "error": "Paramètres de connexion invalides!" }), 401
  

  
  def upload_file():
      if request.method == 'POST':
          fichier = request.files['predire_excel_form']
          if fichier:
              # Charger le fichier Excel dans un DataFrame
              df = pd.read_excel(fichier)
              return df.to_html()
           

    
