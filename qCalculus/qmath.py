import random
import re 
import logging
import math

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
	form_text = '<label>%s</label>' % prompt
	
	for choice in pchoices:
		if tex:		
			choice = '\(\displaystyle{' + choice + '}\)'
		ping = re.search('\*\*',choice)
		if ping:
			choice = re.sub('\*\*', '', choice)
			correct_answer = choice
		form_text += '''
		<label class="radio">
			<input type = "radio" name ="quiz_answer" value = '%s'> 
			<span style="font-weight:bold">%s) </span> %s
		</label> <br>
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
	elif 'sin(x)' in chosen_function:
		slope = math.cos(x)
	elif 'cos(x)' in chosen_function:
		slope = -(math.sin(x))
	elif 'e^{x}' in chosen_function:
		slope = math.exp(x)
	elif 'x^2' in chosen_function:
		slope = 2.*x

	return chosen_function, slope

def get_problem(pname):
	if pname == 'num100':
		a = random.randint(1,10)
		b = random.randint(1,10)
		solution = a+b
		t = "What is %s + %s" %(a,b)		
		return short_answer(t),solution

	if pname == 'num10x':
		choices = ['Henry', 'Alex', 'David', 'Susan**']
		prompt = "What is Susan's name?"
		return multiple_choice(prompt,choices)

	if pname == 'num102x':
		choices = ['\(\pi\)', '\(e\)', '\(2\)', 'These are all numbers**']
		prompt = "which one of the following is not a number?"
		return multiple_choice(prompt,choices)

	if pname == 'num101':
		choices = ['\pi**', 'e**', '2**', '5**', '0**']
		prompt = "Which of the following is a number? Select all that apply"
		return more_than_one(prompt,choices)

	#Problems dealing with sets

	if pname == 'set101':
		choices = ['\{6,8,10\}**', '\{7,9\}', '\{6,8,10,12\}', '\{4,6,8,10\}']
		prompt = "What is the set of all even numbers between \(5\) and \(11\)?"
		return more_than_one(prompt,choices)

	if pname == 'set102':
		choices = ['1**', '1.2**', '1.04**', '4/5**', '\pi**', '1000.230**']
		prompt = "Which of the following is a real number?"
		return more_than_one(prompt,choices)

	if pname == 'set103':
		choices = [
			'A number that makes sense, when you think about it',
			'A number that can be written as a ratio any two numbers',
			'A number than can be written as a ratio of two integers**',
			'Any number']
		prompt = "What is a rational number? Choose the best answer that is also quite clearly not a joke"
		return multiple_choice(prompt,choices, tex=False)

	if pname == 'set104':
		choices = [
			'\pi \\notin \mathbb{R}**',
			'4 \in \\mathbb{Q}',
			'\sqrt{2} \in \mathbb{R}',
			'e \\notin \\mathbb{Q}',
			'3.1415 \in \\mathbb{R}'
			]
		prompt = '''
		If \( \mathbb{R} \) is the set of real numbers and \( \mathbb{Q} \) is the set of rational numbers, 
		which one of the following is incorrect? Select all that apply'''
		return more_than_one(prompt,choices)
#########################################################################################
#Limits and limit properties
#########################################################################################
	if pname == 'lim100':
		prompt = '''
		Which of the following correctly describe the process of taking a limit? <br>
		<p>I. Determining the value of a function at a point</p>
		<p>II. Examining the value of a function near a point</p>		
		'''
		choices = ['I. only', 'II. only**', 'I. and II.', 'neither']
		return multiple_choice(prompt, choices, tex=False)

	if pname == 'lim101':
		f_name = random.choice('fghjklmnqw')
		v_name = random.choice('xzt')
		v_value = random.randint(-10,10)
		prompt = 'The correct notation for the limit of the function %s(%s) as %s approaches %s:' % (f_name, v_name, v_name, v_value)
		choices = [
		'\lim_{%s \\to %s} \: %s(%s)**' % (v_name, v_value, f_name, v_name),
		'\lim_{%s = %s} \: %s(%s)' % (v_name, v_value, f_name, v_name),
		'\lim_{%s(%s)} \: %s = %s' % (f_name, v_name, v_name, v_value),
		'\lim \: %s(%s) = %s' % (f_name, v_name, v_value)
		]
		return multiple_choice(prompt, choices)

	if pname == 'lim102':
		f_name = random.choice('fghjklmnqw')
		v_name = random.choice('xzt')
		v_value = random.randint(-10,10)
		prompt = '''What is the correct latex notation for the limit of \(%s(%s)\) as \(%s\) approaches %s?
		''' % (f_name, v_name, v_name, v_value)
		solution = '\lim_{%s \\to %s} %s(%s)' % (v_name, v_value, f_name, v_name)
		return short_answer(prompt), solution

	if pname =='lim103':
		prompt = '''Which of the following might be an appropriate numerical approximation for: $$\lim_{x \\to 2} f(x)$$
		Select all that apply'''
		choices = ['f(1.99)**', 'f(1.9)**', 'f(2.001)**', 'f(2.1)**', 'f(2.003)**']
		return more_than_one(prompt,choices)

	if pname == 'lim104':
		prompt = '''
			Examine the graph of: $$ f(x) = \\frac{x^2-1}{x-1} $$
			Determine the following: $$ \lim_{x \\to 1 } f(x) $$
			You may with to use a graphing calculator or Wolfram Alpha to graph this
			(<a href = "%s" target="_blank">click here to see how</a>)
			''' % r"http://www.wolframalpha.com/input/?i=plot+%28x%5E2-1%29%2F%28x-1%29+for+0%3Cx%3C2"
		choices = ['-1', '3', '1', '2**', '0']
		return multiple_choice(prompt, choices)

	if pname =='lim105':
		prompt = '''Which of the following numbers is not close to 2?'''
		choices = ['10', '1.9', '1.99', '1.99999','Trick question: all of these are close to 2 depending on your definition of "close"**']
		return multiple_choice(prompt, choices, tex = False)

	if pname == 'lim106':
		prompt = '''
		Given the function $$ f(x) = \\begin{cases} 2x & x>3 \\\\ 3 & x<3 \\end{cases} $$
		Find the limit: $$ \lim_{x \\to 3^-} f(x)$$
		'''
		choices = ['3**', '6', 'unknown', 'undefined', '3.001']
		return multiple_choice(prompt, choices, tex = False)

	if pname == 'lim107':
		prompt = '''
		Given the function $$ f(x) = \\begin{cases} 2x & x>3 \\\\ 3 & x<3 \\end{cases} $$
		Find the limit: $$ \lim_{x \\to 3^+} f(x)$$
		'''
		choices = ['3', '6**', 'unknown', 'undefined', '3.001']
		return multiple_choice(prompt, choices, tex = False)

	if pname == 'lim108':
		function1 ='%sx %s %s' % (random.randint(2,9), random.choice(['+', '-']), random.randint(2,9))
		function2 = '-%sx %s %s' % (random.randint(2,9), random.choice(['+', '-']), random.randint(2,9))
		vnum = random.randint(0,5)
		function_to_evaluate = re.sub('x','*%s' % vnum,function2)
		key_value = eval(function_to_evaluate)
		choices = [str(key_value)+'**']
		while len(choices) < 5:				
			x = random.randint(key_value-5, key_value+5)
			add = True	
			for i in choices:				
				if str(x) == i or x == key_value or add == False:
					add = False
				else:
					add = True
			if add == True: 
				choices.append(str(x))
		prompt = '''
		Given the function $$ f(x) = \\begin{cases} %s & x>%s \\\\ %s & x<%s \\end{cases} $$
		Find the limit: $$ \lim_{x \\to %s^-} f(x)$$
		''' % (function1, vnum, function2, vnum, vnum)
		return multiple_choice(prompt, choices, tex = False)

	if pname == 'lim109':
		function1 ='%sx %s %s' % (random.randint(2,9), random.choice(['+', '-']), random.randint(2,9))
		function2 = '-%sx %s %s' % (random.randint(2,9), random.choice(['+', '-']), random.randint(2,9))
		vnum = random.randint(0,5)
		function_to_evaluate = re.sub('x','*%s' % vnum,function1)
		key_value = eval(function_to_evaluate)
		choices = [str(key_value)+'**']
		while len(choices) < 5:				
			x = random.randint(key_value-5, key_value+5)
			add = True	
			for i in choices:				
				if str(x) == i or x == key_value or add == False:
					add = False
				else:
					add = True
			if add == True: 
				choices.append(str(x))
		prompt = '''
		Given the function $$ f(x) = \\begin{cases} %s & x>%s \\\\ %s & x<%s \\end{cases} $$
		Find the limit: $$ \lim_{x \\to %s^+} f(x)$$
		''' % (function1, vnum, function2, vnum, vnum)
		return multiple_choice(prompt, choices, tex = False)

	if pname == 'lim110':
		function1 ='%sx %s %s' % (random.randint(2,9), random.choice(['+', '-']), random.randint(2,9))
		function2 = '%sx %s %s' % (random.randint(2,9), random.choice(['+', '-']), random.randint(2,9))
		vnum = random.randint(0,3)
		function_to_evaluate = re.sub('x','*%s' % vnum,function1)
		lim_right = eval(function_to_evaluate)
		lim_left = eval(re.sub('x','*%s' % vnum,function2))
		prompt = '''
		Given the function $$ f(x) = \\begin{cases} %s & x>%s \\\\ %s & x<%s \\end{cases} $$
		Find the limit: $$ \lim_{x \\to %s} f(x)$$
		''' % (function1, vnum, function2, vnum, vnum)
		if lim_left == lim_right:
			choices = [str(lim_left+random.randint(1,5)), str(lim_left)+'**', 'the limit does not exist']
		else:
			choices = [str(lim_left), str(lim_right), 'the limit does not exist**']

		return multiple_choice(prompt, choices, tex = False)

	if pname == 'lim111':
		function ='%sx %s %s' % (random.randint(2,9), random.choice(['+', '-']), random.randint(2,9))
		key_value = eval(re.sub('x','*0',function))
		choices = [str(key_value)+'**']
		while len(choices) < 5:				
			x = random.randint(key_value-5, key_value+5)
			add = True	
			for i in choices:				
				if str(x) == i or x == key_value or add == False:
					add = False
				else:
					add = True
			if add == True: 
				choices.append(str(x))
		prompt = '''Consider the following limit $$ \lim_{x \\to 0} f(x)$$ 
		Where \(f(x)\) is the piecewise function $$ f(x) = \\begin{cases} a & x < 0 \\\\ %s & x > 0 \\end{cases} $$
		''' % function
		prompt += 'For which value of \(a\) does the limit above exist?'
		return multiple_choice(prompt, choices, tex = False)

	if pname == 'lim112':
		prompt = 'Which statement below best defines the following limit? $$ \lim_{x \\to 4} g(x) = 10 $$ '
		choices = [
		'As \(x\) approaches 4 the value of the function \(g\) approaches 10**',
		'The value of the function \(g\) at 4 is equal to 10', 
		'Impossible to answer without knowing what \(g(x)\) is',
		'As \(x\) appoaches 10 the value of the function \(g\) approaches 4',
		'You really should not choose this answer unless you want to be wrong'
		]
		return multiple_choice(prompt, choices, tex = False)

	if pname == 'lim113':
		prompt = '''
		Consider the limit: $$ \lim_{x \\to 1} f(x)$$
		What must the value of \( \delta \) be to ensure a value of \( \\varepsilon < 0.3 \)? 
		'''
		choices = ['\\text{depends on what } f(x) \\text{ is}' + '**','\delta < 0.3', '\delta <0.4', '\delta < 0.5', '\delta < 0.2']
		return multiple_choice(prompt, choices)

	if pname == 'lim114':
		value1 = random.randint(1,12)
		value2 = random.randint(2,12)
		prompt = '''
			Given the following: $$ \lim_{x \\to 0} f(x) = %s$$ What is the value of: $$ \lim_{x \\to 0} %sf(x) $$
		''' % (value1, value2)
		return short_answer(prompt), str(value1*value2)

	if pname == 'lim115':
		value1 = random.randint(1,12)
		value2 = random.randint(2,12)
		sign = random.choice(['+', '-', '\\times'])
		if sign =='+':
			solution = value1+value2
		elif sign =='-':
			solution = value1-value2
		else:
			solution = value1*value2
		prompt = '''
			Given the following: $$ \lim_{x \\to 0} f(x) = %s \\text{  and  } \lim_{x \\to 0} g(x) = %s$$ 
			What is the value of: $$ \lim_{x \\to 0} \left( f(x) %s g(x) \\right) $$
		''' % (value1, value2, sign)
		return short_answer(prompt), str(solution)

	if pname =='lim116':
		prompt = '''Which of the following are indeterminate forms? Select all that apply'''
		choices = [
		'\\frac{0}{0}**','\\frac{\infty}{\infty}**', '0\\times\infty**', '1^{\infty}**', '0^0**', '\infty^0**', '\infty-\infty**',
		'\\frac{1}{0}', '\infty^1', '1^0'
		]
		return more_than_one(prompt,choices)

	if pname =='lim117':
		prompt = '''What is the value of the following limit 
		$$ \lim_{x \\to \infty} \\frac{3x^7-2x+4}{x^7-5} $$
		'''
		choices = ['3**', '4', '5', '\infty', '\\text{the limit does not exist}']
		return multiple_choice(prompt, choices)

	if pname =='lim118':
		denom = random.choice(['2','3','4','6','8'])
		numer = random.choice(['7', '', '11', '13','5'])
		power = random.randint(4,9)
		power2 = random.randint(2,3)
		prompt = '''What is the value of the following limit 
		$$ \lim_{x \\to \infty} \\frac{%s x^{%s} + %s x ^ %s + %s x}{%s x^{%s} - %s x } $$
		''' % (numer, power, random.randint(2,9), power2, random.randint(2,9),
			denom, power, random.randint(2,9))
		if numer == '':
			numer = '1'
		choices = [
		'\\text{the limit does not exist}', 
		'\infty', 
		'\\frac{%s}{%s}**' % (numer, denom),
		'\\frac{%s}{%s}' % (denom, numer),
		'\\frac{%s}{%s}' % (numer, power2),
		'0'
		]
		return multiple_choice(prompt, choices)


	if pname =='lim119':
		denom = random.choice(['2','3','4','6','8'])
		numer = random.choice(['7', '', '11', '13','5'])
		numpower = random.randint(4,7)
		denpower = random.randint(5,7)
		power2 = random.randint(2,3)
		prompt = '''What is the value of the following limit 
		$$ \lim_{x \\to \infty} \\frac{%s x^{%s} + %s x ^ %s + %s x}{%s x^{%s} - %s x } $$
		''' % (numer, numpower, random.randint(2,9), power2, random.randint(2,9),
			denom, denpower, random.randint(2,9))
		if numer == '':
			numer = '1'
		numheavy, denheavy, num_den_equal = '', '', ''
		if numpower > denpower:
			numheavy = '**'
		elif numpower < denpower:
			denheavy = '**'
		else:
			num_den_equal = '**'
		choices = [
		'\\text{the limit does not exist}', 
		'\infty'+numheavy, 
		'\\frac{%s}{%s}' % (numer, denom) + num_den_equal,
		'\\frac{%s}{%s}' % (denom, numer),
		'\\frac{%s}{%s}' % (numer, power2),
		'0' + denheavy
		]
		return multiple_choice(prompt, choices)

	if pname =='lim120':
		denom = random.choice(['2','3','4','6','8'])
		numer = random.choice(['7', '', '11', '13','5'])
		power = random.randint(4,9)
		power2 = random.randint(2,3)
		prompt = '''Where does the function \(f(x)\) have a horizontal asymptote? 
		$$  \\frac{%s x^{%s} + %s x ^ %s + %s x}{%s x^{%s} - %s x } $$
		''' % (numer, power, random.randint(2,9), power2, random.randint(2,9),
			denom, power, random.randint(2,9))
		if numer == '':
			numer = '1'
		choices = [
		'\\text{the function has no horizontal asymptote}', 
		'x = \infty', 
		'x = \\frac{%s}{%s}**' % (numer, denom),
		'x = \\frac{%s}{%s}' % (denom, numer),
		'x = \\frac{%s}{%s}' % (numer, power2),
		'x = 0'
		]
		return multiple_choice(prompt, choices)

	if pname =='lim121':
		prompt = '''What can be said about the following limits?
		$$\lim_{x \\to 0} \\frac{1}{x^7} = A \\text{  and  } \lim_{x \\to 0} \\frac{1}{x^8} = B$$
		'''
		choices = [
		'\(A\) exists but \(B\) is undefined',
		'\( A = 0, B = \infty\)', 
		'\(A\) does not exist but \( B = \infty \)**', 
		'\(A\) and \(B\) both do not exist', 
		'\(A=B=\infty\)'
		]
		return multiple_choice(prompt, choices, tex=False)

	if pname =='lim122':
		prompt = '''Let \(f(x)\) be a function that is known to be continuous on the open interval \((a,b)\)
		Also, \(c\) is some number such that \( a < c < b \). Which of the following must be true?<br><br>
		<p>I. \(f(c)\) is defined </p>
		<p>II. \( \displaystyle{\lim_{x \\to c} f(x) = f(c)}\) </p>
		<p>III. \( \displaystyle{\lim_{x \\to c^-} f(x) = \lim_{x \\to c^+} f(x) }\)</p>

		'''
		choices = [
		'I. only', 'I. and II. only', 'II. and III. only, ', 'none are true', 'I., II., and III.**'
		]
		return multiple_choice(prompt, choices, tex=False)

	if pname == 'lim123':
		prompt = '''Let \(f(x)\) be a function that is known to be continuous on the close interval \([a,b]\)
		Which of the following must be true if \(f(a) = M\) and \(f(b) = N\) ?
		'''
		choices = ['f(b)>f(a)', 'f(a) \lt f(b)', 'M \lt f(x) \lt N \\text{ for } a \le x \le b',
		'\\text{all of these may be true, but none of these must be true}**']
		return multiple_choice(prompt, choices)

#########################################################################################
#Local Linearity
#########################################################################################

	if pname =='loclin100':
		prompt = 'Which of the following best describes the concept of local linearity?'
		choices = [
		'Every function exhibits linear behavior on a small scale at every point in the domain of that function',
		'Every function exhibits linear behavior on a small scale over an interval for which that function is smooth**', 
		'Every function contains tiny little lines',
		'Every function is a collection of striaght lines',
		'Lines are the best functions around'
		]
		return multiple_choice(prompt, choices, tex=False)

	if pname =='loclin101':
		prompt = 'Which of the following functions cannot be linearized at \(x=0\)? You may wish you graph these. Select all that apply'
		choices = [
		'f(x) = \left| x \\right|**',
		'f(x) = 2x',
		'f(x) = \cos(x)',
		'f(x) = \sin(x)', 
		'f(x) = \sin(x^2)', 
		'f(x) = \\frac{\sin{\left| x \\right|}}{x}**',
		'f(x) = \\frac{1}{x}**'
		]
		return more_than_one(prompt, choices)

	if pname =='loclin102':
		prompt = 'Consider the function \(f(x)\) which is continuous and smooth over its entire domain. Which of the following is a general linear model of \(f(x)\)?'
		choices = [
		'y = mx+b**',
		'y = x^2 +x',
		'y = \cos(x)', 
		'y = Ax^2 + Bx + C'
		]
		return more_than_one(prompt, choices)

	if pname == 'loclin103':
		prompt = 'Let the equation \(y=mx+b\) be a linear model for some function. Which of the following correctly describe the contants \(m\) and \(b\)?'
		choices = [
		'\(m\) is the slope and \(b\) is the \(y\)-intercept of the graph of the equation \(y\)**',
		'\(b\) is the slope and \(m\) is the \(y\)-intercept of the graph the equation \(y\)'
		]
		return more_than_one(prompt, choices, tex = False)

	if pname == 'slope100':
		val1,val2,val3 = unique_integers(3,2,10)
		prompt = 'Which of the following represents a line with slope \(%s\) that passes through the point \((%s,%s)\)' % (val1, val2, val3)
		choices = [
		'y-%s=%s(x-%s)' % (val1, val2, val3),
		'y-%s=%s(x-%s)' % (val2, val3, val1),
		'y-%s=%s(x-%s)**' % (val3, val1, val2),
		'y-%s=%s(x-%s)' % (val2, val1, val3),
		'y-%s=%s(x-%s)' % (val1, val3, val2),
		]
		return multiple_choice(prompt, choices)

	if pname == 'slope101':
		prompt = 'The slope of the function \(f(x)\) near the point \(x=a\) is best given by which of the following? (Assume \(b\) is very close to \(a\) )'
		choices = [
		'\\frac{a-b}{f(a)-f(b)}',
		'\\frac{b-a}{f(b)-f(a)}',
		'\\frac{f(b)-b}{f(a)-a}',
		'\\frac{f(b)-f(a)}{b-a}**',
		'\\frac{f(b)}{f(a)}',
		]
		return multiple_choice(prompt, choices)

	if pname == 'slope102':
		val1 = random.choice('0123456789')
		val2 = val1+'.01'
		prompt = 'An appropriate estimate for the slope of \(f(x)\) near the point \(x = %s\) is: ' % val1
		prompt += '(Select all valid choices, assume \(f(x)\) is continuous and smooth over its entire domain)'
		choices = [
		'\\frac{f(%s)-f(%s)}{%s - %s}**' % (val2, val1, val2, val1),
		'\\frac{f(%s)-f(%s)}{0.01}**' % (val2, val1),
		'\\frac{f(%s)-f(%s)}{%s - %s}' % (val2, val1, val1, val2),
		'\\frac{f(%s)-f(%s)}{%s - %s}' % (val1, val2, val2, val1),
		'\\frac{%s-%s}{f(%s) - f(%s)}' % (val2, val1, val2, val1),
		]
		return more_than_one(prompt, choices)

	if pname == 'slope103':
		value = 0
		while value == 0 :
			value = random.randint(-10,10)
		fn_name, slope = random_function_and_slope(value)
		prompt = 'The slope of the function \(f(x) = %s\) at the point \(x=%s\) is most nearly' % (fn_name, value)
		choices = [
		'%1.4f**' % slope,
		'%1.4f' % (0.5*slope),
		'%1.4f' % (0.8*slope),
		'%1.4f' % (1.5*slope),
		'%1.4f' % (2.*slope),
		]
		return multiple_choice(prompt, choices)