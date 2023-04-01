from flask import Flask, request, jsonify
from chatgpt import ChatGPT, MessageGenerator
from interface import PaperAssistant
from paper import Paper
from logger import log
from config import conf
import time
import os


app = Flask(__name__)
app.config['TIMEOUT'] = 200000 # 如果是Flask（python app.py启动）-生效。 如果是Django（gunicorn启动）-为gunicorn配置文件timeout
app.config['UPLOAD_FOLDER'] = conf.upload_dir


def download_from_url(url):
    import requests

    """ 根据论文id将论文下载到本地

    Parameters
    -----------
    paper_id: str
        论文id
    file_name: Optional[str]
        本地文件名，如果为空则用论文id做文件名

    Returns
    -------
    result: Optional[str]
        论文下载结果。成功则返回本地文件路径，失败则返回None
    """
    # paper_url = "https://arxiv.org/pdf/2303.12060.pdf"
    target_name = conf.account + '_upload_' + str(int(time.time())) + '.pdf'
    target_path = os.path.join(conf.upload_dir, target_name)
    try:
        res = requests.get(url=url)
        if res.status_code == 200:
            with open(target_path, "wb") as f:
                f.write(res.content)
                return 0, target_path
        return -1, ''
    except Exception as e:
        log.error(f'Input paper url error, {e}')
        return -1, e


