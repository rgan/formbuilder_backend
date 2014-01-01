from boto.dynamodb2.items import Item
from boto.dynamodb2.table import Table

class Answer(object):

    @classmethod
    def update(cls, form_id, user_id, answer_json):
        answers_table = Table("answers")
        questions_with_answers = answer_json["questions"]
        for question_with_answer in questions_with_answers:
            item = Item(answers_table, data = { "form_question_id" : cls.form_question_id(form_id, question_with_answer["question_id"]),
                                        "answer": question_with_answer["answer"],
                                        "user_id" : user_id})
            item.save(overwrite=True)

    @classmethod
    def form_question_id(cls, id, question_id):
        return "%s_%s" % (id, question_id)