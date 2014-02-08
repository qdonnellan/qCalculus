def slope(notekey):
	if '100' in notekey:
		return '''
		An important note about the secant line - even though the slope of the secant line is not an exact model for the slope
		of the function it is approximating, the slope of the secant line is equivalent to the average slope of the function 
		between the two points used to create the secant line. Or:
		$$ \\text{Average Slope between a and b } = \\frac{f(b)-f(a)}{b-a} = \\text{Slope of Secant Line} $$
		The average slope is also known as the average rate of change
		<br>
		'''
