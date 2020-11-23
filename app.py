from flask import Flask, render_template, request, url_for
import requests
import urllib3, json
#mean = [7.58716432e+00, 1.50410828e+03, 4.94015524e+00, 6.65630013e+00,
       #2.40410966e-03]
#std = [1.82624194e+01, 1.88860435e+06, 9.10645741e+00, 1.10369545e+01,
       #5.65751707e-01]

app = Flask(__name__)





@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        ws = request.form['a']
        tpc = request.form['b']
        wd = request.form['c']



        print(ws, tpc, wd)
        try:
            ws = float(ws)
            tpc = float(tpc)
            wd = float(wd)


        except:
            return render_template('index.html', err_msg='Enter Valid Data')
        url = "https://iam.cloud.ibm.com/identity/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = "apikey=" + 'ukbFyc5QJS9AHEv85VkJYWeDGZQf55gm8PYhQvNeC2pc' + "&grant_type=urn:ibm:params:oauth:grant-type:apikey"
        IBM_cloud_IAM_uid = "bx"
        IBM_cloud_IAM_pwd = "bx"
        response = requests.post(url, headers=headers, data=data, auth=(IBM_cloud_IAM_uid, IBM_cloud_IAM_pwd))
        print(response)
        iam_token = response.json()["access_token"]
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + iam_token}
        payload_scoring = {"input_data": [
            {"fields": ['Wind Speed (m/s)', 'Theoretical_Power_Curve (KWh)', 'Wind Direction (°)'],
             "values": [[ws, tpc, wd,]]}]}
        response_scoring = requests.post(
            'https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/1524f43a-37a7-4f5b-b133-494f082ac9cb/predictions?version=2020-11-23',
            json=payload_scoring, headers=header)
        print(response_scoring)
        a = json.loads(response_scoring.text)
        print(a)
        pred = a['predictions'][0]['values'][0][0]

        
        return render_template('index.html', result=pred)

    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)