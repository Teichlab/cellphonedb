import pandas as pd
from flask import request, Response

from cellphonedb import extensions
from cellphonedb.api_endpoints.endpoint_base import EndpointBase
from utils import utils


class WebEndpointClusterStatisticalAnalysis(EndpointBase):
    def post(self):
        counts = utils.read_data_from_content_type(request.files['counts_file'], index_column_first=True)
        meta = utils.read_data_from_content_type(request.files['meta_file'], index_column_first=True)

        if not isinstance(counts, pd.DataFrame):
            self.attach_error(
                {'code': 'parsing_error', 'title': 'Error parsing counts file', 'detail': 'Error parsing counts file'})

        if not isinstance(meta, pd.DataFrame):
            self.attach_error(
                {'code': 'parsing_error', 'title': 'Error parsing meta file', 'detail': 'Error parsing meta file'})

        if not self._errors:
            pvalues, means, significant_means, mean_pvalue, deconvoluted = extensions.cellphonedb_flask.cellphonedb.query.cluster_statistical_analysis(
                meta, counts, iterations=2, debug_seed=False)

            self._attach_csv(pvalues.to_csv(), 'pvalues.csv')
            self._attach_csv(means.to_csv(), 'means.csv')
            self._attach_csv(significant_means.to_csv(), 'significant_means.csv')
            self._attach_csv(mean_pvalue.to_csv(), 'mean_pvalue.csv')
            self._attach_csv(deconvoluted.to_csv(), 'deconvoluted.csv')

        self._commit_attachments()

        return Response(self._msg.as_string(), mimetype='multipart/form-data; boundary="%s"' % self._msg.get_boundary())
