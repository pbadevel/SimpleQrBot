from enum import StrEnum




class UserCallbackActions(StrEnum):
    SHOW_QR = "showQr"


class AdminCallbackActions(StrEnum):
    CONFIRM_ENTERANCE = 'ConfirmEntarance'
    REJECT_ENTERANCE = 'RejectEntarance'
    CANCEL_ENTERANCE = 'Cancel'