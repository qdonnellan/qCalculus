from loclin import *
from limits import *
from slope import *
from tangentline import *
from derivative import *
import logging

def get_problem(problem_name):
	if 'loclin' in problem_name:
		return loclin(problem_name)
	elif 'lim' in problem_name:
		return limits(problem_name)
	elif 'slope' in problem_name:
		return slope(problem_name)
	elif 'tangent' in problem_name:
		return tangent(problem_name)
	elif 'derivative' in problem_name:
		return derivative(problem_name)

def problem_map(course_name, problem_number_list):
	compiled_problems = ''
	answer_bank = ''
	problem_list = []
	problem_number = 1
	if course_name == 'cal101':
		if problem_number_list[0] > 0:
			#Unit 1 Problems
			unit_questions = ['lim104*', 'lim108*', 'lim109*', 'lim111*']
			problem_list.extend(populate_questions(unit_questions, problem_number_list[0]))
		if problem_number_list[1] > 0:
			#Unit 2 Problems
			unit_questions = ['lim122*', 'lim124*', 'lim125*', 'lim126*', 'lim127*', 'lim128*', 'lim129*', 'lim130']
			problem_list.extend(populate_questions(unit_questions, problem_number_list[1]))
			

	random.shuffle(problem_list)
	for problem in problem_list:
		problem_text, answer = format_test_problem(problem, problem_number)
		compiled_problems += problem_text
		answer_bank += 'Problem %s : %s <br><br>' % (problem_number, answer)
		if problem_number%2 == 0:
			compiled_problems += '<div style="width:8in; border-bottom:1px solid #ccc; float:left"></div><br><br>'
		problem_number +=1

	return compiled_problems, answer_bank

def populate_questions(possible_question_list,num_to_get):
	#In possible_question_list, denote unique problems with *
	problems_to_return = []
	for i in range(num_to_get):
		choice = random.choice(possible_question_list)
		if '*' in choice:
			possible_question_list.remove(choice)
			choice = re.sub('[*]', '', choice)
		problems_to_return.append(choice)
	return problems_to_return



def format_test_problem(problem_name, problem_number):
		problem_text, answer = get_problem(problem_name)
		problem_text = re.sub(r'type="radio"', 'style="display:none"', problem_text)
		problem_text = re.sub(r'class="radio"', 'style="float:left; margin:10px; height:40px; margin-top:0px;"', problem_text)
		problem_text = re.sub(r'</label><br>', '</label>', problem_text)
		problem_text = re.sub('class="problem-header"', '', problem_text)
		problem_text = re.sub('class="pull-left" style="', 'style="float:left;', problem_text)
		problem_text = re.sub('class="pull-left"', 'style="float:left"', problem_text)
		problem_text = '''
		<div style= "page-break-inside:avoid; width:3.5in; margin-right:0.5in; float:left">
		<br>
			<span style="font-weight:bold">Problem %s:</span>
			 %s 
			<div class="page-header">
			</div>
		</div>
		''' % (problem_number, problem_text)
		return problem_text, answer

