import functools
import inspect


# Base Error
class LinkzoneError(Exception):
    """
    Base Error for Linkzone SDK. This class should not be used directly, Linkzone exceptions should inherit from either
    LinkzoneUserError or LinkzoneInternalError.
    """

    pass


# Two Secondary Errors which differentiate between exceptions that are the user's fault and Linkzone's fault
class LinkzoneUserError(LinkzoneError):
    """
    Exception raised due to incorrect user input to the Linkzone SDK. Can be used directly but children are preferred.
    """

    pass


class LinkzoneInternalError(LinkzoneError):
    """
    Exception raised when user input is correct but an error occurs. Can be used directly but children are preferred.
    """

    pass


# User Exceptions
class MissingParameterError(LinkzoneUserError):
    """
    Exception raised when parameters supplied to the Linkzone SDK are missing.
    """

    pass


class UserValueError(LinkzoneUserError, ValueError):
    """
    Exception raised when a user supplies an invalid value to the Linkzone SDK.
    """

    pass


class UserTypeError(LinkzoneUserError, TypeError):
    """
    Exception raised when a user supplies an argument of the incorrect type to the Linkzone SDK.
    """

    pass


class MethodNotApplicableError(LinkzoneUserError):
    """
    Exception raised when the method called is not valid for the resource.
    """

    pass


class ResponseClientError(LinkzoneUserError):
    """
    Exception raised when a 4XX response is received from the API.
    """

    pass


class ForbiddenError(ResponseClientError):
    """
    Exception raised when a 403 Forbidden response is received from the API.
    """

    pass


# Linkzone Internal Exceptions
class ExpectedParameterNotFoundError(LinkzoneInternalError):
    """
    Exception raised when a field or property should be available from Linkzone but is unexpectedly missing.
    """

    pass


class InternalValueError(LinkzoneInternalError, ValueError):
    """
    Exception raised when a value is unexpected.
    """

    pass


class InternalTypeError(LinkzoneInternalError, TypeError):
    """
    Exception raised when a value type is unexpected.
    """

    pass


class ResponseServerError(LinkzoneInternalError):
    """
    Exception raised when a 5XX response is received from the API.
    """

    pass


class ResponseRedirectError(LinkzoneInternalError):
    """
    Exception raised when a 3XX response is unexpectedly received from the API.
    """

    pass


def linkzone_excepted(message=None):
    """
    Decorator to wrap user-facing Linkzone functions with exception handling that describes to the user whether the error
    is their fault or is our fault and should be reported.
    :param message: an optional message to prefix the error with, should describe the failure e.g. "failed to send
    inferences" or "an error occurred while creating the model."
    :return: the decorator function
    """
    if message is None:
        prefix = ""
    else:
        prefix = message + " because "

    def decorator_linkzone_excepted(func):
        @functools.wraps(func)
        def wrapper_linkzone_excepted(*args, **kwargs):
            # ensure all required parameters are present: check manually because TypeErrors from internal calls
            #  should not be UserErrors
            try:
                inspect.signature(func).bind(*args, **kwargs)
                success = True
                err_msg = None
            except TypeError as e:
                success = False
                err_msg = str(e)
            if not success:
                raise MissingParameterError(err_msg)

            # call the function
            try:
                return func(*args, **kwargs)
            # if it is a user error simply re-raise
            except LinkzoneUserError as e:
                raise e
            # otherwise wrap it in a message saying it's not the user's fault
            except LinkzoneInternalError as e:
                raise LinkzoneInternalError(
                    prefix
                    + "an internal exception occurred, please report to the package mantainer"
                ) from e
            except Exception as e:
                raise LinkzoneInternalError(
                    prefix
                    + "there was an unexpected internal exception, please report to the package mantainer"
                ) from e

        return wrapper_linkzone_excepted

    return decorator_linkzone_excepted
