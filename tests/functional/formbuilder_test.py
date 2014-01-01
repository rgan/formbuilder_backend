import json
import unittest
import uuid
from boto.dynamodb2.table import Table
from formbuilder.models.answer import Answer
import requests

class FormBuilderTest(unittest.TestCase):

    URL = "http://localhost:5000"

    def setUp(self):
        self.user_id = "unit_test"
        self.question_id = uuid.uuid1().hex
        question_data = { "question_id": self.question_id, "type": "essay", "question": "What is difference between unit and functional tests?" }
        Table("questions").put_item(data=question_data)
        self.form_id = uuid.uuid1().hex
        forms_data = { "form_id" : self.form_id, "name" : "Unit testing",
                       "questions" : set([self.question_id])}
        Table("forms").put_item(data=forms_data)
        answer_data = {"form_question_id" : Answer.form_question_id(self.form_id, self.question_id),
                                        "answer": "This is a test",
                                        "user_id" : self.user_id}
        Table("answers").put_item(data=answer_data)

    def test_get_should_return_form_with_answers(self):
        response = requests.get("%s/forms/%s/users/%s" % (self.URL, self.form_id, self.user_id))
        self.assertEquals(200, response.status_code)
        response_json = json.loads(response.text)
        self.assertEquals("Unit testing", response_json["name"])
        self.assertEquals(self.form_id, response_json["id"])
        self.assertEquals(1, len(response_json["questions"]))
        self.assertEquals(self.question_id, response_json["questions"][0]["question_id"])
        self.assertEquals("essay", response_json["questions"][0]["type"])
        self.assertEquals("What is difference between unit and functional tests?", response_json["questions"][0]["question"])
        self.assertEquals("This is a test", response_json["questions"][0]["answer"])

    def test_post_should_update_answers(self):
        post_data = { "questions": [{ "question_id": self.question_id, "answer": "This is a test - updated"}]}
        response = requests.post("%s/forms/%s/users/%s" % (self.URL, self.form_id, self.user_id), data=json.dumps(post_data))
        self.assertEquals(200, response.status_code)
        item = Table("answers").get_item(form_question_id = Answer.form_question_id(self.form_id, self.question_id),
                                            user_id=self.user_id)
        self.assertEquals("This is a test - updated", item["answer"])

    def tearDown(self):
        Table("answers").delete_item(user_id=self.user_id, form_question_id=Answer.form_question_id(self.form_id, self.question_id))
        Table("forms").delete_item(form_id=self.form_id)
        Table("questions").delete_item(question_id=self.question_id)
