from google.appengine.ext import db
from google.appengine.api import users
import logging
import random
from google.appengine.api import memcache
import re
import datetime
from operator import attrgetter, itemgetter

class Courses(db.Model):
    name = db.StringProperty(required = True)

class Questions(db.Model):
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    user_id = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    tags = db.StringProperty()
    
class Answers(db.Model):
    body = db.TextProperty(required = True)
    question = db.StringProperty(required = True)
    user_id = db.StringProperty(default = 'unknown')
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

class Qscores(db.Model):
    shard_name = db.StringProperty(required = True)
    count = db.IntegerProperty(required = True, default = 0)
    
class Ascores(db.Model):
    shard_name = db.StringProperty(required = True)
    count = db.IntegerProperty(required = True, default = 0)

class MyOwnUsers(db.Model):
    user_id = db.StringProperty(required = True)
    nickname = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    courses = db.StringProperty()
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    levels = db.TextProperty()

class MentorMap(db.Model):
    mentee_id = db.StringProperty(required = True)
    course_name = db.StringProperty(required = True)
    status = db.StringProperty(required = True)

class QuizStats(db.Model):
    quiz_name = db.StringProperty(required = True)
    unit_name = db.StringProperty(required = True)
    user_id = db.StringProperty(required = True)
    score = db.TextProperty(required = True)
    longest_streak = db.IntegerProperty()

class VoteHistory(db.Model):
    user_id = db.StringProperty(required = True)
    vote_history = db.TextProperty(default = "")

class Tags(db.Model):
    tag_name = db.StringProperty(required = True)
    last_modified = db.DateTimeProperty(auto_now = True) 


def get_question_score(question_id, course_name):
    parent_question = get_question_by_id(question_id, course_name)    
    total = memcache.get('Qscores' + course_name + str(question_id))
    if total is None:
        total = 0
        results = Qscores.all().ancestor(parent_question)
        for shard in results:
            total += shard.count
        memcache.add('Qscores' + course_name + str(question_id), total)
    return total

def get_answer_score(answer_id, question_id, course_name):
    parent_answer = get_answer(answer_id, question_id, course_name)
    total = memcache.get('Ascores' + course_name + str(answer_id) + str(question_id))
    if total is None:
        total = 0
        results = Ascores.all().ancestor(parent_answer)
        for shard in results:
            total +=shard.count
        memcache.set('Ascores' + course_name + str(answer_id) + str(question_id),total)
    return total

def get_answer(answer_id,question_id, course_name):
    answer = memcache.get(course_name + 'a' + str(answer_id) + 'q' + str(question_id))
    if answer is None:
        parent_question = get_question_by_id(question_id, course_name)
        answer = Answers.get_by_id(int(answer_id), parent = parent_question)
        if answer is not None:        
            memcache.set(course_name + 'a' + str(answer_id) + 'q' + str(question_id), answer)
    return answer

def edit_answer(new_answer, answer_id, question_id, course_name):
    answer = get_answer(answer_id, question_id, course_name)
    answer.body = new_answer
    answer.put()
    memcache.set(course_name + 'a' + str(answer_id) + 'q' + str(question_id), answer)
    parent_question = get_question_by_id(question_id, course_name)
    results = Answers.all().ancestor(parent_question)  
    memcache.set(course_name + 'answer_bank' + question_id, results)
    memcache.delete('cached_discussion' + course_name)

def get_vote_history(user_id, question_id, course_name, answer_id = None):
    #Let's first check to see if the answer or question of interest belong to the user
    #this is important for preventing users from voting for their own item
    history_value = None
    if answer_id is not None:
        answer = get_answer(answer_id, question_id, course_name)
        if str(answer.user_id) == str(user_id):
            history_value = "selfish"
    else:
        question = get_question_by_id(question_id, course_name)
        if str(question.user_id) == str(user_id):
            history_value = "selfish"
    #history_value returns "selfish" if the answer/question of interest is owned by the user
    

    if history_value != "selfish":
        vote_history = memcache.get(course_name + 'vote_history' + str(user_id))        
        if vote_history is None:
            q = VoteHistory.all().ancestor(get_course(course_name))
            q.filter('user_id = ', str(user_id))
            result = q.get()
            if result is None:
                VoteHistory(user_id = user_id, parent = get_course(course_name), vote_history = '').put()
                vote_history = ''
            else:
                vote_history = result.vote_history
            memcache.set(course_name + 'vote_history' + str(user_id), vote_history)
        
        votes = vote_history.split('|')
        if answer_id is None:
            match_qvote = 'qv' + str(question_id) 
            for vote in votes:
                if match_qvote in vote:
                    history_value = vote.split('qv')[0]

        if answer_id is not None:
            match_avote = 'q' + str(question_id) + 'a' + str(answer_id)
            for vote in votes:
                if match_avote in vote:
                    history_value = vote.split('q')[0]

        if history_value == '1':
            history_value = 'up'
        if history_value == '-1':
            history_value = 'down'



    return history_value

