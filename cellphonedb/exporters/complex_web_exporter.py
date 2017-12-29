from cellphonedb.exporters import complex_exporter


def call():
    complexes = complex_exporter.call()

    complexes.drop(['receptor', 'receptor_highlight', 'receptor_desc', 'iuhpar_ligand', 'is_complex', 'comments'],
                   inplace=True, axis=1)

    return complexes
