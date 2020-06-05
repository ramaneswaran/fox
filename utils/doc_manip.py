from pdf2image import convert_from_path
import logging


class Manip:
    '''
    Class to deals with docs
    '''
    def __init__(self):
        logging.info("Initializing doc manipulator")

    def save_as_image(self, path):
        '''
        This function return path of saved image
        '''

        pages = convert_from_path(path)

        image = page[0]

        image.save('./tmp/img.jpg')

        return './tmp/img.jpg'