from universal_functions import *

#Finding the slope of a function numerically

def slope(pname):
	if '100' in pname:
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

	elif '101' in pname:
		prompt = 'The slope of the function \(f(x)\) near the point \(x=a\) is best given by which of the following? (Assume \(b\) is very close to \(a\) )'
		choices = [
		'\\frac{a-b}{f(a)-f(b)}',
		'\\frac{b-a}{f(b)-f(a)}',
		'\\frac{f(b)-b}{f(a)-a}',
		'\\frac{f(b)-f(a)}{b-a}**',
		'\\frac{f(b)}{f(a)}',
		]
		return multiple_choice(prompt, choices)

	elif '102' in pname:
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

	elif '103' in pname:
		value = random.randint(-10,10)
		fn_name, fn_value, slope = random_function_and_slope(value)
		prompt = 'The slope of the function \(f(x) = %s\) at the point \(x=%s\) is most nearly' % (fn_name, value)
		choices = [
		'%1.4f**' % slope,
		'%1.4f' % (0.5*(slope+.1)),
		'%1.4f' % (0.8*(slope+.1)),
		'%1.4f' % (1.5*(slope+.1)),
		'\\text{undefined}',
		]
		return multiple_choice(prompt, choices)

	elif '104' in pname:
		value = random.randint(1,10)
		val1 = value - 0.01
		val2 = value + 0.01
		prompt = 'Which of the following approximates the slope of the function \(f(x)\) near \(x=%s\)?' % value
		prompt += '(Select all valid choices)'
		choices = [
		'\\frac{f(%s)-f(%s)}{%s - %s}**' % (value, val1, value, val1),
		'\\frac{f(%s)-f(%s)}{%s - %s}**' % (value, val2, value, val2),
		'\\frac{f(%s)-f(%s)}{%s - %s}**' % (val2, val1, val2, val1),
		'\\frac{f(%s)-f(%s)}{%s - %s}' % (value, value, value, value),
		'\\frac{f(%s)-f(%s)}{%s - %s}**' % (val1, val2, val1, val2),
		]
		return more_than_one(prompt, choices)

	elif '105' in pname:
		prompt = '''Consider the function \(m(x)\) defined as:
		$$ m(x) = \\frac{f(b)-f(a)}{b-a} $$
		Where f(x) is some continuous, smooth function over its entire domain and \(x=a\) and \(x=b\) are arbitrarily close. 
		Which of the following describe the function \(m(x)\)? <br>
		<p>I. \(m(x)\) is equal to the slope of \(f(x)\) at \(x=a\)<p>
		<p>II. \(m(x)\) is an approximation of the slope of \(f(x)\) near \(x=a\)<p>
		<p>III. \(m(x)\) is equal to the average slope of \(f(x)\) on the interval [a,b]<p>
		'''
		choices = ['I. only', 'II. only', 'I. and II. only', 'II. and III. only**', 'I. II. and III.']
		return multiple_choice(prompt, choices, tex=False)

	elif '106' in pname:
		prompt = ''' The best model of the slope of a continuous, smooth function \(f(x)\) is given by:'''
		choices = [
		'\lim_{x \\to 0} \\frac{f(x+\Delta x) -f(x) }{\Delta x}',
		'\lim_{x \\to \Delta x} \\frac{f(x+\Delta x) -f(x) }{\Delta x}',
		'\lim_{\Delta x \\to 0} \\frac{f(x+\Delta x) -f(x) }{\Delta x}**',
		'\lim_{\Delta x \\to x} \\frac{f(x+\Delta x) -f(x) }{\Delta x}',
		'\lim_{\Delta x \\to 0} \\frac{f(x+\Delta x)+f(x) }{\Delta x}'
		]
		return multiple_choice(prompt, choices)

	elif '107' in pname:
		val1, val2, val3, val4, val5 = unique_integers(5,2,15)
		prompt = 'Consider the function \( f(x) = %sx+%s \) ' % (val1, val2)
		prompt += 'Evaluate the limit: $$ \lim_{h \\to 0} \\frac{f(x+h)-f(x)}{h} $$'
		choices = [str(val1)+'**', str(val2), str(val3), str(val4), str(val5)]
		return multiple_choice(prompt, choices)

	elif '108' in pname:
		val1, val2, val3, val4, val5 = unique_integers(5,2,15)
		prompt = 'Consider the function \( f(x) = %sx+%s \) What is the instantaneous rate of change of \(f\) at \(x=%s\)' % (val1, val2, val3)
		choices = [str(val1)+'**', str(val2), str(val3), str(val4), str(val5)]
		return multiple_choice(prompt, choices)

	elif '109' in pname:
		val1, val2, val3, val4 = unique_integers(4,2,15)
		prompt = 'Consider the constant function \( y = %s \) What is the derivative of \(y\) at \(x=%s\)' % (val1, val2)
		choices = [str(val1), str(val2), str(val3), str(val4), '0**']
		return multiple_choice(prompt, choices)

	elif '110' in pname:
		fname = random.choice('fghjkpnmbrwq')
		varname = random.choice('xt')
		prompt = '''
		The latex markup for a fraction used on this website is simply: <code>\\frac{3}{2}</code>
		Which will produce the following output: $$ \\frac{3}{2} $$ 
		Using latex markup and Leibniz notation, express the derivative of a function \(%s\) with respect to an independent variable \(%s\) 
		''' % (fname, varname)
		solution = '\\frac{d%s}{d%s}' % (fname, varname)
		return short_answer(prompt), solution

	elif '111' in pname:
		prompt = '''
		Another quiz on Latex markup! To render the angle variable "theta" using the actual greek letter, we use the following markup: 
		<code>\\theta</code> which renders: \( \\theta \) <br> <br>
		Also, the Lagrange notation for derivatives uses the simple single apostrophe <code>'</code>. The derivative of a function \(y(x)\) is written as 
		\(y'(x)\) (which looks like <code>y'(x)</code> in Latex). Using this basic markup, express the derivative of a function \( f(\\theta)\) in Lagrange notation. 
		'''
		solution = "f'(\\theta)"
		return short_answer(prompt), solution

	elif '112' in pname:
		fname = random.choice('abcdfghijklmnopqrstuvwxz')
		prompt = '''
		Isaac Newton's notation for marking the derivative was to place a dot above the differentiated function. The derivative of \(y\) is 
		therefore \( \dot{y}\). To produce this markup in latex we use <code>\dot{y}</code>
		<br><br>
		Using Newton's notation and latex markup express the derivative of some function \(%s \)
		''' % fname
		solution = "\dot{%s}" % fname
		return short_answer(prompt), solution