def increment_answer_score(new_vote, answer_id, question_id, user_id, course_name, clear = None):
    parent_answer = get_answer(answer_id, question_id, course_name)
    vote_history = get_vote_history(user_id = user_id, question_id = question_id, course_name=course_name, answer_id=answer_id)
    if clear is not None or vote_history is None:
        q = VoteHistory.all().ancestor(get_course(course_name))
        q.filter('user_id = ', str(user_id))
        result = q.get()
        if result is None:
            result = VoteHistory(user_id = user_id, parent = get_course(course_name))        
        result.vote_history += str(new_vote) + 'q' + str(question_id) + 'a' + str(answer_id) + '|'
        new_history = result.vote_history
        if clear is not None:
            match = 'q' + str(question_id) + 'a' + str(answer_id)
            result.vote_history = ""
            history = new_history.split('|')
            for vote in history:
                if vote != "":
                    if match not in vote:
                        result.vote_history += vote + '|'
        new_history = result.vote_history
        result.put()
        memcache.set(course_name + 'vote_history' + str(user_id), new_history)
        
        number_of_shards = 10
        def txn():
            index = random.randint(0,number_of_shards-1)
            shard_name = 'shard' + str(index)
            q = Ascores.all()
            q.ancestor(parent_answer)
            q.filter('shard_name = ', shard_name)
            shard = q.get()
            if shard is None:
                shard = Ascores(shard_name = shard_name, parent = parent_answer)
            shard.count += new_vote
            shard.put()
        db.run_in_transaction(txn)
        update_score_cache('Ascores' + course_name + str(answer_id) + str(question_id), new_vote)
        get_or_update_user_score(user_id = parent_answer.user_id, course_name = course_name, update = True)
        get_user_rating(user_id = parent_answer.user_id, course_name = course_name, update = True)
       

def increment_question_score(new_vote, question_id, user_id, course_name, clear = None):
    parent_question = get_question_by_id(question_id, course_name)    
    vote_history = get_vote_history(user_id = user_id, question_id = question_id, course_name = course_name)
    if clear is not None or vote_history is None:
        q = VoteHistory.all().ancestor(get_course(course_name))
        q.filter('user_id = ', str(user_id))
        result = q.get()
        if result is None:
            result = VoteHistory(user_id = user_id, parent = get_course(course_name))
        result.vote_history += str(new_vote) + 'qv' + str(question_id) + '|' 
        new_history = result.vote_history 
        if clear is not None:
            match = 'qv' + str(question_id)
            result.vote_history = ""
            history = new_history.split('|')
            for vote in history:            
                if match not in vote:
                    result.vote_history += vote + '|'
        new_history = result.vote_history
        result.put()
        memcache.set(course_name + 'vote_history' + str(user_id), new_history)


        number_of_shards = 10
        def txn():    
            index = random.randint(0, number_of_shards-1)
            shard_name = 'shard' + str(index)
            q = Qscores.all()
            q.ancestor(parent_question)        
            q.filter('shard_name = ', shard_name)
            shard = q.get()
            if shard is None:
                shard = Qscores(shard_name = shard_name, parent = parent_question)
            shard.count += new_vote
            shard.put()
        db.run_in_transaction(txn)
        update_score_cache('Qscores' + course_name + str(question_id), new_vote) 
        get_or_update_user_score(user_id = parent_question.user_id, course_name = course_name, update = True) 
        get_user_rating(user_id = parent_question.user_id, course_name = course_name, update = True)
       
        

def update_score_cache(key, new_vote):
    client = memcache.Client()
    limit = 0
    while limit < 100:        
        counter = client.gets(key)
        if counter is None:
            counter = 0
        if client.cas(key, counter+new_vote):
            break
        limit += 1

def get_answer_count(question_id, course_name):
    count = 0
    results = memcache.get(course_name + 'answer_bank'+question_id)
    if results is None:
        parent_question = get_question_by_id(question_id, course_name)
        q = Answers.all().ancestor(parent_question) 
        memcache.set(course_name + 'answer_bank' + question_id, q)
        results = q
    if results:
        for i in results:
            count +=1
    return count
        
