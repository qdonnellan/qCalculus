import os
import jinja2
import webapp2
import hashlib
from google.appengine.api import users
import datetime
from dbops import *
from enroll import *



template_dir=os.path.join(os.path.dirname(__file__),"templates")
jinja_environment=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_environment.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):         
        user = self.fetch_user()        
        if user == None:
            profile_msg = "No profile to view"
            current_user = "Not Logged In"
            site_action_url = r"<a href='/login'><i class='icon-globe'></i> Sign in or Register</a>"
        else:
            profile_msg = "<i class='icon-user'></i> Profile"
            current_user = user.nickname
            site_action_url = r"<a href='%s'><i class='icon-off'></i> Sign Out of Google Account</a>" % users.create_logout_url("/")
                   
        self.write(self.render_str(template, 
                                   current_user = current_user,
                                   profile_msg = profile_msg,
                                   site_action_url = site_action_url, 
                                   **kw))        


    def fetch_user(self):
        #this returns the user object if present and None otherwise
        #starting with the assumption of no user presence
        user_presence = None

        #Fetch the current google session user_id
        current_google_session = users.get_current_user()
        if current_google_session:
            user_id = current_google_session.user_id()

            db_user = get_user(user_id)

            if db_user:
                #See if the user is inidivually cached first...
                user_presence = db_user
            
        return user_presence

            
    def login_required(self, wrapped_function):
        """
        This is a decorator for ensuring that a wrapped function requires
        that a user be logged in
        """
        user = self.fetch_user()       
        if user:
            wrapped_function(user)
        else:
            self.redirect("/?errors=You must be logged in to view that content")

    def valid_course(self, course_name):
        current_course_list = ['cal101']
        validity = False
        error = 'There was an error with your request'
        if course_name is not None:
            for course in current_course_list:
                if course_name == course:
                    validity = True


        user = self.fetch_user()
        if not check_enrollment(user, course_name):
            validity = False
            error = 'You are not enrolled in that course'

        if validity:
            return True
        else:            
            self.redirect('/?errors=%s' % error)
            return False

    


        
            
