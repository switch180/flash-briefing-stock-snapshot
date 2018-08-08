import uuid
import json
from datetime import datetime
import logging
logger = logging.getLogger('my-app')

#https://developer.amazon.com/docs/flashbriefing/flash-briefing-skill-api-feed-reference.html
class AlexaResponse:
    def __init__(self, slugs, preamble=None):
        self.uuid = uuid.uuid4()
        self.now = datetime.utcnow()
        self.now_fmt =  self.now.strftime('%Y-%m-%dT%H:%M:%SZ') #2016-05-23T22:34:51.0Z
        self.preamble = None
        self.blurbs = list()
        self.slugs = slugs
        self.preamble = preamble


    def set_title(self, title):
        self.title = title


    def set_blurbs(self, blurbs):
        if isinstance(blurbs, list):
            self.blurbs = blurbs
        else:
            raise ValueError


    def get_blurbs(self):
        return self.blurbs


    def add_blurb(self, blurb):
        self.blurbs.append(blurb.format(**self.slugs))


    def set_preamble(self, preamble):
        self.preamble = preamble


    def get_resp(self):
        main_text = ". ".join(self.blurbs)
        if self.preamble:
            main_text = "{}, {}".format(self.preamble, main_text)

        resp = {
            'uid': str(self.uuid),
            'updateDate': self.now_fmt,
            'titleText': self.title,
            'mainText': main_text,
        }
        return resp


    def __str__(self):
        return json.dumps(self.get_resp())
