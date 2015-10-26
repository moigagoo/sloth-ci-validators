'''Sloth CI validator for `GitHub <https://github.com/>`_ push events.

Usage in the app config::

    provider:
        github:
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


__title__ = 'sloth-ci.validators.github'
__description__ = 'GitHub validator for Sloth CI'
__version__ = '1.0.8'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def validate(request, validation_data):
    '''Check payload from GitHub: the origin IP must be genuine; the repo owner and title must be valid.

    :param request_params: `CherryPy request <http://docs.cherrypy.org/en/latest/pkg/cherrypy.html#cherrypy._cprequest.Request>`_ object instance representing the incoming request
    :param validation_data: dictionary with the keys ``owner``, ``repo``, and ``branches``, parsed from the config

    :returns: (status, message, list of extracted param dicts)
    '''

    from ipaddress import ip_address, ip_network

    if request.method != 'POST':
        return (405, 'Payload validation failed: Wrong method, POST expected, got %s.' % request.method, [])

    trusted_ips = ip_network('192.30.252.0/22')

    remote_ip = ip_address(request.remote.ip)

    if remote_ip not in trusted_ips:
        return (403, 'Payload validation failed: Unverified remote IP: %s.' % remote_ip, [])

    try:
        payload = request.json

        is_ping = 'zen' in payload

        if is_ping:
            owner = payload['repository']['owner']['login']
        else:
            owner = payload['repository']['owner']['name']

        if owner != validation_data['owner']:
            return (403, 'Payload validation failed: wrong owner: %s' % owner, [])

        repo = payload['repository']['name']

        if repo != validation_data['repo']:
            return (403, 'Payload validation failed: wrong repository: %s' % repo, [])

        if is_ping:
            return (200, 'Ping payload validated', [])

        branch = {payload['ref'].split('/')[-1]}

        allowed_branches = set(validation_data.get('branches', branch))

        if not branch & allowed_branches:
            return (403, 'Payload validation failed: wrong branch: %s' % branch, [])

        return (200, 'Payload validated. Branch: %s' % branch, [{'branch': branch}])

    except Exception as e:
        return (400, 'Payload validation failed: %s' % e, [])
