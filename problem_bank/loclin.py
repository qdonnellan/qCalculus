from universal_functions import *

#Local Linearity and Linearization of Functions

def loclin(pname):
	if '100' in pname:
		prompt = 'Which of the following best describes the concept of local linearity?'
		choices = [
		'Every function exhibits linear behavior on a small scale at every point in the domain of that function',
		'Every function exhibits linear behavior on a small scale over an interval for which that function is smooth**', 
		'Every function contains tiny little lines',
		'Every function is a collection of striaght lines',
		'Lines are the best functions around'
		]
		return multiple_choice(prompt, choices, tex=False)

	elif '101' in pname:
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

	elif '102' in pname:
		prompt = 'Consider the function \(f(x)\) which is continuous and smooth over its entire domain. Which of the following is a general linear model of \(f(x)\)?'
		choices = [
		'y = mx+b**',
		'y = x^2 +x',
		'y = \cos(x)', 
		'y = Ax^2 + Bx + C'
		]
		return more_than_one(prompt, choices)

	elif '103' in pname:
		prompt = 'Let the equation \(y=mx+b\) be a linear model for some function. Which of the following correctly describe the contants \(m\) and \(b\)?'
		choices = [
		'\(m\) is the slope and \(b\) is the \(y\)-intercept of the graph of the equation \(y\)**',
		'\(b\) is the slope and \(m\) is the \(y\)-intercept of the graph the equation \(y\)'
		]
		return more_than_one(prompt, choices, tex = False)