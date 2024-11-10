from mitmproxy import http
import ssl
import urllib.request
import json

# Create custom SSL context
sslContext = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
sslContext.verify_mode = ssl.CERT_REQUIRED
sslContext.load_verify_locations(cafile="isrgrootx1.pem")

# Retrieve interop test server root CA
with urllib.request.urlopen('https://test.openquantumsafe.org/CA.crt', context=sslContext) as response:
    data = response.read()
    with open("CA.crt", "w+b") as f:
        f.write(data)

# Trust test.openquantumsafe.org root CA
sslContext.load_verify_locations(cafile="CA.crt")

def request(flow: http.HTTPFlow) -> None:
    try:
        print("-" * 100)
        print(f"Original Request: {flow.request.url}")
        host = flow.request.pretty_host

        if host == "test.openquantumsafe.org":
            # flow.request.host = "test.openquantumsafe.org"
            # flow.request.scheme = "https"
            # flow.request.port = 6138

            # Make a request using the custom SSL context
            try:
                with urllib.request.urlopen('https://test.openquantumsafe.org:6138', context=sslContext) as response:
                    response_data = response.read()
                    if response.getcode() != 200:
                        print("Failed to test successfully")
                    else:
                        print("Success testing at port 6138")

                    # Modify the response to show in the browser
                    flow.response = http.HTTPResponse.make(
                        200,  # (optional) status code
                        response_data,  # content
                        {"Content-Type": "text/html"}  # (optional) headers
                    )
            except Exception as e:
                print(f"Error making request with custom SSL context: {e}")
                flow.response = http.HTTPResponse.make(
                    500,  # status code
                    f"Error making request with custom SSL context: {e}".encode('utf-8'),  # content
                    {"Content-Type": "text/plain"}  # headers
                )

        else:
            flow.request.host = "test.openquantumsafe.org"
            flow.request.scheme = "https"
            flow.request.port = 6138
            print("Request not intercepted")

    except Exception as e:
        print(f"Error in request handler: {e}")
        flow.response = http.HTTPResponse.make(
            500,  # status code
            f"Error in request handler: {e}".encode('utf-8'),  # content
            {"Content-Type": "text/plain"}  # headers
        )

    print("-" * 100)

# Register the request handler
addons = [request]