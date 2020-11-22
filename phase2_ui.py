from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)

from phase2_elasticsearch import elastic_search
from phase2_querying import get_movies


def search(data):
    if data["category"] == "Custom":
        print(data)
        data["result"] = get_movies(data["query"])
        print("custom result:", data["result"])
    
    else:
        data["result"] = elastic_search(data["category"], data["query"])
        print("elastic result:", data["result"])

    return data

@app.route('/')
def index():
	return render_template("./index.html")

@app.route('/flask')
def hello_flask():
   return 'Hello Flask'

@app.route('/result', methods=['POST'])
def hello_python():
   return render_template("./result.html", result =  search ( dict( request.form.items() ) ) )
   

if __name__ == '__main__':
   app.run()