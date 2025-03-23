import yaml
import types
from collections import OrderedDict
from typing import Any, Dict, List


class DotAccessDict:
    """
    A class that provides dot notation access to nested dictionaries loaded from YAML.
    Features:
    - Fast access using SimpleNamespace
    - Dot notation access (a.b.c.d)
    - Preserves key order
    - Sortable
    - Returns None for non-existent keys without raising exceptions
    - Proper equality comparison that considers sort order
    """
    
    def __init__(self, data: Dict = None):
        """
        Initialize a DotAccessDict with optional dictionary data.
        
        Args:
            data: Initial dictionary data
        """
        self._data = OrderedDict()
        self._namespace = types.SimpleNamespace()
        
        if data:
            self._update_from_dict(data)
    
    def _update_from_dict(self, data: Dict) -> None:
        """
        Update internal data structure from a dictionary.
        
        Args:
            data: Dictionary to load data from
        """
        if not isinstance(data, dict):
            return
            
        for key, value in data.items():
            if isinstance(value, dict):
                self._data[key] = DotAccessDict(value)
            elif isinstance(value, list):
                self._data[key] = [
                    DotAccessDict(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                self._data[key] = value
                
            setattr(self._namespace, str(key), self._data[key])
    
    def __getattr__(self, name: str) -> Any:
        """
        Access attributes using dot notation.
        
        Args:
            name: Attribute name to access
            
        Returns:
            The attribute value or None if it doesn't exist
        """
        try:
            return getattr(self._namespace, name)
        except AttributeError:
            # Return a SafeNone object that will return None for any further attribute access
            return SafeNone()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value by key with a default fallback.
        
        Args:
            key: Key to access
            default: Default value if key doesn't exist
            
        Returns:
            Value for the key or default
        """
        return self._data.get(key, default)
    
    def keys(self) -> List[str]:
        """
        Get all keys in the dictionary.
        
        Returns:
            List of keys
        """
        return list(self._data.keys())
    
    def items(self) -> List[tuple]:
        """
        Get all key-value pairs.
        
        Returns:
            List of (key, value) tuples
        """
        return list(self._data.items())
    
    def values(self) -> List[Any]:
        """
        Get all values.
        
        Returns:
            List of values
        """
        return list(self._data.values())
    
    def __eq__(self, other) -> bool:
        """
        Compare equality with another DotAccessDict.
        Also considers the order of items.
        
        Args:
            other: Another DotAccessDict to compare with
            
        Returns:
            True if equal, False otherwise
        """
        if not isinstance(other, DotAccessDict):
            return False
            
        # Compare the items and their order
        return list(self.items()) == list(other.items())
    
    def sort(self, key=None, reverse=False) -> 'DotAccessDict':
        """
        Sort the dictionary by keys or using a custom key function.
        
        Args:
            key: Optional function to determine sort order
            reverse: Whether to sort in reverse order
            
        Returns:
            New sorted DotAccessDict
        """
        sorted_items = sorted(self._data.items(), key=key, reverse=reverse)
        result = DotAccessDict()
        
        for k, v in sorted_items:
            if isinstance(v, DotAccessDict):
                result._data[k] = v.sort(key=key, reverse=reverse)
            elif isinstance(v, list):
                result._data[k] = [
                    item.sort(key=key, reverse=reverse) if isinstance(item, DotAccessDict) else item
                    for item in v
                ]
            else:
                result._data[k] = v
                
            setattr(result._namespace, str(k), result._data[k])
            
        return result
    
    def __repr__(self) -> str:
        """String representation of the object."""
        return f"DotAccessDict({self._data})"


class SafeNone:
    """
    A class that returns None for any attribute access.
    This allows for safely chaining attribute access like a.b.c.d even when
    intermediate attributes don't exist.
    """
    def __getattr__(self, _):
        return None
        
    def __repr__(self):
        return "None"
        
    def __str__(self):
        return "None"
        
    def __bool__(self):
        return False


def load_yaml(file_path: str) -> DotAccessDict:
    """
    Load YAML file into a DotAccessDict.
    
    Args:
        file_path: Path to the YAML file
        
    Returns:
        DotAccessDict containing the YAML data
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return DotAccessDict(data)


def load_yaml_string(yaml_str: str) -> DotAccessDict:
    """
    Load YAML string into a DotAccessDict.
    
    Args:
        yaml_str: YAML content as string
        
    Returns:
        DotAccessDict containing the YAML data
    """
    data = yaml.safe_load(yaml_str)
    return DotAccessDict(data)


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
    sorted_yaml = loaded_yaml.sort()
    if sorted_yaml == loaded_yaml:
        raise("error not sorted")


if __name__ == "__main__":
    main()