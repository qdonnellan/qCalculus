from handlers import MainHandler
from dbops import *
from badges import *
from build_question_list import *
import cgi
from courses import *
import re
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import db
import logging
from operator import itemgetter, attrgetter


class Discussion(MainHandler):
    def get(self, course_name = None):                
        @self.login_required      
        def secured_things(user):            
            if self.valid_course(course_name):
                if course_name == None:
                    self.redirect("/")
                else:
                    sort_method = self.request.get('sort_method')
                    search_word = self.request.get('search')
                    press = self.request.get('press')
                    page = self.request.get('page')
                    filter_tag = self.request.get('tag')
                    edited_decor, created_decor, score_decor = "", "", ""
                    
                    if not sort_method or sort_method == 'last_modified':
                        sort_method = "last_modified"
                        edited_decor = "active"
                        reverse = True
                    else:
                        if sort_method == 'created':
                            created_decor = "active"
                            reverse = False
                        if sort_method == 'score':
                            score_decor = "active"
                            reverse = True

                    if page is None or page =='' or press=='just_then':
                        page = 1 

                    html_to_print, num_next_page_questions = get_discussion_board(
                            page=int(page), 
                            sort_method = sort_method,
                            reverse = reverse,
                            tag = filter_tag,
                            search = search_word,
                            num_to_get = 20,
                            course_name = course_name
                            )   
                                      
                    search_alert = ''
                    additional_query = 'tag=%s' % filter_tag                    
                    if filter_tag is not None and filter_tag != '':
                        search_alert = '''
                        <div class="alert alert-success">
                            Results for the <span class="badge">%s</span> tag
                        <a href = "/course/%s/discussion" class="close">&times;</a>
                        <br>
                        </div>
                        ''' % (filter_tag, course_name)
                        
                    if search_word is not None and search_word != '':
                        search_alert = '''                        
                        <div class="alert alert-success">
                            Search results for "%s"
                        <a href = "/course/%s/discussion" class="close">&times;</a>
                        <br>
                        </div>
                        ''' % (search_word, course_name)
                        additional_query += '&search=%s' % search_word            
                    

                    prev_page_class, next_page_class = "",""            
                    prev_page = 'href="/course/%s/discussion?page=%s&%s&sort_method=%s"' % (course_name, (int(page)-1), additional_query, sort_method)
                    if (int(page)-1) <= 0:
                        prev_page_class = "disabled"
                        prev_page = ''

                    next_page = 'href="/course/%s/discussion?page=%s&%s&sort_method=%s"' % (course_name, (int(page)+1), additional_query, sort_method)
                    if num_next_page_questions == 0:
                        next_page_class = "disabled"
                        next_page = ''

                    if page is not None and page != '':
                        additional_query += '&page=%s' % page

                    recent_tags = get_recent_tags(20, course_name)
                    recent_tag_block = ""
                    for tag in recent_tags:
                        if tag != "":
                            tag_class = tag_check(special_check=tag.tag_name)
                            recent_tag_block += '''
                            <li class="pager %s pull-left">
                                <a href="/course/%s/discussion?tag=%s" style="padding:0 5px">%s</a>
                            </li>
                            ''' % (tag_class, course_name, tag.tag_name, tag.tag_name)                    

                    course = get_course_info(course_name)
                    self.render('questions.html', 
                                question_text = html_to_print,
                                prev_page = prev_page,
                                next_page = next_page,
                                prev_page_class = prev_page_class,
                                next_page_class = next_page_class,
                                created_decor = created_decor,
                                edited_decor = edited_decor,
                                score_decor = score_decor,
                                additional_query = additional_query,
                                search_alert = search_alert,
                                recent_tag_block = recent_tag_block,
                                course=course,
                                discussion_active = "active",
                                profile_url = profile_url(course_name, user)
                                )
    def post(self, course_name):
        @self.login_required
        def secured_things(user):
            #the only form on this page is the search box, this simply redirects the user back to the discussion page
            #but of course the search work is now in the query parameters
            search_word = self.request.get('search_word')
            self.redirect('/course/%s/discussion?search=%s' % (course_name, search_word))

