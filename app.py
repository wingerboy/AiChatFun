from flask import Flask, request, jsonify
from chatgpt import ChatGPT, MessageGenerator
from interface import PaperAssistant
from paper import Paper
from logger import log
from config import conf


app = Flask(__name__)
app.config['TIMEOUT'] = 200000 # 如果是Flask（python app.py启动）-生效。 如果是Django（gunicorn启动）-为gunicorn配置文件timeout

@app.route('/request_paper_summary', methods=['GET', 'POST'])
def paper_summary():
    res = {'ret': -1, 'data': "", 'msg': ''}
    if request.method == 'POST':
        params = request.get_json()
        api_key = params['apiKey']
        paper_link = params['link']
        conf.api_key = api_key
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

        return jsonify(res)
    else:
        res['msg'] = 'Get request not allowed'
        return jsonify(res)


if __name__ == '__main__':
    app.run(port=8000)

# 启动命令 gunicorn -c gunicorn_config.py app:app
