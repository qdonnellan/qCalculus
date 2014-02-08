from universal_functions import *

# Differentiation identities

def get_derivative_prompt(function_name, value):
	prompt_choices = [
	'What is the derivative of the function \(f(x)=%s\) at the point \(x=%s\)' % (function_name, value),
	'The slope of the line tangent to the function \(f(x)=%s\) at the point \(x=%s\) is' % (function_name, value) ,
	"Consider the function \(f(x) = %s\). Find \(f'(%s)\)" % (function_name, value),
	'What is the instantaneous rate of change of the function \(f(x) = %s\) at \(x=%s\)' % (function_name, value)
	]
	return random.choice(prompt_choices)

def basic_trig_problem(function_name):
	function, xvalue, derivative = simple_random_trig_derivative(forced_function = function_name)
	prompt = get_derivative_prompt(function, xvalue)		
	choices = [derivative+'**']
	while len(choices) < 5:
		bad_answer = simple_random_trig_derivative()[2]			
		if bad_answer != derivative and bad_answer not in choices:
			choices.append(bad_answer)
	new_choices = []
	for choice in choices:
		new_choices.append(re.sub('undefined', r'\\text{undefined}', choice))

	return multiple_choice(prompt,new_choices)


def derivative(pname):
	if '100' in pname:
		return basic_trig_problem('\cos(x)')
	elif '101' in pname:
		return basic_trig_problem('\sin(x)')
	elif '102' in pname:
		return basic_trig_problem('\\tan(x)')
	elif '103' in pname:
		return basic_trig_problem('\sec(x)')
	elif '104' in pname:
		derivative, xvalue = random_arctan_derivative()
		xvalue = random.choice(['', '-']) + xvalue
		prompt = get_derivative_prompt('\\arctan(x)', xvalue)
		choices = [derivative+'**']
		while len(choices) < 5:
			bad_answer = random_arctan_derivative()[0]			
			if bad_answer != derivative and bad_answer not in choices:
				choices.append(bad_answer)
		return multiple_choice(prompt,choices)

	elif '105' in pname:
		coeff = random.randint(2,5)
		exponent = random.randint(3,8)
		new_coeff = coeff*exponent
		new_exponent = exponent-1
		prompt = 'Find \(\dfrac{dy}{dx}\) if \(y=%sx^{%s}\)' % (coeff, exponent)
		prompt += '<br><br>Use latex markup and format your answer like <code>ax^n</code> or <code>ax^{n}</code>. '
		solution1 = '%sx^%s' % (new_coeff,new_exponent)
		solution2 = '%sx^{%s}' % (new_coeff,new_exponent)
		solution = solution1 + '<<>>' + solution2
		return short_answer(prompt), solution

	elif '106' in pname:
		coeff = random.randint(2,5)
		exponent = random.randint(3,8)
		new_coeff = coeff*exponent
		new_exponent = exponent-1
		function = '%sx^{%s}' % (coeff, exponent)
		x_value = random.randint(0,2)
		prompt = get_derivative_prompt(function, x_value)
		solution = new_coeff*(x_value**new_exponent)
		return short_answer(prompt), str(solution)

	elif '107' in pname:
		prompt = '''
		Note: to express a trigonometric function such as \(\sin\) in Latex, you use a "backslash" before the 'sin' 
		<pre> \sin </pre>
		Also: although not every time necessary, I recommend always using parentheses "inside" the sine function. Use parentheses in this answer! 
		Futhermore, I always use the convention of putting the trigonometric piece at the "end" of a term. The grading robot will be looking for
		$$ x^3\sin(x) $$<pre> x^3 \sin(x)</pre> and not $$ \sin(x) x^3 $$ <pre>\sin(x) x^3 </pre> So be careful there as well. 
		This is generally considered good practice anyway. Another note - extra spaces will not effect your answer! (see the examples above)
		<br><br>
		If \(f(x)=x^2\sin(x)\) find \(f'(x)\) <br>
		<br>
		'''
		s1 = '2x\sin(x) + x^2\cos(x)'
		return short_answer(prompt), s1

	elif '108' in pname:
		prompt  = ''' \(f(x) = \cos(x^2) \), find \(\dfrac{df}{dx}\). 
		Use Latex typesetting and don't forget the conventions previously discussed!'''
		s1 = "-2x\sin(x^2)"		
		s2 = "-\sin(x^2)2x"
		sol = s1 + '<<>>' + s2
		return short_answer(prompt), sol

	elif '109' in pname:
		prompt = "Given \(g(x)= \sin(x^2 e^x)\) find \(g'(x)\)"
		s1 = "\cos(x^2 e^x) (2xe^x + x^2 e^x)"
		s2 = "(2xe^x + x^2 e^x) \cos(x^2 e^x)"
		sol = s1 + "<<>>" + s2
		return short_answer(prompt), sol


	
