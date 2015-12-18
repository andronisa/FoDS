from data.collection import SimpleDataImporter


def main(*args):
    dataset_name = 'yelp_academic_dataset_user.json'

    if len(args) > 0:
        dataset_name = args[0]

    collection_name = SimpleDataImporter.get_collection_name(dataset_name)
    print collection_name

    simpleImporter = SimpleDataImporter()
    simpleImporter.run(dataset_name, collection_name, True)
    simpleImporter.finish()


if __name__ == '__main__': main()
