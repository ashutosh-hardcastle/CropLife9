# Importing essential libraries and modules
from flask import Flask, render_template, Markup
import pandas as pd
from utils.fertilizer_dict import fertilizer_dic
import disease_dictionary
from flask import request
from flask import Flask, render_template, jsonify, request, Markup
from disease_model import predict_image

# ------------------------------------ FLASK APP -------------------------------------------------

app = Flask(__name__)

@app.route('/')
def home():
    title = 'CropLife'
    return render_template('index.html', title=title)

# render fertilizer calculator form page

@app.route('/crop_disease')
def crop_disease():
    title = 'CropLife'
    return render_template('crop_disease.html', title=title)

# render pest recommendation form page

@app.route('/pest_recommend')
def pest_recommend():
    title = 'CropLife'
    return render_template('/pest.html', title=title)

# render fertilizer recommendation form page

@app.route('/fertilizer')
def fertilizer_recommendation():
    title = 'CropLife'
    return render_template('fertilizer2.html', title=title)


#########Post Functions##########



@app.route('/disease_result', methods=['POST'])
def disease_predict():
    if request.method == 'POST':
        try:
            file = request.files['file']
            img = file.read()
            prediction = predict_image(img)
            print(prediction)
            res = Markup(disease_dictionary.disease_dict[prediction])
            return render_template('disease_result.html', status=200, result=res)
        except:
            pass
    return render_template('disease_result.html', status=500, res="Internal Server Error")



@app.route('/pest_result', methods=['POST'])
def predict():
    title = 'CropLife'
    if request.method == 'POST':
        pest_name = request.form['pestname']
        return render_template(pest_name + ".html", title=title)


@app.route('/fertilizer-result', methods=['POST'])
def fert_recommend():
    title = 'CropLife'

    crop_name = str(request.form['cropname'])
    N = int(request.form['nitrogen'])
    P = int(request.form['phosphorous'])
    K = int(request.form['pottasium'])
    # ph = float(request.form['ph'])

    df = pd.read_csv('Data/fertilizer_data.csv')

    nr = df[df['Crop'] == crop_name]['N'].iloc[0]
    pr = df[df['Crop'] == crop_name]['P'].iloc[0]
    kr = df[df['Crop'] == crop_name]['K'].iloc[0]

    n = nr - N
    p = pr - P
    k = kr - K

    if n < 0:
        key1 = "NHigh"
    elif n > 0:
        key1 = "NLow"
    else:
        key1 = "NNo"

    if p < 0:
        key2 = "PHigh"
    elif p > 0:
        key2 = "PLow"
    else:
        key2 = "PNo"

    if k < 0:
        key3 = "KHigh"
    elif k > 0:
        key3 = "KLow"
    else:
        key3 = "KNo"

    abs_n = abs(n)
    abs_p = abs(p)
    abs_k = abs(k)

    response = Markup(str(fertilizer_dic[key1]))
    response1 = Markup(str(fertilizer_dic[key2]))
    response2 = Markup(str(fertilizer_dic[key3]))

    return render_template('fertilizer-result.html', recommendation=response,
                           recommendation1=response1, recommendation2=response2,
                           title=title, diff_n=abs_n, diff_p=abs_p, diff_k=abs_k)


# ===============================================================================================
if __name__ == '__main__':
    app.run(debug=False)


