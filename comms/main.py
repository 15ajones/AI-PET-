from livereload import Server

from flask import Flask, redirect, url_for

app = Flask(__name__)



@app.route('/')
def home():

    i = 0
    count = 0


    for i in range(10):
    
    
     
     count = count + 2

     count = str(count)
     print(count)
     return count
    
@app.route('/reload') 
def reload():
   return redirect(url_for('index')) 

if __name__ == '__main__':
    app.run(debug=True)
    server = Server(app.wsgi_app)
    server.watch('home')
    server.serve(port=5000, host= 'localhost')