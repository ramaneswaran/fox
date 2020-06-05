import pytesseract
import cv2

class Engine:
    '''
    OCR class
    '''
    def __init__(self):
        '''
        Constructor class for OCR
        '''

        pass

    def get_text(self, path):
        '''
        This function gets text from image
        '''

        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(image)

        return text

    