def new_question(title, body, tags, course_name, user_id):
    parent_course = get_course(course_name)
    question = Questions(title = title, body = body, tags = tags, user_id = user_id, parent = parent_course)
    key = question.put()
    memcache.set(course_name + '|q' + str(key.id()), question)
    cached_questions = get_questions(course_name)
    memcache.set(course_name + 'questions', cached_questions)
    cached_discussion_key_bank(course_name = course_name, delete = True)
    return key.id()


def get_questions(course_name = None):
    if course_name is not None:
        parent_course = get_course(course_name)
        questions = memcache.get(course_name + 'questions')
        if questions is None:
            questions = Questions.all().ancestor(parent_course)
            memcache.set(course_name + 'questions', questions)
        return questions
    else:
        return None



def edit_question(title, body, tags, question_id, course_name):
    question = get_question_by_id(question_id, course_name)
    question.title = title
    question.body = body
    question.tags = tags
    question.put()
    memcache.set(course_name + '|q' + str(question_id), question)
    cached_questions = get_questions(course_name)
    memcache.set(course_name + 'questions', cached_questions)
    cached_discussion_key_bank(course_name = course_name, delete = True)

def get_question_by_id(question_id = None, course_name = None):
    if question_id is not None and course_name is not None:
        question = memcache.get(course_name + '|q' + str(question_id))
        if question is None:
            parent_course = get_course(course_name)
            question = Questions.get_by_id(int(question_id), parent = parent_course)
            memcache.set(course_name + '|q' + str(question_id), question)
        return question

def get_answers_by_question_id(question_id = None, course_name = None):
    if question_id is not None and course_name is not None:
        parent_question = get_question_by_id(question_id, course_name)
        if parent_question is None:
            return None
        else:
            #lets see if the answer bank for that question_id is cached
            results = memcache.get(course_name + 'answer_bank' + question_id)
            #the above cached entity should be refreshed every time an answer is created
            if results is None:
                results = Answers.all().ancestor(parent_question)                
                memcache.set(course_name + 'answer_bank' + question_id, results)
            return results

def get_answers_by_user_id(user_id, course_name = None):
    if course_name is not None:
        cached_answers = memcache.get(course_name + 'answers' + str(user_id))
        if cached_answers is None:
            parent_course = get_course(course_name)
            q = Answers.all().ancestor(parent_course).filter('user_id = ', user_id) 
            memcache.set(course_name + 'answers' + str(user_id),q)
            return q
        else:
            return cached_answers

def get_questions_by_user_id(user_id, course_name = None):
    if course_name is not None:
        cached_questions = memcache.get('course_name' + 'questions' + str(user_id))
        if cached_questions is None:
            parent_course = get_course(course_name)
            q = Questions.all().ancestor(parent_course).filter('user_id =', user_id)
            memcache.set(course_name + 'questions' + str(user_id),q)
            return q
        else:
            return cached_questions

def create_answer(question_id, answer_text, user_id, course_name):
    parent_question = get_question_by_id(question_id, course_name)
    new_answer = Answers(
        body = answer_text, 
        question = str(question_id), 
        parent = parent_question,
        user_id = user_id)

    key = new_answer.put()
    answer_id = str(key.id())
    q = Answers.all().ancestor(parent_question)   
    memcache.set(course_name + 'answer_bank' + question_id, q)
    memcache.set(course_name + 'a' + str(answer_id) + 'q' + str(question_id),new_answer)

    parent_question.put()
    memcache.set(course_name + '|q' + str(question_id), parent_question)
    cached_questions = get_questions(course_name)
    memcache.set(course_name + 'questions', cached_questions)


def create_new_user(user_id, nickname):    

    db_user = get_user(user_id)
    if db_user is not None:
        return False #user already exists in db
    
    else:
        new_user = MyOwnUsers(user_id = user_id, nickname = nickname)
        new_user.put()
        memcache.set(user_id, [new_user.user_id, nickname])
        memcache.set('user' + user_id, new_user)  
        return new_user    
          



def get_local_user(user_id):
    local_user = memcache.get('user' + user_id)
    return local_user

def spaceit(input_text):
    output_text = re.sub('\n','<br>', input_text)
    return output_text

