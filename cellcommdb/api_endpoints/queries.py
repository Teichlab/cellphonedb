import pandas as pd
from flask import request, Response
from flask_restful import Resource, reqparse

from cellcommdb.queries.query0 import Query0
from cellcommdb.queries.query1 import Query1

parser = reqparse.RequestParser()
parser.add_argument('meta')
parser.add_argument('counts')


# Example query
# Query0
# curl -i \
#     -F counts_file=@test_counts.txt \
#     -F meta_file=@test_meta.txt \
#     http://127.0.0.1:5000/api/query0
#
# Query1
# curl -i \
#     -F processed_data=@query_0.csv \
#     http://127.0.0.1:5000/api/query1

class Query0Endpoint(Resource):
    def post(self):
        counts_df = pd.read_csv(request.files['counts_file'].stream, sep='\t')
        meta_df = pd.read_csv(request.files['meta_file'].stream, sep='\t')

        result_df = Query0.call(counts_df, meta_df)

        return Response(result_df.to_csv(index=False), mimetype='text/csv')


class Query1Endpoint(Resource):
    def post(self):
        processed_data = pd.read_csv(request.files['processed_data'].stream)

        result_df = Query1.call(processed_data)

        return Response(result_df.to_csv(index=False), mimetype='text/csv')
