from flask import Flask, render_template, request
from PIL import Image
import matplotlib.pyplot as plt
from src import gcloud_functions as gcf
from src import video_functions as vf
from src import translator_functions as trans_f
from werkzeug import secure_filename
import cv2

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/translation")
def translation():
	return render_template("translation.html", txt_to_txt="false")

@app.route("/upload")
def upload():
	return render_template("file_transfer.html")

@app.route("/img_to_char", methods=["GET", "POST"])
def img_to_char():
	print("img_to_char")
	filepath = request.args.get("filepath")
	prediction = gcf.filepath_to_char(filepath)
	return prediction

# @app.route("/video_to_text", methods=["GET", "POST"])
def video_to_text(filepath):
	# filepath = request.args.get("filepath")
	sentence = vf.get_text(filepath)
	return sentence

def text_to_asl():
	return "0"

@app.route("/speech_to_asl", methods=["GET", "POST"])
def speech_to_asl():
	return "0"

@app.route('/uploader', methods = ['GET', 'POST'])
def video_to_text():
	print(request.form)
	print(request.files)
	if request.method == 'POST':
		f = request.files['file']
		lang_code = request.form["language_code"]

		filepath = "static/video.mp4"
		f.save(filepath)
		vidcap = cv2.VideoCapture(filepath)
		sentence = vf.get_text(filepath, vidcap)

		sentence = trans_f.translate_text(sentence, lang_code)
		return render_template("body_and_description.html", title="Video to Text", description=sentence)

	return render_template("index.html")

@app.route("/translate_to_english", methods=["GET", "POST"])
def translate_to_english():
	print(list(request.args))
	print(request.method)
	if request.method == "POST" or request.method == "GET":
		input_text = request.args["input_text"]
		lang_code = request.args["language_code"]
		print(input_text)
		print(lang_code)
		translated_txt = trans_f.translate_text(input_text, lang_code)
		print(translated_txt)
		return render_template("translation.html", translated_text=translated_txt, txt_to_txt="true", original_language=lang_code[0].upper()+lang_code[1:], original_text=input_text)
	return "Nothing received"

@app.route("/speech_to_text", methods=["GET", "POST"])
def speech_to_text():
	print(request.method)
	print(request.form)
	print(request.args)
	if request.method == "POST":
		print(list(request.args))
		f= request.files["file"]
		lang_code = request.form["language_code"]

		filepath = "static/audio.wav"
		f.save(filepath)

		sentence = trans_f.speech_to_text(lang_code)

		text_to_asl(sentence)

		return render_template("body_and_description.html", title="Voice to Text", description=sentence)

@app.route("/text_to_asl/<text>", methods=["GET", "POST"])
def text_to_asl(text):
	list_of_image_names = []
	for char in text:
		filename = "static/char/"+char.lower()+".png"
		list_of_image_names.append(filename)

	f, axarr = plt.subplots(2,len(list_of_image_names))
	print(axarr)
	for i in range(len(list_of_image_names)):
		try:
			axarr[0,i].imshow(cv2.imread(list_of_image_names[i]))
			print(i)
		except:
			pass

	plt.setp(plt.gcf().get_axes(), xticks=[], yticks=[]);
	plt.savefig("static/asl_complete.png")

	# video = cv2.VideoWriter(video_name, 0, 1, (500,500))
	# for image in images:
	#     video.write(cv2.imread(os.path.join(image_folder, image)))

	return "<img src=\"/static/asl_complete.png\">"

if __name__ == '__main__':
	app.run(debug=True)
