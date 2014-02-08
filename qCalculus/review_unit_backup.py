########################################
		#Review: Numbers and Functions
		########################################
		unit_name = "Unit R: Review: Numbers and Functions"

		lessons = []
		lessons.append(new_lesson(
			title = 'Numbers',
			video = 'hVhi8PEXn48',
			notes = '''
			<p>
			A number is a fundamental mathematical concept typically used to count or measure. 
			Over the many years of human civilization we have developed several symbols which are
			useful in representing numbers, here are a few of them.
			</p>
			<p>
			\(0,1,2,3,4,5,6,7,8,9\) - the Arabic numerals
			</p>
			<p> \(\pi \) - the ratio of a circle's circumference to its diameter</p>
			<p> \(e\) - the base of the natural logarithm and equal to the infinite sum
			 \(1+\\dfrac{1}{1!}+\\dfrac{1}{2!} + \\dfrac{1}{3!} + \\dfrac{1}{4!} + ... \)
			</p>
			<p> \( \\varphi \) - the golden ratio </p>
			'''
			))
		lessons.append(new_lesson(
			title = 'Quiz: Numbers',
			quiz = get_problem('lim102'),
			streak = 1			
			))		
		lessons.append(new_lesson(
			title = 'Sets',
			video = 'I5Nm8JN5L9c',
			notes = '''
			<p>A set is another fundamental mathematical concept and is typically defined 
			as a collection of objects. Each object within the set is referred to as an element
			of that set and is denoted by the notation: $$ x \in A $$ which says that \(x\) is an element
			in the set \(A\). Brackets are used to show that objects belong to a set. For example, 
			the set of odd numbers greater than \(5\) and less than \(21\) can be written as: 
			$$ \{7,9,11,13,15,17,19\} $$ Of course, to express that an object is not in a set:
			$$ 34 \\notin \{7,9,11,13,15,17,19\} $$ \(34 \) is not in that set. </p>
			'''						
			))
		lessons.append(new_lesson(
			title = 'Quiz: Sets',
			quiz = get_problem('lim101'),
			streak = 1			
			))
		lessons.append(new_lesson(
			title = 'Intersections',
			video = 'brnBkqhV5Hs',
			notes = '''
			<p>In set theory, the concept of an 'intersection' is analogous to the central part of a venn diagram. 
			If one set shares common elements with another, then those sets intersect, and the intersection 
			(denoted with the symbol \(\cap\)) of those sets is a third set
			which simply contains the elements that are in both sets. </p>
			<p>Here's an example that helps to define what an intersection is: 
			$$ A = \{1,2,3,4,5\} $$ 
			$$ B = \{3,4,5,6,7,8\} $$
			$$ A \cap B = \{3,4,5\} $$
			The intersection of \(A\) and \(B\) is the set \(\{3,4,5\}\) because those are the elements shared by \(A\) and \(B\). 
			</p>
			'''						
			))
		lessons.append(new_lesson(
			title = 'The Empty Set',
			video = 'TODD8Qnsh48',
			notes = '''
			<p>
			Now, what happens if two sets contain absolutely no common elements? Well, the intersection of those two sets must be nothing.</p>
			Take for example this scenario:
			$$ A = \{1,2,3\} $$
			$$ B = \{4,5,6\} $$
			$$ A \cap B = \{\} $$
			They share nothing in common, so the intersection here is the <b>emtpy set</b>. The empty set is denoted with the symbol \(\\varnothing \)
			</p>
			<p>
			It is very important to note that the empty set is not the same thing as zero. Zero is an integer wheras the emty set is simply nothing. 
			The difference can be realized with this example:
			$$ A = \{-2,-1,0,1,2\} $$
			$$ B = \{-4,-3,0,3,4\} $$
			$$ A \cap B = \{0\} $$
			In this case, the only element shared by both \(A\) and \(B\) is the number \(0\). Thus, the intersection is not empty, it contains the number \(0\).
			</p>
			<p>A common empty set example is the intersection between real numbers and imaginary numbers. $$ \mathbb{R} \cap \mathbb{I} = \\varnothing$$
			No real number is also an imaginary number. </p>
			'''						
			))
		lessons.append(new_lesson(
			title = 'Real Numbers',
			video = '4X1pKnHA76E',
			notes = '''
			<p>One particular set worth mentioning is the set of real numbers, \( \mathbb{R} \).
			The set of real numbers consists of every number that exists in the number line.
			That is to say that \(1\) and \(2\) are real numbers, as are \(1.1\) and \(1.3\), as are the infinite
			quantity of numbers that exist in the continuum of the number line. Real numbers can be rational, or irratoinal</p>
			'''						
			))
		lessons.append(new_lesson(
			title = 'Quiz: Real Numbers',
			quiz = get_problem('set102'),
			streak = 1			
			))
		lessons.append(new_lesson(
			title = 'Rational Numbers',
			video = 'PIdSIxEgcQ4',
			notes = '''
			<p>Rational numbers \( \mathbb{Q} \) are a subset of real numbers \( \mathbb{Q} \in \mathbb{R} \). 
			Rational numbers are numbers that can be expressed as the <b>ratio</b> of two integers. 
			\(1.3\) for example, is a rational number because it can be expressed as \( \\frac{13}{10} \)</p>
			'''						
			))
		lessons.append(new_lesson(
			title = 'Quiz: Rational Numbers',
			quiz = get_problem('set103'),
			streak = 1			
			))
		lessons.append(new_lesson(
			title = 'Irrational Numbers',
			video = 'H-UpmGdHuAM',
			notes = '''
			<p>Interestingly, there are some real numbers that cannot be written as the ratio of two integers.
			Theses numbers are aptly named irrational; they do not represent an integer ratio. Many famous irrational
			numbers come from geometry.</p>
			<p>The ratio of a circle's circumference to its diameter is impossible to express as an integer ratio, but
			we use this number so often that we've given it the symbol \(\pi\).</p>
			<p>The ratio of a square's leg to its diagonal is also impossible to express as an integer ratio, but is
			exactly equal to \( \sqrt{2}\) </p>
			'''						
			))
		lessons.append(new_lesson(
			title = 'Quiz: Irrational Numbers',
			quiz = get_problem('set104'),
			streak = 1			
			))
		lessons.append(new_lesson(
			title = 'Imaginary Numbers',
			video = 'KKDOurz3rHw',
			notes = '''
			<p>Numbers that are not real are called imaginary \( \mathbb{I} \). These numbers all share the property that when squared they
			are negative. \( \sqrt{-2} \) is therefore an imaginary number. Because all imaginary numbers are multiples of the negative
			root of \(1\), they are commonly written as factors of that imaginary unit \(i\). \( \sqrt{-5}\) is written therefore as \(\sqrt{5}i\) 
			where \(i\) is assumed to be equal to \(\sqrt{-1}\)</p>
			<p>Real numbers can also be written as multiples of the 'real unit' which is simply the number \(1\), but this is rarely (if ever)
			written.</p>
			'''						
			))
		lessons.append(new_lesson(
			title = 'Complex Numbers',
			video = 't3z-A4lO5Z8',
			notes = '''
			<p>Some numbers are combinations of real numbers and imaginary numbers, and while we won't deal with these numbers much in this class
			I did want to introduce them here briefly. Complex numbers are written as the real part + the imaginary part.
			$$ 4 + 3i$$ is a complex number with a real part of 4 and an imaginary part of 3</p>
			'''						
			))
		lessons.append(new_lesson(
			title = 'Functions',
			video = None,
			notes = None
			))
		units.append(new_unit(unit_name, lessons))