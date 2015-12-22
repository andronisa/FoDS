import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'FoDS')))

from api import AlchemyAPI
from yelp.data.collection import MongoQuery
from yelp.alchemy.nlp.exception import NLPValueError


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
    mongo_review = nlp_handler.query.find_one('review')

    try:
        nlp_result = nlp_handler.get_combined_result(review_text=mongo_review['text'])
        nlp_handler.update_review_with_nlp_results(mongo_review, nlp_result)
    except NLPValueError as err:
        print(err)
        raise err
