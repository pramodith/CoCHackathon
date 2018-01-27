import pytesseract
from PIL import Image
import nltk
from nltk.corpus import wordnet as wn
class OCR:


    def __init__(self,bill=None):
        path="bill_images\\bill3.jpg"
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
        image_instance=Image.open(path)
        image_instance=image_instance.convert("L")
        text=pytesseract.image_to_string(image_instance,config='-psm 6',lang='eng')
        print(text)
        #requests.post()
c=OCR()
