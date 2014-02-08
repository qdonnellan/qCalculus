import webapp2
import logging
from google.appengine.api import memcache
from google.appengine.ext import db
from handlers import MainHandler
from dbops import *
from google.appengine.api import users
import cgi
from build_question_list import *
import re
from operator import itemgetter, attrgetter
from courses import *
from enroll import *
import time
from badges import *
from profile import *
from discussion import *
from practice import *



class MainPage(MainHandler):
    def get(self):
        #This is the front page of the app which renders the template 'front.html'
        errors = self.request.get('errors') 
        #If there are errors, a 'twitter-bottstrap' alert is displayed at the top of the page
        alert_msg = ''
        if errors:
            alert_msg = r'''
            <div class="alert alert-error">
                <a class="close" data-dismiss="alert" href="/">&times;</a>
                <h4 class="alert-heading">Oh snap!</h4>
                %s ... 
            </div>
            ''' % errors

        #Check to see if a user is present and if they are enrolled in any class
        # x contains the enrollment information for each class displayed on the front page
        # this information toggles button/link appearance and behavior
        user = self.fetch_user()
        x = enroll(user)


        #the profile_url below is injected into the base.html handler (used by every page)
        #the function profile_url can be found in dbops.py
        self.render('front.html', 
            errors=alert_msg, 
            home_active = "active", 
            profile_url = profile_url(user=user),
            enroll = x)
            


class CreateUser(MainHandler):
    def get(self):
        self.redirect('%s' % users.create_login_url("/login/create_true"))
        

class CreateLocalUser(MainHandler):
    def get(self):
        #User gets to here after successfully allowing Google Account to link to this app
        user = users.get_current_user()
        if not user:
            #this condition should only be hit for people trying to circumvent 
            self.redirect('/login')
        
        else:
            local_user = self.fetch_user()
            if local_user:
                #if, after all this, user is indeed in the app database
                self.redirect('/profile')
            else:
                #more likely option - create an account!                
                new_user = create_new_user(user.user_id(), user.nickname())        
                if new_user:
                    self.redirect('/profile')
                else:
                    self.redirect('/login?errors=An error occurred when attempting to create the user account')  
                          
class ExistingLogIn(MainHandler):
    def get(self):
        self.redirect('%s' % users.create_login_url("/login/existing_true"))
        
class ExistingTrue(MainHandler):
    def get(self):
        user = self.fetch_user()
        if user:
            self.redirect('/profile')            
        else:
            self.redirect("/login?errors=That account doesn't exist, please create an account")      

class LoginSignup(MainHandler):
    def get(self):
        errors = self.request.get('errors') 
        alert_msg = ''
        if errors:
            alert_msg = r'''
            <div class="alert alert-error">
                <a class="close" data-dismiss="alert" href="#">&times;</a>
                <h4 class="alert-heading">Oh snap!</h4>
                %s ... 
            </div>
            ''' % errors  
        user = self.fetch_user()    
        self.render('login.html', errors = alert_msg, profile_url = profile_url(user= user))    



class CourseFront(MainHandler):
    def get(self, course_name):
        if self.valid_course(course_name):           
            error = False
            course = get_course_info(course_name)
            if course is None:           
                error = True

            if error:
                self.redirect("/")
            else:
                user = self.fetch_user()
                self.render('course_front.html', 
                    course = course,
                    profile_url = profile_url(course_name, user),
                    course_home_active = 'active')


class CourseEnroll(MainHandler):
    def get(self, course_name):
        @self.login_required
        def secured_things(user):
            course = get_course_info(course_name)
            self.render('enroll.html', 
                course = course, 
                profile_url = profile_url(course_name, user))

    def post(self,course_name):
        @self.login_required
        def secured_things(user):
            new_enrollment(user,course_name)
            self.redirect('/course/%s' % course_name)

class CourseSyllabus(MainHandler):
    def get(self, course_name):
        @self.login_required
        def secured_things(user):
            if self.valid_course(course_name): 
                course = get_course_info(course_name)            
                self.render('syllabus.html', 
                    course= course, 
                    syllabus_active = 'active',
                    syllabus = course.syllabus,
                    profile_url = profile_url(course_name, user))

