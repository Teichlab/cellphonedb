import json

import pandas as pd
from flask import request, Response

from cellcommdb.api_endpoints.endpoint_base import EndpointBase
from cellcommdb.queries import get_rl_lr_interactions_from_multidata

from cellcommdb.common.generic_exception import GenericException
from cellcommdb.repository import multidata_repository


# curl -i \
#      --data "{\"receptor\": \"P25106\"}" \
#      http://127.0.0.1:5000/api/get_ligands_from_receptor
class GetLigandsFromReceptor(EndpointBase):
    def post(self):
        parameters = json.loads(request.get_data(as_text=True))

        receptor = parameters['receptor']

        multidatas_receptors = multidata_repository.get_multidatas_from_string(receptor)

        if multidatas_receptors.empty:
            self.attach_error(
                {'code': 'result_not_found', 'title': '%s not found' % receptor,
                 'details': '%s is not in Cellphone Database' % receptor})

        if not self._errors:
            try:
                result = pd.DataFrame()
                for index, multidata_receptor in multidatas_receptors.iterrows():
                    ligands = get_rl_lr_interactions_from_multidata.call(multidata_receptor, 0.3)
                    result = result.append(ligands, ignore_index=True)

                self._attach_table(result.to_csv(index=False, sep='\t'), 'ligands')
            except GenericException as e:
                self.attach_error(e.args[0])

        self._commit_attachments()

        return Response(self._msg.as_string(), mimetype='multipart/form-data; boundary="%s"' % self._msg.get_boundary())
