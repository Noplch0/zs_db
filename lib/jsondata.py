import json
from datetime import datetime


def df_to_custom_json(df, num_rows=None, columns=None):
    # 如果没有指定列，默认选择所有列
    if columns is None:
        columns = df.columns.tolist()

    # 选择指定的列和行
    df_selected = df[columns].head(num_rows) if num_rows is not None else df[columns]

    # 将 DataFrame 转换为字典
    df_dict = df_selected.to_dict(orient='index')

    # 构建新的 JSON 格式
    custom_json = {}
    for index, values in df_dict.items():
        custom_json[index] = {col: values[col] for col in columns}

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


def update_collections(json_str, text, is_del=0):
    try:
        # 尝试解析 JSON 字符串
        data = json.loads(json_str)
    except json.JSONDecodeError:
        print("Invalid JSON format")
        return None

    # 检查是否存在 "collections" 键
    if "collections" in data:
        # 如果 is_del 为 1，删除对应内容
        if is_del == 1 and text in data["collections"]:
            data["collections"].remove(text)
        # 如果 is_del 为 0，且内容不存在，则添加
        elif is_del == 0 and text not in data["collections"]:
            data["collections"].append(text)
    else:
        # 如果 is_del 为 0，创建一个新的 "collections" 键，并将 text 添加到其中
        if is_del == 0:
            data["collections"] = [text]

    # 将修改后的数据转换回 JSON 字符串
    updated_json_str = json.dumps(data, ensure_ascii=False)

    return updated_json_str


def format_date(input_date):
    # 将字符串解析为日期对象
    date_object = datetime.strptime(str(input_date), '%Y%m%d')

    # 将日期对象格式化为字符串
    formatted_date = date_object.strftime('%Y-%m-%d')

    return formatted_date


def df_to_custom_json_kline(df, num_rows=None, columns=None):
    if columns is None:
        columns = df.columns.tolist()

    df_selected = df[columns].head(num_rows) if num_rows is not None else df[columns]

    # 对日期列应用 format_date 函数
    if 'trade_date' in columns:
        df_selected['trade_date'] = df_selected['trade_date'].apply(format_date)

    df_dict = df_selected.to_dict(orient='index')

    custom_json = {'data': [list(values.values()) for values in df_dict.values()]}

    return custom_json
