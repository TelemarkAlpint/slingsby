#!py

def run():
    """ Sanity-checks the opendkim pillar values. All domains need at least one key,
    and each key needs to have a private part.
    """
    for domain, selector in __pillar__.get('opendkim', {}).iteritems():
        assert 'OPENDKIM_KEY_%s' % selector in __pillar__, (
            'The OpenDKIM selector {0} does not have a key specified in pillar '
            '(should be at OPENDKIM_KEY_{0}'.format(selector)
            )
    return {}
