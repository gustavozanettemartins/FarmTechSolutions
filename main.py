from data import *
from utils import *

def main():
    _data = get_data()
    print(_data, type(_data))
    _data["teste"] = {"a": 0}
    print(update_data(_data))


if __name__ == '__main__':
    main()
