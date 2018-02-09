import pandas as pd
from sqlalchemy import or_

from cellphonedb.database.Repository import Repository
from cellphonedb.models.interaction.db_model_interaction import Interaction
from cellphonedb.models.interaction.functions_interaction import expand_interactions_multidatas
from cellphonedb.models.multidata.db_model_multidata import Multidata


class InteractionRepository(Repository):
    name = 'interaction'

    def get_all(self):
        query = self.database.session.query(Interaction)
        interactions = pd.read_sql(query.statement, self.database.engine)

        return interactions

    def get_interactions_by_multidata_id(self, id):
        """

        :type id: int
        :rtype: pd.DataFrame
        """
        query = self.database.session.query(Interaction).filter(
            or_(Interaction.multidata_1_id == int(id), Interaction.multidata_2_id == int(id)))
        result = pd.read_sql(query.statement, self.database.engine)

        return result

    def get_interactions_multidata_by_multidata_id(self, id):
        """

        :type id: int
        :rtype: pd.DataFrame
        """

        interactions = self.get_interactions_by_multidata_id(id)
        interactions_expanded = expand_interactions_multidatas(interactions)
        return interactions_expanded

    # TODO: Not tested
    def get_all_expanded(self):
        interactions_query = self.database.session.query(Interaction)
        interactions_df = pd.read_sql(interactions_query.statement, self.database.engine)

        multidata_query = self.database.session.query(Multidata.id_multidata)
        multidata_df = pd.read_sql(multidata_query.statement, self.database.engine)

        interactions_df = pd.merge(interactions_df, multidata_df, left_on=['multidata_1_id'], right_on=['id_multidata'])
        interactions_df = pd.merge(interactions_df, multidata_df, left_on=['multidata_2_id'], right_on=['id_multidata'],
                                   suffixes=['_1', '_2'])

        interactions_df.drop(['id_multidata_1', 'id_multidata_2'], axis=1, inplace=True)

        return interactions_df