class MoreInfo(MainHandler):
    def get(self, course_name):
        user = self.fetch_user()
        enrolled = check_enrollment(user, course_name)
        if enrolled:
            self.redirect('/course/%s/syllabus' % course_name)
        else:
            preview_courses = ['cal101']
            preview = False
            for course in preview_courses:
                if course_name == course:
                    preview = True

            if preview:
                course = get_course_info(course_name)
                self.render('more_info.html', 
                    course= course,
                    profile_url = profile_url(course_name))

            else:
                self.redirect('/?errors=No preview for that class exists yet')

class Materials(MainHandler):
    def get(self, course_name):
        @self.login_required
        def secured_things(user):
            if self.valid_course(course_name): 
                self.render('materials.html', 
                    course = get_course_info(course_name),
                    materials_active = 'active',
                    profile_url = profile_url(course_name, user))

class Lessons(MainHandler):
    def get(self, course_name):
        @self.login_required
        def secured_things(user):            
            if self.valid_course(course_name): 
                user_level = get_user_level(course_name, str(user.user_id)) 
                level = 1                
                extras = ''           
                course = get_course_info(course_name)
                
                qalert = ''
                current_unit = self.request.get('unit')                
                current_lesson = self.request.get('lesson')
                success = self.request.get('success')
                ans = self.request.get('ans')

                answer_key = ''
                if current_lesson is None or current_lesson is '':
                    current_lesson = course.units[0].lessons[0].title

                if current_unit is None or current_unit is '':
                    current_unit = course.units[0].title

                current_level = get_lesson_level(course, current_lesson, current_unit)
               

                if current_level is None or current_level > user_level:
                    current_lesson = course.units[0].lessons[0].title
                    current_unit = course.units[0].title
                    self.redirect('/course/%s/lessons?unit=%s&lesson=%s' % (course_name, current_unit, current_lesson))
                else:
                    unit_tab_labels = ''
                    unit_tab_content = ''
                    unit_count = 0
                    for unit in course.units:
                        unit_active = ''
                        lesson_list = ''
                        unit_count +=1                       
                        lesson_count = 0
                        if user_level >=level:
                            lesson_list += '<li class="nav-header">%s</li>' % unit.title 
                        else:
                            lesson_list = '<i class="icon icon-lock"></i>This unit is locked'                           
                        for lesson in unit.lessons:
                            if lesson.quiz is None:
                                lesson_count +=1
                                decorator = str(lesson_count) + ')'
                            else:                                 
                                if user_level <= level:                                     
                                    decorator = '<span class="badge badge-warning"><i class="icon-pencil icon-white"></i></span> '
                                else:                                
                                    decorator = '<span class="badge badge-success"><i class="icon-ok icon-white"></i></span>'
                                    
                            if lesson.title == current_lesson and unit.title == current_unit: 
                                tag_suggestion = re.sub(' ','-',lesson.title.lower())
                                tag_suggestion = re.sub(':','', tag_suggestion)
                                tag_suggestion = 'unit%s-%s' % (unit_count,tag_suggestion)
                                unit_active = 'active'                               
                                active = 'active'                            
                                if lesson.video is not None:
                                    extras = '''
                                        <div class="row-fluid hidden-phone" id ="video-well">
                                            <iframe class = "youtube-player" width="1280" height="750" src="http://www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>    
                                        </div>
                                        <div class="row-fluid visible-phone" id ="video-well">
                                            <h6>Click image to watch video on your mobile device</h6>
                                            <a href="http://youtube.com/watch?v=%s">
                                                <img src="http://img.youtube.com/vi/%s/0.jpg" >
                                            </a>
                                        </div>  
                                    ''' % (lesson.video, lesson.video, lesson.video)
                                elif lesson.quiz is not None:
                                    if lesson.title == current_lesson:
                                        
                                        if success == 'good':
                                            current_streak = get_quiz_stats(course, user, lesson.title, unit.title)[2]
                                            streak_alert = ''
                                            if current_streak is None:
                                                current_streak = 0

                                            if lesson.streak > 1:
                                                percent_streak = str(int(1.*current_streak/lesson.streak*100)) + r'%'  
                                                if user_level <= level:                                          
                                                    streak_alert = 'You need %s in a row to move on' % lesson.streak                                            
                                                    streak_alert += '''
                                                    <div class="progress progress-success progress-striped active">                                                 
                                                        <div class="bar" style="width: %s;"></div>
                                                    </div>
                                                    ''' % percent_streak
                                            else:                                            
                                                streak_alert = '' 

                                            qalert = '''
                                                <div class="alert alert-success">
                                                    <a class="close" data-dismiss="alert" href="#">&times;</a>
                                                    <h4 class="alert-heading">Correct</h4>
                                                    Good job!
                                                    %s
                                                    Current streak: %s
                                                </div>
                                           ''' % (streak_alert, current_streak)

                                        elif success == 'error':
                                            qalert = '''
                                                <div class="alert alert-error">
                                                    <a class="close" data-dismiss="alert" href="#">&times;</a>
                                                    <h4 class="alert-heading">Incorrect</h4>
                                                    Try again...
                                                </div>
                                            '''  

                                                                    
                                    last_so_many_quizzes = 5
                                    qscore,qattempts,streak = get_quiz_stats(course, user, lesson.title, unit.title,last_so_many_quizzes)
                                    longest_streak = get_longest_streak(course.name, lesson.title, unit.title, user.user_id)
                                    if qattempts == 0:                                        
                                        qpercent = '0%'
                                    else:
                                        qpercent = str(int(1.*qscore/qattempts * 100)) + '%'

                                    if qpercent == '100%' and qattempts == last_so_many_quizzes:
                                        great_job_label = '<span class="badge badge-success pull-left">excellent</span>'                                    
                                    else:
                                        great_job_label = ''

                                    extras = '''                                        
                                        <form method = "post">
                                            %s
                                            <br>
                                            <input class="btn" type="submit" value="Submit">
                                            <input type ="hidden" name ="random_cookie" value="%s">
                                        </form>
                                        <h6 class="pull-left" style="margin-right:10px">last %s attempts: %s/%s (%s) longest streak: %s</h6> %s
                                    ''' % (
                                        lesson.quiz, 
                                        lesson.key,
                                        last_so_many_quizzes, 
                                        qscore,
                                        qattempts, 
                                        qpercent,
                                        longest_streak,
                                        great_job_label)
                                elif lesson.notes is not None:
                                    extras = lesson.notes
                                    
                                else:
                                    extras = 'No content for this lesson yet...'

                            else:
                                active = ''
                            lesson_link = '/course/%s/lessons?unit=%s&lesson=%s' %(course_name, unit.title, lesson.title)
                            if user_level >= level:
                                 lesson_list += '''
                                    <li class="%s">
                                        <a href="%s">
                                            %s %s
                                        </a>
                                    </li>
                                ''' % (active,lesson_link, decorator,lesson.title)

                            if lesson.quiz is not None:
                                level += 1


                        unit_tab_labels += '''
                            <li class="%s">
                                <a href = "#tab%s" data-toggle="tab" style="padding:10px">
                                    %s
                                </a>
                            </li>
                        ''' % (unit_active, unit_count,unit_count)

                        unit_tab_content += '''
                            <div class="tab-pane %s" id ="tab%s">
                                <ul class="nav nav-list">
                                    %s
                                </ul>
                            </div>
                        ''' % (unit_active, unit_count,lesson_list)
                            

                    self.render('lessons.html',
                        lesson_title = current_lesson,
                        tag_suggestion = tag_suggestion,
                        unit_title = current_unit, 
                        course = course,
                        lessons_active = 'active', 
                        materials_active = 'active',
                        extras = extras,
                        qalert = qalert,
                        unit_tab_labels = unit_tab_labels,
                        unit_tab_content = unit_tab_content,
                        profile_url = profile_url(course_name, user))

    def post(self,course_name):
        @self.login_required
        def secured_things(user):
            if self.valid_course(course_name):
                current_unit = self.request.get('unit')                
                current_lesson = self.request.get('lesson')
                answer_key = self.request.get('random_cookie')
                user_response = self.request.POST.getall('quiz_answer') 
                course = get_course_info(course_name)                
                ans = ''
                for answer in user_response:
                    ans += str(answer.encode('ascii', 'ignore'))
                correct_ans = memcache.get(answer_key)
                correct_hit = False
                logging.info(correct_ans)
                if '<<>>' in correct_ans: 
                    split_ans = correct_ans.split('<<>>')
                    for each_ans in split_ans:
                        logging.info(each_ans)
                        if re.sub(' ','', cgi.escape(str(each_ans))) == re.sub(' ','',cgi.escape(str(ans))):
                            correct_hit = True
                elif re.sub(' ','', cgi.escape(str(ans))) == re.sub(' ','',cgi.escape(str(correct_ans))): 
                    correct_hit = True

                if correct_hit == True: 
                    record_quiz_score(course, user, current_lesson, current_unit, '1')                                 
                    current_streak = get_quiz_stats(course, user, current_lesson, current_unit)[2]            
                    quiz_streak = get_quiz_streak(course, current_lesson, current_unit)
                    if current_streak >= quiz_streak:
                        increase_user_level(course, user, current_lesson, current_unit)
                    self.redirect('/course/%s/lessons?unit=%s&lesson=%s&success=good&ans=%s' % (course_name, current_unit, current_lesson, ans))
                else:
                    memcache.set(user.user_id + course_name + current_lesson + current_unit, 0)
                    record_quiz_score(course, user, current_lesson, current_unit, '0')                    
                    self.redirect('/course/%s/lessons?unit=%s&lesson=%s&success=error&ans=%s' % (course_name, current_unit, current_lesson, ans))
        