class QuestionAdder(MainHandler):
    #adding a question or editing a quesiton. 
    #question edits are triggered when the question_id is not None
    def get(self, course_name, question_id = None):        
        @self.login_required
        def secured_things(user):
            if self.valid_course(course_name):
                if course_name is None:
                    self.redirect('/')
                else:
                    recent_tags = get_recent_tags(100, course_name)
                    recent_tag_block = ""
                    for tag in recent_tags:
                        #tags are injected into a <ul> element on the discussion page with bootstrap markup
                        if tag != "":
                            tag_class = tag_check(special_check=tag.tag_name)
                            recent_tag_block += '''
                            <li class="pager %s pull-left">
                                <a style="padding:0 5px">%s</a>
                            </li>
                            ''' % (tag_class, tag.tag_name)  
                    #If the user and course are both valid (and the user is registered)...
                    if question_id is not None:
                        #question_id is only passed when an edit button has been clicked
                        question = get_question_by_id(question_id, course_name)
                        if user.user_id != question.user_id:
                            #need to make sure the user is the owner of the question
                            self.redirect('course/%s/questions/%d' % (course_name,int(question_id)))
                        else: 
                            tags = question.tags.split('|')             
                            self.render('addquestion.html', 
                                question_text = question.body, 
                                question_header = question.title,
                                tags = tags,
                                recent_tag_block = recent_tag_block,
                                profile_url = profile_url(course_name, user),
                                course= get_course_info(course_name))
                    else:
                        #if a question_id doesn't already exist, then this must be a new question
                        #this rendered the add-a-quetion form!
                        #notice the profile link and course object are used here again (and on every render)
                        tag_suggestion = self.request.get('tag_suggestion')
                        if tag_suggestion is None or tag_suggestion == '':
                            tags = []
                        else:
                            tags = [tag_suggestion]

                        self.render('addquestion.html',
                            profile_url = profile_url(course_name, user), 
                            course= get_course_info(course_name), 
                            recent_tag_block = recent_tag_block,
                            tags=tags)        
    def post(self, course_name, questionid = None):        
        @self.login_required
        def secured_things(user):
            if self.valid_course(course_name):
                #strange thing, if I set question_id = None as default, GAE did not play nice, but the below dummy variable works...
                #not worth losing more hair so it's stayed in
                question_id = questionid
                #title of the question
                question_header = self.request.get('question_header')
                #body of the question
                question_text = self.request.get('question_text')
                #tags associated with the question
                recent_tags = get_recent_tags(100, course_name)
                recent_tag_block = ""
                for tag in recent_tags:
                    #tags are injected into a <ul> element on the discussion page with bootstrap markup
                    if tag != "":
                        tag_class = tag_check(special_check=tag.tag_name)
                        recent_tag_block += '''
                        <li class="pager %s pull-left">
                            <a style="padding:0 5px">%s</a>
                        </li>
                        ''' % (tag_class, tag.tag_name)
                tags = []
                tags.append(self.request.get('tag#1'))
                tags.append(self.request.get('tag#2'))
                tags.append(self.request.get('tag#3'))
                tags.append(self.request.get('tag#4'))
                tags.append(self.request.get('tag#5'))
                new_tags = []
                for tag in tags:
                    new_tags.append(re.sub(r'\n','',tag))
                tags = new_tags        
                
                
                error = ''
                
                #Check the question title for problems
                #-----------------------------------------------------------
                #display equations are forbidden in the question title
                if len(re.findall('\$\$',question_header)) > 0:                    
                    error += "You cannot use display equations in the question title..."
                if len(re.findall(r'\[', question_header)) > 0 or len(re.findall(r'\]', question_header)) > 0:
                    error += "You cannot use display equations in the question title..."
                
                #Check the latex markup in the title, the function latex_check() can be found in dbops.py
                latex_error = latex_check(question_header, 'question title')
                if latex_error is not None:
                    error += latex_error                

                #no title is a problem
                if not question_header:                
                    error += "Please include a title..."

                #title can only be 140 characters long
                if len(question_header) >= 141:
                    error += "You used %s characters in your title; you may only use 140" % len(question_header) 

               

                #Check the question body for problems
                #-----------------------------------------------------------
                #if there is no question_body, that's a problem
                if not question_text:
                    error += "Don't leave your question blank..."               
               
                #Check the latex markup in the title, the function latex_check() can be found in dopbs.py
                latex_error = latex_check(question_text, 'question body')
                if latex_error is not None:
                    error += latex_error  

                #Check the tags for any errors
                #-----------------------------------------------------------               
                #let's create a useable list of tags from the user-supplied comma separated tags
                           
                tags, tag_error = tag_check(tags, user.user_id)
                if tag_error is not None:
                    error += tag_error

                #If after all that the error has changed, we have a problem
                if error != '':
                    #a bootstrap alert is injected into the page
                    alert_msg = r'''
                    <div class="alert alert-error">
                        <a class="close" data-dismiss="alert" href="#">&times;</a>
                        <h4 class="alert-heading">Oh snap!</h4>
                        %s 
                    </div>
                    ''' % error
                    #question is not added, instead the question page is re-loaded with the previous input perserved
                    self.render('addquestion.html',
                                question_header = question_header,
                                question_text = question_text, 
                                alert_msg = alert_msg,
                                tags=tags,
                                recent_tag_block = recent_tag_block,
                                profile_url = profile_url(course_name, user),
                                course= get_course_info(course_name)
                                )            
                #if there were no errors, we are good to proceed with adding or editing the question
                else:
                    qtags =""
                    for tag in tags:
                        if tag != '':
                            #recompile the tags to a string of pipe-separated tags
                            qtags += tag + '|'

                    if "Submit" in self.request.POST:
                        #if the submit button was pressed...
                        for tag in tags: 
                            #update_tags checks current tags in the db for this class and write them if they don't exist                                                   
                            update_tags(str(tag), course_name)

                        if question_id is not None:
                            #if the question_id exists, then this must be an edit, so fetch the existing question
                            #get_question_by_id returns a question object, can be found in dbops.py
                            question = get_question_by_id(question_id, course_name)
                            if user.user_id != question.user_id:
                                #need to make sure the user is the owner of the question
                                #if the user doesn't own this question he is punted back to the question page
                                self.redirect('course/%s/questions/%d' % (course_name,int(question_id)))
                            else:
                                #edit_question can be found in dbops.py
                                edit_question(
                                    title = question_header, 
                                    body = question_text, 
                                    tags = qtags,
                                    question_id = question_id, 
                                    course_name = course_name)                                    
                                self.redirect("/course/%s/questions/%d" % (course_name,int(question_id)))
                        else:
                            #otherwise, this is a new question that we need to create in the db
                            question_id = new_question(
                                            title = question_header,
                                            body = question_text,
                                            user_id = user.user_id,
                                            tags = qtags,
                                            course_name = course_name)         
                            
                            self.redirect("/course/%s/questions/%d" % (course_name,question_id))

                    if "Preview" in self.request.POST:
                        #if the preview button was pressed...
                        

                        #the preview msg is a block of html injected at the bottom of the page
                        #preview is agnostic towards new questions/editing questions
                        tag_block = ""
                        for tag in tags:
                            if tag != "":
                                tag_class = tag_check(special_check =tag)
                                #this is the standard tag block <ul> element I'm always using, so for each tag there is a <li>
                                tag_block += '''
                                <li class="pager question-tags %s pull-left">
                                    <a href="/course/%s/discussion?tag=%s" style="padding:0 5px">%s</a>
                                </li>
                                ''' % (tag_class, course_name, tag,tag)

                        preview_msg = """
                        <div class="page-header row-fluid">
                            <h2>Preview<small> if you make changes, click preview again to refresh</small></h2></div>
                        <div>
                            <div style="margin-bottom:0">
                                <p class="question-title">%s</p>
                            </div>
                            <ul class="pager pull-left" style="margin:2px">%s</ul>
                            <br>  <br>                          
                            <p>%s</p>
                        </div>
                        """ % (question_header, tag_block, spaceit(cgi.escape(question_text)))
                        #notice that no errors are rendered because if the input has errors it would have been
                        #punted above and the preview not shown...
                        self.render('addquestion.html',
                                question_header = question_header,
                                question_text = question_text,
                                preview_msg = preview_msg,
                                tags = tags,
                                recent_tag_block= recent_tag_block,
                                profile_url = profile_url(course_name, user),
                                course= get_course_info(course_name))

        
