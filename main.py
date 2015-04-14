import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

MAIN_PAGE_TEMPLATE = """\
    <form action="/add_ambassador" method="post">
      <div>Email: <input value="" name="email"></div>
      <div>First Name: <input value="" name="firstName"></div>
      <div>Last Name: <input value="" name="lastName"></div>
      <div>Program: <input value="" name="program"></div>
      <div>Graduation Year: <input value="" name="graduationYear"></div>
      <div>Stream: <input value="" name="stream"></div>
      <div><input type="submit" value="Submit"></div>
    </form>
  </body>
</html>
"""

# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent.  However, the write rate should be limited to
# ~1/second.
def ambassador_key():
    """
    Constructs a Datastore key for a Guestbook entity.
    We use guestbook_name as the key.
    """
    return ndb.Key('Ambassador', 'default_ambassador')

class Ambassador(ndb.Model):
    email = ndb.StringProperty(indexed=False)
    firstName = ndb.StringProperty(indexed=False)
    lastName = ndb.StringProperty(indexed=False)
    program = ndb.StringProperty(indexed=False)
    graduationYear = ndb.StringProperty(indexed=False)
    stream = ndb.StringProperty(indexed=False)
    
class ShadowDay(ndb.Model):
    currentStatus = ndb.StringProperty(indexed=False)
    submissionTime = ndb.DateTimeProperty(auto_now_add=True)
    shadowFirstName = ndb.StringProperty(indexed=False)
    shadowLastName = ndb.StringProperty(indexed=False)
    shadowEmail = ndb.StringProperty(indexed=False)
    shadowPhone = ndb.StringProperty(indexed=False)
    shadowGender = ndb.StringProperty(indexed=False)
    shadowGrade = ndb.StringProperty(indexed=False)
    shadowHighschool = ndb.StringProperty(indexed=False)
    shadowPhone = ndb.StringProperty(indexed=False)
    shadowFirstPick = ndb.StringProperty(indexed=False)
    shadowSecondPick = ndb.StringProperty(indexed=False)
    shadowFoodConstraints = ndb.StringProperty(indexed=False)
    shadowSpecialConstraints = ndb.StringProperty(indexed=False)
    ambassadorFirstName = ndb.StringProperty(indexed=False)
    ambassadorLastName = ndb.StringProperty(indexed=False)
    ambassadorEmail = ndb.StringProperty(indexed=False)
    
class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)

class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

class AmbassadorList(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        # Ancestor Queries, as shown here, are strongly consistent
        # with the High Replication Datastore. Queries that span
        # entity groups are eventually consistent. If we omitted the
        # ancestor from this query there would be a slight chance that
        # Greeting that had just been written would not show up in a
        # query.
        ambassadors_query = Ambassador.query(ancestor=ambassador_key()).order(-Ambassador.program)
        ambassadors = ambassadors_query.fetch(10)

        user = users.get_current_user()
        for ambassador in ambassadors:
            self.response.write('<blockquote>%s</blockquote>' % cgi.escape(ambassador.email))

        self.response.write(MAIN_PAGE_TEMPLATE)

class Add_Ambassador(webapp2.RequestHandler):
    def post(self):                                          
        ambassador = Ambassador(parent=ambassador_key())

        ambassador.email = self.request.get('email', '')
        ambassador.firstName = self.request.get('firstName', '')
        ambassador.lastName = self.request.get('lastName', '')
        ambassador.program = self.request.get('program', '')
        ambassador.graduationYear = self.request.get('graduationYear', '')
        ambassador.stream = self.request.get('stream', '')
        
        ambassador.put()

        self.redirect('/')

application = webapp2.WSGIApplication([
    ('/', AmbassadorList),
    ('/add_ambassador', Add_Ambassador)
], debug=True)