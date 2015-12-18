from data.collection import SimpleDataImporter
import sys

def main():
    dataset_name = 'yelp_academic_dataset_user.json'

    try:
        dataset_name = sys.argv[1]
    except BaseException as e:
        print ('usage: main.py <inputfile>')
        #sys.exit(2)

    simpleImporter = SimpleDataImporter()
    simpleImporter.run(dataset_name, True)
    simpleImporter.finish()

if __name__ == '__main__': main()