class IndividualQuestion(MainHandler):
    #handler for rendering individual questions and their associated answers
    def get(self, course_name, question_id):        
        @self.login_required
        def secured_things(user):
            if self.valid_course(course_name):
                vote_alert = ""  
                #get the user's history of voting for this question          
                vote_history = get_vote_history(question_id = question_id, user_id = user.user_id, course_name = course_name)
                qbtn_type = "btn-info"
                if vote_history is not None:
                    #if the user has already voted (or if he owns the question) the voting options will be for him disabled
                    if vote_history != "selfish":
                        if vote_history == 'down':
                            label_type = "label-important"
                        else:
                            label_type = "label-success" 
                        vote_remove_link = '/course/%s/questions/%d/vote_remove?rep=%s' % (course_name, int(question_id),vote_history)             
                        #if he has already voted, a label will appear indicating so and also have a link to remove the vote if desired
                        vote_alert = '''
                            <span class="label %s" style="font-size:9pt">
                                You voted this question %s 
                            </span>
                            <br>
                            <h6><a href="%s">remove vote</a></h6>
                        ''' % (label_type, vote_history, vote_remove_link)
                    qbtn_type = "disabled"
                    vote_up_link, vote_down_link = "", ""
                else:
                    #if there is no vote_history then the following links are behind the buttons
                    #these links are handled by my voting handlers below (QuestionVote and AnswerVote)
                    vote_up_link = "href ='/course/%s/questions/%d/vote?rep=up'" % (course_name, int(question_id))
                    vote_down_link = "href ='/course/%s/questions/%d/vote?rep=dn'" % (course_name,int(question_id))

                #Errors will have been inserted by the answer-post form below
                error = self.request.get('error')
                #previews will have been inserted by the answer-post form below
                preview = self.request.get('preview')
                previous_answer = ""
                alert_msg = ""
                if error != "":
                    #if there is an error, something is wrong with the answer the user just tried to submit
                    #the user's previous answer is temp. stored in memcached and then promptly deleted
                    previous_answer = memcache.get(str(user.user_id)+'badA'+str(question_id))
                    if previous_answer is None:
                        previous_answer = ""
                    memcache.delete('user.user_id'+'badA'+str(question_id))
                    #the error msg is displayed again as a bootstrap alert
                    alert_msg = r'''
                    <div class="alert alert-error">
                        <a class="close" data-dismiss="alert" href="#">&times;</a>
                        <h4 class="alert-heading">Oh snap!</h4>
                        %s ... 
                    </div>
                    ''' % error 
                preview_msg = ""
                if preview:
                    #similar to the error case, if the preview button was pressed, the user's previous answer is saved
                    #to a temp. memcache entry and then promptly deleted
                    previous_answer = memcache.get(str(user.user_id) + 'prev' + str(question_id))
                    preview_msg = """
                        <div class="page-header span12">
                            <h2>Preview<small> if you make changes, click preview again to refresh</small></h2>                        
                        </div>
                        <div class="span12">                        
                            <p>%s</p>
                        </div>
                    """ % spaceit(cgi.escape(previous_answer))
                    memcache.delete(str(user.user_id) + 'prev' + str(question_id))

                #we need the current question object as well as all the answers associated
                question = get_question_by_id(question_id, course_name)
                answers = get_answers_by_question_id(question_id, course_name)
                answer_tuple = []
                if answers:
                    for answer in answers:
                        #each answer item is injected into a temp. tuple along with that answer's score
                        #I do this because the score is saved in shards in a separate db and not as a property in the
                        #answer entity (doing so would eliminate the benifit of sharded counting)
                        #of course the purpose of this is to sort the list based on the score...
                        answer_tuple.append([
                            answer,
                            get_answer_score(
                                question_id= question_id, 
                                answer_id=str(answer.key().id()), 
                                course_name = course_name) 
                            ])                  

                    answer_tuple = sorted(answer_tuple, key = itemgetter(1), reverse = True)
                    #answer_tuple is sorted based on the answer score
                    
                answer_block = ""
                if answers:
                    for item in answer_tuple:
                        answer = item[0]
                        #we fetch back the first item of the temp answer_tuple which is the original answer object
                        answer_id = str(answer.key().id())
                        avote_history = get_vote_history(
                            question_id = question_id, 
                            answer_id = answer_id, 
                            user_id = user.user_id,
                            course_name = course_name)
                        abtn_type = "btn-info"
                        avote_alert = ""
                        if avote_history is not None:
                            #this is similar to the question voting behavior above. If a user has already voted for an answer
                            #or if the user owns the answer the voting options are disabled
                            if avote_history != "selfish":
                                if avote_history == 'down':                                    
                                    label_type = "label-important"
                                else: 
                                    label_type = "label-success"
                                avote_remove_link = '/course/%s/questions/%d/%d/vote_remove?rep=%s' % (course_name, int(question_id), int(answer_id), avote_history) 
                                #user is reminded that they voted for this answer and are given the option to remove
                                avote_alert = '''
                                    <span class="label %s" style = "font-size:8pt">
                                    You voted this answer %s
                                    </span>
                                    <h6><a href ="%s">remove vote</a></h6>
                                ''' % (label_type, avote_history, avote_remove_link)
                            abtn_type = "disabled"
                            a_up_link, a_dn_link = "", ""
                        else:
                            #just like the question voting above, these will redirect to the vote handlers (QuestionVote and AnswerVote)
                            a_up_link = "href='/course/%s/questions/%d/%d/vote?rep=up'" % (course_name, int(question_id),int(answer_id))
                            a_dn_link = "href='/course/%s/questions/%d/%d/vote?rep=dn'" % (course_name, int(question_id),int(answer_id))
                        aedit_link = ""

                        if avote_history == "selfish":
                            #if the user owns the answer they are allowed to edit it!
                            aedit_link = "<a href='/course/%s/questions/%d/%d/edit'>Edit your Answer</a>" % (course_name, int(question_id), int(answer_id))
                        #This is the answer block - it is iterated for each answer stored for this question                        
                        answer_block += '''
                        <div>
                            <div class = "page-header row-fluid">
                                <div class = "span1">
                                    <div style = "width:60px" class="pull-left">
                                        <a %s>
                                            <div class="vote-icon upvote-icon"></div>
                                        </a>
                                        <div class="vote-score">
                                            %s
                                        </div>
                                        <a %s>
                                            <div class="vote-icon downvote-icon"></div>
                                        </a>
                                    </div>
                                </div>              
                                <div class = "span11">                                                           
                                    <p class="answer-body">%s</p>
                                    <br> 
                                    <h6>%s</h6>
                                    %s 
                                    <div class="pull-right">
                                        <p style="color:#999">answered by <a href="/course/%s/profile/%d">%s</a> %s</p>
                                          
                                    </div>
                                     
                                                   
                                </div>
                            </div> 
                        </div>
                        <br>
                        ''' % (
                            a_up_link, item[1], a_dn_link,                       
                            spaceit(cgi.escape(answer.body)),
                            aedit_link, avote_alert,
                            course_name, 
                            int(answer.user_id),
                            get_user_nickname(answer.user_id),
                            get_time_ago_string(answer.last_modified)
                            
                            )                            
                #get the current vote score of the question
                score = get_question_score(question_id, course_name)
                edit_link = ""
                if question.user_id == user.user_id:
                    #if the user owns the question they can edit it 
                    edit_link = "<a href='/course/%s/questions/%d/edit'>Edit your Question</a>" % (course_name, int(question_id))
                
                #tags for indiv. questions are in the question object, easy to fetch
                tags = question.tags
                tags = tags.split('|')
                tag_block = ""
                for tag in tags:
                    if tag != "":
                        #this is the standard tag block <ul> element I'm always using, so for each tag there is a <li>
                        tag_class = tag_check(special_check=tag)
                        tag_block += '''
                        <li class="pager %s pull-left">
                            <a href="/course/%s/discussion?tag=%s" style="padding:0 5px">%s</a>
                        </li>
                        ''' % (tag_class, course_name, tag,tag)


                #there is a ton of information injected into the indiv_question template)               
                self.render("individual_question.html", 
                            question_title = question.title,
                            question_body = spaceit(cgi.escape(question.body)), 
                            qbtn_type = qbtn_type,
                            answer_block = answer_block,
                            vote_up = vote_up_link, 
                            vote_down = vote_down_link,
                            score = score,
                            answer = previous_answer,
                            bad_answer_alert = alert_msg,
                            user_who_asked = get_user_nickname(question.user_id),
                            preview_msg = preview_msg,
                            vote_alert = vote_alert,
                            edit_link = edit_link,
                            tag_block = tag_block,
                            question_time = get_time_ago_string(question.created),
                            user_id = question.user_id,
                            course= get_course_info(course_name),
                            profile_url = profile_url(course_name, user)
                            )
            
    def post(self, course_name, question_id):
        #this handles answer submissions to individual questions
        @self.login_required
        def secured_things(user):
            if self.valid_course(course_name):
                error = ''
                #get the answer text from form submission
                answer_text = self.request.get('answer_text')
               
                #make sure the answer isn't blank!
                if not answer_text:
                    error = '?error=You left your answer blank!'

                #Check the answer text for latex errors, latex_check() can be found in dbops.py
                latex_error = latex_check(answer_text, 'answer')
                if latex_error is not None:
                    error = '?error=%s' % latex_error

                #If there are any errors, pass back the form with errors in query parameters (set above as ?error=) 
                #the bad answer is set in the cache and red back by IndividualQuestion handler above
                if error != '': 
                    memcache.set(str(user.user_id)+'badA'+str(question_id),answer_text)
                    self.redirect("/course/%s/questions/%d%s" % (course_name, int(question_id),error))

                else:
                    #If the submit button was pressed, create a new answer object in the db. create_answer() can be found in dbops.py
                    if "Submit" in self.request.POST:       
                        create_answer(
                            question_id = question_id, 
                            answer_text = answer_text, 
                            user_id = user.user_id, 
                            course_name = course_name)                  
                        self.redirect("/course/%s/questions/%d" % (course_name, int(question_id)))

                    #If the preview button was pressed, pass back the form with the preview answer set in the cache
                    if "Preview" in self.request.POST:                                   
                        memcache.set(str(user.user_id) + 'prev' + str(question_id), answer_text)
                        self.redirect("/course/%s/questions/%d?preview=True#AnswerForm" % (course_name, int(question_id)))

