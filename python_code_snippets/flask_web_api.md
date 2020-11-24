# Flask Web API

Flask wrapper to use object oriented way, use together with uwsgi server.

```python
from datetime import datetime

from flask import Flask, render_template, request, Response


class EndpointAction(object):
    def __init__(self, action):
        self.action = action

    def __call__(self, *args):
        response = self.action(*args)
        return response


class FlaskAppWrapper(object):
    app = None

    def __init__(self, name):
        self.app = Flask(name, template_folder='templates')

    def run(self):
        self.app.run()

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=None):
        self.app.add_url_rule(rule=endpoint, endpoint=endpoint_name, view_func=EndpointAction(handler), methods=methods)


class WebApi(object):
    time_last_message = None

    def __init__(self):
        self.startup_time = datetime.now()

    def __call__(self, *args, **kwargs):
        flask = FlaskAppWrapper(__name__)
        index_url = {'endpoint': '/api/', 'endpoint_name': 'index', 'handler': self.app_index, 'methods': ['GET']}
        webhook_url = {'endpoint': '/api/webhook', 'endpoint_name': 'webhook', 'handler': self.bitbucket_event_handler,
                       'methods': ['POST']}
        flask.add_endpoint(**index_url)
        flask.add_endpoint(**webhook_url)
        flask.run()

    def view_post(self):
        if request.is_json:
            payload = request.get_json()
            print(payload)
        return Response(status=200, headers={})

    def app_index(self):
        params = {'value': 'value_a'}
        return render_template('index.html', **params)


if __name__ == '__main__':
    api = WebApi()
    api()
```

in folder templates/index.html
```html
<!DOCTYPE html>
<html>
<body>

<h1>data: {{value}}</h1>

</body>
</html>
```
