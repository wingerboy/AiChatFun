from flask import Flask, request
from chatgpt import ChatGPT, MessageGenerator
from paper import Paper


app = Flask(__name__)

@app.route('/request_paper_summary', methods=['GET', 'POST'])
def paper_summary():
    res = {'ret': -1, 'data': "", 'msg': ''}
    if request.method == 'POST':
        api_key = request.form.get('apiKey', '')
        paper_link = request.form.get('link', '')
        if api_key == '' or paper_link == '':
            res['msg'] = 'Empty parameter, link: %s, api_key: %s' % (paper_link, api_key)
        else:
            res['data'] = PaperAssistant().paper_summary_chatgpt(Paper(download_url=paper_link))

        return res
    else:
        res['msg'] = 'Get request not allowed'
        return res


if __name__ == '__main__':
    app.run(port=8000)
