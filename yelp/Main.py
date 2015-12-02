from YLPDataCollection import *

def main():
    
    simpleImporter = SimpleDataImporter()
    simpleImporter.run('yelp_academic_dataset_user.json', True)
    simpleImporter.finish()

if __name__ == '__main__': main()
