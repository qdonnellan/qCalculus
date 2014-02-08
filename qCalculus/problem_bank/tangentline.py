from universal_functions import *

#Questions about the Tangent Line


def tangent(pname):
	if '100' in pname:		
		value = random.randint(-10,10)
		fn_name, fn_value, slope = random_function_and_slope(value)
		prompt = 'Which of the following approximates the best linear model of the function \(f(x) = %s\) at \(x=%s\)?' % (fn_name, value)
		choices = [
		'y-%1.4f=%1.4f(x-%s)**' % (fn_value, slope, value),
		'y-%1.4f=%1.4f(x-%s)' % (fn_value, (0.5*(slope+.1)), value),
		'y-%1.4f=%1.4f(x-%s)' % (fn_value, (1.8*(slope+.1)), value),
		'y-%1.4f=%1.4f(x-%s)' % (fn_value, (2*(slope+.1)), value),
		'y-%1.4f=%1.4f(x-%s)' % (fn_value, (3*(slope+.1)), value),
		]
		return multiple_choice(prompt, choices)

	if '101' in pname:
		xval, yval, slope = unique_integers(3,2,10)
		prompt = '''
		At the point \((%s,%s)\), the slope of the line tangent to \(f\) at that point is \(%s\). 
		Which of the following is the best linear model for \(f\) at that point? (Assume \(f\) is continuous and smooth over its entire domain.)
		''' % (xval, yval, slope)
		choices = [
		'y-%s = %s(x-%s)' % (xval, yval, slope),
		'y-%s = %s(x-%s)' % (yval, xval, slope),
		'y-%s = %s(x-%s)' % (xval, slope, xval),
		'y-%s = %s(x-%s)' % (xval, slope, xval),
		'y-%s = %s(x-%s)**' % (yval, slope, xval),
		]
		return multiple_choice(prompt, choices)

