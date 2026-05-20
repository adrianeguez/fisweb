from urllib.parse import urlparse


def abort_request(request):
    """Abort third-party requests to keep pilot runs fast and deterministic."""
    hostname = urlparse(request.url).hostname or ""
    if hostname.endswith("fis.epn.edu.ec"):
        return False

    if request.resource_type in {"document", "xhr", "fetch"} and "epn.edu.ec" in hostname:
        return False

    return True
