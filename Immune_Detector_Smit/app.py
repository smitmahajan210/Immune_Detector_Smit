from flask import Flask,render_template,request
from flask import redirect, url_for
from flask import jsonify
import requests
import pickle
import numpy as np
import sklearn
#ur
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn import metrics

app = Flask(__name__)


@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        name = (request.form['nameid'])
        sex = (request.form['sex'])
        rbc=(request.form['rbc'])
        wbc=(request.form['wbc'])
        hemo=(request.form['Hemo'])
        mcv=(request.form['mcv'])
        mch=(request.form['mch'])
        mchc=(request.form['mchc'])
        Neutro=(request.form['Neutro'])
        platlet=(request.form['platlet'])
        features = [[rbc,wbc,hemo,mcv,mch,mchc,Neutro,platlet]]
        features = np.asarray(features, dtype='float64')
        deficiency = []
        str1=""
        
        if rbc < '4.5':
            deficiency  += ['rbc'] 
        if wbc < '3000':
            deficiency  += ['wbc'] 
        if hemo < '115':
            deficiency  += ['hemo'] 
        if mcv < '60':
            deficiency  += ['mcv'] 
        if mch < '25':
            deficiency  += ['mch'] 
        if mchc < '2.0':
            deficiency  += ['mchc'] 
        if Neutro < '30':
            deficiency  += ['Neutro'] 
        if platlet < '120000':
            deficiency  += ['platlet']
        No_of_ele = deficiency.count(('rbc','wbc','hemo','mcv','mch','mchc','Neutro','platlet'))
        No_for_loop = int(No_of_ele - 1)
        for ele in deficiency:  
            str1 += ele
            str1 += ' '

        if(sex=='male'or'Male'or'MALE' ):
            clf = joblib.load('knnmale.sav')
            output = clf.predict(features)[0]
        else:
            clf = joblib.load('knnfemale.sav')
            output = clf.predict(features)[0]

        if output == 0:
            return render_template('index.html',Hello="Hello",name=name,prediction_text="Your Immune level is Low.",def_pred="You have defeciency in ",def_val=str1 ,prediction_text2= "We suggest you to go through diet to improve Immune.",set_tab=1)
        else:
            return render_template('index.html',Hello="Hello",name=name,prediction_text="Your Immune is Healthy.",set_tab=1)
    else:
        return render_template('index.html')







if __name__=="__main__":
    app.run(debug=True)