class CourseNotes(MainHandler):
    def get(self, course_name):
        @self.login_required
        def secured_things(user):
            if self.valid_course(course_name):
                course = get_course_info(course_name)
                notes = 'Notes Coming Soon'
                x = self.render('notes.html', 
                    course = course, 
                    notes_active = 'active',
                    notes = notes,
                    profile_url = profile_url(course_name, user))

class FlushCache(MainHandler):
    def get(self):
        memcache.flush_all()
        self.redirect('/')

class AddMentor(MainHandler):
    def get(self, course_name):
        @self.login_required
        def secured_things(user):
            if self.valid_course(course_name):
                course = get_course_info(course_name)
                approval = self.request.get('verify')
                if approval == 'true':
                    mentee_id = self.request.get('mentee')
                    approve_mentorship(user, course_name, mentee_id)
                    self.redirect('/course/%s/profile?tab=mentor' % course_name)
                elif approval == 'false':
                    mentee_id = self.request.get('mentee')
                    decline_mentorship(user, course_name, mentee_id)
                    self.redirect('/course/%s/profile?tab=mentor' % course_name)
                else:
                    self.render('addmentor.html', 
                        course=course,
                        profile_url = profile_url(course_name, user))

    def post(self,course_name):
        @self.login_required
        def secured_things(user):
            if self.valid_course(course_name):
                mentor_id = self.request.get('mentor_id')
                mentor_error = check_valid_mentor(user, mentor_id, course_name)
                if mentor_error is not None:
                    course=get_course_info(course_name)
                    self.render('addmentor.html', 
                        course=course,
                        profile_url = profile_url(course_name, user),
                        mentor_id = mentor_id,
                        mentor_error = mentor_error
                        )
                else:
                    create_mentor_request(mentor_id, user, course_name)
                    self.redirect('/course/%s/profile?tab=mentor' % course_name)

