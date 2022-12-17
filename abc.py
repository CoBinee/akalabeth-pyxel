# abc.py - Applesoft Basic Compiler
#


# 参照
#
import sys
import argparse
import akalabeth
from akalabeth import ApplesoftBasic

# アプリケーションのエントリポイント
#
if __name__ == '__main__':

    # 引数の取得
    argument_parser = argparse.ArgumentParser(description='Akalabeth: World of Doom!')
    argument_parser.add_argument('-i', '--indent', type=int, help='.json indent length')
    argument_parser.add_argument('-c', '--compile',  action='store_true', help='compile basic code')
    argument_parser.add_argument('-o', '--output', help='.json file name')
    argument_parser.add_argument('basicfile', nargs='?', help='basic file name')
    args = argument_parser.parse_args()

    # Basic コードのコンパイル
    if args.compile:

        # Basic ファイルの確認
        if args.basicfile is None:
            argument_parser.print_help()
            exit()

        # 出力ファイルの取得
        if args.output is None:
            args.output = args.basicfile + '.json'

        # コンパイル
        applesoftbasic = ApplesoftBasic()
        applesoftbasic.ready(args.basicfile)
        applesoftbasic.export(args.output, args.indent)

    # ゲームの実行
    else:
        akalabeth.run()
