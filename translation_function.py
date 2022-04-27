import googletrans
from googletrans import *
import pyttsx3
from image_ocr.ocr_process import *
def translate():
    id,last_n,name = ocr_pross()
    print(name[1])
    translator = googletrans.Translator()
    translate = translator.translate(name[1], dest='english')
    print(translate.text)
    return translate.text

translate()