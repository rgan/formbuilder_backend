from boto.dynamodb2.table import Table
from formbuilder.models.answer import Answer
from formbuilder.models.question import Question


class Form(object):

    def __init__(self, id=None, name=None, questions=None):
        self.id = id
        self.name = name
        self.questions = questions

    @classmethod
    def from_id(cls, id):
        forms_table = Table("forms")
        form_item = forms_table.get_item(form_id=id)
        return Form(id=id, name=form_item["name"], questions=Question.from_ids(form_item["questions"]))

    def update_with_answers(self, user_id):
        answers_table = Table("answers")
        for q in self.questions:
            answer_item = answers_table.get_item(user_id=user_id, form_question_id=Answer.form_question_id(self.id, q.id()))
            q.update_with_answer(answer_item["answer"] if len(answer_item.items()) > 0 else "")


    def as_dict(self):
        return { "id": self.id, "name": self.name, "questions" : [q.as_dict() for q in self.questions]}