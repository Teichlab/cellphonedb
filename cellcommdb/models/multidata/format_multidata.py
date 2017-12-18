def get_value_with_prefix(multidata_protein, suffix=''):
    if multidata_protein['is_complex%s' % suffix]:
        return 'complex:%s' % multidata_protein['name%s' % suffix]

    return 'simple:%s' % multidata_protein['entry_name%s' % suffix]
