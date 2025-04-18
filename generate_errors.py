import os
import shutil

error_codes = {
    "100": {"title": "Continue", "description": "Continue", "message": "The server has received the request headers and the client should proceed to send the request body.", "emoji": "⏳", "additional": "Please wait while we process your request."},
    "101": {"title": "Switching Protocols", "description": "Switching Protocols", "message": "The server is switching protocols as requested by the client.", "emoji": "🔄", "additional": "The server is upgrading the connection."},
    "102": {"title": "Processing", "description": "Processing", "message": "The server has received and is processing the request.", "emoji": "⚙️", "additional": "Your request is being processed."},
    
    "200": {"title": "OK", "description": "OK", "message": "The request has succeeded.", "emoji": "✅", "additional": "Everything is working as expected."},
    "201": {"title": "Created", "description": "Created", "message": "The request has been fulfilled and resulted in a new resource being created.", "emoji": "✨", "additional": "A new resource has been created."},
    "202": {"title": "Accepted", "description": "Accepted", "message": "The request has been accepted for processing.", "emoji": "👍", "additional": "Your request has been accepted."},
    "204": {"title": "No Content", "description": "No Content", "message": "The server successfully processed the request but is not returning any content.", "emoji": "📭", "additional": "The request was successful but there's no content to return."},
    "206": {"title": "Partial Content", "description": "Partial Content", "message": "The server is delivering only part of the resource due to a range header sent by the client.", "emoji": "📄", "additional": "Partial content is being returned."},
    "207": {"title": "Multi-Status", "description": "Multi-Status", "message": "The message body that follows is an XML message and can contain a number of separate response codes.", "emoji": "📊", "additional": "Multiple status codes are being returned."},
    
    "300": {"title": "Multiple Choices", "description": "Multiple Choices", "message": "The request has more than one possible response.", "emoji": "🔀", "additional": "Please choose one of the available options."},
    "301": {"title": "Moved Permanently", "description": "Moved Permanently", "message": "The URL of the requested resource has been changed permanently.", "emoji": "➡️", "additional": "The resource has been moved to a new location."},
    "302": {"title": "Found", "description": "Found", "message": "The URL of the requested resource has been changed temporarily.", "emoji": "🔍", "additional": "The resource has been temporarily moved."},
    "303": {"title": "See Other", "description": "See Other", "message": "The response to the request can be found under another URI.", "emoji": "👀", "additional": "Please check the other URI for the response."},
    "304": {"title": "Not Modified", "description": "Not Modified", "message": "The resource has not been modified since the last request.", "emoji": "🔄", "additional": "The cached version is still valid."},
    "305": {"title": "Use Proxy", "description": "Use Proxy", "message": "The requested resource must be accessed through the proxy given by the Location field.", "emoji": "🔒", "additional": "Please use the specified proxy."},
    "307": {"title": "Temporary Redirect", "description": "Temporary Redirect", "message": "The request should be repeated with another URI.", "emoji": "🔄", "additional": "Please try the request again with the new URI."},
    
    "400": {"title": "Bad Request", "description": "Bad Request", "message": "The server cannot process the request due to a client error.", "emoji": "❌", "additional": "Please check your request and try again."},
    "401": {"title": "Unauthorized", "description": "Unauthorized", "message": "Authentication is required to access this resource.", "emoji": "🔒", "additional": "Please log in to access this resource."},
    "402": {"title": "Payment Required", "description": "Payment Required", "message": "Payment is required to access this resource.", "emoji": "💰", "additional": "Please complete the payment to proceed."},
    "403": {"title": "Forbidden", "description": "Forbidden", "message": "You don't have permission to access this resource.", "emoji": "🚫", "additional": "Please contact the administrator if you believe this is an error."},
    "404": {"title": "Not Found", "description": "Not Found", "message": "The requested resource could not be found.", "emoji": "🔍", "additional": "The page might have been moved, deleted, or never existed."},
    "405": {"title": "Method Not Allowed", "description": "Method Not Allowed", "message": "The method specified in the request is not allowed.", "emoji": "🚫", "additional": "Please check the allowed methods for this resource."},
    "406": {"title": "Not Acceptable", "description": "Not Acceptable", "message": "The server cannot produce a response matching the list of acceptable values.", "emoji": "❌", "additional": "Please check your request headers."},
    "408": {"title": "Request Timeout", "description": "Request Timeout", "message": "The server timed out waiting for the request.", "emoji": "⏰", "additional": "Please try your request again."},
    "409": {"title": "Conflict", "description": "Conflict", "message": "The request could not be completed due to a conflict with the current state of the resource.", "emoji": "⚔️", "additional": "Please resolve the conflict and try again."},
    "410": {"title": "Gone", "description": "Gone", "message": "The requested resource is no longer available.", "emoji": "🗑️", "additional": "The resource has been permanently removed."},
    "411": {"title": "Length Required", "description": "Length Required", "message": "The request did not specify the length of its content.", "emoji": "📏", "additional": "Please include a Content-Length header."},
    "412": {"title": "Precondition Failed", "description": "Precondition Failed", "message": "One or more conditions in the request header fields evaluated to false.", "emoji": "❌", "additional": "Please check your request headers."},
    "413": {"title": "Payload Too Large", "description": "Payload Too Large", "message": "The request is larger than the server is willing or able to process.", "emoji": "📦", "additional": "Please reduce the size of your request."},
    "414": {"title": "URI Too Long", "description": "URI Too Long", "message": "The URI provided was too long for the server to process.", "emoji": "🔗", "additional": "Please shorten your request URI."},
    "415": {"title": "Unsupported Media Type", "description": "Unsupported Media Type", "message": "The request entity has a media type which the server or resource does not support.", "emoji": "📄", "additional": "Please check the media type of your request."},
    "416": {"title": "Range Not Satisfiable", "description": "Range Not Satisfiable", "message": "The client has asked for a portion of the file that cannot be supplied.", "emoji": "🎯", "additional": "Please check your range request."},
    "417": {"title": "Expectation Failed", "description": "Expectation Failed", "message": "The server cannot meet the requirements of the Expect request-header field.", "emoji": "❌", "additional": "Please check your request expectations."},
    "418": {"title": "I'm a teapot", "description": "I'm a teapot", "message": "I'm a teapot, not a coffee maker.", "emoji": "🫖", "additional": "This is an April Fools' joke from 1998."},
    "420": {"title": "Enhance Your Calm", "description": "Enhance Your Calm", "message": "You are being rate limited.", "emoji": "🧘", "additional": "Please slow down your requests."},
    "421": {"title": "Misdirected Request", "description": "Misdirected Request", "message": "The request was directed at a server that is not able to produce a response.", "emoji": "🔄", "additional": "Please try a different server."},
    "422": {"title": "Unprocessable Entity", "description": "Unprocessable Entity", "message": "The request was well-formed but was unable to be followed due to semantic errors.", "emoji": "❌", "additional": "Please check your request data."},
    "423": {"title": "Locked", "description": "Locked", "message": "The resource that is being accessed is locked.", "emoji": "🔒", "additional": "The resource is currently locked."},
    "424": {"title": "Failed Dependency", "description": "Failed Dependency", "message": "The request failed due to failure of a previous request.", "emoji": "⛓️", "additional": "A dependent request has failed."},
    "425": {"title": "Too Early", "description": "Too Early", "message": "The server is unwilling to risk processing a request that might be replayed.", "emoji": "⏰", "additional": "Please try again later."},
    "426": {"title": "Upgrade Required", "description": "Upgrade Required", "message": "The client should switch to a different protocol.", "emoji": "⬆️", "additional": "Please upgrade your protocol."},
    "429": {"title": "Too Many Requests", "description": "Too Many Requests", "message": "The user has sent too many requests in a given amount of time.", "emoji": "⏱️", "additional": "Please try again later."},
    "431": {"title": "Request Header Fields Too Large", "description": "Request Header Fields Too Large", "message": "The server is unwilling to process the request because its header fields are too large.", "emoji": "📝", "additional": "Please reduce the size of your request headers."},
    "444": {"title": "No Response", "description": "No Response", "message": "The server returns no information and closes the connection.", "emoji": "🤐", "additional": "The server has closed the connection."},
    "450": {"title": "Blocked by Windows Parental Controls", "description": "Blocked by Windows Parental Controls", "message": "The resource is blocked by Windows Parental Controls.", "emoji": "👪", "additional": "This resource is blocked by parental controls."},
    "451": {"title": "Unavailable For Legal Reasons", "description": "Unavailable For Legal Reasons", "message": "The resource is unavailable for legal reasons.", "emoji": "⚖️", "additional": "This resource is not available in your region."},
    "497": {"title": "HTTP Request Sent to HTTPS Port", "description": "HTTP Request Sent to HTTPS Port", "message": "An HTTP request was sent to an HTTPS port.", "emoji": "🔒", "additional": "Please use HTTPS instead of HTTP."},
    "498": {"title": "Token Expired/Invalid", "description": "Token Expired/Invalid", "message": "The token has expired or is invalid.", "emoji": "🔑", "additional": "Please obtain a new token."},
    "499": {"title": "Client Closed Request", "description": "Client Closed Request", "message": "The client closed the connection before the server could send a response.", "emoji": "🚪", "additional": "The connection was closed by the client."},
    
    "500": {"title": "Internal Server Error", "description": "Internal Server Error", "message": "The server encountered an unexpected condition.", "emoji": "😿", "additional": "Our team has been notified and is working to fix the issue."},
    "501": {"title": "Not Implemented", "description": "Not Implemented", "message": "The server does not support the functionality required to fulfill the request.", "emoji": "🔧", "additional": "This feature is not yet implemented."},
    "502": {"title": "Bad Gateway", "description": "Bad Gateway", "message": "The server received an invalid response from an upstream server.", "emoji": "🔌", "additional": "Please try again later."},
    "503": {"title": "Service Unavailable", "description": "Service Unavailable", "message": "The server is currently unable to handle the request.", "emoji": "🔧", "additional": "The service will be back soon."},
    "504": {"title": "Gateway Timeout", "description": "Gateway Timeout", "message": "The server did not receive a timely response from an upstream server.", "emoji": "⏰", "additional": "Please try again later."},
    "506": {"title": "Variant Also Negotiates", "description": "Variant Also Negotiates", "message": "The server has an internal configuration error.", "emoji": "⚙️", "additional": "The server configuration needs attention."},
    "507": {"title": "Insufficient Storage", "description": "Insufficient Storage", "message": "The server is unable to store the representation needed to complete the request.", "emoji": "💾", "additional": "The server is running out of storage space."},
    "508": {"title": "Loop Detected", "description": "Loop Detected", "message": "The server detected an infinite loop while processing the request.", "emoji": "🔄", "additional": "An infinite loop was detected in the request."},
    "509": {"title": "Bandwidth Limit Exceeded", "description": "Bandwidth Limit Exceeded", "message": "The server's bandwidth limit has been exceeded.", "emoji": "📊", "additional": "Please try again later."},
    "510": {"title": "Not Extended", "description": "Not Extended", "message": "Further extensions to the request are required for the server to fulfill it.", "emoji": "➕", "additional": "Additional extensions are required."},
    "511": {"title": "Network Authentication Required", "description": "Network Authentication Required", "message": "The client needs to authenticate to gain network access.", "emoji": "🔒", "additional": "Please authenticate to access the network."},
    "521": {"title": "Web Server Is Down", "description": "Web Server Is Down", "message": "The origin web server is down.", "emoji": "🔌", "additional": "The web server is currently offline."},
    "522": {"title": "Connection Timed Out", "description": "Connection Timed Out", "message": "The connection to the origin server timed out.", "emoji": "⏰", "additional": "The connection attempt timed out."},
    "523": {"title": "Origin Is Unreachable", "description": "Origin Is Unreachable", "message": "The origin server is unreachable.", "emoji": "🔍", "additional": "The origin server cannot be reached."},
    "525": {"title": "SSL Handshake Failed", "description": "SSL Handshake Failed", "message": "The SSL handshake failed.", "emoji": "🔒", "additional": "The secure connection could not be established."},
    "599": {"title": "Network Connect Timeout Error", "description": "Network Connect Timeout Error", "message": "A network connect timeout error occurred.", "emoji": "⏰", "additional": "The network connection timed out."}
}

def create_error_pages():
    if not os.path.exists('errors'):
        os.makedirs('errors')
    
    with open('errors/template.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    for code, info in error_codes.items():
        content = template
        content = content.replace('ERROR_CODE', code)
        content = content.replace('ERROR_TITLE', info['title'])
        content = content.replace('ERROR_DESCRIPTION', info['description'])
        content = content.replace('ERROR_MESSAGE', info['message'])
        content = content.replace('ERROR_EMOJI', info['emoji'])
        content = content.replace('ERROR_ADDITIONAL_MESSAGE', info['additional'])
        
        with open(f'errors/{code}.html', 'w', encoding='utf-8') as f:
            f.write(content)
    
    print("Error pages generated successfully!")

if __name__ == "__main__":
    create_error_pages() 