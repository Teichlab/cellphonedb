from cellphonedb.core.exporters import complex_exporter


def call(complexes, multidatas, complex_compositions, proteins):
    complexes = complex_exporter.call(complexes, multidatas, complex_compositions, proteins)

    complexes.drop(
        ['receptor', 'receptor_desc', 'is_complex', 'comments_complex'],
        inplace=True, axis=1)

    return complexes
