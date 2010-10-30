QBMS_EXCEPTIONS = {
    # Usage:
        # Call an Exception(QBMSEXCEPTIONS[code]) and handle
        # the equivalent exception appropriately
    # Connection related errors
    # Returned in the StatusCode field of:
    # SignonDesktopRs, SignonTicketRs, SignonAppCertRs
     '2000': 'AuthenticationError',
     '2010': 'UnauthorizedAccess',
     '2020': 'SessionAuthenticationRequired',
     '2030': 'UnsupportedSignonVersion',
     '2040': 'InternalError',
    # End QBMS Connection errors
    # Other response errors
    '10100': 'ValidationErrorVoidManual',
    '10101': 'ValidationError',
    '10200': 'CommunicationError',
    '10201': 'GatewayLoginError',
    '10202': 'AccountValidationError',
    '10300': 'AmountConversionError',
    '10301': 'InvalidCardNumber',
    '10302': 'DateValidationError',
    '10303': 'RequirementMissing',
    '10304': 'MaxLengthExceeded',
    '10305': 'DateValidationError',
    '10306': 'BooleanError',
    '10307': 'MinLengthReceded', # Not sure what else to call this one.
    '10308': 'MaxRequestsExceeded',
    '10309': 'InvalidFormat',
    '10312': 'InvalidField',
    '10313': 'InvalidAggregate',
    '10314': 'TransRequestIDReuseError', # Lengthy
    '10400': 'InsufficientFunds',
    '10401': 'RequestDeclined',
    '10402': 'CardUnsupported',
    '10403': 'UnrecognizedMerchant',
    '10404': 'VoiceAuthRequired',
    '10405': 'VoidError',
    '10406': 'CaptureError',
    '10407': 'SalesCapExceeded',
    '10408': 'InvalidFormat', # Verify similarity to 10309
    '10409': 'ValidationError', # Response may specify specific problem.
    '10413': 'BatchIDMissing',
    '10500': 'GatewayError',
    '10501': 'GeneralSystemError',
}

class QBMSException:
    def __init__(self):                 pass
    class BatchIDMissing:               pass
    class InvalidFormat:                pass
    class MaxRequestsExceeded:          pass
    class MinLengthReceded:             pass
    class BooleanError:                 pass
    class DateValidationError:          pass
    class MaxLengthExceeded:            pass
    class RequirementMissing:           pass
    class DateValidationError:          pass
    class InvalidCardNumber:            pass
    class AmountConversionError:        pass
    class ValidationError:              pass
    class ValidationErrorVoidManual:    pass
    class UnsupportedSignonVersion:     pass
    class UnauthorizedAccess:           pass
    class InsufficientFunds:            pass
    class RequestDeclined:              pass
    class CardUnsupported:              pass
    class UnrecognizedMerchant:         pass
    class VoiceAuthRequired:            pass
    class VoidError:                    pass
    class CaptureError:                 pass
    class SalesCapExceeded:             pass
    class InvalidFormat:                pass
    class ValidationError:              pass
    class InvalidField:                 pass
    class InvalidAggregate:             pass
    class TransRequestIDReuseError:     pass
    class AccountValidationError:       pass
    class CommunicationError:           pass
    class GatewayLoginError:            pass
    class GeneralSystemError:           pass
    class GatewayError:                 pass
    class InternalError:                pass
    class AuthenticationError:          pass
    class SessionAuthenticationRequired:pass
    def raiseError(self, code): raise eval('self.%s' % QBMS_EXCEPTIONS[code])
