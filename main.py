# Import Libraries
import shutil
import uvicorn
from fastapi import FastAPI, Form, UploadFile, File
import spacy
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
import speech_recognition as sr
from scipy.io import wavfile

# Create the app object
app = FastAPI()
spacy.cli.download("en_core_web_sm")
classifier = spacy.load("en_core_web_sm")

templates = Jinja2Templates(directory="templates")

@app.post('/predicttext/{text}')
def predict_data(request: Request, text: str):
    # text = text[1:-1]
    # print(text)
    
    Words = []
    POS = [] # Parts Of Speech
    Lemma = [] # Lemmatization
    Dep = [] # Dependency
    doc = classifier(text)
    
    for token in doc:
        Words.append(token.text)
        POS.append(token.pos_)
        Lemma.append(token.lemma_)
        Dep.append(token.dep_)


    return {'Words': Words, 'POS':POS, 'Lemma': Lemma, 'Dep': Dep}

@app.post("/predictvoicee/")
def predict_voice1(file: UploadFile = File(...)):
    with open("test.wav", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # return {"file_name": file.filename}
    
    transcript = ""
    print(file)
    print(type(file))
    recognizer = sr.Recognizer()
    audioFile = sr.AudioFile("test.wav")
    print(audioFile)
    with audioFile as source:
        data = recognizer.record(source)
    transcript = recognizer.recognize_google(data, key=None)

    return {"Text": transcript}
    # return templates.TemplateResponse('index2.html', transcript=transcript)


@app.api_route("/predictvoice/", methods=["GET", "POST"])
def predict_voice(request: Request):
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            templates.red
            print(request.url)
            # return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            print(request.url)
            # return redirect(request.url)

        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)

    return templates.TemplateResponse('index2.html', transcript=transcript)

# if __name__=="__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)