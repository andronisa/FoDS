import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'FoDS')))

from api import AlchemyAPI
from yelp.data.collection import MongoQuery
from yelp.data.collection import DBConnector
from yelp.alchemy.nlp.exception import NLPValueError

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config'))

class NLPHandler(object):
    def __init__(self):
        self.alchemy_api = AlchemyAPI()
        self.query = MongoQuery()

    def get_combined_result(self, review_text=''):
        opts = {
            'sentiment': 1
        }
        response = self.alchemy_api.combined('text', review_text, options=opts)

        if response['status'] == 'OK':
            return response
        else:
            raise NLPValueError('Error in combined call: ' + response['statusInfo'])

    def get_sentiment_result(self, review_text=''):
        response = self.alchemy_api.sentiment('text', review_text)
        if response['status'] == 'OK':
            return response
        else:
            raise NLPValueError('Error in sentiment analysis call: ' + response['statusInfo'])

    def update_review_with_nlp_results(self, review, nlp_dict):
        self.query.find_and_update(
            query={'review_id': review['review_id']},
            updateQuery={'$set': {'alc_result': nlp_dict}},
            collection_name='review'
        )


if __name__ == '__main__':
    nlp_handler = NLPHandler()
    # mongo_review = nlp_handler.query.find_one('review')
    #
    # try:
    #     nlp_result = nlp_handler.get_combined_result(review_text=mongo_review['text'])
    #     nlp_handler.update_review_with_nlp_results(mongo_review, nlp_result)
    # except NLPValueError as err:
    #     print(err)
    #     raise err

    dbConnector = DBConnector(os.path.join(CONFIG_PATH, 'config.json'))
    dbConnector.connect()
    dbConnector.reset_database_name('yelp', 'review_category')
    t_collection = dbConnector.get_database_name('yelp', 'review_category')

    business_fields = ['business_id', 'categories']
    user_fields = ['user_id', 'elite', 'votes']
    review_fields = ['business_id', 'review_id', 'text', 'user_id']
    collection_name = 'review'
    documents = nlp_handler.query.find_all(collection_name, review_fields)
    print("\n" + str(documents.count()) + "\n")

    index = 0
    batch_number = 5000

    batch_documents = [i for i in range(batch_number)]

    for document in documents:
        try:
            business_id = document['business_id']
            review_id = document['review_id']
            text = document['text']
            user_id = document['user_id']

            business_doc = nlp_handler.query.find_one('business', ('business_id', business_id), business_fields)
            categories = business_doc['categories']

            user_doc = nlp_handler.query.find_one('user', ('user_id', user_id), user_fields)
            elite = len(user_doc['elite'])
            useful = user_doc['votes']['useful']

            new_doc = {
                'review_id': review_id,
                'business_id': business_id,
                'user_id': user_id,
                'categories': categories,
                'elite': elite,
                'useful': useful,
                'text': text,
            }

            batch_documents[index % batch_number] = new_doc

            if (index + 1) % batch_number == 0:
                t_collection.insert(batch_documents)
                print("\n" + str(index) + "\n")
            index += 1
        except:
            print 'Unexpected error:', sys.exc_info()[0], ', for index ', index
            raise
    dbConnector.disconnect()

# db.review_category.aggregate([{ $unwind: "$categories"}, {$group: { _id : "$categories", count: {$sum: 1}} }, {$sort: {count: -1}}, {$limit:1}], {allowDiskUse:true})
# db.review_category.aggregate([{ $unwind: "$categories"}, { $match : { categories : "Restaurants" } }, {$group: { _id : "$business_id", count: {$sum: 1}} }, {$sort: {count: -1}}, {$match : {count: {$lte:1000}}}, {$limit : 12}], {allowDiskUse:true})