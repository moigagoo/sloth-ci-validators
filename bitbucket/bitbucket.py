'''Sloth CI validator for `Bitbucket <https://bitbucket.org/>`_ push events.

Usage in the app config::

    provider:
        bitbucket:
            # Repository owner. Mandatory parameter.
            owner: moigagoo

            # Repository title as it appears in the URL, i.e. slug.
            # Mandatory parameter.
            repo: sloth-ci

            # Only pushes to these branches will initiate a build.
            # Skip this parameter to allow all branches to fire builds.
            branches:
                - master
                - staging
'''


__title__ = 'sloth-ci.validators.bitbucket'
__description__ = 'Bitbucket validator for Sloth CI'
__version__ = '1.0.7'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def validate(request, validation_data):
    '''Check payload from Bitbucket: the origin IP must be genuine; the repo owner and title must be valid.

    :param request_params: CherryPy request <http://docs.cherrypy.org/en/latest/pkg/cherrypy.ht
       ml#cherrypy._cprequest.Request>`_ object instance representing the incoming request
    :param validation_data: dictionary with the keys ``owner``, ``repo``, and ``branches``, pars
       ed from the config

    :returns: (status, message, list of extracted param dicts)
    '''

    from ipaddress import ip_address, ip_network

    if request.method != 'POST':
        return (405, 'Payload validation failed: Wrong method, POST expected, got %s.' % request.method, [])

    trusted_ips = (ip_network(ip_range) for ip_range in ('131.103.20.160/27', '165.254.145.0/26', '104.192.143.0/24'))

    remote_ip = ip_address(request.remote.ip)

    if not (ips for ips in trusted_ips if remote_ip in ips):
        return (403, 'Payload validation failed: Unverified remote IP: %s.' % remote_ip, [])

    try:
        payload = request.json

        owner = payload['repository']['owner']['username']

        if owner != validation_data['owner']:
            return (403, 'Payload validation failed: wrong owner: %s' % owner, [])

        repo = payload['repository']['name']

        if repo != validation_data['repo']:
            return (403, 'Payload validation failed: wrong repository: %s' % repo, [])

        branches = {change['new']['name'] for change in payload['push']['changes']}

        allowed_branches = set(validation_data.get('branches', branches))

        if not branches & allowed_branches:
            return (403, 'Payload validation failed: wrong branches: %s' % branches, [])

        param_dicts = [{'branch': branch} for branch in branches & allowed_branches]

        return (200, 'Payload validated. Branches: %s' % ', '.join(branches), param_dicts)

    except Exception as e:
        return (400, 'Payload validation failed: %s' % e, [])
