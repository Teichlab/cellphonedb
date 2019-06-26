from flask import request, Response

from cellphonedb.src.app.cellphonedb_app import cellphonedb_app
from cellphonedb.src.api_endpoints.web_api.web_api_endpoint_base import WebApiEndpointBase


class WebEndpointQueryInteractionGene(WebApiEndpointBase):
    @staticmethod
    def get():
        columns = request.args.get('columns')

        columns = columns.split(',') if columns else None

        genes = cellphonedb_app.cellphonedb.query.get_all_genes(columns)
        genes = genes.to_json(orient='records')

        response = Response(genes, content_type='application/json')

        return response
