'''Dummy validator.

Dummy Sloth CI validator that checks if the ``message`` param in a ``GET`` request is the same the ``message`` value in the ``provider``: ``dummy`` config section.

.. hint:: Use this validator as a reference when writing *real* validators.

A validator must implement the ``validate(request, validation_data)`` function. The ``request`` param is a CherryPy request object, and ``validation_data`` is a dict with values to check the payload against (obtained from the provider's config section).
'''


__title__ = 'sloth-ci.validators.dummy'
__description__ = 'Dummy validator for Sloth CI'
__version__ = '1.0.3'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def validate(request, validation_data):
    '''Validate dummy payload against a given message (obtained from the Sloth app config)

    :param request: request with payload to validate
    :param validation_data: dictionary with the key ``message``
    :returns: (True, success message, extracted data dict) if the payload is valid, (False, error message, extracted data dict) otherwise
    '''

    if request.method != 'GET':
        return (405, 'Payload validation failed: Wrong method, GET expected, got {method}.', {'method': request.method})

    message = request.params.get('message')

    valid_message = validation_data.get('message')

    if message and message == valid_message:
        return (200, 'Payload validated. Message: {message}', {'message': message})
    else:
        return (403, 'Payload validation failed. Message: {message}', {'message': message})
