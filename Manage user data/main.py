import urllib.parse as up
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS
import flask

app = Flask(__name__)
cors = CORS(app, origins=["https://chat.openai.com"])
up.uses_netloc.append("postgres")
url = up.urlparse(
  "postgres://taocnyoe:pTw0JEEoG_C63PLaukw6DJQuZvINTDyg@mahmud.db.elephantsql.com/taocnyoe"
)
conn = psycopg2.connect(database=url.path[1:],
                        user=url.username,
                        password=url.password,
                        host=url.hostname,
                        port=url.port)


@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    request1 = flask.request.get_json(force=True)
    username = request1['username']
    email = request1['email']
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)",
                   (username, email))
    conn.commit()
    cursor.close()
    return flask.Response(response='OK', status=200)
  return 'hello'


@app.route('/query', methods=['GET', 'POST'])
def query():
  if request.method == 'POST':
    request1 = flask.request.get_json(force=True)
    username = request1['username']
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username, ))
    results = cursor.fetchall()
    cursor.close()
    if results:
      response = {
        'message': f"User '{username}' exists in the database!",
        'data': results
      }
      return jsonify(response), 200
    else:
      response = {
        'message': f"User '{username}' does not exist in the database!"
      }
      return jsonify(response), 200


@app.route("/delete", methods=['POST'])
def delete():
  request1 = request.get_json(force=True)
  username = request1['username']
  cursor = conn.cursor()
  cursor.execute("DELETE FROM users WHERE username = %s", (username, ))
  conn.commit()
  if cursor.rowcount:
    response = {
      'message': f"User '{username}' has been deleted from the database!"
    }
    status_code = 200
  else:
    response = {
      'message': f"User '{username}' does not exist in the database!"
    }
    status_code = 404
  cursor.close()
  return jsonify(response), status_code


@app.get("/logo.png")
def plugin_logo():
  filename = 'logo.png'
  return flask.send_file(filename, mimetype='image/png')


@app.get("/.well-known/ai-plugin.json")
def plugin_manifest():
  with open("./.well-known/ai-plugin.json") as f:
    text = f.read()
    return flask.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
def openapi_spec():
  with open("openapi.yaml") as f:
    text = f.read()
    return flask.Response(text, mimetype="text/yaml")


if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5005)
