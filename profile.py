from handlers import MainHandler
from dbops import *
from badges import *
from build_question_list import *
import cgi
from courses import *
import re
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import db
import logging
from operator import itemgetter, attrgetter

class ProfilePage(MainHandler):    
    def get(self, coursename = None, other_user=None):
        @self.login_required
        def secured_things(user):
            course_name = coursename
            courses = user.courses
            num_next_page_questions = 0
            html_to_print = ''
            lesson_content = ''
            badge_list = ''
            course_links = ''
            if courses:
                courses = courses.split('|')
                for course in courses:
                    if course != '':
                        clink = '/course/%s/profile' % course
                        course_links += '<a class="btn" href=%s>%s</a>' % (clink, course)

            if course_name is None and courses is None or courses =='':
                banner = '''
                    <h2>You are not enrolled in any courses</h2>
                    <a class="btn btn-primary" href="/courses">Enroll in a course now!</a>
                '''
                self.render('empty_profile.html', banner=banner)
            elif course_name is None and courses is not None:
                banner = '''
                    <div class="page-header">
                        <h2>Your Courses
                            <small>Choose one to view your profile in that class</small>
                        </h2>
                        
                    </div>
                '''
                self.render('empty_profile.html', banner = banner, choices = course_links)
            else:        
                if self.valid_course(course_name):
                    if other_user and str(other_user) != str(user.user_id):
                        user_id = other_user
                        who_did = str(get_user_nickname(user_id))
                        nickname = get_user_nickname(user_id) + "'s"
                        protected =  'hidden'
                        profile_active = ''
                        my_student = is_this_my_student(mentee_id = user_id, user=user, course_name = course_name)
                        
                    else:
                        user_id = user.user_id
                        who_did = "You've" 
                        nickname = 'Your'
                        protected = ''
                        profile_active = 'active'
                        my_student = False
                              
                    badge_list = build_badge_list(user_id, course_name)

                    page = self.request.get('page')
                    tab = self.request.get('tab')
                    if tab is None or tab == '':
                        if protected is 'hidden':
                            tab = 'stats'
                        else:
                            tab = 'stats'
                    press = self.request.get('press')
                    sort_method = self.request.get('sort_method')
                    if sort_method is None or sort_method == '':
                        sort_method = "last_modified"

                    if page is None or page == '' or press =='just_then':
                        page = 1;   

                    if course_name is None:
                        course_name = 'cal101'
                    decor = tab_decor()                    
                    if tab == 'answers':
                        decor.answers = 'active'
                        user_answers = get_answers_by_user_id(user_id, course_name)
                        html_to_print = ''
                        count = 0
                        num_per_page = 5
                        page = int(page)
                        for ans in user_answers:
                            count+=1

                        if sort_method =='last_modified':
                            user_answers = sorted(user_answers, key = attrgetter(sort_method), reverse = True)
                        elif sort_method == 'score':
                            temp_tuple = []
                            for ans in user_answers:
                                temp_tuple.append([
                                    ans,
                                    get_answer_score(answer_id = str(ans.key().id()), question_id = str(ans.question), course_name = course_name)
                                    ])
                            temp_tuple = sorted(temp_tuple, key = itemgetter(1), reverse = True)
                            user_answers = []
                            for ans in temp_tuple:
                                user_answers.append(ans[0])

                        user_answers = user_answers[num_per_page*(page-1):num_per_page*page]
                        num_next_page_questions = count - (num_per_page*page)
                        logging.info(str(num_next_page_questions)+'answers leftover')


                        for ans in user_answers:                    
                            question = get_question_by_id(ans.question, course_name)
                            score = get_answer_score(answer_id = str(ans.key().id()), question_id = str(ans.question), course_name = course_name)
                            last_time = get_time_ago_string(ans.last_modified)
                            leader_text = ans.body[0:30] + '...'
                            html_to_print += '''             
                                <tr>     
                                    <td class = "hidden-phone" style="width:50px;">
                                        <div class="btn-group ">
                                            <button class="btn disabled btn-mini ">
                                                <h3>%s</h3>
                                                <p>score</p>                            
                                            </button>                            
                                        </div>
                                    </td>
                                    <td>
                                        <div>
                                            <a href = "/course/%s/questions/%d">
                                                <p class="question-leader"><span class="answer-lead">In question:</span> %s</p>
                                            </a>
                                            <p class="answer-body pull-left">%s</p>
                                            <div class="btn-group pull-left visible-phone" style="margin-right:2px" >
                                                <button class="btn disabled btn-mini" >score: %s</button>
                                            </div>
                                            <span class="pull-right">%s, %s</span>
                                        </div>  
                                    </td>
                                </tr>                        
                                ''' % ( 
                                       score, course_name,
                                       question.key().id(),        
                                       cgi.escape(question.title),
                                       leader_text,
                                       score, 
                                       last_time, get_user_nickname(user_id)           
                                       )
                        html_to_print = "<h3>%s answered %s questions</h3>" % (who_did,str(count)) + html_to_print

                    elif tab == 'votes':
                        qups,qdowns,aups,adowns = get_user_vote_counts(user_id, course_name)
                        total_votes = qups+qdowns+aups+adowns
                        html_to_print = "<h3>%s voted %s times</h3>" % (who_did,total_votes)
                        vote_info = '''
                            <div class="vote-count-block">
                                <h6>Questions</h6>
                                <button class="btn disabled pull-left vote-count" >            
                                    <span style="font-size:20pt">+</span>            
                                </button><p class="pull-left">%s</p>
                                <button class="btn disabled pull-left vote-count" >            
                                    <span style="font-size:20pt">-</span>            
                                </button><p class="pull-left">%s</p>
                                <br> <br> <br>
                                <h6>Answers</h6>
                                <button class="btn disabled pull-left vote-count" >            
                                    <span style="font-size:20pt">+</span>            
                                </button><p class="pull-left"> %s</p> 
                                <button class="btn disabled pull-left vote-count">            
                                    <span style="font-size:20pt">-</span>            
                                </button><p class="pull-left">%s</p>
                            </div>
                        ''' % (qups,qdowns,aups,adowns)
                        html_to_print = html_to_print + vote_info
                        num_next_page_questions = 0
                        decor.votes = 'active'
                        
                    elif tab == 'questions':
                        decor.questions = 'active'
                        questions_html, num_next_page_questions = build_question_list(
                            page = int(page), 
                            user_id = user_id, 
                            num_to_get = 5,
                            sort_method = sort_method,
                            course_name = course_name)
                        count = get_question_count_by_user_id(user_id, course_name)
                        html_to_print = "<h3>%s asked %s questions</h3>" % (who_did,str(count)) + questions_html                    

                    elif tab == 'stats':
                        decor.stats = 'active'
                        personal_info = get_personal_info(str(user_id))
                        d_rep = get_discussion_reputation(course_name, user_id)
                        q_score = get_user_level(user_id = user_id, course_name = course_name)
                        edit_link = ''
                        if protected != 'hidden':
                            edit_link = '''
                            <a class = "btn btn-info" href = "/course/%s/edit_personal_info">
                                <h5><i class="icon-pencil icon-white"></i> change personal information</h5>
                            </a>
                            <br> <br>
                            ''' % course_name

                        html_to_print = '''
                            <div class="page-header">
                                <h2>Personal Information</h2>
                            </div>
                            <div class="row-fluid">
                                <div class="span4">
                                    <p><small>First name: </small>%s</p>
                                    <p><small>Last name: </small>%s</p>
                                    <p><small>Nickname: </small>%s</p>
                                    %s
                                </div>
                                <div class="span8">
                                    <div class="row-fluid">
                                        <ul class="thumbnails">
                                            <li class="span4">
                                                <div class="thumbnail">
                                                    <div class="big-stat-number">%s</div>  
                                                    <button class="btn disabled btn-small row-fluid">discussion reputation</button>                                              
                                                </div>
                                            </li>
                                            <li class="span4">
                                                <div class="thumbnail">
                                                    <div class="big-stat-number">%s</div>  
                                                    <button class="btn btn-small disabled row-fluid">quiz level</button>                                              
                                                </div>
                                            </li>
                                            <li class="span4">
                                                <div class="thumbnail">
                                                    <div class="big-stat-number">%s</div>  
                                                    <button class="btn btn-small disabled row-fluid">overall rating</button>                                              
                                                </div>
                                            </li>                                           
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        ''' % (
                            personal_info.first_name, 
                            personal_info.last_name, 
                            personal_info.nickname,
                            edit_link, 
                            d_rep, 
                            q_score,
                            d_rep+q_score)

                        html_to_print += '''
                            <div class="page-header">
                                <h2>Ribbons earned</h2>
                            </div>
                            <div class="row-fluid">%s</div>
                            <br>
                            <br>
                            <div>
                            <a class="btn btn-info" href="/course/%s/ribbons">
                                <h5><i class="icon-question-sign icon-white"></i> learn more about ribbons</h5>
                            </a>
                            </div>
                        ''' % (badge_list, course_name)

                    elif tab =='mentor' and protected != 'hidden':
                        decor.mentor = 'active'
                        my_mentors = get_my_mentors(user_id, course_name)
                        mentor_list = ''
                        for mentor in my_mentors:
                            mentor_user, mentor_status = mentor[0], mentor[1]
                            status_pending = ''
                            if mentor_status == 'pending':
                                status_pending = '<span class="label label-warning">pending</span>'
                            mentor_list += '%s %s, ' % (mentor_user.nickname, status_pending)    

                        if mentor_list == '':
                            mentor_list += "You have not assigned a mentor for this course yet"


                        html_to_print = '''                        
                        <div class="page-header">
                            <h2>Your mentors<small> let someone else track your %s journey</small></h2>
                        </div>
                        %s <br><br>
                        <a class="btn btn-primary" href="/course/%s/addmentor">add mentor</a>
                        <br><br>
                        <div class="row-fluid">
                            <div class="page-header span8">
                                <h2 id="student-list">Your students
                                    <small> track the progress of your students</small>
                                </h2>
                                <h4><small>Share your mentor id with your students to they can add you as a mentor!</small></h4> 
                            </div>
                            <div class="span4">
                                <ul class="thumbnails">
                                    <li class="span12">
                                        <div class="thumbnail">
                                            <div class="mentor-number">%s</div>  
                                            <button class="btn btn-info disabled row-fluid">Your Mentor ID</button>                                                                           
                                        </div>
                                    </li>                                 
                                </ul>
                            </div>
                            <h4><small>Click on column heading to sort list by that column</small></h4> 
                        </div> 

                        ''' % (course_name.upper(), mentor_list, course_name, get_mentor_id(user_id))
                        students = get_students(user,course_name)                        
                        student_count = 0
                        student_sort_param = self.request.get('student_sort')
                        student_dict_list = build_student_info_list(students, course_name, student_sort_param)
                        student_list = ''    
                        for student in student_dict_list:
                            student_count += 1                            
                            if student['status'] == 'active':                                
                                
                                student_list += '''
                                    <tr>
                                        <td><a href='/course/%s/profile/%s'>%s</a></td>
                                        <td>%s</td>
                                        <td>%s</td>
                                        <td>%s</td>
                                        <td>%s</td>
                                        <td>%s</td>
                                    </tr>
                                ''' %(
                                    course_name, student['id'], student['nickname'],
                                    student['full_name'],
                                    student['discussion_rep'], 
                                    student['level'], 
                                    student['question_count'], 
                                    student['answer_count']
                                    )

                            else:
                                student_list += '''
                                    <tr>
                                        <td>%s</td>
                                        <td>
                                            <a class="btn btn-success" href="/course/%s/addmentor?verify=true&mentee=%s">
                                                approve request
                                            </a>
                                        </td>
                                        <td>
                                            <a class="btn btn-danger" href="/course/%s/addmentor?verify=false&mentee=%s">
                                                deny request
                                            </a>
                                        </td>
                                        <td> </td>
                                        <td> </td>
                                        <td> </td>
                                    </tr>
                                '''% (student['nickname'],course_name, student['id'], course_name, student['id'])

                        student_table = '''
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th><a href='/course/cnamehere/profile?tab=mentor&student_sort=nickname#student-list'>Nickname</a></th>
                                        <th><a href='/course/cnamehere/profile?tab=mentor&student_sort=full_name#student-list'>Full Name</a></th>
                                        <th><a href='/course/cnamehere/profile?tab=mentor&student_sort=discusison_rep#student-list'>Discussion Rep.</a></th>
                                        <th><a href='/course/cnamehere/profile?tab=mentor&student_sort=level#student-list'>Quiz Level</a></th>
                                        <th><a href='/course/cnamehere/profile?tab=mentor&student_sort=question_count#student-list'>Questions</a></th>
                                        <th><a href='/course/cnamehere/profile?tab=mentor&student_sort=answer_count#student-list'>Answers</a></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    %s
                                </tbody>
                            </table>
                        ''' % student_list
                        student_table = re.sub('cnamehere', course_name, student_table)
                        html_to_print += student_table

                    

                    elif tab =='quizzes' and protected != 'hidden':# or my_student):
                        user_level = get_user_level(course_name, str(user.user_id))
                        course = get_course_info(course_name)
                        html_to_print = '<ul class="nav nav-list span6">'
                        level = 1 
                        previous_unit_levels = 0 
                        for unit in course.units:                            
                            if user_level >= level:                                
                                levels_this_unit = 0
                                user_level_this_unit = user_level - previous_unit_levels - 1
                                for lesson in unit.lessons:
                                    if lesson.quiz is not None:
                                        levels_this_unit +=1 
                                if user_level_this_unit > levels_this_unit:
                                    user_level_this_unit = levels_this_unit   
                                if levels_this_unit == 0:
                                    percent_done = '0%'
                                else:                                    
                                    percent_done = str(1. * user_level_this_unit / levels_this_unit * 100) + r'%'
                                html_to_print +='''
                                <br>
                                <li class="nav-header">%s (%s of %s complete)</li>
                                <div> 
                                    <div class="progress progress-striped progress info active">  
                                        <div class="bar" style="width: %s;"></div>
                                    </div>
                                </div>

                                ''' % (unit.title,user_level_this_unit,levels_this_unit,percent_done)
                                for lesson in unit.lessons:
                                    if user_level > level: 
                                        if lesson.quiz is not None:
                                            last_so_many_quizzes = 5
                                            qscore,qattempts,streak = get_quiz_stats(course, user, lesson.title, unit.title,last_so_many_quizzes)
                                            longest_streak = get_longest_streak(course.name, lesson.title, unit.title, user.user_id)
                                            if qattempts == 0:                                        
                                                qpercent = '0%'
                                            else:
                                                qpercent = str(int(1.*qscore/qattempts * 100)) + '%'

                                            if qpercent == '100%' and qattempts == last_so_many_quizzes:
                                                great_job_label = 'excellent!'                
                                            else:
                                                great_job_label = '' 

                                            html_to_print += '''
                                            <li><a href="/course/%s/lessons?unit=%s&lesson=%s">                                                
                                                    <span class="badge badge-success" style="margin-right:10px">
                                                        <i class="icon-ok icon-white"></i> %s
                                                    </span>%s
                                                <h6>last %s attempts: %s/%s (%s) longest streak: %s</h6>
                                                </a>
                                            </li>
                                            ''' % (course.name, unit.title, lesson.title, great_job_label, lesson.title, last_so_many_quizzes, qscore, qattempts, qpercent, longest_streak)                                       
                                    elif user_level == level:
                                        if lesson.quiz is not None:
                                            html_to_print += '''
                                            <li><a href="/course/%s/lessons?unit=%s&lesson=%s">                                                
                                                    <span class="badge badge-warning" style="margin-right:10px">
                                                        <i class="icon-pencil icon-white"></i>
                                                    </span> %s
                                                    <h6>Pass this quiz to unlock more lessons</h6>                                                    
                                                </a>

                                            </li>
                                            ''' % (course.name, unit.title, lesson.title, lesson.title)
                                    if lesson.quiz is not None:
                                        level += 1
                                previous_unit_levels += levels_this_unit                       


                        html_to_print += '</ul>'      
                        decor.quizzes = 'active'

                    additional_query = ''
                    if page is not None and page != '':
                        additional_query += '&page=%s' % page

                    prev_page_class, next_page_class = "",""            
                    prev_page = 'href="/course/%s/profile/%d?page=%s&tab=%s&sort_method=%s"' % (course_name, int(user_id),(int(page)-1), tab, sort_method)
                    if (int(page)-1) <= 0:
                        #previous page is page 0?
                        prev_page_class = "disabled"
                        prev_page = ''
                    next_page = 'href="/course/%s/profile/%d?page=%s&tab=%s&sort_method=%s"' % (course_name, int(user_id),(int(page)+1),tab, sort_method)
                    if num_next_page_questions <= 0 :
                        #there are no questions on the next page...
                        next_page_class = "disabled"
                        next_page = ''

                    if tab =='answers' or tab == 'questions' or tab is None or tab == '':
                        footer = '''
                            <div class = "row-fluid">
                                <ul class="pager">
                                    <li class="previous %s">
                                        <a %s >&larr; Previous 5</a>
                                    </li>
                                    <li class="next %s">
                                        <a %s >Next 5 &rarr;</a>
                                    </li>
                                </ul>   
                            </div>
                            ''' % (prev_page_class, prev_page, next_page_class, next_page)

                        sort_tabs = '''
                            <div class = "row-fluid">
                                <ul class="pager pull-left">
                                    <li>
                                        <a href="/course/%s/profile/%d?tab=%s&press=just_then&sort_method=last_modified&%s">Last Modified</a>
                                    </li>
                                    <li>
                                        <a href="/course/%s/profile/%d?tab=%s&press=just_then&sort_method=score&%s">Score</a>
                                    </li>
                                </ul>   
                            </div>
                            ''' % (
                                    course_name,
                                    int(user_id),
                                    tab,
                                    additional_query,
                                    course_name,
                                    int(user_id),
                                    tab,
                                    additional_query)
                    else:
                        footer, sort_tabs = '',''

                    mentor_protection = protected

                    if my_student:
                        quiz_protection = ''
                    else:
                        quiz_protection = protected

                    self.render('profile.html',                         
                                nickname = nickname,
                                html_to_print = html_to_print,
                                footer = footer,
                                decor = decor,
                                additional_query = additional_query,                                
                                tab = tab,
                                sort_tabs = sort_tabs,
                                sort_method = sort_method,
                                user_id = int(user_id),
                                profile_url = profile_url(course_name, user),
                                course = get_course_info(course_name),
                                profile_active = profile_active,
                                quiz_tab_visible = quiz_protection,
                                mentor_tab_visible = mentor_protection,
                                badge_list = badge_list) 