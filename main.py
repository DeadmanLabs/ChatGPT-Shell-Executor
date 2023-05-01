import json
import subprocess

import quart
import quart_cors
from quart import request

app = quart_cors.cors(quart.Quart(__name__), allow_origin="*")

_globalVariable = {}

@app.post("/execute/<path:command>")
async def execute(command):
	request_data = await request.get_json(force=True)
	result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, input=json.dumps(request_data), text=True).stdout.strip()
	return quart.Response(response=json.dumps({ "result": str(result) }), status=200)

@app.get("/logo.png")
async def plugin_logo():
	filename = 'logo.png'
	return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
	host = request.headers['Host']
	with open("./.well-known/ai-plugin.json") as f:
		text = f.read()
		return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openai_spec():
	host = request.headers['Host']
	with open("openapi.yaml") as f:
		text = f.read()
		return quart.Response(text, mimetype="text/yaml")

def main():
	app.run(debug=True, host="0.0.0.0", port=3333)

if __name__ == "__main__":
	main()
