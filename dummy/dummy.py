__title__ = 'sloth-ci.validators.dummy'
__version__ = '1.0.0'
__author__ = 'Konstantin Molchanov'
__license__ = 'MIT'


def validate(request, validation_data):
    """Dummy validator.

    A validator must implement the ``validate`` function with params ``request``, which is a CherryPy request object, and ``validation_data``—a dict with values to check the payload against.

    The ``validate`` function must return a tuple of validation status (True or False), success or failure message, and a dictionary with the data extracted from the payload. 

    :param request: request with payload to validate
    :param validation_data: dictionary with the key ``message``

    :returns: (True, success message, extracted data dict) if the payload is valid, (False, error message, extracted data dict) otherwise
    """

    if request.method != 'GET':
        return (False, 'Payload validation failed: Wrong method, GET expected, got {method}.', {'method': request.method})

    message = request.params.get('message')

    valid_message = validation_data.get('message')

    if message and message == valid_message:
        return (True, 'Payload validated. Message: {message}', {'message': message})
    else:
        return (False, 'Payload validation failed. Message: {message}', {'message': message})
