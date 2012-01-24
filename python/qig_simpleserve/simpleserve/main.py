import web, json, cgi
from datetime import datetime

connection_list = []

urls = (
    '/api', 'Api',
    '/', 'Index'
)

class Index:
    def GET(self):
        render = web.template.render('templates')
        return render.main()

class Api:

    def GET(self):
        data = json.dumps(connection_list)
        web.header('Content-Type', 'application/json')
        return data

    def POST(self):
        try:
            msg = cgi.escape(web.data())
        except Exception:
            msg = ''
        ip = web.ctx.ip
        now = datetime.now().strftime('%c')
        item = (ip, now, msg)
        connection_list.append(item)
        web.header('Content-Type', 'application/json')
        raise web.created(data=json.dumps(item))


#web.config.debug = True
app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
else:
    app = app.wsgifunc()
