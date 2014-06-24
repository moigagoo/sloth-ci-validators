'''Dummy validator.

Dummy Sloth CI validator that checks if the ``message`` param in a ``GET`` request is the same the ``message`` value in the ``provider_data`` config section.

Use this validator as a reference when writing *real* validators.

A validator must implement the ``validate`` function with params ``request``, which is a CherryPy request object, and ``validation_data``?�a dict with values to check the payload against.

The ``validate`` function must return a tuple of validation status (True or False), success or failure message, and a dictionary with the data extracted from the payload.
'''


__title__ = 'sloth-ci.validators.dummy'
__description__ = 'Dummy validator for Sloth CI'
__version__ = '1.0.1'
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
        return (False, 'Payload validation failed: Wrong method, GET expected, got {method}.', {'method': request.method})

    message = request.params.get('message')

    valid_message = validation_data.get('message')

    if message and message == valid_message:
        return (True, 'Payload validated. Message: {message}', {'message': message})
    else:
        return (False, 'Payload validation failed. Message: {message}', {'message': message})