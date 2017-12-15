from flask_restful import Resource, reqparse, marshal, fields

from cellcommdb.extensions import db
from cellcommdb.models.complex.db_model_complex import Complex
from cellcommdb.models.protein.db_model_protein import Protein


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


class ComplexResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', required=False)
    parser.add_argument('name', required=False)

    mapper = {
        "id": fields.Integer,
        "name": fields.String,
        "proteins": fields.List(fields.Nested(ProteinResource.mapper))
    }

    def get(self):
        args = self.parser.parse_args()
        base_query = db.session.query(Complex)
        if args.get('id'):
            base_query = base_query.filter(Complex.id == args['id'])
        if args.get('name'):
            base_query = base_query.filter(Complex.name == args['name'])
        result = base_query.all()

        return marshal(result, self.mapper)


