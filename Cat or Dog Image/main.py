from flask import Flask, jsonify, render_template_string
import flask
from flask_cors import CORS
import requests

app = Flask(__name__)
cors = CORS(app, origins=["https://chat.openai.com"])


@app.route('/dog', methods=['GET'])
def get_random_dog():
  # 使用TheCatAPI获取随机猫图片的URL
  response = requests.get('https://api.thedogapi.com/v1/images/search')
  dog_data = response.json()
  url = dog_data[0]["url"]
  # 返回一个HTML页面，这个页面中包含了猫图片
  return render_template_string('<img src="{{ url }}" />', url=url)


@app.route('/cat', methods=['GET'])
def get_random_cat():
  # 使用TheCatAPI获取随机猫图片的URL
  response = requests.get('https://api.thecatapi.com/v1/images/search')
  cat_data = response.json()
  url = cat_data[0]["url"]
  # 返回一个HTML页面，这个页面中包含了猫图片
  return render_template_string('<img src="{{ url }}" />', url=url)


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
