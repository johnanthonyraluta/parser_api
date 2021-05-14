import glob
import xlrd

class File:
    
    @staticmethod
    def crawl(filepath):
        return [x for x in glob.glob(filepath)]
