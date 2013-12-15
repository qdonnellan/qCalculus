from dbops import *
import re
from courses import *

badge_bank = {
	'supporter' : 'Answer at least 1 question on the discussion board',
	'student' : 'Ask at least 1 question on the discussion board',
	'good_question' : 'One of your questions has a score of 5 or more',
	'great_question' : 'One of your questions has a score of 20 or more',
	'epic_question' : 'One of your questions has a score of 100 or more',
	#'legendary_question' : 'One of your questions has a score of 500 or more',
	'good_answer' : 'One of your answers has a score of 5 or more',
	'great_answer' : 'One of your answers has a score of 20 or more',
	'epic_answer' : 'One of your answers has a score of 100 or more',
	#'legendary_answer' : 'One of your answers has a score of 500 or more',
	'novice' : 'reach quiz level 5',
	'quiz_streak_10' : 'achieve a streak of 10 or more on a quiz',
	'quiz_streak_20' : 'achieve a streak of 20 or more on a quiz'
}

def add_badge(badge_name, number_of_badges, badges):
	badges[badge_name] = badge_bank[badge_name]
	number_of_honors = int(number_of_badges/5)
	if number_of_honors >= 1:
		#one * is appended to the end of the badge name for every 5 badges earned
		badges[badge_name] += '*'*number_of_honors
	return badges

def check_badges(user_id, course_name):
	answers = get_answers_by_user_id(user_id = user_id, course_name = course_name)
	questions = get_questions_by_user_id(user_id = user_id, course_name = course_name)
	badges = {}
	if answers is not None:
		num_ans = 0
		num_good_answers = 0
		num_great_answers = 0
		num_epic_answers = 0
		num_legendary_answers = 0
		for ans in answers:
			num_ans+=1
			score = get_answer_score(ans.key().id(), ans.question, course_name)
			if score >= 5:
				num_good_answers +=1
			if score >= 20:
				num_great_answers += 1
			if score >= 100:
				num_epic_answers += 1
			if score >= 500:
				num_legendary_answers += 1

		if num_good_answers >0:
			badges = add_badge('good_answer', num_good_answers, badges)

		if num_great_answers >0:
			badges = add_badge('great_answer', num_great_answers, badges)

		if num_epic_answers >0:
			badges = add_badge('epic_answer', num_epic_answers, badges)

		if num_legendary_answers >0:
			badges = add_badge('legendary_answer', num_legendary_questions, badges)

		if num_ans >0:
			badges = add_badge('supporter', num_ans, badges)




	if questions is not None:
		num_q = 0
		num_good_questions = 0
		num_great_questions = 0
		num_epic_questions = 0
		num_legendary_questions = 0
		for q in questions:
			num_q += 1			
			score = get_question_score(q.key().id(), course_name)
			if score >= 5:
				num_good_questions +=1
			if score >= 20:
				num_great_questions += 1
			if score >= 100:
				num_epic_questions += 1
			if score >= 500:
				num_legendary_questions += 1

		if num_q >0:
			badges = add_badge('student', num_q, badges)

		if num_good_questions >0:
			badges = add_badge('good_question', num_good_questions, badges)

		if num_great_questions >0:
			badges = add_badge('great_question', num_great_questions, badges)

		if num_epic_questions >0:
			badges = add_badge('epic_question', num_epic_questions, badges)

		if num_legendary_questions >0:
			badges = add_badge('legendary_question', num_legendary_questions, badges)

	user_level = get_user_level(course_name, user_id)
	if user_level >= 5:
		badges = add_badge('novice', 1, badges)


	course = get_course_info(course_name)
	unit_level = 0
	ten_streak = 0
	twen_streak = 0
	for unit in course.units:
		unit_level += 1
		if user_level >= unit_level:
			for lesson in unit.lessons:
				if lesson.quiz is not None:
					longest_streak = get_longest_streak(course_name, lesson.title, unit.title, user_id)
					if longest_streak >= 10:
						ten_streak += 1
					if longest_streak >= 20:
						twen_streak += 1
	if ten_streak > 0:
		badges = add_badge('quiz_streak_10', ten_streak, badges)
	if twen_streak > 0:
		badges = add_badge('quiz_streak_20', twen_streak, badges)




	return badges

def add_honor_bar(honor_bar_color):
	honor_bar_html = '''
		<button class="btn" style="width:5px; background:%s; color:%s; padding-left:5px; padding-right:5px"></button>
	''' % (honor_bar_color, honor_bar_color)
	return honor_bar_html


def build_badge_list(user_id=None, course_name=None, demo=False):
	if demo is False:
		badges = check_badges(user_id, course_name)
	else:
		badges = badge_bank
		user_badges = check_badges(user_id, course_name)
	html_to_print = ''
	for i in badges:		
		tooltip = badges[i]
		honor_bar = ''
		honors = re.findall('\*',tooltip)
		num_honors = len(honors)
		bronze_bar = '#b97333'
		silver_bar = '#c8c8c8'
		gold_bar = '#ffcc00'
		medals=''
		if num_honors == 1:
			medals = '<img src="/images/bronzemedal.png" class="medal" style="margin-left:50px">'
		elif num_honors == 2:
			medals = '<img src="/images/bronzemedal.png" class="medal" style="margin-left:38px"><img src="/images/bronzemedal.png" class="medal" style="margin-left:5px">'
		elif num_honors == 3:
			medals = '<img src="/images/silvermedal.png" class="medal" style="margin-left:50px">'
		elif num_honors == 4:
			medals = '<img src="/images/silvermedal.png" class="medal" style="margin-left:38px"><img src="/images/silvermedal.png" class="medal" style="margin-left:5px">'
		elif num_honors == 5:
			medals = '<img src="/images/goldmedal.png" class="medal" style="margin-left:50px">'
		elif num_honors >= 6:
			medals = '<img src="/images/goldmedal.png" class="medal" style="margin-left:38px"><img src="/images/goldmedal.png" class="medal" style="margin-left:5px">'

		tooltip = re.sub('\*', '', tooltip)

		
		if demo is False:		
			html_to_print += '''
			<div class="ribbon pull-left" style="background-image:url('/images/ribbons/%s.png')" title="%s: %s">%s</div>
			''' % (i,re.sub('_',' ',i), tooltip, medals)
		else:
			badge_earned = ''
			if i in user_badges:
				badge_earned="<span class='label label-success'>earned</span>"

			html_to_print += '''
			<tr>
				<td>
					<div class="ribbon pull-left" style="background-image:url('/images/ribbons/%s.png')" title="%s"></div>
				</td>
				<td>
					<h5>%s<small> %s</small></h5>
					<p><small>%s</small></p>
				</td>
			</tr>
			''' % (i,re.sub('_',' ',i),re.sub('_',' ',i).title(),badge_earned, tooltip)


	return html_to_print