def update_tags(new_tag, course_name):
    if new_tag:
        parent_course = get_course(course_name)
        cached_tag = memcache.get(course_name + 'tag'+new_tag)
        if cached_tag is None:
            q = Tags.all().ancestor(parent_course)
            q.filter('tag_name =', new_tag)
            result = q.get()
            if result is None:
                tag = Tags(tag_name = new_tag, parent = parent_course)
                tag.put()             
                memcache.set(course_name + 'tag'+new_tag, tag)
                all_tags = Tags.all()
                memcache.set(course_name + 'all_tags', all_tags)
        else:
            cached_tag.put()

def get_time_ago_string(datetime_object):
    asked_time = datetime_object
    long_ago = datetime.datetime.utcnow() - asked_time
    total_seconds = int(long_ago.total_seconds())
    if total_seconds > 24*3600:
        if total_seconds > 7*24*3600:
            weeks_ago = int(total_seconds/(7*24*3600))
            asked_time = str(weeks_ago) + 'wks ago'
        else:
            days_ago = int(total_seconds/(24*3600))
            if days_ago == 1:
                asked_time = "yesterday"
            else:
                asked_time = str(days_ago) + "d ago"
    else:
        if total_seconds > 3600:
            hours = int(total_seconds/3600)
            if hours == 1:
                asked_time = str(hours) + "h ago" 
            else:
                asked_time = str(hours) + "h ago"

        elif total_seconds > 60:
            minutes = int(total_seconds/60)
            if minutes == 1:
                asked_time = "1m ago"
            else:
                asked_time = str(minutes) + "m ago" 
        else: 
            asked_time = str(total_seconds) + "s ago"

    return asked_time

def filter_questions(questions = None, user_id = None, tag = None, search = None):
    if questions:
        temp_tuple = []
        if user_id is not None:
            for question in questions:
                if question.user_id == str(user_id):
                    temp_tuple.append(question)

        if tag is not None:
            for question in questions:
                qtags = question.tags
                if qtags:
                    qtags = qtags.split('|')                    
                    for qtag in qtags:
                        if qtag == tag:
                            temp_tuple.append(question) 

        if search is not None:
            for question in questions:
                if search.lower() in question.title.lower():
                    temp_tuple.append(question)
                else:
                    if search.lower() in question.body.lower():
                        temp_tuple.append(question)
        return temp_tuple

def get_last_activity(question_id, course_name):
    question = get_question_by_id(question_id, course_name)
    answers = get_answers_by_question_id(question_id, course_name)
    last_answer_time = datetime.datetime.min
    last_answer = question

    if answers is None:
        return question.last_modified, question.user_id

    else:
        for answer in answers:
            if (answer.last_modified > question.last_modified) and (answer.last_modified > last_answer_time):
                last_answer = answer               
                last_answer_time = answer.last_modified
        return last_answer.last_modified, last_answer.user_id

def get_recent_tags(number_to_get, course_name):
    all_tags = memcache.get(course_name + 'all_tags')
    parent_course = get_course(course_name)
    if all_tags is None:
        all_tags = Tags.all().ancestor(parent_course)
        if all_tags is None:
            all_tags = []
        memcache.set(course_name + 'all_tags', all_tags)

    all_tags = sorted(all_tags, key = attrgetter("last_modified"), reverse = True)
    return all_tags[0:number_to_get]

def get_question_count_by_user_id(user_id, course_name):
    questions = get_questions_by_user_id(user_id = user_id, course_name = course_name)
    count = 0
    if questions:
        for question in questions:
            count+=1
    return count 

def get_answer_count_by_user_id(user_id, course_name):
    answers = get_answers_by_user_id(user_id = user_id, course_name = course_name)
    count = 0
    if answers:
        for answer in answers:
            count +=1
    return count

def get_user_vote_counts(user_id, course_name):
    vote_history = memcache.get(course_name + 'vote_history' + str(user_id))
    if vote_history is None:
        q = VoteHistory.all().ancestor(get_course(course_name))
        q.filter('user_id = ', str(user_id))
        result = q.get()
        if result is None:
            VoteHistory(user_id = user_id, parent = get_course(course_name), vote_history = '').put()
            vote_history = ''
        else:
            vote_history = result.vote_history
        memcache.set(course_name + 'vote_history' + str(user_id), vote_history)
    
    votes = vote_history.split('|')
    qups,qdowns,aups,adowns = 0,0,0,0
    for vote in votes:
        if vote != '':
            if 'qv' in vote:
                value = vote.split('qv')[0]
                if value == '1':
                    qups += 1
                if value == '-1':
                    qdowns += 1
            if 'a' in vote:
                value = vote.split('q')[0]
                if value == '1':
                    aups += 1
                if value == '-1':
                    adowns += 1
    return qups,qdowns,aups,adowns

