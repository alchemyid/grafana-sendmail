import json
import falcon
from helpers import helpers
from urllib.parse import urlparse
import os

class checkEnvironment(object):

    def process_resource(self, req, resp, resource, params):
        
        aclDomain = helpers.read_config("domain_acl", None)
        parse = urlparse(os.getenv('GF_URI_SCHEMA')+"://"+os.getenv('GF_HOST'))
        domain = '{uri.netloc}'.format(uri=parse)

        if helpers.env() == True and domain in aclDomain:
            return
        else:
            description = (
                'Please check your environment variable!')
            raise falcon.HTTPPreconditionFailed('Failed', description)
        
        
class JSONTranslator:

    def process_request(self, req, resp):
        """
        req.stream corresponds to the WSGI wsgi.input environ variable,
        and allows you to read bytes from the request body.
        See also: PEP 3333
        """
        if req.content_length in (None, 0):
            return

        body = req.stream.read()

        if not body:
            raise falcon.HTTPBadRequest(
                'Empty request body. A valid JSON document is required.'
            )

        try:
            req.context['request'] = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(
                falcon.HTTP_753,
                'Malformed JSON. Could not decode the request body.'
                'The JSON was incorrect or not encoded as UTF-8.'
            )

    def process_response(self, req, resp, resource, req_succeeded):
        if 'response' not in resp.context:
            return

        resp.text = json.dumps(
            resp.context['response'],
            default=helpers.jsonSerializer,
            sort_keys=True,
            indent=2,
            separators=(',', ': ')
        )