from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid
import joblib
import pandas as pd

model_corr = joblib.load("./ml_models/RandomForest_One_Vs_All.pkl")
model_no_corr = joblib.load("./ml_models/RandomForest_One_Vs_All_No_Corr.pkl")

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
  

  def predict(self):
    data = {
    "balance": request.form.get('balance'),
    "balance_freq": request.form.get('balance_freq'),
    "purchases": request.form.get('purchases'),
    "oneoff_purchases": request.form.get('oneoff_purchases'),
    "installments_purchase": request.form.get('installments_purchase'),
    "cash_advance": request.form.get('cash_advance'),
    "purchases_freq": request.form.get('purchases_freq'),
    "oneoff_purchases_freq": request.form.get('oneoff_purchases_freq'),
    "purchase_installments_freq": request.form.get('purchase_installments_freq'),
    "cash_advance_freq": request.form.get('cash_advance_freq'),
    "cash_advance_trx": request.form.get('cash_advance_trx'),
    "purchases_trx": request.form.get('purchases_trx'),
    "credit_limit": request.form.get('credit_limit'),
    "payments": request.form.get('payments'),
    "min_payments": request.form.get('min_payments'),

    "pct_off_full_payment": request.form.get('pct_off_full_payment'),
    "min_payments": request.form.get('tenure')
  }
    data = request.get_json(force=True)
    X = pd.DataFrame.from_dict(data, orient='index').transpose()
    y_pred = model_corr.predict(X)

    return jsonify(prediction=y_pred.tolist()), 200
  

