from collections import OrderedDict

import yaml
from box import Box

def create_ordered_box(data):
    """OrderedDict を使用して Box を作成する関数"""
    ordered_data = OrderedDict(sorted(data.items()))  # キーでソート
    return Box(ordered_data, default_box=True)  # default_box=True で None を返す


def sort_ordered_box(box: Box) -> Box:
    # Boxを辞書に変換
    dict_data = box.to_dict()
    # 再帰的にソート
    sorted_dict = sort_nested_dictionary(dict_data)
    # ソート済みの辞書からBoxを作成
    return Box(sorted_dict, default_box=True)


def sort_nested_dictionary(d):
    # 辞書を再帰的にソート
    if isinstance(d, dict):
        return OrderedDict(sorted(
            [(k, sort_nested_dictionary(v)) for k, v in d.items()],
            key=lambda x: str(x[0])  # キーでソート
        ))
    elif isinstance(d, list):
        return [sort_nested_dictionary(i) for i in d]
    else:
        return d
    

def load_yaml(file_path: str) -> Box:
    """
    Load YAML file into a DotAccessDict.
    
    Args:
        file_path: Path to the YAML file
        
    Returns:
        yamldata
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return create_ordered_box(data)


def load_yaml_string(yaml_str: str) -> Box:
    """
    Load YAML string into a DotAccessDict.
    
    Args:
        yaml_str: YAML content as string
        
    Returns:
        yamldata
    """
    data = yaml.safe_load(yaml_str)
    return create_ordered_box(data)


def main():
    """メイン関数"""
    # YAMLファイルからデータを読み込む
    file_path = "data.yaml"  # YAMLファイルのパス
    loaded_yaml = load_yaml(file_path)

    # リストの場合、最初の要素を処理する例
    if isinstance(loaded_yaml, list):
        loaded_yaml = loaded_yaml[0]

    # ドットアクセス
    a = loaded_yaml.Test1.KueTwVaOzF.IMNaOXFnhj.JSfOMwNdIt.BUCvSDjfsc
    b = loaded_yaml.c.e
    if b:
        raise("Error not None")
    loaded_yaml.c.e = a

    # キー順序
    k = list(loaded_yaml.__dict__.keys())
    # ソート
    sorted_yaml = sort_ordered_box(loaded_yaml)
    if sorted_yaml == loaded_yaml:
        raise("error not sorted")


if __name__ == "__main__":
    main()
