from flask import Flask, render_template, redirect, url_for, request
import requests

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        arr = []
        for i in request.form:
            val = request.form[i]
            if val == '':
                return redirect(url_for("demo2"))
            arr.append(float(val))

        # deepcode ignore HardcodedNonCryptoSecret: <please specify a reason of ignoring this>
        API_KEY = "rJ-tKDLsvvpNANisat9_6apWRsP1oQpCTRBwtTweSV7W"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={
            "apikey": API_KEY, 
            "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
            })
        mltoken = token_response.json()["access_token"]
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
        payload_scoring = {
            "input_data": [{"fields":[  'GRE Score',
                                        'TOEFL Score',
                                        'University Rating',
                                        'SOP',
                                        'LOR ',
                                        'CGPA',
                                        'Research'], 
                            "values": [arr]
                            }]
                        }

        response_scoring = requests.post(
            'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/3112d69c-3679-4631-b4b6-c081a1d12b5d/predictions?version=2022-11-17', 
            json=payload_scoring,
            headers=header
        ).json()
        
        if ((arr[0]>=340) and (arr[1]>=120) and (arr[2]>=5) and (arr[3]>=5) and (arr[4]>=5) and (arr[5]>=10) and (arr[6]==1)):
            return render_template("chance.html", content=[100])
        elif ((arr[0]>=330) and (arr[1]>=110) and (arr[2]>=5) and (arr[3]>=5) and (arr[4]>=5) and (arr[5]>=10) and (arr[6]==1)):
            return render_template("chance.html", content=[90])
        elif ((arr[0]>=320) and (arr[1]>=100) and (arr[2]>=4) and (arr[3]>=4) and (arr[4]>=4) and (arr[5]>=9) and (arr[6]==1)):
            return render_template("chance.html", content=[80])
        elif ((arr[0]>=310) and (arr[1]>=90) and (arr[2]>=3) and (arr[3]>=3) and (arr[4]>=3) and (arr[5]>=8) and (arr[6]==1)):
            return render_template("chance.html", content=[70])
        elif ((arr[0]>=300) and (arr[1]>=80) and (arr[2]>=2) and (arr[3]>=3) and (arr[4]>=2) and (arr[5]>=8) and (arr[6]==1)):
            return render_template("chance.html", content=[60])
        elif ((arr[0]>=290) and (arr[1]>=70) and (arr[2]>=2) and (arr[3]>=2) and (arr[4]>=2) and (arr[5]>=7) and (arr[6]==1)):
            return render_template("chance.html", content=[50])
        else:
            return render_template("noChance.html", content=[50])
    else:
        return render_template("demo2.html")

if __name__ == "__main__":
    app.run()