def get_course(course_name):
    if course_name:
        course = memcache.get(course_name)
        if course is None:
            q = Courses.all()
            q.filter('name = ', course_name)
            course = q.get()
            if course is None:
                course = Courses(name = course_name)
                course.put()
                memcache.set(course_name, course)
    
    return course

def profile_url(course_name = None, user = None):
    if course_name is not None and user is not None:
        profile_url = "/course/%s/profile" % course_name
    if user is not None and course_name is None:
        profile_url = "/profile"
    if user is None:
        profile_url = '/'

    return profile_url

def get_user_level(course_name, user_id):
    cached_user = memcache.get('user' + str(user_id))    
    if cached_user is None:
        q=MyOwnUsers.all()
        q.filter('user_id = ', str(user_id))
        user = q.get()
        levels = user.levels
        memcache.set('user' + str(user_id), user)
    else:
        levels = cached_user.levels

    level_to_return = 1
    if levels:
        levels = levels.split('|')
        for level in levels:
            if level != '':
                level_course, current_level = level.split('level')
                if level_course == course_name:
                    level_to_return = int(current_level)

    #To unlock all quizzes for the mentor_id = 1 user
    if int(get_mentor_id(str(user_id))) in [1,114, 59]:
       level_to_return = 100
    return level_to_return

def get_lesson_level(course, lesson_title, unit_title):
    level = 1
    current_level = None
    for unit in course.units:
        for lesson in unit.lessons:
            if lesson.title == lesson_title and unit.title == unit_title:
                current_level = level
            if lesson.quiz is not None:
                level+=1

    return current_level

def increase_user_level(course, user, current_quiz, current_unit):
    quiz_level = get_lesson_level(course, current_quiz, current_unit)    
    current_level = get_user_level(course.name, str(user.user_id))
    if current_level <= quiz_level:
        current_level += 1
        levels = user.levels 
        new_levels = ''
        if levels:
            levels = levels.split('|')
            for level in levels:
                if level != '':
                    level_course, saved_level = level.split('level')
                    if level_course == course.name:
                        new_levels += level_course + 'level' + str(current_level) + '|'
                    else:
                        new_levels += level_course + 'level' + str(saved_level) + '|'
        else:
            new_levels = course.name + 'level' + str(current_level) + '|'

        
        q = MyOwnUsers.all()
        q.filter('user_id =', user.user_id)
        user = q.get()
        user.levels = new_levels
        user.put()
        memcache.set('user' + str(user.user_id), user)
        get_user_rating(user_id = user.user_id, course_name = course.name, update = True)
       


def record_quiz_score(course, user, current_quiz, current_unit, new_score):
    #get the current quiz level of the quiz in question
    quiz_level = get_lesson_level(course, current_quiz, current_unit)
    #determine if the current quiz stats for this user are in the cache
    current_quiz_stats = memcache.get(course.name+user.user_id+current_quiz + current_unit)
    #if the current quiz stats are not in the cache, query the database
    if current_quiz_stats is None:
        q = QuizStats.all().ancestor(get_course(course.name))
        q.filter('user_id = ', user.user_id)
        q.filter('quiz_name =', current_quiz)
        q.filter('unit_name = ', current_unit)
        current_quiz_stats = q.get()
        #if the current_quiz stats are not in the database, this must be the first time
        #this user has attempted this quiz
        if current_quiz_stats is None:
            new_quiz_stats = QuizStats(
                    user_id = user.user_id,
                    quiz_name = current_quiz,
                    unit_name = current_unit, 
                    parent = get_course(course.name),
                    score = new_score
                )
            new_quiz_stats.put()
            current_quiz_stats = new_quiz_stats
        #otherwise, this quiz has been attempted before
        else:            
            current_quiz_stats.score += new_score
            current_quiz_stats.put()
    #and of course, update the quiz stats that were found in the cache if any
    else:
        current_quiz_stats.score += new_score
        current_quiz_stats.put()

    memcache.set(course.name+user.user_id+current_quiz + current_unit, current_quiz_stats)