class Badges(MainHandler):
    def get(self, course_name):
        @self.login_required
        def secured_things(user):
            if self.valid_course(course_name):
                course = get_course_info(course_name)
                course_badges = build_badge_list(user_id = user.user_id, course_name = course_name, demo=True)
                html_to_print = course_badges
                bronze_bar = '#b97333'
                silver_bar = '#c8c8c8'
                gold_bar = '#ffcc00'
                honor_badges = ''
                honor_badges += '''
                    <tr>
                        <td>
                            <div class="ribbon pull-left" style="background-image:url('/images/ribbons/sample.png')" title="sample">
                                <img src="/images/bronzemedal.png" class="medal" style="margin-left:50px">
                            </div>           
                        </td>
                        <td>
                            <h5>Bronze Star</h5>
                            <p><small>earn the same ribbon 5 times</small></p>
                        </td>                            
                    </tr>
                    ''' 
                honor_badges += '''
                    <tr>
                        <td>
                            <div class="ribbon pull-left" style="background-image:url('/images/ribbons/sample.png')" title="sample">
                                <img src="/images/silvermedal.png" class="medal" style="margin-left:50px">
                            </div> 
                        </td>
                        <td>
                            <h5>Silver Star</h5>
                            <p><small>earn a bronze star for the same ribbon 3 times</small></p>
                        </td> 
                    </tr>
                    ''' 
                honor_badges += '''
                    <tr>
                        <td>
                            <div class="ribbon pull-left" style="background-image:url('/images/ribbons/sample.png')" title="sample">
                                <img src="/images/goldmedal.png" class="medal" style="margin-left:50px">
                            </div> 
                        </td>
                        <td>
                            <h5>Gold Star</h5>
                            <p><small>earn a silver star for the same ribbon 3 times</small></p>
                        </td> 
                    </tr>
                    ''' 

                self.render('badges.html', 
                    profile_url = profile_url(course_name, user), 
                    course = course, 
                    html_to_print=html_to_print,
                    honor_badges = honor_badges)

