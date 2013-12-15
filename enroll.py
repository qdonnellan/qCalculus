from dbops import *

class enroll():
	def __init__(self, user = None):
		current_course_list = ['cal101', 'cal102']
		if user is None:
			for course in current_course_list:
				exec 'self.%slink="/login"' % course
				exec 'self.%smsg="Log in to Enroll"' % course

		else:
			for course in current_course_list:
				if check_enrollment(user, course):
					exec 'self.%slink="/course/%s"' % (course, course)
					exec 'self.%smsg="Go to Class"' % course
				else:
					exec 'self.%slink="/course/%s/enroll"' % (course, course)
					exec 'self.%smsg="Enroll"' % course


def check_enrollment(user, course_name):
	enrollment = False
	if user is not None:
		user_id = user.user_id		
		courses = user.courses
		if courses is None:
			q = MyOwnUsers.all()
			q.filter('user_id = ', user_id)
			result = q.get()
			courses = result.courses
			if courses is None:
				enrollment = False

		if courses:
			courses = courses.split('|')
			for course in courses:
				if course == course_name:
					enrollment = True
	return enrollment

def new_enrollment(user,course_name):
	current_enrollment = check_enrollment(user, course_name)
	if not current_enrollment:
		if user.courses is None:
			user.courses = course_name + '|'
		else:
			user.courses += course_name + '|'

		if user.levels is None:
			user.levels = course_name + 'level' + '1' + '|'
		else:
			user.levels += course_name + 'level' + '1' + '|'
		user.put()
		memcache.set('user' + str(user.user_id), user)