def get_quiz_stats(course, user, current_quiz, current_unit,last_so_many_quizzes=None):
    #get the current quiz level of the quiz in question
    quiz_level = get_lesson_level(course, current_quiz, current_unit)
    #determine if the current quiz stats for this user are in the cache
    current_quiz_stats = memcache.get(course.name+user.user_id+current_quiz + current_unit)
    #if the current quiz stats are not in the cache, query the database
    if current_quiz_stats is None:
        q = QuizStats.all().ancestor(get_course(course.name))
        q.filter('user_id = ', user.user_id)
        q.filter('quiz_name =', current_quiz)
        q.filter('unit_name = ', current_unit)
        current_quiz_stats = q.get()
        memcache.set(course.name+user.user_id+current_quiz + current_unit, current_quiz_stats)

    if current_quiz_stats is None:
        scores = ''
    else:
        scores = current_quiz_stats.score
    #scores is a string in the form: '11010010010111110101111' where each digit is a quiz attempt
    #a 1 represents success and a 0 represent incorrect
    #what we do here is start at the end and count back the last_so_many_quizzes to get the user's
    #quiz history for those last_so_many attempts    total_attempts = len(scores)
    total_attempts = len(scores)
    #python indexes start at 0 not 1, so we need to take that into account
    last_attempt = total_attempts - 1
    #then, starting at the last attempt, we go backwards and add up all the attemps until we hit
    #the last_so_many_quiz number or unitl there are no more attempts to read
    if last_so_many_quizzes is None:
        last_so_many_quizzes = total_attempts
    if last_so_many_quizzes > total_attempts:
        last_so_many_quizzes = total_attempts
    count = 0
    streak = 0
    for i in range(last_so_many_quizzes):
        x = last_attempt - last_so_many_quizzes + i + 1
        count += int(scores[x]) 
        if int(scores[x]) == 1:
            streak += 1 
        else:
            streak = 0 

    if current_quiz_stats:
        if current_quiz_stats.longest_streak:            
            if streak > current_quiz_stats.longest_streak:
                current_quiz_stats.longest_streak = streak
                current_quiz_stats.put()
        else:
            current_quiz_stats.longest_streak = streak
            current_quiz_stats.put()   

        memcache.set(course.name+user.user_id+current_quiz + current_unit, current_quiz_stats)

    return count, last_so_many_quizzes, streak

def get_longest_streak(course_name, current_quiz, current_unit, user_id):
    current_quiz_stats = memcache.get(course_name +user_id + current_quiz + current_unit)
    if current_quiz_stats is None:
        q = QuizStats.all().ancestor(get_course(course_name))
        q.filter('user_id = ', user_id)
        q.filter('quiz_name =', current_quiz)
        q.filter('unit_name = ', current_unit)
        current_quiz_stats = q.get()
        memcache.set(course_name+user_id+current_quiz + current_unit, current_quiz_stats)

    if current_quiz_stats is not None:
        longest_streak = current_quiz_stats.longest_streak
        if longest_streak is None:
            longest_streak = 0
    else:
        longest_streak = 0

    return longest_streak


def get_quiz_streak(course,current_quiz,current_unit):  
    streak = 1  
    for unit in course.units:
        for lesson in unit.lessons:
            if lesson.quiz is not None:
                if lesson.title == current_quiz and unit.title == current_unit:
                    streak = lesson.streak
    return streak
            

def get_or_update_user_score(course_name,user_id,update=False):
    if update:
        memcache.delete(user_id + course_name + 'vote_record')        

    vote_record = memcache.get(user_id+course_name+'vote_record')
    if vote_record is None:
        user_answers = get_answers_by_user_id(user_id = user_id, course_name = course_name)
        user_questions = get_questions_by_user_id(user_id = user_id, course_name = course_name)
        answer_score = 0
        for answer in user_answers:
            score = get_answer_score(answer_id = answer.key().id(), question_id = answer.question, course_name = course_name)            
            answer_score += score

        question_score = 0
        for question in user_questions:
            question_score += get_question_score(question_id = question.key().id(), course_name = course_name)

        vote_record = [answer_score,question_score]
        memcache.set(user_id + course_name + 'vote_record',vote_record)

    return vote_record

def latex_check(passed_string, passed_string_title='no object specified'):
    #Check the passed string for latex markup indicators and pass an error if something is wrong

    error = ''
    #if the beginnings don't have a matching end, that's a problem...
    if len(re.findall(r'\(', passed_string)) != len(re.findall(r'\)', passed_string)):
        error += "There's something wrong with the latex code in the %s..." % str(passed_string_title)

    #check the number of double dollar signs ($$) if there is not an evern number, that's a problem
    latex_dollar_pairs = re.findall('\$\$',passed_string)
    if len(latex_dollar_pairs) % 2 != 0:
        error += "There's something wrong with the latex code in the %s..." % str(passed_string_title)


    #returned error is None if there is no error and a string if there is one
    if error == '':
        error = None
    return error

