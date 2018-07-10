
#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import logging
import tornado.escape
import tornado.ioloop
import tornado.web
import os.path
import uuid
import time
import json

from tornado import gen
from tornado.options import define, options, parse_command_line
from motor import MotorClient


define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")


motor_client = MotorClient('localhost', 27017)
motor_db = motor_client.neighbour_finder


class NeighboursHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        x = float(self.get_argument('x'))
        y = float(self.get_argument('y'))
        limit = int(self.get_argument('limit', 1))
        pipeline = [] 
        pipeline.append({ "$geoNear": {"near": (x, y), "distanceField": "distance", "spherical": True}})
        pipeline.append({"$limit": limit})
        cursor = motor_db.neighbours.aggregate(pipeline)
        docs = []
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            docs.append({k:v for k, v in doc.items() if k in ['distance', 'name']})
        self.write(json.dumps(docs))

    @gen.coroutine
    def post(self):
        body = json.loads(self.request.body)
        x = float(body["x"])
        y = float(body["y"])
        name = body["name"]
        yield motor_db.neighbours.insert_one( { 'name': name, 'location': {'type': 'Point', 'coordinates': [x, y]} } )


def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/neighbours", NeighboursHandler),
        ],
        cookie_secret="e8f4cd1c0d0446dea71c60c64ff8fccf",
        debug=options.debug,
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

