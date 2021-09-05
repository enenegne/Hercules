import googletrans

translator = googletrans.Translator()

languages_dict = googletrans.LANGUAGES

def list_languages():
    value = []
    for key in languages_dict.keys():
        value.append(googletrans.LANGUAGES[key].capitalize())
    
    return value

def do_translation(dest_lang, text):
    dest_lang_key = list(languages_dict.keys())[list(languages_dict.values()).index(dest_lang)]
    translated_text = translator.translate(text, dest_lang_key).text
    
    return translated_text