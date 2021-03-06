
MESSAGE_END = "\n"

COMMAND_QUIT = '!quit'
COMMAND_WHO = '!who'
COMMAND_MSG = '@'

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

BAD_RESPONSE = [UNKNOWN, IN_USE, BUSY, BAD_RQST_HDR, BAD_RQST_BODY]
GOOD_RESPONSE = [HELLO, WHO_OK, SEND_OK, DELIVERY]
