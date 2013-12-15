from universal_functions import *
from fractions import Fraction

import logging

#Limits and Properties of Limits

def limits(pname):
	if '100' in pname:
		prompt = '''
		Which of the following correctly describe the process of taking a limit? <br>
		<p>I. Determining the value of a function at a point</p>
		<p>II. Examining the value of a function near a point</p>		
		'''
		choices = ['I. only', 'II. only**', 'I. and II.', 'neither']
		return multiple_choice(prompt, choices, tex=False)

	elif '101' in pname:
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

	elif '102' in pname:
		f_name = random.choice('fghjklmnqw')
		v_name = random.choice('xzt')
		v_value = random.randint(-10,10)
		prompt = '''What is the correct latex notation for the limit of \(%s(%s)\) as \(%s\) approaches %s?
		''' % (f_name, v_name, v_name, v_value)
		solution = '\lim_{%s \\to %s} %s(%s)' % (v_name, v_value, f_name, v_name)
		return short_answer(prompt), solution

	elif '103' in pname:
		prompt = '''Which of the following might be an appropriate numerical approximation for: $$\lim_{x \\to 2} f(x)$$
		Select all that apply'''
		choices = ['f(1.99)**', 'f(1.9)**', 'f(2.001)**', 'f(2.1)**', 'f(2.003)**']
		return more_than_one(prompt,choices)

	elif '104' in pname:
		prompt = '''
			$$ f(x) = \\frac{x^2-1}{x-1} $$
			Determine the following: $$ \lim_{x \\to 1 } f(x) $$			
			''' 
		choices = ['-1', '3', '1', '2**', '0']
		return multiple_choice(prompt, choices)

	elif '105' in pname:
		prompt = '''Which of the following numbers is not close to 2?'''
		choices = ['10', '1.9', '1.99', '1.99999','Trick question: all of these are close to 2 depending on your definition of "close"**']
		return multiple_choice(prompt, choices, tex = False)

	elif '106' in pname:
		prompt = '''
		Given the function $$ f(x) = \\begin{cases} 2x & x>3 \\\\ 3 & x<3 \\end{cases} $$
		Find the limit: $$ \lim_{x \\to 3^-} f(x)$$
		'''
		choices = ['3**', '6', 'unknown', 'undefined', '3.001']
		return multiple_choice(prompt, choices, tex = False)

	elif '107' in pname:
		prompt = '''
		Given the function $$ f(x) = \\begin{cases} 2x & x>3 \\\\ 3 & x<3 \\end{cases} $$
		Find the limit: $$ \lim_{x \\to 3^+} f(x)$$
		'''
		choices = ['3', '6**', 'unknown', 'undefined', '3.001']
		return multiple_choice(prompt, choices, tex = False)

	elif '108' in pname:
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
		return multiple_choice(prompt, choices)

	elif '109' in pname:
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
		return multiple_choice(prompt, choices)

	elif '110' in pname:
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
			choices = [str(lim_left), str(lim_right), '\\text{limit does not exist}**']

		return multiple_choice(prompt, choices)

	elif '111' in pname:
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
		prompt += 'For which value of \(a\) does the limit above exist? <br>'
		return multiple_choice(prompt, choices)

	elif '112' in pname:
		prompt = 'Which statement below best defines the following limit? $$ \lim_{x \\to 4} g(x) = 10 $$ '
		choices = [
		'As \(x\) approaches 4 the value of the function \(g\) approaches 10**',
		'The value of the function \(g\) at 4 is equal to 10', 
		'Impossible to answer without knowing what \(g(x)\) is',
		'As \(x\) appoaches 10 the value of the function \(g\) approaches 4',
		'You really should not choose this answer unless you want to be wrong'
		]
		return multiple_choice(prompt, choices, tex = False)

	elif '113' in pname:
		prompt = '''
		Consider the limit: $$ \lim_{x \\to 1} f(x)$$
		What must the value of \( \delta \) be to ensure a value of \( \\varepsilon < 0.3 \)? 
		'''
		choices = ['\\text{depends on what } f(x) \\text{ is}' + '**','\delta < 0.3', '\delta <0.4', '\delta < 0.5', '\delta < 0.2']
		return multiple_choice(prompt, choices)

	elif '114' in pname:
		value1 = random.randint(1,12)
		value2 = random.randint(2,12)
		prompt = '''
			Given the following: $$ \lim_{x \\to 0} f(x) = %s$$ What is the value of: $$ \lim_{x \\to 0} %sf(x) $$
		''' % (value1, value2)
		return short_answer(prompt), str(value1*value2)

	elif '115' in pname:
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

	elif '116' in pname:
		prompt = '''Which of the following are indeterminate forms? Select all that apply'''
		choices = [
		'\\frac{0}{0}**','\\frac{\infty}{\infty}**', '0\\times\infty**', '1^{\infty}**', '0^0**', '\infty^0**', '\infty-\infty**',
		'\\frac{1}{0}', '\infty^1', '1^0'
		]
		return more_than_one(prompt,choices)

	elif '117' in pname:
		prompt = '''What is the value of the following limit 
		$$ \lim_{x \\to \infty} \\frac{3x^7-2x+4}{x^7-5} $$
		'''
		choices = ['3**', '4', '5', '\infty', '\\text{the limit does not exist}']
		return multiple_choice(prompt, choices)

	elif '118' in pname:
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
		'0'
		]
		return multiple_choice(prompt, choices)


	elif '119' in pname:
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
		'0' + denheavy
		]
		return multiple_choice(prompt, choices)

	elif '120' in pname:
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
		'\\text{no horizontal asymptote}', 
		'y = \\frac{%s}{%s}**' % (numer, denom),
		'y = \\frac{%s}{%s}' % (denom, numer),
		'y = \\frac{%s}{%s}' % (numer, power2),
		'y = 0'
		]
		return multiple_choice(prompt, choices)

	elif '121' in pname:
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

	elif '122' in pname:
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

	elif '123' in pname:
		prompt = '''Let \(f(x)\) be a function that is known to be continuous on the close interval \([a,b]\)
		Which of the following must be true if \(f(a) = M\) and \(f(b) = N\) ?
		'''
		choices = ['f(b)>f(a)', 'f(a) \lt f(b)', 'M \lt f(x) \lt N \\text{ for } a \le x \le b',
		'\\text{all of these may be true, but none of these must be true}**']
		return multiple_choice(prompt, choices)

	elif '124' in pname:
		num_power = random.randint(5,7)
		den_power = random.randint(5,7)
		sign = random.choice(['-',''])
		if num_power == den_power and sign == '':
			choices = ['1**', '2', '\\text{none}', '3', '\\text{unknown}']
		elif num_power == den_power and sign == '-':
			choices = ['1', '2**', '\\text{none}', '3', '\\text{unknown}']
		elif num_power < den_power:
			choices = ['1', '2**', '\\text{none}', '3', '\\text{unknown}']
		else:
			choices = ['1**', '2', '\\text{none}', '3', '\\text{unknown}']


		function = '\\frac{\pi x^%s+%s}{%s2 x^%s+%s}' % (num_power, random_latex_poly(2), sign, den_power, random_latex_poly(2))
		function = re.sub('[+][-]', '-', function)
		function = re.sub('[+][+]','+', function)
		prompt = '''How many unique horizontal asymptotes does the graph of \(f(x)\) have?
		$$ f(x) =  \\begin{cases} %s & x>%s \\\\  \\\\ %s & x<%s \\end{cases} $$
		''' % ('\\arctan(x)', '0', function, '0')
		
		return multiple_choice(prompt, choices)

	elif '125' in pname:
		root1 = random.randint(2,4)
		root2 = random.randint(1,5)
		b_value = root1+root2
		c_value = root1*root2
		problem_set = [
		['x^2-%sx+%s' % (b_value, c_value), 'x^2-%s' % (root1**2), 'removable'],
		['x^2+%sx+%s' % (b_value, c_value), 'x^2-%s' % (root1), 'infinite'],
		['x^2+%sx+%s' % (b_value, c_value), 'x^2-%s' % (root1**2), 'infinite'],
		]
		chosen_set = random.choice(problem_set)
		prompt = '''
		Let \(f\) be a function such that $$f(x)=\\frac{%s}{%s} $$ Describe the discontinuity at \(x=%s\) <br>
		''' % (chosen_set[0], chosen_set[1], root1)
		raw_choices = [
		'removable', 
		'infinite', 
		'jump', 
		'no discontinuity', 
		'not enough information'
		]
		choices = []
		for choice in raw_choices:
			if choice == chosen_set[2]:
				choices.append(choice+'**')
			else:
				choices.append(choice)
		return multiple_choice(prompt, choices, tex=False)

	elif '126' in pname:
		num_power = random.randint(2,5)
		den_power = random.randint(2,5)
		if num_power > den_power:
			correct = '0'
		else:
			correct = '1'
		prompt = 'How many unique horizontal asymptotes does the graph of \(f(x)\) below have?'
		prompt += '$$ f(x) = \\frac{x^%s + %s}{x^%s + %s} $$' % (num_power, random.randint(1,9), den_power, random.randint(1,9))
		raw_choices = ['1', '2', '3', '\\text{unknown}', '0']
		choices = []
		for choice in raw_choices:
			if choice == correct:
				choices.append(choice+'**')
			else:
				choices.append(choice)

		return multiple_choice(prompt, choices)

	elif '127' in pname:
		den_power = random.choice(['', '^2'])
		if den_power == '':
			correct = '2'
		else:
			correct = '1'

		prompt = 'How many unique horizontal asymptotes does the graph of \(f(x)\) below have?'
		prompt += '$$ f(x) = \\frac{\sqrt{x^2 + %s}}{x%s + %s} $$' % (random.randint(1,9), den_power, random.randint(1,9))
		raw_choices = ['1', '2', '3', '\\text{unknown}', '0']
		choices = []
		for choice in raw_choices:
			if choice == correct:
				choices.append(choice+'**')
			else:
				choices.append(choice)

		return multiple_choice(prompt, choices)

	elif '128' in pname:
		root1 = random.randint(2,4)
		root2 = random.randint(1,5)
		wrong1 = '\\frac{x^2+%sx+%s}{2}' % (root1, root2)
		wrong2 = '\\frac{x^2+%sx+%s}{x+%s}' % (root2+root1, root2*root1, root1)
		wrong3 = '\\frac{x^2-%sx+%s}{x^2-%s}' % (root2+root1, root2*root1, root1**2)
		wrong4 = '\\frac{x^2+%sx+%s}{x-%s}' % (root2+root1, root2*root1, root1)
		correct  = '\\frac{x^2+%sx+%s}{x-%s}**' % (root2*3, root2*root1, root1)
		choices = [wrong1, wrong2, wrong3, wrong4, correct]
		prompt = 'Which of the following has a vertical asymptote at \(x=%s\) <br>' % root1
		return multiple_choice(prompt, choices)

	elif '129' in pname:
		prompt = 'Evaluate the following limit'
		power1 = random.choice(['', '^2', '^3'])
		root = random.randint(1,9)
		prompt += '$$ \lim_{x \\to 0} \\frac{x^2 + %s}{x%s} = $$' % (root, power1)
		if power1 == '':
			correct = '\\text{does not exist}'
		if power1 == '^2':
			correct = '\infty'
		if power1 == '^3':
			correct = '0'

		raw_choices = [
		'\\text{does not exist}', '\infty', '-\infty', '0', '1'
		]
		choices = []
		for choice in raw_choices:
			if choice == correct:
				choices.append(choice+'**')
			else:
				choices.append(choice)

		return multiple_choice(prompt, choices)

	elif '130' in pname:
		numer = random.randint(3,13)
		denom = random.randint(3,13)
		power1 = random.randint(5,8)
		power2 = random.randint(5,8)
		top = '%sx^%s +%s' % (numer, power1, random_latex_poly(3))
		bottom = '%sx^%s +%s' % (denom, power2, random_latex_poly(3))
		top = re.sub('[+][-]', '-', top)
		bottom = re.sub('[+][-]', '-', bottom)
		frac1 = str(Fraction(numer, denom))
		frac2 = str(Fraction(denom, numer))
		if frac1 == frac2:
			frac2 = str(Fraction(denom, numer+1))
		if power1 > power2:
			correct = '\infty'
		if power1 == power2:
			correct = frac1
		if power1 < power2:
			correct = '0'
		prompt = 'Evaluate $$ \lim_{x \\to \infty } \\frac{%s}{%s} $$' % (top, bottom)
		raw_choices = ['\infty', '0', frac1, frac2, '\\text{does not exist}' ]
		choices = []
		for choice in raw_choices:
			if choice == correct:
				choices.append(choice+'**')
			else:
				choices.append(choice)

		return multiple_choice(prompt, choices)





	

