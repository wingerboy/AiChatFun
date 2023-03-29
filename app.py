from flask import Flask, request
from chatgpt import ChatGPT, MessageGenerator
from paper import Paper
from logger import log


app = Flask(__name__)

@app.route('/request_paper_summary', methods=['GET', 'POST'])
def paper_summary():
    res = {'ret': -1, 'data': "", 'msg': ''}
    if request.method == 'POST':
        params = request.get_json()
        api_key = params['apiKey']
        paper_link = params['link']
        log.debug(f'input parameter, api_key: {api_key}, paper_link: {paper_link}')
        if api_key == '' or paper_link == '':
            res['msg'] = 'Empty parameter, link: %s, api_key: %s' % (paper_link, api_key)
        else:
            try:
                res['data'] = PaperAssistant().paper_summary_chatgpt(Paper(download_url=paper_link))
                res['msg'] = 'ok'
                res['ret'] = 0
            except Exception as e:
                log.error(f"Request error: {e}")
                res['msg'] = e

        return res
    else:
        res['msg'] = 'Get request not allowed'
        return res


if __name__ == '__main__':
    app.run(port=8000)
