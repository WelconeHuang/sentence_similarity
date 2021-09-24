import sys

# [START functions_helloworld_http]
# [START functions_http_content]
from flask import escape

# https://github.com/fxsjy/jieba
import jieba
import simplejson as json
import cmath


def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args
    # print(f"request_args:{request_args}")

    sentence_1 = "我喜欢看电视，不喜欢看电影。"
    sentence_2 = "我不喜欢看电视，也不喜欢看电影。"

    if request.method.__eq__("GET"):
        sentence_1 = request_args['sentence_1']
        sentence_2 = request_args['sentence_2']
    elif request.method.__eq__('POST'):
        sentence_1 = request_json['sentence_1']
        sentence_2 = request_json['sentence_2']
    else:
        return 'error: ?sentence_1=你好还是不好?&sentence_2=我不好还是你不好?'

    # print(f'sentence_1:{sentence_1} , sentence_2: {sentence_2} ')
    # 分词
    result_fenci = fenci(sentence_1, sentence_2)
    percent = yuxuan(result_fenci)
    # print(f"percent:{percent}")
    return dic_json({"percent": percent})


def fenci(sentence_1="我喜欢看电视，不喜欢看电影。", sentence_2="我不喜欢看电视，也不喜欢看电影。"):

    # 分词
    seg_list_1 = jieba.lcut(sentence_1)
    seg_list_2 = jieba.lcut(sentence_2)

    # 找出所有的词
    vocabularies = set(seg_list_1+seg_list_2)
    print(vocabularies)
    # 统计

    result = {1: [], 2: []}
    for v in vocabularies:
        result[1].append(sentence_1.count(v))
        result[2].append(sentence_2.count(v))
    return result


def yuxuan(array_data={1: [], 2: []}):
    result = aibi(array_data) / (ai2_sqr(array_data[1]) * ai2_sqr(array_data[2]))
    return "%.3f" % result.real


# 计算平方和的根号
def ai2_sqr(array_data=[1, 2, 3]):
    total = 0
    index = 0
    while index < len(array_data):
        i = array_data[index]
        total = total + i * i
        index += 1
    # print(f"ai2_sqr: {total}")
    return cmath.sqrt(total)


# 计算 Ai * Bi
def aibi(array_data={1: [1, 2, 3], 2: [4, 5, 6]}):
    total = 0
    index = 0
    # print(f"aibi:{array_data}")
    while index < len(array_data[1]):
        total = total + array_data[1][index] * array_data[2][index]
        index += 1
    # print(f"Ai * Bi 和: {total}")

    return total


def dic_json(dic):
    if dic is None:
        dic = {
            'name': 'messenger',
            'playstore': True,
            'company': 'Facebook',
            'price': 100
        }
    return json.dumps(dic, iterable_as_array=True)


# if __name__ == '__main__':
#     result = yuxuan(fenci())
#     print(result)