def get_mentor_id(user_id):
    mentor_id = memcache.get('mentor_id' + str(user_id))
    if mentor_id is None:
        q = MyOwnUsers.all()
        q.filter('user_id =', user_id)
        result = q.get()
        mentor_id = str(result.key().id())
        memcache.set('mentor_id' + str(user_id),mentor_id)
    return mentor_id

def get_students(user,course_name):
    mentor_id = get_mentor_id(str(user.user_id))
    mentor = get_mentor(mentor_id)
    students = memcache.get(mentor_id + course_name)
    if students is None:       
        students = MentorMap.all().ancestor(mentor).filter('course_name =', course_name)
        memcache.set(mentor_id + course_name, students)
    return students

def is_this_my_student(mentee_id, user, course_name):
    my_students = get_students(user, course_name)
    ping = ''
    for student in my_students:
        if student.mentee_id == mentee_id:
            ping += 'yes'
    if 'yes' in ping:
        return True
    else:
        return False


def create_mentor_request(mentor_id,user,course_name):
    mentor = get_mentor(mentor_id)
    mentor_error = check_valid_mentor(user,mentor_id,course_name)
    if mentor_error is None:
        new_mentor_request = MentorMap(parent = mentor, status = 'pending', course_name = course_name, mentee_id = user.user_id)
        new_mentor_request.put()
        memcache.delete(mentor_id+course_name)
        memcache.delete('mentors' + user.user_id + course_name)

def get_mentor(mentor_id):
    mentor = memcache.get('mentor'+mentor_id)
    if mentor is None:
        mentor =  MyOwnUsers.get_by_id(int(mentor_id))
        memcache.set('mentor' + mentor_id, mentor)
    return mentor

def check_valid_mentor(user,mentor_id, course_name):
    error = None
    mentor = get_mentor(mentor_id)
    if mentor is None:
        error = 'That mentor does not exist'
    else:
        if str(mentor.user_id) == str(user.user_id):
            error = 'You cannot add yourself as your own mentor!'
        else:
            students = memcache.get(mentor_id + course_name)
            if students is None:       
                students = MentorMap.all().ancestor(mentor).filter('course_name =', course_name)
                memcache.set(mentor_id + course_name, students)
            
            if students is not None:
                for student in students:
                    if student.mentee_id == user.user_id:
                        error = 'You have already added this person as a mentor'
    return error


def get_user(user_id):
    user = get_local_user(user_id)
    if user is None:
        user = MyOwnUsers.all().filter('user_id = ', user_id).get()
        memcache.set('user' + user_id, user)
    return user


def get_my_mentors(user_id, course_name):
    my_mentors = memcache.get('mentors' + user_id + course_name)
    if my_mentors is None:
        my_mentors =[]
        my_own_student_instances = MentorMap.all().filter('mentee_id =', user_id).filter('course_name = ', course_name)
        for instance_of_me in my_own_student_instances:
            my_mentors.append([instance_of_me.parent(),instance_of_me.status])
        memcache.set('mentors' + user_id + course_name, my_mentors)
    return my_mentors

def approve_mentorship(user, course_name, mentee_id):
    students = get_students(user, course_name)
    for student in students:
        if student.mentee_id == mentee_id:
            student.status = 'active'
            student.put()
            mentor_id = get_mentor_id(user.user_id)
            memcache.delete(mentor_id + course_name)
            memcache.delete('mentors' + mentee_id + course_name)

def decline_mentorship(user, course_name, mentee_id):
    students = get_students(user, course_name)
    for student in students:
        if student.mentee_id == mentee_id:
            student.delete()
            mentor_id = get_mentor_id(user.user_id)
            memcache.delete(mentor_id + course_name)
            memcache.delete('mentors' + mentee_id + course_name)

def get_discussion_reputation(course_name, user_id):
    user_stats = get_or_update_user_score(course_name, user_id,update=True)
    user_votes = get_user_vote_counts(user_id, course_name)
    d_rep =  user_stats[0] + user_stats[1] - user_votes[1] - user_votes[3]  
    return d_rep

def get_user_rating(course_name, user_id, update = False):
    if update == True:
        memcache.delete('user_rating' + course_name + user_id)
    user_rating = memcache.get('user_rating' + course_name + user_id)
    if user_rating is None or update == True:
        quiz_level = get_user_level(course_name, user_id)
        discussion_rep = get_discussion_reputation(course_name, user_id)
        user_rating = quiz_level + discussion_rep
        memcache.set('user_rating' + course_name + user_id, user_rating)
    return user_rating

