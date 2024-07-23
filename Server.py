import asyncio
import os
from ParseMamlRequestResponse import ParseMamlRequestResponse
import tornado
import yaml
import json
class MainHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        self.write("Hello, world")
    def post(self):
        yaml_in = yaml.safe_load(self.request.body)
        #print(yaml_in['details']['author'])
        # I promise I will use an sqlite database for user data/configs in the future
        parser = ParseMamlRequestResponse(yaml_in, "/tmp/")
        # this begs for a worker pool with a ticket uuid up front and a sqlite db
        # long requests will have to do for now.
       
        parser.fill_vars_with_nbef()
        ## combinations, include eventually
        if parser.printer.final_path:
            with open(parser.printer.final_path, 'rb') as file:
                self.set_header("Content-Type", "audio/midi")
                self.set_status(200)
                self.write(file.read())
            os.remove(parser.printer.final_path)
        else:
            self.set_header("Content-Type", "text/json")
            self.set_status(500)
            self.write(json.dumps({'error': 'no midi file generated'}))
        #parser.handle_combinations()
        

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
         (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "./public/"})
    ])

async def main():
    app = make_app()
    app.listen(8888)
    print('listening on 8888')
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())