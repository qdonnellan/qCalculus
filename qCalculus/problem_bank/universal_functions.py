import math
import re
import random
from fractions import Fraction


def short_answer(prompt):
	form_text = '''
	<label>%s</label>
    <input type="text" value = '' name = 'quiz_answer' id = "short-input">
    ''' % prompt
	return form_text

def multiple_choice(prompt,pchoices,tex=True):
	leaders = ['A','B','C','D','E','F']
	index_num = 0
	correct_answer = ''
	pchoices = sorted(pchoices, key=lambda *args: random.random()) 
	form_text = '<label class="problem-header">%s</label><br><br>' % prompt	
	for choice in pchoices:
		if '--' in choice:
			choice = re.sub('--', '+', choice)

		if tex:		
			choice = '\(\displaystyle{' + choice + '}\)'
		ping = re.search('\*\*',choice)
		if ping:
			choice = re.sub('\*\*', '', choice)
			correct_answer = choice
		form_text += '''
		<label class="radio">
			<input type="radio" name ="quiz_answer" value = '%s'> 
			<div class="pull-left" style="font-weight:bold; margin-right:10px">%s) </div> <div class="pull-left">%s</div>
		</label><br>
		''' % (choice, leaders[index_num], choice)
		
		index_num +=1
	return form_text, correct_answer

def more_than_one(prompt,pchoices,tex=True):
	pchoices = sorted(pchoices, key=lambda *args: random.random())
	form_text = '<label>%s</label>' % prompt
	
	correct_answer = ''
	for choice in pchoices:
		if tex:		
			choice = '\(\displaystyle{' + choice + '}\)'
		ping = re.search('\*\*',choice)
		if ping:
			choice = re.sub('\*\*', '', choice)
			correct_answer += choice
		form_text += '''
		<label class="checkbox">
			<input type = "checkbox" name ="quiz_answer" value = '%s' /> 
			%s
		</label> <br>
		''' % (choice, choice)
	return form_text, correct_answer

def unique_integers(num_to_get, min_integer, max_integer):
	bank = range(min_integer, max_integer)
	unique_integers = []
	for i in range(num_to_get):
		integer_chosen = random.choice(bank)
		unique_integers.append(integer_chosen)
		bank.remove(integer_chosen)
	return unique_integers

def random_function_and_slope(value_to_find_slope_at):
	x = value_to_find_slope_at
	function_bank = ['\cos(x)', '\sin(x)', 'e^{x}', '\\arctan(x)', 'x^2']
	chosen_function = random.choice(function_bank)
	if 'arctan' in chosen_function:
		slope = 1./(x**2 +1)
		function_value = math.atan(x)
	elif 'sin(x)' in chosen_function:
		slope = math.cos(x)
		function_value = math.sin(x)
	elif 'cos(x)' in chosen_function:
		slope = -(math.sin(x))
		function_value = math.cos(x)
	elif 'e^{x}' in chosen_function:
		slope = math.exp(x)
		function_value = math.exp(x)
	elif 'x^2' in chosen_function:
		slope = 2.*x
		function_value = x**2

	return chosen_function, function_value, slope

def get_random_pi_fraction():
	random_number = random.choice('02346p')
	if random_number == '0':
		return '0'
	elif random_number == 'p':
		return '\pi'
	else:
		pi_frac = '\\frac{\pi}{%s}' % random_number
		return pi_frac

def eval_trig_at_pi_fraction(myfunction, pi_frac):
	if 'cos(x)' in myfunction:
		cosine_bank = {
		'0'					: '1',
		'\\frac{\pi}{6}' 	: '\\frac{\sqrt{3}}{2}',
		'\\frac{\pi}{4}'	: '\\frac{\sqrt{2}}{2}', 
		'\\frac{\pi}{3}'	: '\\frac{1}{2}', 
		'\\frac{\pi}{2}'	: '0',
		'\pi'				: '-1'
		}
		return cosine_bank[pi_frac]
	elif 'sin(x)' in myfunction:
		sine_bank = {
		'0'					: '0',
		'\\frac{\pi}{6}' 	: '\\frac{1}{2}',
		'\\frac{\pi}{4}'	: '\\frac{\sqrt{2}}{2}', 
		'\\frac{\pi}{3}'	: '\\frac{\sqrt{3}}{2}', 
		'\\frac{\pi}{2}'	: '1',
		'\pi'				: '0'
		}
		return sine_bank[pi_frac]
	elif 'tan(x)' in myfunction and 'sec(x)tan(x)' not in myfunction:
		tan_bank = {
		'0'					: '0',
		'\\frac{\pi}{6}' 	: '\\frac{\sqrt{3}}{3}',
		'\\frac{\pi}{4}'	: '1', 
		'\\frac{\pi}{3}'	: '\sqrt{3}', 
		'\\frac{\pi}{2}'	: 'undefined',
		'\pi'				: '0'
		}
		return tan_bank[pi_frac]
	elif 'sec(x)' in myfunction and 'sec(x)tan(x)' not in myfunction:
		sec_bank = {
		'0'					: '1',
		'\\frac{\pi}{6}' 	: '\\frac{2\sqrt{3}}{3}',
		'\\frac{\pi}{4}'	: '\sqrt{2}', 
		'\\frac{\pi}{3}'	: '2', 
		'\\frac{\pi}{2}'	: 'undefined',
		'\pi'				: '-1'
		}
		return sec_bank[pi_frac]
	elif 'sec^2(x)' in myfunction:
		sec2_bank = {
		'0'					: '1',
		'\\frac{\pi}{6}' 	: '\\frac{4}{3}',
		'\\frac{\pi}{4}'	: '2', 
		'\\frac{\pi}{3}'	: '4', 
		'\\frac{\pi}{2}'	: 'undefined',
		'\pi'				: '1'
		}
		return sec2_bank[pi_frac]
	elif 'sec(x)tan(x)' in myfunction:
		sectan_bank = {
		'0'					: '0',
		'\\frac{\pi}{6}' 	: '\\frac{2}{3}',
		'\\frac{\pi}{4}'	: '\sqrt{2}', 
		'\\frac{\pi}{3}'	: '2\sqrt{3}', 
		'\\frac{\pi}{2}'	: 'undefined',
		'\pi'				: '0'
		}

