from flask import Flask, send_from_directory
from hello import hello
from download_grib2_files import download_grib2_files

 #app is an instance of the Flask class and __name__ is a Python predefined variable which is set to the name of the module in which it is used.
# static_folder is the folder where the app will look for static files like images, CSS, and JavaScript files.
# static_url_path is the URL path that will be used to access the static files.
app = Flask(__name__, static_folder='dist', static_url_path='/')

@app.route('/')
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__': #conditional runs app only if the script is executed directly from the Python interpreter and not used as an imported module
    app.run(debug=True, host='localhost', port=8080) # debug=True will automatically reload the server when you make changes to the code

#To run the app, run the following command in the terminal: python app.py 
#this will start the server and you can access the app in your browser at the URL given in the terminal output.
    
#venv is a virtual environment that is used to isolate the dependencies required by different projects.
    




