from google.appengine.api import memcache
import cgi
from operator import attrgetter, itemgetter
import datetime
from dbops import *
from time import time



def get_discussion_board(page=1, reverse=True, user_id=None, sort_method=None, tag=None, search=None, course_name=None, num_to_get=20):  
    
    if course_name is None:
        return 'Invalid course name',0
    else:  
        discussion_key = 'cached_discussion' + course_name + str(page) + str(user_id) + str(sort_method) + str(tag) + str(search)
        cached_discussion_key_bank(course_name, new_key = discussion_key)
        cached_discussion = memcache.get(discussion_key)   
        if cached_discussion is None:
            questions, num_next_page_questions = get_discussion_questions(page,reverse,user_id,sort_method,tag,search,course_name,num_to_get)
            discussion = populate_wireframe_discussion(questions, course_name)
            question_list = make_question_list(questions)
            memcache.set(discussion_key, [discussion, question_list, num_next_page_questions])
        else:
            discussion, question_list, num_next_page_questions = cached_discussion
        
        discussion = populate_latest_question_stats(question_list, discussion, course_name)
       
        return discussion, num_next_page_questions

def make_question_list(questions):
    question_list = []
    for question in questions:
        question_id = str(question.key().id())
        question_list.append(question_id)
    return question_list


def get_discussion_questions(page,reverse,user_id,sort_method,tag,search,course_name,num_to_get):
    questions = None
    if user_id is not None:
        all_questions = get_questions_by_user_id(user_id, course_name)
    else:
        all_questions = get_questions(course_name = course_name)

    if tag is not None and tag != '':
        all_questions = filter_questions(all_questions, tag = tag)

    if search is not None and search != '':
        all_questions = filter_questions(all_questions, search = search)
            
    if sort_method is None:
        sort_method = 'last_modified'
    if sort_method == 'score':
        temp_tuple = []
        for question in all_questions:
            temp_tuple.append([
                question,
                get_question_score(str(question.key().id()), course_name)
                ])
        temp_tuple = sorted(temp_tuple, key = itemgetter(1), reverse = reverse)
        all_questions = []
        for question in temp_tuple:
            all_questions.append(question[0])
    else:
        if all_questions is not None:
            all_questions = sorted(all_questions, key = attrgetter(sort_method), reverse = reverse)

    if all_questions is not None:
        num_per_page = num_to_get
        questions = all_questions[num_per_page*(page-1):num_per_page*page]

    if all_questions is not None:
        next_questions = all_questions[num_per_page*(page):num_per_page*(page+1)]
        num_next_page_questions = len(next_questions)
    else:
        num_next_page_questions = 0

    return questions, num_next_page_questions


def populate_wireframe_discussion(questions, course_name):
    if questions is None:
        return 'No questions'
    else:
        wireframe_discussion = get_wireframe_discussion(len(questions))
        wireframe_discussion = re.sub('course_name', course_name, wireframe_discussion)
        index = 0
        tag_block = ''
        for question in questions:
            wireframe_discussion = re.sub('question.%s.title' % index, question.title, wireframe_discussion)
            tags = question.tags
            tag_block = ''
            if tags:
                tags = tags.split('|')                
                for tag in tags:
                    if tag != "":
                        tag_class = tag_check(special_check = tag)
                        tag_block += r'''                  
                        <li class="pager %s pull-left">
                            <a href="/course/%s/discussion?tag=%s" style="padding:0 5px">%s</a>
                        </li>
                        ''' % (tag_class, course_name, tag,tag)            
            wireframe_discussion = re.sub('question.%s.tag_block' % index, tag_block, wireframe_discussion)
            wireframe_discussion = re.sub('question.%s.id' % index, str(question.key().id()), wireframe_discussion) 
            index+=1
        return wireframe_discussion

def populate_latest_question_stats(question_list, discussion_html, course_name):
    index = 0
    for question_id in question_list:
        answer_count = get_answer_count(question_id, course_name)
        last_time_edited, last_user_id = get_last_activity(question_id, course_name)
        user_rating = get_user_rating(course_name, str(last_user_id))
        nickname_and_level = get_user_nickname(last_user_id) + ' ('+ str(user_rating)+')'
        discussion_html = re.sub('question.%s.last_user_id_to_edit' % index, str(last_user_id) , discussion_html)
        discussion_html = re.sub('question.%s.last_time_edited' % index, get_time_ago_string(last_time_edited) , discussion_html)
        discussion_html = re.sub('question.%s.last_user_to_edit' % index, nickname_and_level , discussion_html)
        discussion_html = re.sub('question.%s.num_answers' % index, str(answer_count) , discussion_html)
        discussion_html = re.sub('question.%s.score' % index, str(get_question_score(question_id, course_name)), discussion_html)
        
        if answer_count == 0:
            btntype = "btn-danger"
        else:
            btntype = ""
        discussion_html = re.sub('question.%s.answer_btntype' % index, btntype, discussion_html)
        index+=1
    return discussion_html



def get_wireframe_discussion(number_of_questions_to_display):
    wireframe_html = memcache.get('wireframe' + str(number_of_questions_to_display))
    if wireframe_html is None:
        wireframe_html = ''
        for i in range(number_of_questions_to_display):
            wireframe_html += r'''
            <tr>     
                <td class = "hidden-phone" style="width:100px;">
                    <div class="btn-group ">                            
                        <button class="btn disabled btn-mini {0}answer_btntype">
                            <h3>{0}num_answers</h3>
                            <p>answers</p>
                        </button>
                        <button class="btn disabled btn-mini ">
                            <h3>{0}score</h3>
                            <p>score</p>                            
                        </button>                            
                    </div>
                </td>
                <td>
                    <div>
                        <a href = "/course/course_name/questions/{0}id">
                            <p class="question-leader">{0}title</p>
                        </a>
                        <div class="btn-group pull-left visible-phone" style="margin-right:2px" >
                            <button class="btn disabled {0}answer_btntype btn-mini">
                                ans: {0}num_answers
                            </button>
                            <button class="btn disabled btn-mini" >
                                score: {0}score
                            </button>
                        </div> 
                        <ul class="pager pull-left" style="margin:0; padding:0">
                            {0}tag_block
                        </ul> 
                        <p class="pull-right">
                            <small>last activity:</small>
                            <a href = "/course/course_name/profile/{0}last_user_id_to_edit">
                                {0}last_user_to_edit
                            </a>
                            <small>{0}last_time_edited<small>
                        </p>                           
                    </div>  
                </td>
            </tr>                  

            '''.format(r'question.%s.' % i)

        wireframe_html = '''
        <table class="table">
            <tbody >                    
                %s
            </tbody>
        </table>
        ''' % wireframe_html
        memcache.set('wireframe' + str(number_of_questions_to_display), wireframe_html)
    return wireframe_html
