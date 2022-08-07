from flask import Flask, request, session

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello!</h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)



#never enable debug mode on a productino server. the debuggerallows theclient to request remote code execution, so it makes your prod server vulnerable to attacks. 
#as a simple protection measure, the debugger needs to be activated with a PIN, printedon the console by the 'flask run' command

#export FLASK_APP=app.py in linux/macos is the same as set FLASK_APP=app.py in windows.
#simliar for FLASK_DEBUG=1 etc etc and all environment variables

# when flask recieves a request from a client, the view function is served with several objects. one being the 'request object'. this object encapsulates the HTTP reuqest sent by theclient.

#the view function gains access to the request object Flask uses "contexts" to temporarily make certain objects globally accessible. 

@app.route('/contexts')
def context():
    user_agent = request.headers.get('User-Agent') #note how this is used as if it were a global variable, 'request.attr' (NOTE THE REQUESTS OBJECT IS NOT ACTUALLY A GLOBAL VAR)
    return '<p>Your browser is {}</p>'.format(user_agent)

#THERE ARE TWO CONTEXTS IN FLASK: the application context and the request context. 

#each of these 'exposes' variables for use:
#request: request context: object that holds HTTP request
#session: request context: user session. returns dictionary that the app can use to store values that are 'remembered' between requests
#current_app: application context: the application instance for the active application
#g: application context: an object that the application can use for temporary storage during the handling of a request. This variable is reset with each request.

#steps/ order of operations for contexts:
#Flask activates (pushes) the application and request contexts before dispatching a request to the applicatio, and removes them after the request is handled.
#when the application context is pushed, the 'current_app' and 'g' variables become available to the trhead
#when the request context is pushed, the request and session objects become availabel to the thread.

#if any of these variables are accessed WITHOUT an activate application or request context, and error is generated. 
#WILL BE EXPLAINED MORE CONCRETELYE HOW THESE ARE UTILIZING IN FUTURE CHAPTERS. 

from flask import current_app

print(app.url_map) #prints out the URL mappings for each of the view functions tied to the decorators. 
#flask also includes a /static/<filename> route that allow flask to access static files

#it also lists a GET, HEAD, AND OPTIONS list of elements:
#these are the'request methods' that are handled by the routes.
#the HTTP specification defines that all requests are issues with a method, which normally indicates what action the client is asking the server to perform.
#flask attaches methods to each route so that different request methods sent to the same URL can be handledby different view functions. 

#HEAD and OPTIONS are handled automatically by flask.
#in this application in essence all of the routes are attached ot the GET method, which is used when the client wants to reuqest information such as a web page.


####
#the request object:

#flask exposes the request object as a context variable named 'REQUEST'. this object contains all usfeull information that the brownser includedin the HTTP requset:
#some of most commonly use attributes:

#request.args, reguest.values,request.form, request.cookies, request.headers, request.files, request.get_data(), request.get_json(), request.blueprint, request.endpoint(), request.method(), request.scheme(), request.is_secure()
#an example using request.is_secure() which returns True is request came trhogh a secure (HTTPS) connections:

@app.route('/secure')
def check_secure():
    sec = request.is_secure
    return f'<h1>The connection uses HTTPS: {sec}</h1>'

@app.route('/getpost')
def get_post():
    method_type = request.method
    return method_type

@app.route('/getip')
def get_ip():
    ip = request.remote_addr
    return ip

#REQUEST HOOKS:
#sometimes it is useful to executre code BEFORE or AFTER each request is processed. eg. at start of each rquest it may be necessary to create a database connection or authenticate the user making
#the resuest. request hooks allow you to execute this code prior to, after, prior to the first request.

#before_request : registers a function to run before each request
#before_first_request : registeres a functino to run only before the first request is handled (convenient for addition of server init tasks)
#after_request : registers a function to run after each request, but only if no unhandled exceptions occur
#teardown_request : registers a function to run after each request, even if unhandled exceptions occur

#NOTE: a common pattern to share data b/w request hook functions and view functions is to the the g context global as storage. example: a 'before_request can load the logged in user from the database and
# store it in g.user.  later when the view fucntion is invoked, it can retrieve the user from g.user.

#RESPONSES:
#When flask invokes a view function , it expects its return value to be the response to the request. in most cases the reponse is a simple string that is sent backt ot the client as an HTML page
#HTTP procotrol however rqequires more than a strong as a response to a request. part of that response is the 'status code' which flask default as 200 (successful response)
#when a view function needs to reponse with a different status code,it can add the number code s a second return value after the response:

@app.route('/status')
def status():
    return '<h1>Bad Request</h1>', 400

if __name__ == '__main__':
    app.run(debug=True) #note: calling app.run() within the files instructs the 
    #environment variables of FLASK_APP and FLASK_DEBUGto NOT be used. Hence youc annot enable debug mode from the commandline with environment variables when app.run is used within the script


