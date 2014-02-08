from handlers import MainHandler
from dbops import *
from courses import *
import logging
from problem_bank.main import problem_map

def get_available_user_units(user, course):
	user_level = get_user_level(course.name, user.user_id)
	unit_count = 0
	level = 0                
	for unit in course.units:
		construction_alert = ''
		for lesson in unit.lessons:
			if lesson.quiz is not None:
				level += 1
			if 'under_construction' in lesson.title:
				construction_alert += 'T'
		if user_level >= level and construction_alert == '':
			unit_count += 1
	return unit_count


class Practice(MainHandler):
    def get(self, course_name):
        @self.login_required
        def secured_things(user):
            if self.valid_course(course_name):
            	error = self.request.get('error')
            	if error != '':
            		error_alert = '''
            		<div class="alert alert-error">
		                <a class="close" data-dismiss="alert" href="/course/%s/practice">&times;</a>
		                <h4 class="alert-heading">Oh snap!</h4>
		                %s ... 
		            </div>
            		''' % (course_name, error)
            	else:
            		error_alert = ''
                course = get_course_info(course_name)
                unit_count = get_available_user_units(user, course)
            	html_to_print = '<h3>You have completed these units<small> unlock more units in the "lessons" tab above</small></h3> <br>'
            	for i in range(unit_count):
            		unit_title = course.units[i].title
            		html_to_print += unit_title + '<br>'

            	html_to_print += '<br> <h3>Tell us what to generate <small> pick problems from completed units</small></h3>'

            	generate_questions_block = ''
            	for i in range(unit_count):
            		label = '<label>Number of practice problems from Unit %s</label>' % (i+1)
            		input_block = '<input type="text" name = "unit%sproblems" value = "">' % (i+1)
            		generate_questions_block += label  + input_block + '<br>'

                self.render('generate_practice.html', 
                	profile_url = profile_url(user), 
                	course=course,
                	html_to_print = html_to_print,
                	error_alert = error_alert,
                	form_text = generate_questions_block)

    def post(self, course_name):
        @self.login_required
        def secured_things(user):
            if self.valid_course(course_name):
            	course = get_course_info(course_name)
            	unit_count = get_available_user_units(user, course)
            	html_to_print = ''
            	error = ''
            	number_of_problems = []
            	for i in range(unit_count):
            		problems = self.request.get('unit%sproblems' % (i+1))
            		if problems == '' or problems is None:
            			problems = '0'
            		if not problems.isdigit():
            			error = 'Only use integer numbers to specify how many questions you want'
            		else:
            			number_of_problems.append(int(problems))
            	if error != '':
            		self.redirect('/course/%s/practice?error=%s' % (course.name, error))
            	else: 
            		fetched_problems, answer_bank = problem_map(course_name, number_of_problems)
            		html_to_print += fetched_problems
	            	self.render('generated_test.html',
	            		profile_url = profile_url(user), 
	                	course=course,
	                	html_to_print = html_to_print,
                        answer_bank = answer_bank)
