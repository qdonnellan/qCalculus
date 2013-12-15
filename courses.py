import logging
from problem_bank.main import get_problem
from note_bank.main import get_notes
import hashlib
from datetime import datetime
import random
from google.appengine.api import memcache
import string

def get_course_info(course_name):
	if course_name == 'cal101':
		course = cal101()
	elif course_name == 'cal102':
		course = cal102()
	else:
		course = None
	return course

class new_lesson():
	def __init__(self, title, video = None, quiz = None, streak = None, notes = None):
		#the title of the lesson (or the title of the quiz)
		self.title = title
		#the youtube video reference
		self.video = video
		if quiz is not None:
			#the number of attempts in a row that the user must correctly complete to pass this quiz
			if streak is None:
				#the default streak is 1 attempt correct in a row
				streak = 1
			self.streak = streak
			self.quiz = quiz[0]
			x = string.digits + string.letters
			salt = ''
			for i in range(8):
				salt += random.choice(x)
			salt += title + str(datetime.now())
			key = hashlib.sha1(title + str(quiz[1]) + salt).hexdigest()
			self.key = key
			memcache.set(key,quiz[1])
		else:
			self.quiz = None
			self.key = None

		self.notes = notes

			

class new_unit():
	def __init__(self, title, lessons):
		self.lessons = lessons
		self.title = title