def random_arctan_derivative():
	numerator = random.randint(0,6)
	denominator = random.randint(1,6)
	if numerator == 0:
		xvalue = 0
		solution = 1
	else:
		xvalue = Fraction(numerator,denominator)
		sol_numerator = denominator**2
		sol_denominator = numerator**2 + denominator**2
		solution = Fraction(sol_numerator, sol_denominator)

	solution = str(solution)
	if '/' in solution:
		numerator, denominator = solution.split('/')
		latex_solution = '\\frac{%s}{%s}' % (numerator, denominator)
	else:
		latex_solution = solution

	if '/' in str(xvalue):
		numerator, denominator = str(xvalue).split('/')
		xvalue = '\\frac{%s}{%s}' % (numerator, denominator)
	return latex_solution, str(xvalue)


def simple_random_trig_derivative(forced_function = None):
	if forced_function is not None:
		function_bank = [forced_function]
	else:
		function_bank = ['\cos(x)', '\sin(x)', r'\\tan(x)', '\sec(x)']
	pi_fraction_bank = ['0', '\\frac{\pi}{6}','\\frac{\pi}{4}','\\frac{\pi}{3}','\\frac{\pi}{2}', '\pi' ]
	xval = random.choice(pi_fraction_bank)
	chosen_function = random.choice(function_bank)
	if 'cos(x)' in chosen_function:
		derivative = eval_trig_at_pi_fraction('sin(x)',xval)
		derivative = '-' + derivative
	elif 'sin(x)' in chosen_function:
		derivative = eval_trig_at_pi_fraction('cos(x)',xval)
	elif 'tan(x)' and not 'arctan(x)' in chosen_function:
		derivative = eval_trig_at_pi_fraction('sec^2(x)', xval)
	elif 'sec(x)' in chosen_function:
		derivative = eval_trig_at_pi_fraction('sec(x)tan(x)', xval)
	else:
		return 'Something went wrong setting this problem...'

	derivative = re.sub('-0', '0', derivative)
	derivative = re.sub('--', '+', derivative)
	if derivative[0] =='+':
		derivative = re.sub('+', '', derivative, 1)

	return chosen_function, xval, derivative

def random_latex_poly(highest_order):
	poly_coefficients = []
	for i in range(highest_order):
		poly_coefficients.append(random.randint(-5,5))
	return latex_polynomial(poly_coefficients)


def latex_polynomial(poly_coefficients):
	num_terms = len(poly_coefficients)
	power_list = range(num_terms)
	power_list.reverse()
	latex_poly = ''
	for power in range(num_terms):
		current_power = power_list[power]
		current_coefficient = poly_coefficients[power]
		if current_coefficient != 0:
			if latex_poly != '':
				latex_poly += '+'
			if current_power == 1:
				latex_poly += '%sx' % current_coefficient
			elif current_power == 0:
				latex_poly += str(current_coefficient)
			else:
				latex_poly += '%sx^{%s}' % (current_coefficient, current_power)

	latex_poly = re.sub('[+][-]','-', latex_poly)
	latex_poly = re.sub('[+][+]','+', latex_poly)
	latex_poly = re.sub('1x','x', latex_poly)
	

	return latex_poly


def polynomial_derivative(poly_coefficients, xvalue = None):
	num_terms = len(poly_coefficients)-1	
	power_list = range(num_terms)
	power_list.reverse()
	new_coefficients = []
	latex_poly = ''
	if xvalue is not None:
		result = 0
	else:
		result = None
	for power in range(num_terms):
		current_power = power_list[power]
		new_coefficient = poly_coefficients[power] * (current_power+1)
		new_coefficients.append(new_coefficient)
		if xvalue is not None:
			result += new_coefficient*(xvalue**current_power)
	
	original_poly = latex_polynomial(poly_coefficients)
	derivative_poly = latex_polynomial(new_coefficients)			

	return original_poly, derivative_poly, result
		





