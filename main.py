import shutil
from fastapi import FastAPI, UploadFile, File
import spacy
from fastapi import FastAPI
import speech_recognition as sr
import NLP_Semantic_Work as semantic

# Create the app object
app = FastAPI()
classifier = spacy.load("en_core_web_sm")

@app.api_route('/predicttext/{text}', methods=["GET", "POST"])
async def predict_data(text: str):
    Words = []
    POS = [] # Parts Of Speech
    Lemma = [] # Lemmatization
    Dep = [] # Dependency
    text = text.lower()
    doc = classifier(text)
    for token in doc:
        Words.append(token.text)
        POS.append(token.pos_)
        Lemma.append(token.lemma_)
        Dep.append(token.dep_)
    
    async def ReceiveDataFromMainSceneBH():
        result = await semantic.Find_Data(words=Words, pos=POS, dep=Dep, lemmas=Lemma)
        return result
    
    To_Spawn_Dictionary, To_Position, To_Reference_Spawn_Dictionary, To_Weather = await ReceiveDataFromMainSceneBH()
    print(To_Spawn_Dictionary, To_Position, To_Reference_Spawn_Dictionary, To_Weather)
    if len(To_Spawn_Dictionary) > 0 and len(To_Position) > 0 and len(To_Reference_Spawn_Dictionary) > 0 and len(To_Weather) > 0:
        return f"{To_Spawn_Dictionary};{To_Position};{To_Reference_Spawn_Dictionary};{To_Weather}"
    if len(To_Spawn_Dictionary) > 0 and len(To_Position) > 0 and len(To_Reference_Spawn_Dictionary) > 0 and len(To_Weather) <= 0:
        return f"{To_Spawn_Dictionary};{To_Position};{To_Reference_Spawn_Dictionary}"
    if len(To_Spawn_Dictionary) > 0 and len(To_Position) <= 0 and len(To_Reference_Spawn_Dictionary) <= 0 and len(To_Weather) <= 0:
        return f"{To_Spawn_Dictionary}"
    if len(To_Spawn_Dictionary) > 0 and len(To_Position) <= 0 and len(To_Reference_Spawn_Dictionary) <= 0  and len(To_Weather) > 0:
        return f"{To_Spawn_Dictionary};{To_Weather}"

@app.post("/predictvoicee/")
def predict_voice1(file: UploadFile = File(...)):
    try:
        with open("test.wav", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        transcript = ""
        recognizer = sr.Recognizer()
        audioFile = sr.AudioFile("test.wav")
        with audioFile as source:
            data = recognizer.record(source)
        transcript = recognizer.recognize_google(data, key=None)

        return transcript
    except:
        return "Caught An error in DeepSpeech"