class cal101():
	def __init__(self):
		self.title = "CAL101 - Foundations of Calculus"
		self.description = "In this course we will discuss limits, continuity, derivatives, and integrals. "
		self.name = 'cal101'
		self.syllabus = '''

			<h4>Unit 1: Introduction to Limits</h4>
			<p>Informal, formal definitions of a limit, one-sided limits, numerical and graphical solutions </p>
			<h4>Unit 2: Limit Applications</h4>
			<p>Infinite limits, limits at infinity, continuity, and general properties of limits</p>
			<h4>Unit 3: The Slope Problem</h4>
			<p>Using limits and the concept of local linearity to define the slope of a line, our first introduction to the derivative</p>
			<h4>Unit 4: The Derivative</h4>
			<p>A brief view of differentiation rules including of transcendentals</p>
			<h4>Unit 5: The Area Problem</h4>
			<p>Introducing the area under a curve as an infinite Riemann Sum</p>
			<h4>Unit 6: The Definite Integral</h4>
			<p>Formal definition of the definite integral and basic properties</p>

		'''		
		units=[]

		########################################
		#Unit 1: Limits
		########################################
		unit_name = "Unit 1: Limits"

		lessons = []
		
		lessons.append(new_lesson(
			title = 'Taking a limit',
			video = 'vEbBamS2E1U',
			notes = '''
			<p>We are used to evaluating a function <b>at</b> a particular point, but there is another concept that is just as important: 
			evaluating a function <b>near</b> a particular point. Similiarly, we should understand how a function <b>behaves</b> near a point. 
			The process of evaluating a function near a point is what is meant by <b>taking a limit</b>. </p>
			<p>Taking a limit is quite the important process in calculus; some functions prohibit us from evaluating them at certain points, take the
			function below for example: $$f(x)=\\frac{\cos{x}}{\sin{x}}$$</p>
			<p> What does this function look like near \(x=0\)? We certainly can't plug in \(0\)
			to this function - we will need a new approach.</p>
			'''
			))
		lessons.append(new_lesson(
			title = 'Quiz 1',
			quiz = get_problem('lim100'),
			streak = 1
			))
		lessons.append(new_lesson(
			title = 'Limit Notation',
			video = '3pr6QydOqBY',
			notes = '''
			<p>To specify that you are examining a function near a point, use limit notation:</p>
			$$\lim_{x \\to 0} f(x) $$
			<p>This says "what does the function \(f(x)\) look like when \(x\) approaches \(0\)?</p>
			'''
			))
		lessons.append(new_lesson(
			title = 'Quiz 2',
			quiz = get_problem('lim101'),
			streak = 1			
			))
		lessons.append(new_lesson(
			title = 'Limits in Latex',
			video = None,
			notes = '''
			To express a limit using the latex markup language, use the following method:
			<pre> \lim_{x \\to 0} f(x) </pre>
			$$\lim_{x \\to 0} f(x)$$
			Remember, you can right click and select <b>Show Math as | TeX commands</b> to view the Latex code behind any formula on this website
			'''

			))
		lessons.append(new_lesson(
			title = 'Quiz 3',
			quiz = get_problem('lim102'),
			streak = 1			
			))
		lessons.append(new_lesson(
			title = 'Limits Numerically',
			video = 'QCi02cHXwSs',
			notes = '''
			<p>Of course, if you'd like to know what the value of a function is near a point, just plug in a value near the interesting point and see what you get!
			I know this seems rather tedious, but in fact this is how many engineering problems are solved - tedius numerical calculations (typcally done by computer)</p>
			<p>For example, here is a piecewise function with an unknown value at an interesting point: 
			$$  f(x) = 
			\\begin{cases}
			x^2 & x \\neq 2 \\\\
			undefined & x = 2
			\\end{cases}
			$$
			<p>By definition, this function is undefined at 2, so we can't just plug in 2 to find the function's value. But, we can plug in a number really close to 2, say
			1.999 and see what we get.
			$$ f(1.999) = 3.996001 $$
			So, real close to 2, the function's value is real close to 4. 
			Of course we could have also picked a number "on the other side of 2", say 2.001, and it should also be close to 4. When it is not, that's a problem, and we'll
			go over that in the next part </p>
			'''
			))
		lessons.append(new_lesson(title = 'Quiz 4',		quiz = get_problem('lim103'),	streak = 1))
		lessons.append(new_lesson(title = 'More on Numerical Limits',video = 'H4HdwTG3akY'))
		lessons.append(new_lesson(title = 'What Does Limit Mean',video = 'CjnhGhKCdyY'))
		lessons.append(new_lesson(title = 'Quiz 5',		quiz = get_problem('lim112'),	streak = 1))				
		lessons.append(new_lesson(title = 'An Informal Limit Definition',video = '8Q6MV-cF910'))
		lessons.append(new_lesson(title = 'No Limit',video = 'bwUj8u9MJjI'))
		lessons.append(new_lesson(title = 'Epsilon Delta Definition',video = 'c-mWRxwBj6U'))
		lessons.append(new_lesson(title = 'Quiz 6',		quiz = get_problem('lim113'),	streak = 1))	
		lessons.append(new_lesson(title = 'Never Too Close',video ='KdqAnJfIxIk'))
		lessons.append(new_lesson(title = 'Limits Graphically',video = 'v-DcY40cjB4'))
		lessons.append(new_lesson(title = 'Quiz 7',		quiz = get_problem('lim104')))
		lessons.append(new_lesson(title = 'One Sided Limits',video = 'dlb1GPhE6ck'))
		lessons.append(new_lesson(title = 'Left Sided Limits',video = 'DzFhFYHxUg8'))
		lessons.append(new_lesson(title = 'Quiz 8',		quiz = get_problem('lim106'),	streak = 1))
		lessons.append(new_lesson(title = 'Right Sided Limits',video = 'Njm1Wfa8qV8'))
		lessons.append(new_lesson(title = 'Quiz 9',		quiz = get_problem('lim107'),	streak = 1))
		lessons.append(new_lesson(title = 'Left Example',video = 'KQJjGM7C-6Y'))
		lessons.append(new_lesson(title = 'Quiz 10',	quiz = get_problem('lim108'),	streak = 1))
		lessons.append(new_lesson(title = 'Right Example',video = 'UzZcEXz8MSE'	))	
		lessons.append(new_lesson(title = 'Quiz 11',	quiz = get_problem('lim109'),	streak = 1))
		lessons.append(new_lesson(title = "For a limit to exist",video = 'tq-xe5ri1po'))
		lessons.append(new_lesson(title = 'Quiz 12',	quiz = get_problem('lim111'),	streak = 5))	
		units.append(new_unit(unit_name, lessons))

		########################################
		#Unit 2: Properties of Limits
		########################################
		unit_name = "Unit 2: Applications of Limits"
		lessons = []
		lessons.append(new_lesson(title='Constants in Limits', video='q-sgQVBsgWU'))
		lessons.append(new_lesson(title='Quiz 1', 		quiz=get_problem('lim114')))		
		lessons.append(new_lesson(title='Limit Addition', video='MaZdvR6TomY'))	
		lessons.append(new_lesson(title='Quiz 2', 		quiz=get_problem('lim115')))	
		lessons.append(new_lesson(title='Limit Division', video='PRfcDn-FJ34'))
		lessons.append(new_lesson(title='Limit Exponents', video='SqeGY4ZmOq8'))
		lessons.append(new_lesson(title='Limits at Infinity', video='zgfoSh3TAUI'))
		lessons.append(new_lesson(title='Indeterminate Forms', video='0RpV_1M4k-k'))
		lessons.append(new_lesson(title='Quiz 3', 		quiz=get_problem('lim116')))
		lessons.append(new_lesson(title='Factor Makes Easier', video='7eDskq2kkV8'))
		lessons.append(new_lesson(title='Quiz 4', 		quiz=get_problem('lim117')))		
		lessons.append(new_lesson(title='Factoring Example', video='HH26S-Rawcs'))
		lessons.append(new_lesson(title='Quiz 5', 		quiz=get_problem('lim118')))
		lessons.append(new_lesson(title='Shortcut', video='HPch9i9YZfk'))
		lessons.append(new_lesson(title='Quiz 6', 		quiz=get_problem('lim119'), streak = 5))
		lessons.append(new_lesson(title='Horizontal Asymptotes', video='fE5LYMKYnAI'))
		lessons.append(new_lesson(title='Quiz 7', 		quiz=get_problem('lim120'), streak = 2))
		lessons.append(new_lesson(title='Infinite Limits', video='F0Z27eWP7qQ'))
		lessons.append(new_lesson(title='Infinite Limits that DNE', video='kJSHsoB0Mqc'))
		lessons.append(new_lesson(title='Infinite Limits that DE', video='u6BgSoys4c4'))
		lessons.append(new_lesson(title='Quiz 8', 		quiz=get_problem('lim121')))
		lessons.append(new_lesson(title='Vertical Asymptotes', video='48n09mnCNwY'))
		lessons.append(new_lesson(title='Continuity', video='PL0k8-jHU54'))
		lessons.append(new_lesson(title='Formal Continuity', video='0t554YpiGrA'))
		lessons.append(new_lesson(title='Quiz 9', 		quiz=get_problem('lim122')))
		lessons.append(new_lesson(title='Discontinuities', video='BeDcRWIRytc'))
		lessons.append(new_lesson(title='Intermediate Values', video='ynZB-ru7APU'))
		lessons.append(new_lesson(title='Quiz 10', 		quiz=get_problem('lim123')))
		lessons.append(new_lesson(title='Easy Limit Evaluation', video='j3GyFuQbU_w'))
		lessons.append(new_lesson(title='Quiz 11', 		quiz=get_problem('lim119'), streak = 5))
		units.append(new_unit(unit_name, lessons))
		self.units = units

		########################################
		#Unit 3: The Area Problem
		########################################
		unit_name = "Unit 3: The Slope Problem"

		lessons = []
		lessons.append(new_lesson(title = 'Local Linearity', video = 'EhLBBoMxsjU'))
		lessons.append(new_lesson(title = 'Quiz 1',	quiz = get_problem('loclin100')))
		lessons.append(new_lesson(title = 'Not Smooth', video = 'WwEEadTgA9U'))
		lessons.append(new_lesson(title = 'Quiz 2',	quiz = get_problem('loclin101')))
		lessons.append(new_lesson(title = 'Importance', video = 'uiNm8AxzA4s'))
		lessons.append(new_lesson(title = 'Quiz 3',	quiz = get_problem('loclin102')))
		lessons.append(new_lesson(title = 'Parts of a Line', video = 'OkF4s2rmiiY'))
		lessons.append(new_lesson(title = 'Quiz 4',	quiz = get_problem('loclin103')))
		lessons.append(new_lesson(title = 'Tricky B', video = '0JBakMgG2Kc'))
		lessons.append(new_lesson(title = 'Point Slope Form', video = 'I3chnW8p0Mg'))
		lessons.append(new_lesson(title = 'Quiz 5',	quiz = get_problem('slope100')))
		lessons.append(new_lesson(title = 'The Bottom Line', video = 'D0ywWWeEry4'))
		lessons.append(new_lesson(title = 'What is slope', video = 'QxfRYs4kS8U'))		
		lessons.append(new_lesson(title = 'F of x notation', video = '-4TCNNs1SKk'))
		lessons.append(new_lesson(title = 'Quiz 6',	quiz = get_problem('slope101')))
		lessons.append(new_lesson(title = 'An example', video = '0oLtX4JxMPU'))
		lessons.append(new_lesson(title = 'Quiz 7',	quiz = get_problem('slope102')))
		lessons.append(new_lesson(title = 'An example continued', video = 'q9SE32PvQvQ'))
		lessons.append(new_lesson(title = 'Quiz 8',	quiz = get_problem('slope103')))
		lessons.append(new_lesson(title = 'Close not exact', video = 'Kf82MD2Oa-4'))
		lessons.append(new_lesson(title = 'Quiz 9',	quiz = get_problem('slope104')))
		lessons.append(new_lesson(title = 'The Secant Line', video = 'uJEtYyvW2Fc'))
		lessons.append(new_lesson(title = 'Average Slope',	notes = get_notes('slope100')))
		lessons.append(new_lesson(title = 'Quiz 10',	quiz = get_problem('slope105')))
		lessons.append(new_lesson(title = 'Better than Secant', video = 'tljjI3Kt6ao'))
		lessons.append(new_lesson(title = 'Changing x notations', video = '_mwpcWyoNQI'))
		lessons.append(new_lesson(title = 'Slope as limit', video = 'y7ZrzGnfRWI'))
		lessons.append(new_lesson(title = 'Quiz 11',	quiz = get_problem('slope106')))
		lessons.append(new_lesson(title = 'Limit definition of slope', video = 'FEOySMwlC5I'))
		lessons.append(new_lesson(title = 'The Tangent Line', video = 'Fyk9UdzqMv4'))	
		lessons.append(new_lesson(title = 'Important Statement about Tangent Line', video = 'BMiN8fJzaek'))	
		lessons.append(new_lesson(title = 'Quiz 12',	quiz = get_problem('tangent101'), streak = 2))	
		lessons.append(new_lesson(title = 'Tangent Line Definition',	notes = get_notes('tangent100')))
		lessons.append(new_lesson(title = 'Quiz 13',	quiz = get_problem('tangent100'), streak = 5))	
			
		#lessons.append(new_lesson(title = 'Quiz 12',	quiz = get_problem('tangent100')))
		units.append(new_unit(unit_name, lessons))
		self.units = units

		########################################
		#Unit 4: Definite Integrals
		########################################
		unit_name = "Unit 4: The Derivative"

		lessons = []
		lessons.append(new_lesson(title = 'Usefulness of Limit', video = 'V58_jPeLnrs'))
		lessons.append(new_lesson(title = 'Quiz 1',	quiz = get_problem('slope107')))
		lessons.append(new_lesson(title = 'Instantaneous Rate of Change', video = 'xN-zY2XBbsA'))
		lessons.append(new_lesson(title = 'Quiz 2',	quiz = get_problem('slope108')))
		lessons.append(new_lesson(title = 'The Derivative', video = 'xy_fRiNDiN8'))
		lessons.append(new_lesson(title = 'Quiz 3',	quiz = get_problem('slope109')))
		lessons.append(new_lesson(title = 'Leibniz Notation', video = 'Gh2ir1DhYPk'))
		lessons.append(new_lesson(title = 'Quiz 4',	quiz = get_problem('slope110')))
		lessons.append(new_lesson(title = 'Lagrange and Euler Notations', video = 'KI89euBCt8U'))
		lessons.append(new_lesson(title = 'Quiz 5',	quiz = get_problem('slope111')))
		lessons.append(new_lesson(title = 'Newton Notation', video = 'TpVxkzPPLaw'))
		lessons.append(new_lesson(title = 'Quiz 6',	quiz = get_problem('slope112')))
		lessons.append(new_lesson(title = 'Summary of Notations', video = '4BJMpo04jaA'))
		lessons.append(new_lesson(title = 'Cheats', video = 'llGQL_c6Q6Y'))
		lessons.append(new_lesson(title = 'Power Rule', video = 'lnGCwld8TwQ'))
		lessons.append(new_lesson(title = 'Quiz 7',	quiz = get_problem('derivative105'), streak = 5))
		lessons.append(new_lesson(title = 'More on the Power Rule', video = 'KB7WyOKJIL0'))
		lessons.append(new_lesson(title = 'Quiz 8',	quiz = get_problem('derivative106'), streak = 5))
		lessons.append(new_lesson(title = 'Even More on the Power Rule', video = 'TyKoQGNWJIU'))
		lessons.append(new_lesson(title = 'Derivatives of Constants', video = 'Ee4BtTzvn7w'))
		lessons.append(new_lesson(title = 'Exponential Function', video = '_wjaVCiukT0'))		
		lessons.append(new_lesson(title = 'Some Trig Cheats', video = '24yvho8UFR4'))		
		lessons.append(new_lesson(title = 'Quiz 9',	quiz = get_problem('derivative100')))
		lessons.append(new_lesson(title = 'Quiz 10',	quiz = get_problem('derivative101')))
		lessons.append(new_lesson(title = 'Quiz 11',	quiz = get_problem('derivative104')))
		lessons.append(new_lesson(title = 'Product Rule', video = 'gtt2VyKowsk'))
		lessons.append(new_lesson(title = 'Quiz 12',	quiz = get_problem('derivative107')))
		lessons.append(new_lesson(title = 'Quotient Rule', video = 'nZ0LzpFW-RA'))
		lessons.append(new_lesson(title = 'Chain Rule', video = 'pnAujhJNIuE'))
		lessons.append(new_lesson(title = 'Quiz 13',	quiz = get_problem('derivative108')))
		lessons.append(new_lesson(title = 'More on the Chain Rule', video = '58Yf94LCp9U'))
		lessons.append(new_lesson(title = 'Quiz 14',	quiz = get_problem('derivative109')))
		lessons.append(new_lesson(title = 'Even More on the Chain Rule', video = 'UE670hNuSEA'))
		lessons.append(new_lesson(title = 'Superposition', video = 'aj1dpZEUH4E'))	

		units.append(new_unit(unit_name, lessons))


		self.units = units

		########################################
		#Unit 5: The Slope Problem
		########################################
		unit_name = "Unit 5: The Area Problem"

		lessons = []
		lessons.append(new_lesson(title = 'under_construction'))

		units.append(new_unit(unit_name, lessons))


		self.units = units

		########################################
		#Unit 6: coming
		########################################
		unit_name = "Unit 6: The Definite Integral"

		lessons = []
		lessons.append(new_lesson(title = 'under_construction'))

		units.append(new_unit(unit_name, lessons))


		self.units = units
		

class cal102():
	def __init__(self):
		self.title = "CAL102 - Early Applications of Calculus"
		self.description = "In this course we will examine..."
		self.name = 'cal102'


		
