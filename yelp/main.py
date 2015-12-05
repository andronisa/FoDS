from data.collection import SimpleDataImporter

def main(*agrs):
    dataset_name = None
    if len(agrs) > 0:
        dataset_name = agrs[0]
    else:
        dataset_name = 'yelp_academic_dataset_user.json'

    simpleImporter = SimpleDataImporter()
    simpleImporter.run(dataset_name, True)
    simpleImporter.finish()

if __name__ == '__main__': main()
