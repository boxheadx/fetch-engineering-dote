import requests
import json

r=requests.Session()

host="api.engineeringdote.com"

endpoints={
    "subjects":"/subject",
    "qbank":"/qbank/start-exam",
    "questions":"/exam/questions"
}


token="Bearer 5JFL9WPpTinpI5oAG3TNtKL6JfvRsSV175dQ5gtn55EJRtY11jFjHB4xdoF7"

headers={
    "Authorization": token
}

subjects = r.get("https://" + host + endpoints.get('subjects'), headers=headers)

def chapters(subject, unit):
    chapts=[]
    sub_unit=json.loads(subjects.text)[subject].get('units')[unit-1].get('chapters')
    for i in range(len(sub_unit)):
        chapts.append([sub_unit[i].get('id'),sub_unit[i].get('name')])
    return chapts

def fetch_questions(subject, unit, chapter, marks):
    exam_init_datas={
        "familarity":"all",
        "noOfQuestions":"150",
        "marks":str(marks),
        "examType":"practice",
        "chapters":chapters(subject,unit)[chapter-1][0]
    }

    qbank = r.post("https://" + host + endpoints.get('qbank'), headers=headers, data=exam_init_datas)
    examSessionId=json.loads(qbank.text).get('examSessionId')

    qn_id=json.loads(qbank.text).get('questions')

    qn_id_str = [str(qn) for qn in qn_id]

    qn_fetch_datas={
        "sessionID": str(examSessionId),"questionIDs": str(','.join(qn_id_str))
    }

    questions = r.post("https://" + host + endpoints.get('questions'), headers=headers, data=qn_fetch_datas)
    return questions.text

def display_questions(subject,unit,chapter, marks):
    fetched=json.loads(fetch_questions(subject, unit=unit, chapter=chapter, marks=marks))
    for j in range(len(fetched)):
        print(str(fetched[j].get('questionData').get('id')) + " : " + str(fetched[j].get('questionData').get('quest_title')))
        print("(a) " + str(fetched[j].get('questionData').get('ans1_txt')))
        print("(b) " + str(fetched[j].get('questionData').get('ans2_txt')))
        print("(c) " + str(fetched[j].get('questionData').get('ans3_txt')))
        print("(d) " + str(fetched[j].get('questionData').get('ans4_txt')))
        print("(Right Answer) " + str(fetched[j].get('questionData').get('right_answer')))
    

print('Question Fetcher\n1.Physics\n2.Maths\n3.Chemistry\n4.English')
subject = int(input('Subject: '))
unit=int(input('unit: '))
chapter=int(input('chapter: '))
marks=int(input('marks: '))
display_questions(subject-1,unit,chapter,marks)