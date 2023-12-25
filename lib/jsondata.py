import pandas as pd
import json


def df_to_custom_json(df, num_rows=None):
    # 选择要保留的行数
    if num_rows is not None:
        df = df.head(num_rows)

    # 转换 DataFrame 为字典形式
    df_dict = df.to_dict(orient='index')

    # 构建新的 JSON 格式
    custom_json = {}
    for index, values in df_dict.items():
        custom_json[index] = {
            'open': values['open'],
            'high': values['high'],
            'low': values['low'],
            'close': values['close']
        }

    return custom_json


def add_name_to_json(input_json, name):
    """
    将 JSON 字典中的每个元素的键值添加一个新的外部键名

    参数:
    - input_json: 输入的 JSON 字典
    - name: 要添加的外部键名

    返回:
    - 修改后的 JSON 字典
    """
    output_json = {name: input_json}
    return output_json


def write_json(json_data, filepath):
    with open(filepath, 'w') as file:
        json.dump(json_data, file, indent=4)


def add_data(orgin_json, data_json):
    o = json.loads(orgin_json)
    a = json.loads(data_json)
    return json.dumps(o + a)