class AnswerEdit(MainHandler):
    def get(self, course_name, question_id, answer_id):
        @self.login_required
        def secured_things(user):
            if self.valid_course(course_name):
                answer = get_answer(answer_id, question_id, course_name)
                if answer.user_id == user.user_id:
                    #check to make sure the current user owns the answer                        
                    self.render('edit_answer.html', 
                        answer_text = answer.body,
                        profile_url = profile_url(course_name, user),
                        course= get_course_info(course_name))
                else:
                    #current user does not own the answer, sent back to question page
                    self.redirect("/course/%s/questions/%d" % (course_name,int(question_id)))

    def post(self, course_name, question_id, answer_id):
        @self.login_required
        def secured_things(user):
            if self.valid_course(course_name):
                answer_text = self.request.get('answer_text')
                results = re.findall('\$\$',answer_text)
                error = ""
                if not answer_text:
                    error = "You left your answer blank..."
                else:
                    if len(results) % 2 != 0:
                        error = "There's a problem with your LATEX code..."
                if error != "":
                    alert_msg = r'''
                        <div class="alert alert-error">
                            <a class="close" data-dismiss="alert" href="#">&times;</a>
                            <h4 class="alert-heading">Oh snap!</h4>
                            %s 
                        </div>
                        ''' % error
                    self.render('edit_answer.html', 
                        alert_msg = alert_msg, 
                        answer_text = answer_text,
                        profile_url = profile_url(course_name, user),
                        course= get_course_info(course_name))

                else:
                    if "Submit" in self.request.POST:
                        new_answer = self.request.get('answer_text')
                        edit_answer(new_answer, answer_id, question_id, course_name)
                        self.redirect('/course/%s/questions/%d' % (course_name, int(question_id)))

                    if "Preview" in self.request.POST:
                        answer = get_answer(answer_id, question_id, course_name)
                        edited_answer = self.request.get('answer_text')
                        
                        preview_msg = """
                                <div class="page-header span12">
                                    <h2>Preview<small> if you make changes, click preview again to refresh</small></h2>                        
                                </div>
                                <div class="span12">                        
                                    <p>%s</p>
                                </div>
                            """ % spaceit(cgi.escape(edited_answer))

                        self.render('edit_answer.html', 
                            answer_text = edited_answer, 
                            preview_msg = preview_msg,
                            profile_url = profile_url(course_name, user),
                            course= get_course_info(course_name))