def build_student_info_list(students, course_name, sort_method = None):
    student_list = []
    for student in students:        
        vote_counts = get_user_vote_counts(user_id = student.mentee_id, course_name = course_name)
        personal_info = get_personal_info(student.mentee_id)
        student_dict ={}
        student_dict['user_object'] = get_user(student.mentee_id) 
        student_dict['nickname'] = personal_info.nickname
        student_dict['full_name'] = personal_info.first_name + ' ' + personal_info.last_name
        student_dict['discussion_rep'] = get_discussion_reputation(course_name, student.mentee_id)
        student_dict['level'] = get_user_level(user_id=student.mentee_id, course_name = course_name)
        student_dict['answer_count'] = get_answer_count_by_user_id(user_id = student.mentee_id, course_name = course_name)
        student_dict['question_count'] = get_question_count_by_user_id(user_id = student.mentee_id, course_name = course_name)        
        student_dict['up_votes'] = vote_counts[0] + vote_counts[2]
        student_dict['down_votes'] = vote_counts[1] + vote_counts[3]
        student_dict['status'] = student.status
        student_dict['id'] = student.mentee_id
        student_list.append(student_dict)

    if sort_method in ['level', 'up_votes', 'down_votes', 'discussion_rep', 'answer_count', 'question_count']:
        sorted_list = sorted(student_list, key = itemgetter(sort_method), reverse = True)
    else:
        sorted_list = sorted(student_list, key = itemgetter('nickname'), reverse = False)

    return sorted_list
    

def tag_check(tag_list=None, user_id=None, special_check=None, suppress_special = False):
    error = ''
    reformed_tags = []
    super_tags =['announcement', 'important']
    super_user_ids = ['6001']
    if special_check is not None:
        if special_check.lower() in super_tags:
            if suppress_special:
                return None            
            else:
                return "tag-special"
        else:
            return 'question-tags'
    else:
        for tag in tag_list:           
            USER_RE = re.compile(r"^[a-zA-Z0-9-]{3,30}$")
            valid_tag = USER_RE.match(tag)
            if not valid_tag:
                if tag != '':
                    error += "There's something wrong with your tags..."

            if tag.lower() in super_tags:
                if get_mentor_id(user_id) in super_user_ids:
                    reformed_tags.append(tag.upper())
                else:
                    error += "You are not authorized to use that tag"
            else:
                reformed_tags.append(tag)

        if error == '':
            error = None

        return reformed_tags, error

class tab_decor():
    def __init__(self):
        self.votes = ''
        self.stats = ''
        self.answers = ''
        self.questions = ''
        self.mentor = ''
        self.quizzes = ''

######################################################
#USER INFORMATION
######################################################

def get_personal_info(user_id):
    person = memcache.get('personal'+user_id)
    if person is None:
        q = MyOwnUsers.all()
        q.filter('user_id = ', user_id)
        result = q.get()
        person = update_personal_info(result)
    return person

def edit_user_information(user_id, nickname = None, last_name = None, first_name = None):
    user = get_user(user_id)
    if nickname is not None:
        user.nickname = nickname
    if last_name is not None:
        user.last_name = last_name
    if first_name is not None:
        user.first_name = first_name
    user.put()
    update_personal_info(user)

def update_personal_info(user_object):
    updated_person = make_personal_info(user_object.last_name, user_object.first_name, user_object.nickname)
    memcache.set('personal' + str(user_object.user_id), updated_person)
    return updated_person

class make_personal_info():
    def __init__(self, last_name, first_name, nickname):
        if last_name is None:
            last_name = 'no last name on file ...'
        if first_name is None:
            first_name = 'no first name on file ...'
        self.last_name = last_name
        self.first_name = first_name
        self.nickname = nickname

def get_user_nickname(user_id):
    personal_info = get_personal_info(user_id)
    return personal_info.nickname


def cached_discussion_key_bank(course_name, new_key = None, delete = False):
    if new_key is not None:
        bank = memcache.get('cached_discussion_key_bank' + course_name)
        if bank is None:
            bank = []
        bank.append(new_key)
        memcache.set('cached_discussion_key_bank' + course_name, bank)

    if delete:
        bank = memcache.get('cached_discussion_key_bank' + course_name)
        for key in bank:
            memcache.delete(key)
    









        








