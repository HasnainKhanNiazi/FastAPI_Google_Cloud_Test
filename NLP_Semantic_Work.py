from word2number import w2n

SpawnPositionReference = ["left", "right", "before", "front", "at", "ahead", "end", "edge", "behind", "back", "after", "next", "beside", "by", "with", "next", "near", "nearby", "on", "above", "under", "below", "underneath", "far away", "in", "below"]
AnimalPartsReference = ["nose", "eye", "leg", "leg", "head", "ear", "mouth", "belly", "neck", "hump", "tail"]
ObjectsScaleReference = ["small", "big", "giant", "huge", "tiny", "thick"]
ObjectsAnimationReference = ["fly", "run", "sleep", "talk", "eat", "jump", "sit", "swim", "walk", "idle", "look"]
ObjectsShortReference = ["he", "she", "it"]
WeatherEffectReference = ["rain", "sunny", "morning", "stormy", "night", "snow", "dawn", "afternoon", "raining", "snowing"]
AnimalEffectReference = ["happy", "angry", "surprise"]
ColorReference = ["red", "golden", "pink", "yellow", "orange", "blue", "green", "grey", "white", "back", "purple", "brown"]

FoundNouns_Data = []
FoundNouns_DataTypes = []
FoundEffect_Data = []
FoundWeatherEffect_Data = []
FoundSpawnPosition_Data = []
FoundScale_Data = []
FoundParts_Data = []
FoundAnimation_Data = []
FoundShortReference_Data = []
FoundNumber_Data = []
FoundColor_Data = []

To_Spawn_Dictionary = {}
To_Reference_Spawn_Dictionary = {}
To_Position = {}
To_Weather = {}

def Clear_Info():
    FoundNouns_Data.clear()
    FoundNouns_DataTypes.clear()
    FoundEffect_Data.clear()
    FoundWeatherEffect_Data.clear()
    FoundSpawnPosition_Data.clear()
    FoundScale_Data.clear()
    FoundParts_Data.clear()
    FoundAnimation_Data.clear()
    FoundShortReference_Data.clear()
    FoundNumber_Data.clear()
    FoundColor_Data.clear()

def add_Spawn_Reference_Info():
    if len(FoundNouns_Data) > 0:
        To_Reference_Spawn_Dictionary["noun"] =  FoundNouns_Data[0]
    if len(FoundShortReference_Data) > 0:
        To_Reference_Spawn_Dictionary["noun"] = FoundShortReference_Data[0]
    if len(FoundColor_Data) > 0:
        To_Reference_Spawn_Dictionary["color"] = FoundColor_Data[0]
    if len(FoundScale_Data) > 0:
        To_Reference_Spawn_Dictionary["scale"] = FoundScale_Data[0]
    if len(FoundParts_Data) > 0:
        To_Reference_Spawn_Dictionary["part"] = FoundParts_Data[0]
    if len(FoundEffect_Data) > 0:
        To_Reference_Spawn_Dictionary["effect"] = FoundEffect_Data[0]
    if len(FoundNumber_Data) > 0:
        To_Reference_Spawn_Dictionary["count"] = FoundNumber_Data[0]
        
def add_Spawn_Info():
    if len(FoundNouns_Data) > 0:
        To_Spawn_Dictionary["noun"] =  FoundNouns_Data[0]
    if len(FoundShortReference_Data) > 0:
        To_Spawn_Dictionary["noun"] = FoundShortReference_Data[0]
    if len(FoundColor_Data) > 0:
        To_Spawn_Dictionary["color"] = FoundColor_Data[0]
    if len(FoundScale_Data) > 0:
        To_Spawn_Dictionary["scale"] = FoundScale_Data[0]
    if len(FoundParts_Data) > 0:
        To_Spawn_Dictionary["part"] = FoundParts_Data[0]
    if len(FoundEffect_Data) > 0:
        To_Spawn_Dictionary["effect"] = FoundEffect_Data[0]
    if len(FoundNumber_Data) > 0:
        To_Spawn_Dictionary["count"] = FoundNumber_Data[0]

def add_Weather_Info():
    if len(FoundWeatherEffect_Data) > 0:
        To_Weather["weather"] = FoundWeatherEffect_Data[0]


async def Find_Data(words, pos, dep, lemmas):
    Clear_Info()
    To_Spawn_Dictionary.clear()
    To_Reference_Spawn_Dictionary.clear()
    To_Position.clear()
    for i in range(0, len(lemmas)):
        # This is for getting appropriate nouns
        if pos[i] == "NOUN" and (not WeatherEffectReference.__contains__(words[i])) and not(AnimalPartsReference.__contains__(words[i])) and not(SpawnPositionReference.__contains__(words[i])):
            FoundNouns_Data.append(words[i]);
            FoundNouns_DataTypes.append(dep[i].lower())
            if FoundNouns_DataTypes[0].lower() == "nsubj" or FoundNouns_DataTypes[0].lower() == "sobj" or FoundNouns_DataTypes[0].lower() == "attr" or FoundNouns_DataTypes[0].lower() == "root":
                add_Spawn_Info()
                Clear_Info()
            else:
                add_Spawn_Reference_Info()
                Clear_Info()
        
        # Object Effect "Happy", etc
        if (AnimalEffectReference.__contains__(lemmas[i])):
            FoundEffect_Data.append(lemmas[i].lower())
            
        # Weather Effect "Rain", etc
        if (WeatherEffectReference.__contains__(lemmas[i])):
            FoundWeatherEffect_Data.append(lemmas[i].lower())
        
        # Spawn Position "Left, Right", etc
        if (SpawnPositionReference.__contains__(words[i])):
            FoundSpawnPosition_Data.append(words[i].lower())
            To_Position["position"] = words[i].lower()
            
        # Animal size, small, huge, etc
        if (ObjectsScaleReference.__contains__(lemmas[i])):
            FoundScale_Data.append(lemmas[i].lower())
            
        # Animal Parts "legs, etc"
        if (AnimalPartsReference.__contains__(words[i])):
            FoundParts_Data.append(words[i].lower())
            
        # Object Animation  "walk", "run", "fly", "sleep", "eat", etc
        if (ObjectsAnimationReference.__contains__(lemmas[i])):
            FoundAnimation_Data.append(lemmas[i].lower())
            To_Spawn_Dictionary["animation"] =  FoundAnimation_Data[0]
        
        # Object Short Reference "he", "she", "it", etc
        if (ObjectsShortReference.__contains__(lemmas[i].lower())):
            FoundShortReference_Data.append(lemmas[i].lower())
        
        # Object Count "One", "Two", etc
        if (pos[i] == "NUM"):
           FoundNumber_Data.append(w2n.word_to_num(lemmas[i]))
        
        # Object Color "Red", etc
        if (pos[i] == "ADJ" and ColorReference.__contains__(lemmas[i].lower())):
            FoundColor_Data.append(lemmas[i].lower())
    
    
    return To_Spawn_Dictionary, To_Position, To_Reference_Spawn_Dictionary, To_Weather