class QuestionVote(MainHandler):
    def get(self, course_name, question_id):
        @self.login_required
        def secured_things(user):
            if self.valid_course(course_name):
                tally = self.request.get('rep')
                if tally == 'up':
                    increment_question_score(1,question_id, user.user_id, course_name)
                if tally == 'dn':
                    increment_question_score(-1,question_id, user.user_id, course_name)
                                         
                self.redirect("/course/%s/questions/%d" % (course_name, int(question_id)))

class QuestionVoteRemove(MainHandler):
    def get(self, course_name, question_id):
        @self.login_required
        def secured_things(user):
            if self.valid_course(course_name):
                tally = self.request.get('rep')
                if tally == 'down':
                    increment_question_score(1, question_id, user.user_id, course_name, clear = True)
                if tally == 'up':
                    increment_question_score(-1, question_id, user.user_id, course_name, clear = True)
                self.redirect("/course/%s/questions/%d" % (course_name, int(question_id)))

class AnswerVote(MainHandler):
    def get(self, course_name, question_id, answer_id):
        @self.login_required
        def secured_things(user):
            if self.valid_course(course_name):
                tally = self.request.get('rep')
                if tally == 'up':
                    increment_answer_score(1,answer_id, question_id, user.user_id, course_name)
                if tally == 'dn':
                    increment_answer_score(-1,answer_id, question_id, user.user_id, course_name)
            self.redirect("/course/%s/questions/%d" % (course_name, int(question_id)))

class AnswerVoteRemove(MainHandler):
    def get(self, course_name, question_id, answer_id):
        @self.login_required
        def secured_things(user):
            if self.valid_course(course_name):
                tally = self.request.get('rep')
                if tally == 'down':
                    increment_answer_score(1,answer_id, question_id, user.user_id, course_name, clear = True)
                if tally == 'up':
                    increment_answer_score(-1,answer_id, question_id, user.user_id, course_name, clear = True)
                self.redirect("/course/%s/questions/%d" % (course_name, int(question_id)))
        

