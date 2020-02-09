import enum


class Protocol(enum.Enum):
    HELLO_FROM = 'HELLO-FROM'
    HELLO = 'HELLO'
    WHO = 'WHO'
    WHO_OK = 'WHO-OK'
    SEND = 'SEND'
    SEND_OK = 'SEND-OK'
    UNKNOWN = 'UNKNOWN'
    DELIVERY = 'DELIVERY'
    IN_USE = 'IN-USE'
    BUSY = 'BUSY'
    BAD_RQST_HDR = 'BAD-RQST-HDR'
    BAD_RQST_BODY = 'BAD-RQST-BODY'
