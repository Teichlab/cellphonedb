from flask.ext.restful import Resource, reqparse, marshal, fields

from cellcommdb.extensions import db
from cellcommdb.models import *


class ProteinResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', required=False)
    parser.add_argument('uniprot', required=False)

    mapper = {
        "id": fields.Integer,
        "uniprot": fields.String,
        "entry_name": fields.String,
        "transmembrane": fields.Boolean,
        "secretion": fields.Boolean,
        "peripheral": fields.Boolean,
        "receptor": fields.Boolean,
        "receptor_highlight": fields.Boolean,
        "receptor_desc": fields.String,
        "adhesion": fields.Boolean,
        "other": fields.Boolean,
        "other_desc": fields.String,
        "transporter": fields.Boolean,
        "secreted_highlight": fields.Boolean,
        "secreted_desc": fields.String,
        "tags": fields.String,
        "tags_reason": fields.String
    }

    def get(self):

        args = self.parser.parse_args()
        base_query = db.session.query(Protein)
        if args.get('id'):
            base_query = base_query.filter(Protein.id == args['id'])
        if args.get('uniprot'):
            base_query = base_query.filter(Protein.uniprot == args['uniprot'])
        result = base_query.all()

        return marshal(result, self.mapper)