class About(MainHandler):
    def get(self):
        self.render('about.html')




class EditPersonalInfo(MainHandler):
    def get(self, course_name):
        @self.login_required
        def secured_things(user):
            if self.valid_course(course_name):
                personal_info = get_personal_info(str(user.user_id))
                error = self.request.get('error')
                self.render('edit_personal_info.html', 
                    profile_url = profile_url(course_name, user),
                    course = get_course_info(course_name),
                    personal_info = personal_info,
                    error = error)

    def post(self,course_name):
        @self.login_required
        def secured_things(user):
            last_name = self.request.get('last_name')
            first_name = self.request.get('first_name')
            nickname = self.request.get('nickname')
            error = ''
            if last_name == '' or last_name is None:
                error += 'Last name cannot be blank... '
            if first_name =='' or first_name is None:
                error += 'First name cannot be blank... '
            if nickname == '' or nickname is None:
                error += 'nickname cannot be blank... '

            if error != '':
                self.redirect('/course/%s/edit_personal_info?error=%s' % (course_name, error))
            else:
                edit_user_information(user.user_id, nickname, last_name, first_name)
                self.redirect('/course/%s/profile' % course_name)
            


app = webapp2.WSGIApplication([('/course/(\w+)', CourseFront),
                               ('/about', About),
                               ('/course/(\w+)/enroll', CourseEnroll),
                               ('/course/(\w+)/info', MoreInfo),
                               ('/course/(\w+)/notes', CourseNotes),
                               ('/course/(\w+)/materials', Materials),
                               ('/course/(\w+)/lessons', Lessons),
                               ('/course/(\w+)/addmentor', AddMentor),
                               ('/course/(\w+)/ribbons', Badges),
                               ('/course/(\w+)/practice', Practice),
                               ('/course/(\w+)/edit_personal_info', EditPersonalInfo),
                               ('/course/(\w+)/discussion', Discussion),
                               ('/course/(\w+)/questions/add', QuestionAdder),
                               ('/course/(\w+)/questions/(\d+)', IndividualQuestion),
                               ('/course/(\w+)/questions/(\d+)/edit', QuestionAdder),
                               ('/course/(\w+)/questions/(\d+)/(\d+)/edit', AnswerEdit),
                               ('/course/(\w+)/questions/(\d+)/vote', QuestionVote),
                               ('/course/(\w+)/questions/(\d+)/vote_remove', QuestionVoteRemove), 
                               ('/course/(\w+)/questions/(\d+)/(\d+)/vote', AnswerVote),
                               ('/course/(\w+)/questions/(\d+)/(\d+)/vote_remove', AnswerVoteRemove),
                               ('/course/(\w+)/syllabus', CourseSyllabus),
                               ('/login', LoginSignup),
                               ('/login/create', CreateUser),
                               ('/login/create_true', CreateLocalUser),
                               ('/login/existing', ExistingLogIn),
                               ('/login/existing_true', ExistingTrue),
                               ('/profile', ProfilePage),                               
                               ('/course/(\w+)/profile', ProfilePage),
                               ('/course/(\w+)/profile/(\d+)', ProfilePage),
                               ('/flush', FlushCache),                               
                               ('/.*', MainPage)],
                              debug=True)