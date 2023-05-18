import falcon
from middleware import JSONTranslator
from libs import uuid, dashboardfile

def handle_404(req, resp):
    data = {
        'response': 'not found',
    }

    resp.status = falcon.HTTP_404
    resp.context['response'] = data

class index(object):
    def on_get(self, req, resp):
        data = {'status': 200,
                'appName': 'Shutdown Scheduler',
                'author': 'devops@xti'
                }

        resp.status = falcon.HTTP_200
        resp.context['response'] = data

def routes() -> falcon.App:
    app = falcon.App(middleware=[
        JSONTranslator()

    ])

    app.add_route('/', index())
    app.add_route('/id/{id}', uuid())
    app.add_route('/assets/{id}', dashboardfile())
    app.add_sink(handle_404, '')
    return app