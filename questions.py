import requests
class Question():
    def __init__(self, id, title, body, user_ask, coin):
        self.id = id
        self.title = title
        self.body = body
        self.user_ask = user_ask
        self.coin = coin

def getQuestions():
    questions = requests.get("http://127.0.0.1:5000/questions").json()
    list_questions = []
    for question in questions:
        id = question['id']
        title = question['title']
        body = question['body']
        user_ask = question['user_ask']
        coin = question['coin']
        new_question = Question(id, title, body, user_ask, coin)
        list_questions.append(new_question)
    return list_questions

def question(list_questions, user_ask):
    for q in list_questions:
        if q.user_ask == user_ask:
            return q