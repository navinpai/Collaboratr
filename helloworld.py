import webapp2
import os
import urllib
import random
import string
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.ext import db
import time
import json



class Code(db.Model):
    id =db.StringProperty(required=True)
    code = db.TextProperty(required=True)
    num=db.IntegerProperty(required=True)
    language=db.StringProperty(required=True)
  
class New(webapp2.RequestHandler):
    def get(self):
        id=''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6))
        e=Code(id=id,code='/*'+'print "#gcdcrocks"'+'*/',num=0,language="PYTHON")
        e.put()
        #self.response.out.write(id)
        time.sleep(3)
        self.redirect('/'+id)
        
  
class MainPage(webapp2.RequestHandler):
    def get(self):
        '''self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('')
        '''
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path,None))
        '''e=Code(id='1235',code='print "Hello"',num=0)
        e.put()
        '''
  
class Run(webapp2.RequestHandler):
    def post(self):
        form_fields = {'client_secret': '940667541fd208054683c5be8a0290c8a7e9331b','async':0,'time_limit': 5, 'source': self.request.get('code'),'lang': self.request.get('lang')}
        form_data = urllib.urlencode(form_fields)
        result = urlfetch.fetch(url='http://api.hackerearth.com/code/run/',payload=form_data,method=urlfetch.POST)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(result.content)#template.render(path,None))
         #,headers={'Content-Type': 'application/x-www-form-urlencoded'})'''


class Update(webapp2.RequestHandler):
    def post(self):
        q = Code.all()
        q.filter("id =", self.request.get('id'))
        
        result = q.get()
        if result is not None:
            result.code='/*'+self.request.get('code')+'*/'
            result.language=self.request.get('language')
            result.put()
        else:
            self.response.out.write("Error")

class GetCode(webapp2.RequestHandler):
    def get(self):
        q = Code.all()
        q.filter("id =", self.request.get('id'))
        result = q.get()
        if result is not None:
            self.response.headers['Content-Type'] = 'application/json'
            obj = {
                   'code': result.code, 
                   'language':result.language
                   } 
            self.response.out.write(json.dumps(obj))
        else:
            self.response.out.write("Error")

class CollabPage(webapp2.RequestHandler):
    def get(self,identifier):
        q = Code.all()
        q.filter("id =", identifier)
        result = q.get()
        if result is not None:
            template_values = {
            'result': urllib.unquote(result.code),
            'resultid':identifier,
            'language':result.language
        }
        #self.response.out.write(result.code)
            path = os.path.join(os.path.dirname(__file__), 'collab.html')
            self.response.out.write(template.render(path,template_values))
        else:
            self.response.out.write("Error :(")

class ViewPage(webapp2.RequestHandler):
    def get(self,identifier):
        q = Code.all()
        q.filter("id =", identifier)
        result = q.get()
        if result is not None:
            template_values = {
            'result': urllib.unquote(result.code),
            'resultid':identifier
        }
        #self.response.out.write(result.code)
            path = os.path.join(os.path.dirname(__file__), 'view.html')
            self.response.out.write(template.render(path,template_values))
        else:
            self.response.out.write("Error :(")
 
               

app = webapp2.WSGIApplication([
                               ('/', MainPage),
                               ('/update',Update),
                               ('/get',GetCode),
                               ('/new',New),
                               ('/run',Run),
                               ('/(\w+)',CollabPage),
                               ('/!(\w+)',ViewPage),
                               ])
