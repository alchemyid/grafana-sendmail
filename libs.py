import falcon
from  helpers import helpers
import mimetypes

class uuid(object):
    def on_get(self, req, resp, id):
        try:
            receive = req.get_param('receive')
            
            if receive == None: 
                raise falcon.HTTPBadRequest(
                    'Please set param url `receive` to get latest report!'
                )
            else:
                helpers.getImage(id, receive)
                data = {'status': 200,
                        'sent_to': receive
                        }
                resp.status = falcon.HTTP_200
                resp.context['response'] = data

        except ValueError as e:
            raise falcon.HTTPError(falcon.HTTP_500, description=str(e))

class dashboardfile(object):
    def on_get(self, req, resp, id):
        try:
            # do some sanity check on the filename
            
            resp.status = falcon.HTTP_200
            resp.content_type = 'image/png'

            with open("assets/"+id, 'rb') as f:
                resp.body = f.read()

        except ValueError as e:
            raise falcon.HTTPError(falcon.HTTP_404, description=str(e))