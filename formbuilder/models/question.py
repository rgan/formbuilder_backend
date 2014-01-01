import json
from boto.dynamodb2.table import Table

class Question(object):

    def __init__(self, items):
        self.content = {}
        for field, val in items:
            self.content[field] = val

    def id(self):
        return self.content["question_id"]

    def update_with_answer(self, answer):
        self.content.update({"answer": answer})

    @classmethod
    def get_question_type(cls, items):
        for field, val in items:
            if field == "type":
                return val
        raise Exception("Type attribute not found in question")

    @classmethod
    def create_question(cls, items):
        if cls.get_question_type(items) == "choice":
            return ChoiceQuestion(items)
        else:
            return Question(items)

    @classmethod
    def from_ids(cls, ids):
        question_table = Table("questions")
        questions = []
        for id in ids:
            questions.append(cls.create_question(question_table.get_item(question_id=id).items()))
        return questions

    def as_dict(self):
        return self.content

class ChoiceQuestion(Question):

    def __init__(self, items):
        self.content = {}
        for field, val in items:
            if field == "choices":
                self.content[field] = json.loads(val)
            else:
                self.content[field] = val