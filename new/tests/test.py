import os, sys
sys.path.append(os.path.dirname(os.getcwd()))
from data import StockDataHelper


def main():
    helper = StockDataHelper()
    helper.save_to_disk()
# end function main

if __name__ == '__main__':
    main()
