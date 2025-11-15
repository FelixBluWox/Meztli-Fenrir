
http_codes = {
    400:"The request could not be understood by the server due to malformed syntax. The client SHOULD NOT repeat the request without modifications.",
    401:"The request requires user authentication but has failed or not yet been provided.",
    402:"This code is reserved for future use.",
    403:"The server understood the request, but is refusing to fulfill it. Authorization will not help and the request SHOULD NOT be repeated.",
    404:"The server has not found anything matching the Request-URI. No indication is given of whether the condition is temporary or permanent.",
    405:"The method specified in the Request-Line is not allowed for the resource identified by the Request-URI.",
    406:"The resource identified by the request is only capable of generating response entities which have content characteristics not acceptable according to the accept headers sent in the request.",
    407:"The client must first authenticate itself with the proxy.",
    408:"The client did not produce a request within the time that the server was prepared to wait.",
    409:"The request could not be completed due to a conflict with the current state of the resource.",
    410:"The requested resource is no longer available at the server and no forwarding address is known.",
    411:"The server refuses to accept the request without a defined Content- Length.",
    412:"The server does not meet one of the preconditions that the requester put on the request.",
    413:"The request is larger than the server is willing or able to process.",
    414:"The server is refusing to service the request because the Request-URI is longer than the server is willing to interpret.",
    415:"The server is refusing to service the request because the entity of the request is in a format not supported by the requested resource for the requested method.",
    416:"The client has asked for a portion of the file, but the server cannot supply that portion.",
    417:"The server cannot meet the requirements of the Expect request-header field.",
    418:"This code was defined in 1998 as one of the traditional IETF April Fools' jokes, in RFC 2324, Hyper Text Coffee Pot Control Protocol, and is not expected to be implemented by actual HTTP servers.",
    419:"Returned by the Twitter Search and Trends API when the client is being rate limited.",
    422:"The request was well-formed but was unable to be followed due to semantic errors.",
    423:"The resource that is being accessed is locked.",
    424:"The request failed due to failure of a previous request.",
    425:"Reserved for WebDAV",
    426:"Allows a server to definitively state the precise protocol extensions a given resource must be served with.",
    427:"The origin server requires the request to be conditional.",
    428:"The user has sent too many requests in a given amount of time (rate limiting).",
    431:"The server is unwilling to process the request because its header fields are too large.",
    444:"The server returns no information to the client and closes the connection.",
    449:"The request should be retried after performing the appropriate action.",
    450:"This error is given when Windows Parental Controls are turned on and are blocking access to the given webpage.",
    451:"Intended to be used when resource access is denied for legal reasons, e.g. censorship or government-mandated blocked access.",
    499:"This code is introduced to log the case when the connection is closed by client while HTTP server is processing its request, making server unable to send the HTTP header back.",
    500:"The server encountered an unexpected condition which prevented it from fulfilling the request.",
    501:"The server does not support the functionality required to fulfill the request.",
    502:"The server, while acting as a gateway or proxy, received an invalid response from the upstream server it accessed in attempting to fulfill the request.",
    503:"The server is currently unable to handle the request due to a temporary overloading or maintenance of the server.",
    504:"The server was acting as a gateway or proxy and did not receive a timely response from the upstream server.",
    505:"The server does not support, or refuses to support, the HTTP protocol version that was used in the request message.",
    506:"Transparent content negotiation for the request results in a circular reference.",
    507:"The server is unable to store the representation needed to complete the request.",
    508:"The server detected an infinite loop while processing the request.",
    509:"The website you are trying to visit has gone over their hosting bandwidth limit.",
    510:"Further extensions to the request are required for the server to fulfill it.",
    511:"The client needs to authenticate to gain network access."
}

class HttpResponseError(Exception):
    "{'error': 'Gone', 'status': 410, 'message': 'v3 is a lie but v5 is still alive. See https://dev.twitch.tv/docs'}"

    def __init__(self, response):
        self.json = response
        self.error = response['error']
        self.status = response['status']
        self.message = response['message']
        super().__init__(f'{self.status} {self.error}: self.message', http_codes.get(self.status, 418))

    def __str__(self):
        return f'{self.status} {self.error}: self.message'