@app.route('/request_paper_summary', methods=['GET', 'POST'])
def paper_summary():
    res = {'ret': -1, 'data': "", 'msg': ''}
    if request.method == 'POST':
        params = request.get_json()
        api_key = params['apiKey']
        paper_link = params['link']
        paper_uploaded = params['fileName']
        conf.api_key = api_key
        log.info(f'input parameter, api_key: {api_key}, paper_upload: {paper_uploaded}, paper_link: {paper_link}')
        if api_key == '':
            res['msg'] = 'Please input your API KEY'
            return jsonify(res)

        paper_file = ''
        if paper_uploaded == '':
            res['ret'], paper_file = download_from_url(paper_link)
        else:
            paper_file = paper_uploaded
            res['ret'] = 0 if os.path.exists(paper_file) else -1

        if res['ret'] == -1 or not os.path.exists(paper_file) :# 文件为空
            res['msg'] = 'Please upload file or input paper link'
            return jsonify(res)

        try:
            # res['data'] = PaperAssistant().paper_summary_chatgpt(Paper(file_path=paper_file))
            # res['msg'] = 'ok'
            # res['ret'] = 0
            res = {"data":"1. Title: VideoXum: Cross-modal Visual and Textural Summarization of Videos (\u89c6\u89c9\u548c\u6587\u672c\u53cc\u6a21\u6001\u89c6\u9891\u6458\u8981\u7684VideoXum)\n                     \n                     \n2. Authors: Mengyue Wu, Jingwen Bian, Lin Ma, Yanfeng Wang, Xiaodan Liang, Xiaoyong Shen, Eric P. Xing\n\n                     \n3. Affiliation: Department of Machine Intelligence, Tencent Technology Co., Ltd. (\u817e\u8baf\u79d1\u6280\u6709\u9650\u516c\u53f8)\n\n                     \n4. Keywords: Video summarization, Cross-modal, Language model, Dataset\n\n                     \n5. Urls: \nPaper: https://arxiv.org/pdf/2303.12060.pdf\nGithub: None\n\n                     \n6. Summary: \n\n(1): \u672c\u6587\u7814\u7a76\u80cc\u666f\u662f\u4f20\u7edf\u7684\u89c6\u9891\u6458\u8981\u65b9\u6cd5\u53ea\u80fd\u6458\u9009\u91cd\u8981\u7247\u6bb5\u6216\u751f\u6210\u89c6\u9891\u6807\u9898\uff0c\u800c\u65e0\u6cd5\u5b9e\u73b0\u89c6\u9891\u5185\u5bb9\u4e0e\u81ea\u7136\u8bed\u8a00\u4e4b\u95f4\u7684\u7cbe\u786e\u5bf9\u9f50\u3002\n\n(2): \u8fc7\u53bb\u7684\u65b9\u6cd5\u5c06\u89c6\u9891\u6458\u8981\u548c\u6587\u672c\u6458\u8981\u89c6\u4e3a\u4e24\u4e2a\u72ec\u7acb\u7684\u4efb\u52a1\uff0c\u65e0\u6cd5\u6709\u6548\u5efa\u7acb\u89c6\u9891\u4e0e\u6587\u672c\u4e4b\u95f4\u7684\u8054\u7cfb\u3002\u867d\u7136\u65e9\u671f\u66fe\u6709\u90e8\u5206\u7814\u7a76\u4ec5\u5bf9\u957f\u89c6\u9891\u8fdb\u884c\u89c6\u9891\u53ca\u6587\u672c\u6458\u8981\uff0c\u4f46\u8be5\u65b9\u6cd5\u672a\u80fd\u4fdd\u8bc1\u751f\u6210\u7684\u89c6\u9891\u548c\u6587\u672c\u6458\u8981\u7684\u8bed\u4e49\u5bf9\u9f50\u3002\u5728\u6b64\u80cc\u666f\u4e0b\uff0c\u672c\u6587\u65e8\u5728\u901a\u8fc7\u5efa\u7acb\u5927\u89c4\u6a21\u6570\u636e\u96c6\uff0c\u63d0\u51fa\u8de8\u6a21\u6001\u89c6\u9891\u6458\u8981\u6765\u4f18\u5316\u6b64\u95ee\u9898\u3002\n\n(3): \u9996\u5148\uff0c\u5728\u8457\u540d\u7684ActivityNet Captions\u4e0a\u6784\u5efa\u4e86\u4e00\u4e2a\u65b0\u7684\u6570\u636e\u96c6VideoXum\uff0c\u4ecb\u6b21\u6570\u636e\u96c6\u7684\u89c6\u9891\u548c\u6587\u672c\u5206\u522b\u76f8\u4e92\u5bf9\u9f50\uff0c\u5171\u670914K\u4e2a\u957f\u89c6\u9891\u548c140K\u5bf9\u89c6\u9891/\u6587\u672c\u5bf9\uff0c\u53ef\u4ee5\u4f7f\u5f97\u89c6\u9891\u5185\u5bb9\u4e0e\u6587\u672c\u8bed\u4e49\u4e0a\u5bf9\u9f50\u3002\u6839\u636e\u751f\u6210\u6458\u8981\u7684\u6a21\u5f0f\uff0c\u672c\u6587\u5c06\u8de8\u6a21\u6001\u6458\u8981\u5206\u4e3a\u4e09\u4e2a\u5b50\u4efb\u52a1\uff1a\n(1) \u89c6\u9891\u5230\u89c6\u9891\u6458\u8981\uff0c\u76ee\u6807\u662f\u4ece\u6e90\u89c6\u9891\u4e2d\u63d0\u53d6\u91cd\u8981\u7684\u7247\u6bb5\uff0c\u751f\u6210\u6e90\u89c6\u9891\u7684\u6982\u8c8c\u7248\u672c\uff1b\n(2) \u89c6\u9891\u5230\u6587\u672c\u6458\u8981\uff0c\u76ee\u6807\u662f\u603b\u7ed3\u6e90\u89c6\u9891\u7684\u4e3b\u8981\u5185\u5bb9\u5e76\u751f\u6210\u7b80\u77ed\u7684\u6587\u672c\u63cf\u8ff0\uff1b\n(3) \u89c6\u9891\u5230\u89c6\u9891\u548c\u6587\u672c\u6458\u8981\uff1a\u4efb\u52a1\u9700\u8981\u6a21\u578b\u540c\u65f6\u5b8c\u6210\u4ece\u6e90\u89c6\u9891\u4e2d\u603b\u7ed3\u77ed\u89c6\u9891\u548c\u76f8\u5173\u53d9\u8ff0\u4e24\u79cd\u6458\u8981\u7684\u884c\u52a8\uff0c\u540c\u65f6\uff0c\u4e24\u79cd\u6a21\u6001\u7684\u603b\u7ed3\u8bed\u4e49\u5fc5\u987b\u80fd\u591f\u5f97\u5230\u826f\u597d\u7684\u5bf9\u9f50\u3002\n\n(4): \u57fa\u4e8e\u6b64\u65b9\u6cd5\uff0c\u672c\u6587\u63d0\u51fa\u4e86VTSUM-BLIP\u7684\u7aef\u5230\u7aef\u8de8\u6a21\u6001\u89c6\u9891\u6458\u8981\u6a21\u578b\u3002\u4e3a\u4e86\u5145\u5206\u5229\u7528\u9884\u8bad\u7ec3\u8bed\u8a00\u6a21\u578b\u7684\u5f3a\u5927\u80fd\u529b\uff0c\u672c\u6587\u4f7f\u7528BLIP\u4f5c\u4e3a\u6a21\u578b\u9aa8\u67b6\u3002\u7ed3\u5408HERO\u548c\u65f6\u95f4\u5efa\u6a21\u6a21\u5757\u8bbe\u8ba1\u4e86\u4e00\u79cd\u9ad8\u6548\u7684\u89c6\u9891\u7f16\u7801\u7b56\u7565\uff0c\u53ef\u4ee5\u5bf9\u957f\u89c6\u9891\u8fdb\u884c\u7f16\u7801\u3002\u672c\u6587\u8fd8\u9488\u5bf9\u4e09\u4e2a\u5b50\u4efb\u52a1\u8bbe\u8ba1\u4e86\u4e0d\u540c\u7684\u89e3\u7801\u5668\u8fdb\u884c\u89c6\u9891\u548c\u6587\u672c\u6458\u8981\u3002\u672c\u6587\u7684\u6a21\u5757\u5316\u8bbe\u8ba1\u4f7f\u6211\u4eec\u80fd\u591f\u5728\u4e0d\u6539\u53d8\u9884\u8bad\u7ec3\u6a21\u578b\u7ed3\u6784\u7684\u60c5\u51b5\u4e0b\u6267\u884c\u66f4\u590d\u6742\u7684\u4e0b\u6e38\u4efb\u52a1\u3002\u901a\u8fc7\u5728VideoXum\u4e0a\u8fdb\u884c\u5168\u9762\u5b9e\u9a8c\u5206\u6790\uff0cVTSUM-BLIP\u8fbe\u5230\u4e86\u826f\u597d\u7684\u6027\u80fd\u3002\u6b64\u5916\uff0c\u672c\u6587\u8fd8\u8bbe\u8ba1\u4e86\u4e00\u79cd\u65b0\u7684\u8bc4\u4f30\u6307\u6807VT-CLIPScore\uff0c\u7528\u4e8e\u8bc4\u4f30\u8de8\u6a21\u6001\u6458\u8981\u7684\u8bed\u4e49\u4e00\u81f4\u6027\uff0c\u7ed3\u679c\u663e\u793a\u672c\u6587\u7684\u8bc4\u4f30\u6307\u6807\u4e0e\u4eba\u7c7b\u8bc4\u4f30\u7ed3\u679c\u9ad8\u5ea6\u4e00\u81f4\u3002\u56e0\u6b64\uff0c\u672c\u6587\u4e3b\u8981\u8d21\u732e\u5305\u62ec\uff1a(1)\u6784\u5efa\u4e86\u9002\u5f53\u7684\u6570\u636e\u96c6VideoXum\uff1b(2)\u63d0\u51fa\u4e86\u4e00\u79cd\u65b0\u9896\u7684\u7aef\u5230\u7aef\u89c6\u9891\u6458\u8981\u6a21\u578b\uff1b(3)\u9996\u6b21\u63d0\u51fa\u4e86\u8bc4\u4f30\u8de8\u6a21\u6001\u8bed\u4e49\u4e00\u81f4\u6027\u7684\u65b0\u6307\u6807VT-CLIPscore\u3002\n\n\n7. Methods:\n\n- (1): \u672c\u6587\u63d0\u51fa\u4e86\u4e00\u79cd\u8de8\u6a21\u6001\u89c6\u9891\u6458\u8981\u7684\u65b9\u6cd5\uff0c\u65e8\u5728\u5bf9\u9f50\u89c6\u9891\u548c\u6587\u672c\u7684\u5185\u5bb9\uff0c\u5177\u4f53\u5206\u4e3a\u4e09\u4e2a\u5b50\u4efb\u52a1\uff1a\u89c6\u9891\u5230\u89c6\u9891\u6458\u8981\u3001\u89c6\u9891\u5230\u6587\u672c\u6458\u8981\u3001\u89c6\u9891\u5230\u89c6\u9891\u548c\u6587\u672c\u6458\u8981\u3002\u9488\u5bf9\u6bcf\u4e2a\u5b50\u4efb\u52a1\uff0c\u672c\u6587\u8bbe\u8ba1\u4e86\u4e0d\u540c\u7684\u89e3\u7801\u5668\u3002\u901a\u8fc7\u5efa\u7acb\u5927\u89c4\u6a21\u6570\u636e\u96c6VideoXum\uff0c\u542b140K\u5bf9\u89c6\u9891/\u6587\u672c\u5bf9\uff0c\u53ef\u4ee5\u786e\u4fdd\u89c6\u9891\u5185\u5bb9\u4e0e\u6587\u672c\u8bed\u4e49\u4e0a\u5bf9\u9f50\u3002\n\n- (2): \u57fa\u4e8eVideoXum\u6570\u636e\u96c6\uff0c\u672c\u6587\u63d0\u51fa\u4e86\u4e00\u79cd\u7aef\u5230\u7aef\u7684\u8de8\u6a21\u6001\u89c6\u9891\u6458\u8981\u6a21\u578bVTSUM-BLIP\uff0c\u7ed3\u5408HERO\u3001\u65f6\u95f4\u5efa\u6a21\u3001FFN\u7b49\u591a\u79cd\u65b9\u6cd5\u8fdb\u884c\u9ad8\u6548\u7684\u89c6\u9891\u7f16\u7801\uff0c\u4e3a\u63d0\u53d6\u91cd\u8981\u7279\u5f81\u63d0\u4f9b\u652f\u6301\u3002\u672c\u6587\u5c06BLIP\u4f5c\u4e3a\u6a21\u578b\u9aa8\u67b6\uff0c\u91c7\u7528\u4e0d\u540c\u7684\u89e3\u7801\u5668\u751f\u6210\u89c6\u9891\u548c\u6587\u672c\u7684\u6458\u8981\u3002\n\n- (3): \u4e3a\u4e86\u8bc4\u4f30\u8de8\u6a21\u6001\u6458\u8981\u7684\u8bed\u4e49\u4e00\u81f4\u6027\uff0c\u672c\u6587\u63d0\u51fa\u4e86\u65b0\u7684\u8bc4\u4f30\u6307\u6807VT-CLIPScore\uff0c\u5e76\u5728\u6a21\u578b\u4e0a\u8fdb\u884c\u5168\u9762\u5b9e\u9a8c\u5206\u6790\uff0cVTSUM-BLIP\u8fbe\u5230\u4e86\u826f\u597d\u7684\u6027\u80fd\u3002\u56e0\u6b64\uff0c\u672c\u6587\u4e3b\u8981\u7684\u65b9\u6cd5\u548c\u8d21\u732e\u5305\u62ec\uff1a(1)\u6784\u5efa\u89c4\u6a21\u9002\u5f53\u7684\u6570\u636e\u96c6\uff0c(2)\u63d0\u51fa\u4e00\u79cd\u65b0\u9896\u7684\u7aef\u5230\u7aef\u89c6\u9891\u6458\u8981\u6a21\u578b\uff0c(3)\u9996\u6b21\u63d0\u51fa\u8bc4\u4f30\u8de8\u6a21\u6001\u8bed\u4e49\u4e00\u81f4\u6027\u7684\u65b0\u6307\u6807VT-CLIPscore\u3002\n\n\n8. Conclusion: \n                             \n- (1): \u672c\u6587\u63d0\u51fa\u4e86\u4e00\u79cd\u8de8\u6a21\u6001\u89c6\u9891\u6458\u8981\u7684\u65b9\u6cd5\uff0c\u65e8\u5728\u901a\u8fc7\u5efa\u7acb\u6570\u636e\u96c6\u548c\u5f00\u53d1\u65b0\u7684\u8de8\u6a21\u6001\u6458\u8981\u6a21\u578b\uff0c\u63d0\u5347\u4e86\u89c6\u9891\u548c\u6587\u672c\u5185\u5bb9\u7684\u8bed\u4e49\u5bf9\u9f50\u6027\u3002\u540c\u65f6\uff0c\u672c\u6587\u9996\u6b21\u63d0\u51fa\u4e86\u4e00\u4e2a\u65b0\u7684\u8bc4\u4f30\u6307\u6807VT-CLIPScore\u7528\u4e8e\u8bc4\u4f30\u8de8\u6a21\u6001\u6458\u8981\u7684\u8bed\u4e49\u4e00\u81f4\u6027\uff0c\u5177\u6709\u91cd\u8981\u7684\u5b9e\u9645\u5e94\u7528\u4ef7\u503c\u3002\n                     \n- (2): \u521b\u65b0\u70b9\u65b9\u9762\uff0c\u672c\u6587\u63d0\u51fa\u4e86\u8de8\u6a21\u6001\u89c6\u9891\u6458\u8981\u7684\u65b0\u6982\u5ff5\uff0c\u5e76\u6210\u529f\u5e94\u7528\u4e8e\u5927\u89c4\u6a21\u6570\u636e\u96c6VideoXum\u4e0a\u3002\u5728\u6027\u80fd\u6307\u6807\u65b9\u9762\uff0c\u672c\u6587\u7684\u6a21\u578bVTSUM-BLIP\u5728\u5404\u9879\u8bc4\u4f30\u6307\u6807\u4e0a\u5177\u6709\u660e\u663e\u4f18\u52bf\uff0c\u8fbe\u5230\u4e86\u8f83\u597d\u7684\u5b9e\u9a8c\u6548\u679c\u3002\u5728\u5de5\u4f5c\u91cf\u65b9\u9762\uff0c\u7531\u4e8e\u672c\u6587\u63d0\u4f9b\u7684\u6570\u636e\u96c6\u89c4\u6a21\u9002\u5f53\uff0c\u80fd\u591f\u786e\u4fdd\u89c6\u9891\u5185\u5bb9\u4e0e\u6587\u672c\u8bed\u4e49\u4e0a\u5bf9\u9f50\uff0c\u4ece\u800c\u53ef\u4ee5\u6709\u6548\u63d0\u9ad8\u6a21\u578b\u7684\u8bad\u7ec3\u6548\u7387\u548c\u63a8\u7406\u901f\u5ea6\u3002\u4f46\u662f\uff0c\u8be5\u6a21\u578b\u4ecd\u5b58\u5728\u4e00\u4e9b\u6f5c\u5728\u7684\u95ee\u9898\uff0c\u4f8b\u5982\u6a21\u578b\u7684\u6cdb\u5316\u80fd\u529b\u6709\u5f85\u63d0\u9ad8\uff0c\u9700\u8981\u8fdb\u4e00\u6b65\u4f18\u5316\u6a21\u578b\u7684\u7ed3\u6784\u548c\u7b97\u6cd5\u3002","msg":"ok","ret":0}
        except Exception as e:
            log.error(f"Request error: {e}")
            res['msg'] = e

        return jsonify(res)
    else:
        res['msg'] = 'Get request not allowed'
        return jsonify(res)


@app.route('/request_paper_upload', methods=['POST'])
def paper_upload():
    res = {'ret': -1, 'data': "", 'msg': ''}
    # 检查请求是否包含文件
    if 'file' not in request.files:
        res['msg'] = 'No file uploaded'
        return jsonify(res)

    # 从请求中获取文件对象
    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    
    # 将文件保存到指定目录中
    filename = conf.account + '_' + str(int(time.time())) + '_' + filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # print("filepath:", filepath)
    uploaded_file.save(filepath)
    res['msg'] = 'File uploaded successfully'
    res['data'] = filepath
    res['ret'] = -1
    
    # 响应客户端请求
    return jsonify(res)


if __name__ == '__main__':
    app.run(port=8000)

# 启动命令 gunicorn -c gunicorn_config.py app:app
