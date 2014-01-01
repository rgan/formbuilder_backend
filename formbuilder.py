import json
from flask import Flask
from flask import request
from formbuilder.models.answer import Answer
from formbuilder.models.form import Form

app = Flask(__name__)

@app.route('/forms/<form_id>/users/<user_id>', methods=['GET', 'POST'])
def get_or_post(form_id, user_id):
    if request.method == 'POST':
        Answer.update(form_id, user_id, json.loads(request.data))
        return request.data
    else:
        form = Form.from_id(form_id)
        form.update_with_answers(user_id)
        return json.dumps(form.as_dict())

if __name__ == "__main__":
    app.run()