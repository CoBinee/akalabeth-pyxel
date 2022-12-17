# applesoftbasic.py - Applesoft Basic
#


# 参照
#
import sys
import os
import re
import math
import random
from lark import Lark
from lark import Tree
from lark import Token
from lark import Transformer
import pyxel


# Applesoft Basic クラス
#
class ApplesoftBasic(Transformer):

    # コンストラクタ
    def __init__(self):

        # Applesoft Basic の初期化

        # パスの初期化
        self._path = None

        # リストの初期化
        self._lines = dict()
        self._lists = dict()
        self._nexts = dict()
        self._start = -1

        # ツリーの初期化
        self._trees = dict()

        # 変数の初期化
        self._variables = dict()

        # 配列の初期化
        self._arrays = dict()

        # GOSUB の初期化
        self._gosubs = list()

        # FOR の初期化
        self._fors = list()

        # DATA の初期化
        self._datas = list()
        self._data_index = 0

        # Pyxel の初期化

        # フレームバッファの初期化
        self._frame_buffer = 2

        # フォントの初期化
        self._font_image = 0
        self._font_size_x = 6
        self._font_size_y = 8

        # テキストの初期化
        self._text_size_x = 40
        self._text_size_y = 24
        self._text_size_hires = 4
        self._text_clip_x = 0
        self._text_clip_y = 0
        self._text_clip_size_x = self._text_size_x
        self._text_clip_size_y = self._text_size_y
        self._text_mode = 'normal'

        # グラフィックの初期化
        self._hires_size_x = self._text_size_x * self._font_size_x
        self._hires_size_y = (self._text_size_y - self._text_size_hires) * self._font_size_y
        self._hires_rate_x = self._hires_size_x / 280.0
        self._hires_rate_y = self._hires_size_y / 160.0
        self._hires_clip_x = 0
        self._hires_clip_y = 0
        self._hires_clip_size_x = self._hires_size_x
        self._hires_clip_size_y = self._hires_size_y

        # 画面の初期化
        self._screen_size_x = self._text_size_x * self._font_size_x
        self._screen_size_y = self._text_size_y * self._font_size_y
        self._screen_mode = 'text'

        # カーソルの初期化
        self._cursor_x = 0
        self._cursor_y = 0

        # タブの初期化
        self._tab = 8

        # 色の初期化
        self._color_front = 7
        self._color_back = 0
        self._color_hires = 7
        self._colors = [0, 11, 2, 7, 0, 9, 12, 7]

        # キーコード
        self._keycodes = {
            pyxel.KEY_ESCAPE: 0x1b, 
            pyxel.KEY_RETURN: 0x0d, 
            pyxel.KEY_BACKSPACE: 0x7f, 
            pyxel.KEY_DELETE: 0x7f, 
            pyxel.KEY_UP: 0x0d, # 0x0b
            pyxel.KEY_DOWN: 0x2f, # 0x0a 
            pyxel.KEY_LEFT: 0x08, 
            pyxel.KEY_RIGHT: 0x15, 
            pyxel.KEY_SPACE: 0x20,
            pyxel.KEY_SLASH: 0x2f, 
            pyxel.KEY_0: 0x30, 
            pyxel.KEY_1: 0x31, 
            pyxel.KEY_2: 0x32, 
            pyxel.KEY_3: 0x33, 
            pyxel.KEY_4: 0x34, 
            pyxel.KEY_5: 0x35, 
            pyxel.KEY_6: 0x36, 
            pyxel.KEY_7: 0x37, 
            pyxel.KEY_8: 0x38, 
            pyxel.KEY_9: 0x39, 
            pyxel.KEY_A: 0x41, 
            pyxel.KEY_B: 0x42, 
            pyxel.KEY_C: 0x43, 
            pyxel.KEY_D: 0x44, 
            pyxel.KEY_E: 0x45, 
            pyxel.KEY_F: 0x46, 
            pyxel.KEY_G: 0x47, 
            pyxel.KEY_H: 0x48, 
            pyxel.KEY_I: 0x49, 
            pyxel.KEY_J: 0x4a, 
            pyxel.KEY_K: 0x4b, 
            pyxel.KEY_L: 0x4c, 
            pyxel.KEY_M: 0x4d, 
            pyxel.KEY_N: 0x4e, 
            pyxel.KEY_O: 0x4f, 
            pyxel.KEY_P: 0x50, 
            pyxel.KEY_Q: 0x51, 
            pyxel.KEY_R: 0x52, 
            pyxel.KEY_S: 0x53, 
            pyxel.KEY_T: 0x54, 
            pyxel.KEY_U: 0x55, 
            pyxel.KEY_V: 0x56, 
            pyxel.KEY_W: 0x57, 
            pyxel.KEY_X: 0x58, 
            pyxel.KEY_Y: 0x59, 
            pyxel.KEY_Z: 0x5a, 
            pyxel.KEY_KP_0: 0x30, 
            pyxel.KEY_KP_1: 0x31, 
            pyxel.KEY_KP_2: 0x32, 
            pyxel.KEY_KP_3: 0x33, 
            pyxel.KEY_KP_4: 0x34, 
            pyxel.KEY_KP_5: 0x35, 
            pyxel.KEY_KP_6: 0x36, 
            pyxel.KEY_KP_7: 0x37, 
            pyxel.KEY_KP_8: 0x38, 
            pyxel.KEY_KP_9: 0x39, 
            pyxel.KEY_KP_ENTER: 0x0d, 
        }

        # 入力の初期化
        self._key_mode = None
        self._key_name = None
        self._key_string = ''
        self._key_length = 8
        self._key_blink = 0
        self._key_peek_16384 = False

        # ログの初期化
        self._log_level = 2

    # Applesoft Basic を準備する
    def ready(self, path):

        # パスの設定
        self._path = path

        # ファイルの読み込み
        if not self._load():
            exit()

        # リストの解析
        if not self._parse():
            exit()

        # プログラムの実行
        if not self._execute():
            exit()

    # ファイルを読み込む
    def _load(self):

        # ファイルの読み込み
        try:
            with open(self._path, 'r', encoding='UTF-8') as file:
                last = -1
                for line in file:
                    match = re.match(r'^\s*(\d+)\s*(.*)\n?$', line)
                    if match is not None:
                        number = int(match.group(1))
                        self._lines[number] = match.group(2)
                        self._nexts[last] = number
                        if self._start < 0 or self._start > number:
                            self._start = number
                        last = number

        # 例外
        except Exception as e:
            sys.stderr.write('{0}\n'.format(e))
            return False

        # 読み込みの完了
        finally:
            pass

        # ステートメント毎に分割
        for number in self._lines.keys():
            line = self._lines[number]
            statement = 0
            head = 0
            length = len(line)
            while head < length:
                while head < length and (line[head] == ' ' or line[head] == '\t'):
                    head = head + 1
                if head < length:
                    if re.match(r'(?i)^rem', line[head:]) is not None:
                        head = length
                    elif re.match(r'(?i)^(hi|lo)mem:', line[head:]) is not None:
                        head = head + 6
                        while head < length and line[head] != ':':
                            head = head + 1
                        head = head + 1
                    elif re.match(r'(?i)^(dim|onerr|resume|pr#|in#|fre|pdl|pos|scrn)', line[head:]) is not None:
                        while head < length and line[head] != ':':
                            head = head + 1
                        head = head + 1
                    else:
                        tail = head
                        while tail < length and line[tail] != ':':
                            if line[tail] == '"':
                                tail = tail + 1
                                while tail < length and line[tail] != '"':
                                    tail = tail + 1
                                if tail < length:
                                    tail = tail + 1
                            elif line[tail] == "'":
                                tail = tail + 1
                                while tail < length and line[tail] != "'":
                                    tail = tail + 1
                                if tail < length:
                                    tail = tail + 1
                            else:
                                tail = tail + 1
                        if number not in self._lists:
                            self._lists[number] = dict()
                        self._lists[number][statement] = line[head:tail]
                        statement = statement + 1
                        head = tail + 1

        # 終了
        return True

    # リストを解析する
    def _parse(self):

        # Lark による解析
        try:

            # 文法の定義
            lark = Lark(r'''
                statement           :   command_clear
                                    |   command_let
                                //  |   command_dim
                                //  |   command_def
                                    |   command_goto
                                    |   command_gosub
                                    |   command_return
                                    |   command_on_goto
                                    |   command_on_gosub
                                //  |   command_pop
                                    |   command_for
                                    |   command_next
                                    |   command_if
                                    |   command_stop
                                //  |   command_onerr
                                //  |   command_resume
                                    |   command_print
                                    |   command_input
                                    |   command_get
                                    |   command_home
                                    |   command_htab
                                    |   command_vtab
                                    |   command_inverse
                                //  |   command_flash
                                    |   command_normal
                                    |   command_text
                                    |   command_hgr
                                    |   command_hplot
                                    |   command_hcolor
                                    |   command_data
                                    |   command_read
                                    |   command_restore
                                    |   command_poke
                                    |   command_call
                                //  |   command_pr
                                //  |   command_in
                command_clear       :   "CLEAR"i
                command_let         :   ("LET"i)? let ("," let)*
                let                 :   variable_number "=" expression
                                    |   variable_string "=" sentence
            //  command_dim         :   "DIM"i ...
            //  command_def         :   "DEF"i "FN"i ...
                command_goto        :   ("GOTO"i)? expression
                command_gosub       :   "GOSUB"i expression
                command_return      :   "RETURN"i
                command_on_goto     :   "ON"i expression "GOTO"i expression ("," expression)*
                command_on_gosub    :   "ON"i expression "GOSUB"i expression ("," expression)*
            //  command_pop         :   "POP"i
                command_for         :   "FOR"i variable_number "=" expression "TO"i expression ("STEP"i expression)?
                command_next        :   "NEXT"i variable_number?
                command_if          :   "IF"i expression ("THEN"i)? statement
                command_stop        :   "STOP"i
                                    |   "END"i
            //  command_onerr       |   "ONERR"i "GOTO"i ...
            //  command_resume      |   "RESUME" ...
                command_print       :   "PRINT"i (expression | sentence | SEMICOLON | COMMA)*
                command_input       :   "INPUT"i (sentence ";")? (variable_number | variable_string)
                command_get         :   "GET"i (variable_number | variable_string)
                command_home        :   "HOME"i
                command_htab        :   "HTAB"i expression
                command_vtab        :   "VTAB"i expression
                command_inverse     :   "INVERSE"i
            //  command_flash       :   "FLASH"i
                command_normal      :   "NORMAL"i
                command_text        :   "TEXT"i
                command_hgr         :   "HGR"i
                command_hplot       :   "HPLOT"i ("TO"i)? expression "," expression ("TO"i expression "," expression)*
                command_hcolor      :   "HCOLOR"i "=" expression
                command_data        :   "DATA"i (expression | sentence) ("," (expression | sentence))*
                command_read        :   "READ"i (variable_number | variable_string) ("," (variable_number | variable_string))*
                command_restore     :   "RESTORE"i
            //  command_pr          :   "PR#"i ...
            //  command_in          :   "IN#"i ...
                command_poke        :   "POKE"i expression "," expression
                command_call        :   "CALL"i expression
                function_abs        :   "ABS"i "(" expression ")"
                function_atn        :   "ATN"i "(" expression ")"
                function_cos        :   "COS"i "(" expression ")"
                function_exp        :   "EXP"i "(" expression ")"
                function_int        :   "INT"i "(" expression ")"
                function_log        :   "LOG"i "(" expression ")"
                function_rnd        :   "RND"i "(" expression ")"
                function_sgn        :   "SGN"i "(" expression ")"
                function_sin        :   "SIN"i "(" expression ")"
                function_sqr        :   "SQR"i "(" expression ")"
                function_tan        :   "TAN"i "(" expression ")"
                function_len        :   "LEN"i "(" sentence ")"
                function_left       :   "LEFT$"i "(" sentence "," expression ")"
                function_mid        :   "MID$"i "(" sentence "," expression ("," expression)? ")"
                function_right      :   "RIGHT$"i "(" sentence "," expression ")"
                function_asc        :   "ASC"i "(" sentence ")"
                function_chr        :   "CHR$"i "(" expression ")"
                function_str        :   "STR$"i "(" expression ")"
                function_val        :   "VAL"i "(" sentence ")"
                function_peek       :   "PEEK"i "(" expression ")"
                expression          :   logical_or
                logical_or          :   logical_and
                                    |   logical_or "OR"i logical_and
                logical_and         :   compare
                                    |   logical_and "AND"i compare
                compare             :   sum
                                    |   sum ">" sum  -> greater
                                    |   sum ">=" sum -> greater_equal
                                    |   sum "=>" sum -> greater_equal
                                    |   sum "<" sum  -> less
                                    |   sum "<=" sum -> less_equal
                                    |   sum "=<" sum -> less_equal
                                    |   sum "=" sum  -> equal
                                    |   sum "<>" sum -> not_equal
                                    |   sum "><" sum -> not_equal
                                    |   sentence "=" sentence -> equal
                                    |   sentence "<>" sentence -> not_equal
                                    |   sentence "><" sentence -> not_equal
                sum                 :   product
                                    |   sum "+" product -> addition
                                    |   sum "-" product -> subtraction
                product             :   exponent
                                    |   product "*" exponent -> multiply
                                    |   product "/" exponent -> division
                exponent            :   atom
                                    |   exponent "^" atom -> power
                atom                :   positive
                                    |   negative
                                    |   negation
                                    |   "(" expression ")"
                positive            :   "+"? factor
                negative            :   "-" factor
                negation            :   "NOT"i factor
                factor              :   NUMBER
                                    |   variable_number
                                    |   function_abs
                                    |   function_atn
                                    |   function_cos
                                    |   function_exp
                                    |   function_int
                                    |   function_log
                                    |   function_rnd
                                    |   function_sgn
                                    |   function_sin
                                    |   function_sqr
                                    |   function_tan
                                    |   function_len
                                    |   function_asc
                                    |   function_val
                                    |   function_peek
                sentence            :   term
                                    |   sentence "+" term -> strcat
                term                :   STRING
                                    |   variable_string
                                    |   function_left
                                    |   function_mid
                                    |   function_right
                                    |   function_chr
                                    |   function_str
                variable_number     :   (NAME_INTEGER | NAME_REAL) ("(" expression ("," expression)? ")")?
                variable_string     :   NAME_STRING ("(" expression ("," expression)? ")")?
                NAME_REAL           :   /[A-Za-z][A-Za-z0-9]*/
                NAME_INTEGER        :   /[A-Za-z][A-Za-z0-9]*%/
                NAME_STRING         :   /[A-Za-z][A-Za-z0-9]*\$/
                NUMBER              :   /[0-9]+(\.[0-9]+)?|\.[0-9]+/
                STRING              :   /[\"][^\"]*[\"]|[\'][^\']*[\']|[\"][^\"]*$|[\'][^\']*$/
                SEMICOLON           :   ";"
                COMMA               :   ","
                %import common (WS)
                %ignore WS
            ''', parser='lalr', start='statement')

            # リストの解析
            for number in self._lists.keys():
                count = 0
                for statement in self._lists[number].keys():
                    if number not in self._trees:
                        self._trees[number] = dict()
                    self._log(f'parse//{number}, {statement}: {self._lists[number][statement]}', level=1)
                    if len(self._lists[number][statement]) > 0:
                        tree = lark.parse(self._lists[number][statement])
                        if tree.data == 'statement':
                            if tree.children[0].data == 'command_if':
                                self._trees[number][count] = Tree('statement', [Tree('command_if', [tree.children[0].children[0]])])
                                count = count + 1
                                self._trees[number][count] = tree.children[0].children[1]
                                count = count + 1
                            elif tree.children[0].data == 'command_data':
                                for child in tree.children[0].children:
                                    value = None
                                    sign = 1
                                    while value is None:
                                        if type(child) is Tree:
                                            if child.data == 'negative':
                                                sign = -1
                                            child = child.children[0]
                                        elif type(child) is Token:
                                            if child.type == 'NUMBER':
                                                value = float(child.value) * sign
                                            else:
                                                value = child.value[1:len(child.value) - 1]
                                    self._datas.append(value)
                                self._trees[number][count] = tree
                                count = count + 1
                            else:
                                self._trees[number][count] = tree
                                count = count + 1

        # 例外
        except Exception as e:
            sys.stderr.write('{0}\n'.format(e))
            return False

        # 解析の完了
        finally:
            pass

        # 終了
        return True

    # 実行する
    def _execute(self):

        # 実行の初期化
        self._number = self._get_goto_number(self._start)
        self._statement = 0
        self._speed = 1000

        # 終了
        return True

    # 1 フレームの更新を行う
    def update(self):

        # 1 回の更新
        if self._key_mode is None:
            cycle = 0
            while self._number >= 0 and cycle < self._speed and self._key_mode is None and (not self._key_peek_16384):
                self._number, self._statement, self._key_mode, self._key_name = self._process(self._number, self._statement)
                cycle = cycle + 1
            self._key_string = ''
            self._key_blink = 0
            self._key_peek_16384 = False

        # 文字列の入力
        if self._key_mode == 'input':
            if self._input():
                self._set_variable(['VARIABLE_STRING', self._key_name], self._key_string)
                self._number, self._statement = self._get_next_statement(self._number, self._statement)
                self._key_mode = None

        # 1 文字の入力
        elif self._key_mode == 'get':
            if self._getkey():
                self._set_variable(['VARIABLE_STRING', self._key_name], self._key_string)
                self._number, self._statement = self._get_next_statement(self._number, self._statement)
                self._key_mode = None

        # キー入力待ち
        elif self._key_mode == 'wait':
            if self._getkey():
                self._number, self._statement = self._get_next_statement(self._number, self._statement)
                self._key_mode = None

        # プログラムの終了
        return True if self._number >= 0 else False

    # 1 フレームの描画を行う
    def draw(self):

        # 画面の更新
        pyxel.blt(0, 0, self._frame_buffer, 0, 0, self._screen_size_x, self._screen_size_y)

    # プログラムを処理する
    def _process(self, number, statement):

        # 処理の開始
        result = None
        mode = None
        name = None
        self._log(f'process//{number}, {statement}: ', level=1)

        # ステートメントの実行
        try:
            if (number in self._trees) and (statement in self._trees[number]):
                result = self.transform(self._trees[number][statement])

        # 例外
        except Exception as e:
            sys.stderr.write('{0}\n'.format(e))
            return 0, 0, None, None

        # 実行の完了
        finally:
            if result[0] == 'else':
                if number in self._nexts:
                    number = self._nexts[number]
                    statement = 0
                else:
                    number = -1
            elif result[0] == 'goto':
                number = self._get_goto_number(result[1])
                statement = 0
                """
                if result[1] == 1:
                    number = -1
                else:
                    number = self._get_goto_number(result[1])
                    statement = 0
                """
            elif result[0] == 'gosub':
                number, statement = self._get_next_statement(number, statement)
                self._gosubs.append([number, statement])
                number = self._get_goto_number(result[1])
                statement = 0
            elif result[0] == 'return':
                params = self._gosubs.pop()
                number = params[0]
                statement = params[1]
            elif result[0] == 'for':
                number, statement = self._get_next_statement(number, statement)
                self._fors.append([number, statement, result[1], result[2], result[3]])
            elif result[0] == 'next':
                if result[1] is not None:
                    number = result[1][0]
                    statement = result[1][1]
                else:
                    number, statement = self._get_next_statement(number, statement)
            elif result[0] == 'stop':
                number = -1
            elif result[0] == 'input':
                mode = 'input'
                name = result[1]
            elif result[0] == 'get':
                mode = 'get'
                name = result[1]
            elif result[0] == 'wait':
                mode = 'wait'
                name = None
            else:
                number, statement = self._get_next_statement(number, statement)

        # 終了
        return number, statement, mode, name

    # Transformer

    # statement
    def statement(self, tree):
        self._log(f'statement: {tree}')
        return tree[0]

    # command_clear
    def command_clear(self, tree):
        self._log(f'command_clear: {tree}')
        self._variables.clear()
        self._arrays.clear()
        self._gosubs.clear()
        self._fors.clear()
        self._data_index = 0
        return [None, None]

    # command_let
    def command_let(self, tree):
        self._log(f'command_let: {tree}')
        return [None, None]

    # let
    def let(self, tree):
        self._log(f'let: {tree}')
        result = self._set_variable(tree[0], tree[1][1])
        return ['NUMBER', result]

    # command_goto
    def command_goto(self, tree):
        self._log(f'command_goto: {tree}')
        return ['goto', int(tree[0][1])]
    
    # command_gosub
    def command_gosub(self, tree):
        self._log(f'command_gosub: {tree}')
        return ['gosub', int(tree[0][1])]
    
    # command_return
    def command_return(self, tree):
        self._log(f'command_return: {tree}')
        return ['return', None]
    
    # command_on_goto
    def command_on_goto(self, tree):
        self._log(f'command_on_goto: {tree}')
        return ['goto', int(tree[int(tree[0][1])][1])]
    
    # command_on_gosub
    def command_on_gosub(self, tree):
        self._log(f'command_on_gosub: {tree}')
        return ['gosub', int(tree[int(tree[0][1])][1])]
    
    # command_for
    def command_for(self, tree):
        self._log(f'command_for: {tree}')
        # 配列は非対応
        self._set_variable(tree[0], tree[1][1])
        return ['for', tree[0][1], tree[2][1], tree[3][1] if len(tree) >= 4 else 1]
    
    # command_next
    def command_next(self, tree):
        self._log(f'command_next: {tree}')
        i = len(self._fors) - 1
        if len(tree) > 0:
            while i >= 0 and self._fors[i][2] != tree[0][1]:
                self._fors.pop()
                i = i - 1
        result = None
        if i >= 0:
            name = self._fors[i][2]
            kind = 'VARIABLE_STRING' if name[-1] == '$' else ('VARIABLE_INTEGER' if name[-1] == '%' else 'VARIABLE_REAL')
            goal = self._fors[i][3]
            step = self._fors[i][4]
            value = self._get_variable([kind, name]) + step
            self._set_variable([kind, name], value)
            if (step > 0 and value <= goal) or (step < 0 and value >= goal):
                result = [self._fors[i][0], self._fors[i][1]]
            else:
                self._fors.pop()
        return ['next', result]
    
    # command_if
    def command_if(self, tree):
        self._log(f'command_if: {tree}')
        return [None, None] if tree[0][1] != 0 else ['else', None]
    
    # command_if_goto
    def command_if_goto(self, tree):
        self._log(f'command_if_goto: {tree}')
        return ['goto', int(tree[1][1])] if tree[0][1] != 0 else ['else', None]
    
    # command_stop
    def command_stop(self, tree):
        self._log(f'command_stop: {tree}')
        return ['stop', None]

    # command_print
    def command_print(self, tree):
        self._log(f'command_print: {tree}')
        result = None
        cr = True
        for element in tree:
            if element[0] == 'STRING':
                bload = re.search(r'(?i)bload\s*(aka\d)', element[1])
                if bload is not None:
                    if self._view_image(bload.group(1)):
                        result = 'wait'
                else:
                    self._print(element[1])
                    cr = True
            elif element[0] == 'NUMBER':
                self._print(str(int(element[1])))
                cr = True
            elif element[0] == 'SEMICOLON':
                cr = False
            elif element[0] == 'COMMA':
                tab = self._tab - self._cursor_x % self._tab
                while tab > 0:
                    self._print(' ')
                    tab = tab - 1
                cr = True
            else:
                pass
        if cr:
            self._newline()
        return [result, None]

    # command_input
    def command_input(self, tree):
        self._log(f'command_input: {tree}')
        i = 0
        if tree[i][0] == 'STRING':
            self._print(tree[i][1])
            i = i + 1
        return ['input', tree[i][1]]

    # command_get
    def command_get(self, tree):
        self._log(f'command_get: {tree}')
        return ['get', tree[0][1]]

    # command_home
    def command_home(self, tree):
        self._log(f'command_home: {tree}')
        self._cursor_x = self._text_clip_x
        self._cursor_y = self._text_clip_y
        self._clear_text()
        return [None, None]

    # command_htab
    def command_htab(self, tree):
        self._log(f'command_htab: {tree}')
        self._cursor_x = int(tree[0][1]) - 1
        return [None, None]

    # command_vtab
    def command_vtab(self, tree):
        self._log(f'command_vtab: {tree}')
        self._cursor_y = int(tree[0][1]) - 1
        return [None, None]

    # command_inverse
    def command_inverse(self, tree):
        self._log(f'command_inverse: {tree}')
        self._text_mode = 'inverse'
        return [None, None]

    # command_normal
    def command_normal(self, tree):
        self._log(f'command_normal: {tree}')
        self._text_mode = 'normal'
        return [None, None]

    # command_text
    def command_text(self, tree):
        self._log(f'command_text: {tree}')
        self._text_clip_x = 0
        self._text_clip_y = 0
        self._text_clip_size_x = self._text_size_x
        self._text_clip_size_y = self._text_size_y
        self._screen_mode = 'text'
        return [None, None]

    # command_hgr
    def command_hgr(self, tree):
        self._log(f'command_hgr: {tree}')
      # self._text_clip_x = 0
        self._text_clip_y = self._text_size_y - self._text_size_hires
      # self._text_clip_size_x = self._text_size_x
        self._text_clip_size_y = self._text_size_hires
        self._screen_mode = 'hires'
        self._clear_hires()
        return [None, None]

    # command_hplot
    def command_hplot(self, tree):
        self._log(f'command_hplot: {tree}')
        positions = []
        for value in tree:
            positions.append(int(value[1]))
        self._plot(positions)
        return [None, None]

    # command_hcolor
    def command_hcolor(self, tree):
        self._log(f'command_hcolor: {tree}')
        # self._color_hires = self._colors[int(tree[0])]
        return [None, None]

    # command_data
    def command_data(self, tree):
        self._log(f'command_data: {tree}')
        return [None, None]

    # command_read
    def command_read(self, tree):
        self._log(f'command_read: {tree}')
        for var in tree:
            self._set_variable(var, self._datas[self._data_index])
            self._data_index = self._data_index + 1
        return [None, None]

    # command_restore
    def command_restore(self, tree):
        self._log(f'command_restore: {tree}')
        self._data_index = 0
        return [None, None]

    # command_poke
    def command_poke(self, tree):
        self._log(f'command_poke: {tree}')
        address = int(tree[0][1])
        value = int(tree[1][1])
        if address == 32:
            self._text_clip_x = value
        elif address == 33:
            self._text_clip_size_x = value
        elif address == 34:
            bottom = self._text_clip_y + self._text_clip_size_y
            self._text_clip_y = value
            self._text_clip_size_y = bottom - value
        elif address == 35:
            self._text_clip_size_y = value - self._text_clip_y
        elif address == 36:
            self._cursor_x = value
        elif address == 37:
            self._cursor_y = value
        elif address == -16368:
            pass
        return [None, None]

    # command_call
    def command_call(self, tree):
        self._log(f'command_call: {tree}')
        address = int(tree[0][1])
        if address == -868:
            self._clear_text_line()
        elif address == 62450:
            self._clear_hires()
        return [None, None]

    # function_abs
    def function_abs(self, tree):
        self._log(f'function_abs: {tree}')
        return ['NUMBER', abs(tree[0][1])]

    # function_atn
    def function_atn(self, tree):
        self._log(f'function_atn: {tree}')
        return ['NUMBER', math.atan(tree[0][1])]

    # function_cos
    def function_cos(self, tree):
        self._log(f'function_cos: {tree}')
        return ['NUMBER', math.cos(tree[0][1])]

    # function_exp
    def function_exp(self, tree):
        self._log(f'function_exp: {tree}')
        return ['NUMBER', math.exp(tree[0][1])]

    # function_int
    def function_int(self, tree):
        self._log(f'function_int: {tree}')
        return ['NUMBER', int(tree[0][1])]

    # function_log
    def function_log(self, tree):
        self._log(f'function_log: {tree}')
        return ['NUMBER', math.log(tree[0][1])]

    # function_rnd
    def function_rnd(self, tree):
        self._log(f'function_rnd: {tree}')
        if tree[0][1] < 0:
            random.seed(tree[0][1])
        return ['NUMBER', random.random()]

    # function_sgn
    def function_sgn(self, tree):
        self._log(f'function_sgn: {tree}')
        return ['NUMBER', 1 if tree[0][1] > 0 else (-1 if tree[0][1] < 0 else 0)]

    # function_sin
    def function_sin(self, tree):
        self._log(f'function_sin: {tree}')
        return ['NUMBER', math.sin(tree[0][1])]

    # function_sqr
    def function_sqr(self, tree):
        self._log(f'function_sqr: {tree}')
        return ['NUMBER', math.sqrt(tree[0][1])]

    # function_tan
    def function_tan(self, tree):
        self._log(f'function_tan: {tree}')
        return ['NUMBER', math.tan(tree[0][1])]

    # function_len
    def function_len(self, tree):
        self._log(f'function_len: {tree}')
        return ['NUMBER', len(tree[0][1])]

    # function_left
    def function_left(self, tree):
        self._log(f'function_left: {tree}')
        return ['STRING', tree[0][1][:int(tree[1])]]

    # function_mid
    def function_mid(self, tree):
        self._log(f'function_mid: {tree}')
        head = int(tree[1][1])
        tail = int(tree[1][1]) + int(tree[2][1]) if len(tree) > 2 else len(tree[0][1])
        return ['STRING', tree[0][1][head:tail]]

    # function_right
    def function_right(self, tree):
        self._log(f'function_right: {tree}')
        return ['STRING', tree[0][1][-int(tree[1]):]]

    # function_asc
    def function_asc(self, tree):
        self._log(f'function_asc: {tree}')
        return ['NUMBER', ord(tree[0][1][0])]

    # function_chr
    def function_chr(self, tree):
        self._log(f'function_chr: {tree}')
        return ['NUMBER', chr(int(tree[0][1]))]

    # function_str
    def function_str(self, tree):
        self._log(f'function_str: {tree}')
        return ['STRING', str(int(tree[0][1]))]

    # function_val
    def function_val(self, tree):
        self._log(f'function_val: {tree}')
        result = 0.0
        try:
            result = float(tree[0][1])
        except:
            pass
        return ['NUMBER', result]

    # function_peek
    def function_peek(self, tree):
        self._log(f'function_peek: {tree}')
        result = 0
        address = int(tree[0][1])
        if address == -16384:
            result = self._inkey()
            self._key_peek_16384 = True
        return ['NUMBER', result]

    # expression
    def expression(self, tree):
        self._log(f'expression: {tree}')
        return tree[0]

    # logical_or
    def logical_or(self, tree):
        self._log(f'logical_or: {tree}')
        result = tree[0][1]
        if len(tree) > 1:
            result = 0
            for value in tree:
                if value[1] != 0:
                    result = 1
        return ['NUMBER', result]

    # logical_and
    def logical_and(self, tree):
        self._log(f'logical_and: {tree}')
        result = tree[0][1]
        if len(tree) > 1:
            result = 1
            for value in tree:
                if value[1] == 0:
                    result = 0
        return ['NUMBER', result]

    # compare
    def compare(self, tree):
        self._log(f'compare: {tree}')
        return tree[0]

    # greater
    def greater(self, tree):
        self._log(f'greater: {tree}')
        return ['NUMBER', 1 if tree[0][1] > tree[1][1] else 0]
        
    # greater_equal
    def greater_equal(self, tree):
        self._log(f'greater: {tree}')
        return ['NUMBER', 1 if tree[0][1] >= tree[1][1] else 0]
        
    # less
    def less(self, tree):
        self._log(f'less: {tree}')
        return ['NUMBER', 1 if tree[0][1] < tree[1][1] else 0]
        
    # less_equal
    def less_equal(self, tree):
        self._log(f'less_equal: {tree}')
        return ['NUMBER', 1 if tree[0][1] <= tree[1][1] else 0]
        
    # equal
    def equal(self, tree):
        self._log(f'equal: {tree}')
        return ['NUMBER', 1 if tree[0][1] == tree[1][1] else 0]
        
    # not_equal
    def not_equal(self, tree):
        self._log(f'not_equal: {tree}')
        return ['NUMBER', 1 if tree[0][1] != tree[1][1] else 0]
        
    # sum
    def sum(self, tree):
        self._log(f'sum: {tree}')
        return tree[0]

    # addition
    def addition(self, tree):
        self._log(f'addition: {tree}')
        return ['NUMBER', tree[0][1] + tree[1][1]]

    # subtraction
    def subtraction(self, tree):
        self._log(f'subtraction: {tree}')
        return ['NUMBER', tree[0][1] - tree[1][1]]

    # product
    def product(self, tree):
        self._log(f'product: {tree}')
        return tree[0]

    # multiply
    def multiply(self, tree):
        self._log(f'multiply: {tree}')
        return ['NUMBER', tree[0][1] * tree[1][1]]

    # division
    def division(self, tree):
        self._log(f'division: {tree}')
        return ['NUMBER', tree[0][1] / tree[1][1]]

    # exponent
    def exponent(self, tree):
        self._log(f'exponent: {tree}')
        return tree[0]

    # power
    def power(self, tree):
        self._log(f'power: {tree}')
        return ['NUMBER', tree[0][1] ** tree[1][1]]

    # atom
    def atom(self, tree):
        self._log(f'atom: {tree}')
        return tree[0]

    # positive
    def positive(self, tree):
        self._log(f'positive: {tree}')
        return tree[0]

    # negative
    def negative(self, tree):
        self._log(f'negative: {tree}')
        return ['NUMBER', -tree[0][1]]

    # negation
    def negation(self, tree):
        self._log(f'negation: {tree}')
        return ['NUMBER', 1 if tree[0][1] == 0 else 0]

    # factor
    def factor(self, tree):
        self._log(f'factor: {tree}')
        result = tree[0][1] if tree[0][0] != 'VARIABLE_REAL' and tree[0][0] != 'VARIABLE_INTEGER' else self._get_variable(tree[0])
        return ['NUMBER', result]

    # sentence
    def sentence(self, tree):
        self._log(f'sentence: {tree}')
        return tree[0]

    # strcat
    def strcat(self, tree):
        self._log(f'strcat: {tree}')
        return ['STRING', tree[0][1] + tree[1][1]]

    # term
    def term(self, tree):
        self._log(f'term: {tree}')
        result = tree[0][1] if tree[0][0] != 'VARIABLE_STRING' else self._get_variable(tree[0])
        return ['STRING', result]

    # variable_number
    def variable_number(self, tree):
        self._log(f'variable_number: {tree}')
        result = ['VARIABLE_REAL' if tree[0][0] == 'NAME_REAL' else 'VARIABLE_INTEGER']
        for i in range(len(tree)):
            result.append(tree[i][1])
        return result

    # variable_string
    def variable_string(self, tree):
        self._log(f'variable_string: {tree}')
        result = ['VARIABLE_STRING']
        for i in range(len(tree)):
            result.append(tree[i][1])
        return result

    # NAME_REAL
    def NAME_REAL(self, tree):
        self._log(f'NAME_REAL: {tree}')
        return ['NAME_REAL', tree.value.upper()[0:2]]

    # NAME_INTERER
    def NAME_INTEGER(self, tree):
        self._log(f'NAME_INTEGER: {tree}')
        tail = 2 if len(tree.value) > 2 else 1
        return ['NAME_INTEGER', tree.value.upper()[0:tail] + '%']

    # NAME_STRING
    def NAME_STRING(self, tree):
        self._log(f'NAME_STRING: {tree}')
        tail = 2 if len(tree.value) > 2 else 1
        return ['NAME_STRING', tree.value.upper()[0:tail] + '$']

    # NUMBER
    def NUMBER(self, tree):
        self._log(f'NUMBER: {tree}')
        return ['NUMBER', float(tree.value)]

    # STRING
    def STRING(self, tree):
        self._log(f'STRING: {tree}')
        tail = len(tree.value) - 1
        if tree.value[0] == "\"":
            if tree.value[tail] == "\"":
                tail = tail - 1
        elif tree.value[0] == "'":
            if tree.value[tail] == "'":
                tail = tail - 1
        return ['STRING', tree.value[1:tail + 1]]

    # SEMICOLON
    def SEMICOLON(self, tree):
        self._log(f'SEMICOLON{tree}')
        return ['SEMICOLON', 0]

    # COMMA
    def COMMA(self, tree):
        self._log(f'COMMA{tree}')
        return ['COMMA', 0]

    # 変数に値を代入する
    def _set_variable(self, vars, value):
        result = None
        if vars[0] == 'VARIABLE_REAL':
            try:
                result = float(value)
            except:
                result = 0.0
        elif vars[0] == 'VARIABLE_INTEGER':
            try:
                result = int(value)
            except:
                result = 0
        else:
            result= str(value)
        key = vars[1]
        length = len(vars)
        if length == 2:
            self._variables[key] = result
        elif length == 3:
            if key not in self._arrays:
                self._arrays[key] = dict()
            dim_1 = int(vars[2])
            self._arrays[key][dim_1] = result
        elif length == 4:
            if key not in self._arrays:
                self._arrays[key] = dict()
            dim_1 = int(vars[2])
            if dim_1 not in self._arrays[key]:
                self._arrays[key][dim_1] = dict()
            dim_2 = int(vars[3])
            self._arrays[key][dim_1][dim_2] = result
        return result

    # 変数の値を取得する
    def _get_variable(self, vars):
        result = None
        key = vars[1]
        length = len(vars)
        if length == 2:
            if key in self._variables:
                result = self._variables[key]
        elif length == 3:
            if key not in self._arrays:
                self._arrays[key] = dict()
            dim_1 = int(vars[2])
            if dim_1 in self._arrays[key]:
                result = self._arrays[key][dim_1]
        elif length == 4:
            if key not in self._arrays:
                self._arrays[key] = dict()
            dim_1 = int(vars[2])
            if dim_1 not in self._arrays[key]:
                self._arrays[key][dim_1] = dict()
            dim_2 = int(vars[3])
            if dim_2 in self._arrays[key][dim_1]:
                result = self._arrays[key][dim_1][dim_2]
        return result if result is not None else (0 if vars[0] != 'VARIABLE_STRING' else '')

    # goto でジャンプできる行を取得する
    def _get_goto_number(self, number):
        while not number in self._trees:
            number = number + 1
        return number

    # 次のステートメントを取得する
    def _get_next_statement(self, number, statement):
        statement = statement + 1
        if (number not in self._trees) or (statement not in self._trees[number]):
            if number in self._nexts:
                number = self._get_goto_number(self._nexts[number])
                statement = 0
            else:
                number = -1
        else:
            pass
        return number, statement

    # 画面をクリアする
    def _clear_screen(self):

        # クリップの解除
        # pyxel.clip()

        # 画面のクリア
        pyxel.image(self._frame_buffer).cls(self._color_back)

    # テキストをクリップする
    def _clip_text(self):

        # テキストのクリップ
        # pyxel.clip(self._text_clip_x * self._font_size_x, self._text_clip_y * self._font_size_y, self._text_clip_size_x * self._font_size_x, self._text_clip_size_y * self._font_size_y)
        pass

    # テキストをクリアする
    def _clear_text(self):

        # クリップ
        # self._clip_text()

        # テキストのクリア
        pyxel.image(self._frame_buffer).rect(self._text_clip_x * self._font_size_x, self._text_clip_y * self._font_size_y, self._text_clip_size_x * self._font_size_x, self._text_clip_size_y * self._font_size_y, self._color_back)

    # カーソル位置から右端までのテキストを消去する
    def _clear_text_line(self):

        # クリップ
        # self._clip_text()

        # テキストの消去
        pyxel.image(self._frame_buffer).rect(self._cursor_x * self._font_size_x, self._cursor_y * self._font_size_y, (self._text_clip_x + self._text_clip_size_x - self._cursor_x) * self._font_size_x, self._font_size_y, self._color_back)

    # 文字列を出力する
    def _print(self, string):

        # クリップ
        # self._clip_text()

        # １文字ずつ出力
        for c in string:
            self._putc(c)

    # １文字を出力する
    def _putc(self, c, cursor = True):

        # 色の取得
        color = 0 if self._text_mode == 'normal' else 128

        # 位置の取得
        x = self._cursor_x * self._font_size_x
        y = self._cursor_y * self._font_size_y

        # １文字の出力
        pyxel.image(self._frame_buffer).blt(x, y, self._font_image, ((ord(c) - 0x20) & 0x0f) * 0x08 + color, ((ord(c) - 0x20) >> 4) * 0x08, self._font_size_x, self._font_size_y)

        # カーソルの更新
        if cursor:
            self._cursor_x = self._cursor_x + 1
            if self._cursor_x >= self._text_clip_x + self._text_clip_size_x:
                self._newline()

    # 改行する
    def _newline(self):
        
        # 改行
        self._cursor_x = self._text_clip_x
        self._cursor_y = self._cursor_y + 1

        # スクロール
        if self._cursor_y >= self._text_clip_y + self._text_clip_size_y:
            pyxel.image(self._frame_buffer).blt(self._text_clip_x * self._font_size_x, self._text_clip_y * self._font_size_y, self._frame_buffer, self._text_clip_x * self._font_size_x, (self._text_clip_y + 1) * self._font_size_y, self._text_clip_size_x * self._font_size_x, (self._text_clip_size_y - 1) * self._font_size_y)
            pyxel.image(self._frame_buffer).rect(self._text_clip_x * self._font_size_x, (self._text_clip_y + self._text_clip_size_y - 1) * self._font_size_y, self._text_clip_size_x * self._font_size_x, self._font_size_y, self._color_back)
            self._cursor_y = self._text_clip_y + self._text_clip_size_y - 1

    # 文字列入力を受け付ける
    def _input(self):

        # クリップ
        # self._clip_text()

        # ENTER が押されるまで
        enter = False

        # カーソルの消去
        self._putc(' ', cursor = False)

        # キーの入力
        for key in self._keycodes:
            if pyxel.btnp(key):
                code = self._keycodes[key]
                if code == 0x0d:
                    enter = True
                elif code == 0x7f:
                    if len(self._key_string) > 0:
                        self._key_string = self._key_string[:-1]
                        self._cursor_x = self._cursor_x - 1
                        self._putc(' ', cursor = False)
                        self._key_blink = 0
                elif len(self._key_string) < self._key_length:
                    if code >= 0x20:
                        c = chr(code)
                        self._key_string = self._key_string + c
                        self._putc(c)
                        self._key_blink = 0

        # カーソルの描画
        if ((self._key_blink & 0x08) == 0) and (not enter):
            self._putc('_', cursor = False)

        # 点滅の更新
        self._key_blink = self._key_blink + 1

        # 改行
        if enter:
            self._newline()

        # 終了
        return enter

    # 文字入力を受け付ける
    def _getkey(self):

        # 文字が押されるまで
        getkey = False

        # カーソルの消去
        self._putc(' ', cursor = False)

        # キーの入力
        for key in self._keycodes:
            if pyxel.btnp(key):
                code = self._keycodes[key]
                if 0x20 <= code and code < 0x7f:
                    self._key_string = chr(code)
                    getkey = True

        # カーソルの描画
        if ((self._key_blink & 0x08) == 0) and (not getkey):
            self._putc('_', cursor = False)

        # 点滅の更新
        self._key_blink = self._key_blink + 1

        # 終了
        return getkey

    # キー入力を受け付ける
    def _inkey(self):

        # 文字列の初期化
        code = 0

        # キーの入力
        for key in self._keycodes:
            if pyxel.btnp(key):
                code = self._keycodes[key] | 0x80

        # 終了
        return code

    # グラフィックをクリップする
    def _clip_hires(self):

        # グラフィックのクリップ
        # pyxel.clip(self._hires_clip_x, self._hires_clip_y, self._hires_clip_size_x, self._hires_clip_size_y)
        pass

    # グラフィックをクリップする
    def _clear_hires(self):

        # クリップ
        # self._clip_hires()

        # グラフィックのクリア
        if self._screen_mode == 'hires':
            pyxel.image(self._frame_buffer).rect(self._hires_clip_x, self._hires_clip_y, self._hires_clip_size_x, self._hires_clip_size_y, self._color_back)

    # 線を引く
    def _plot(self, positions):

        # クリップ
        # self._clip_hires()

        # 点
        if len(positions) == 2:
            pyxel.image(self._frame_buffer).pset(positions[0] * self._hires_rate_x, positions[1] * self._hires_rate_y, self._color_hires)

        # 線
        else:
            i = 0
            while i <= len(positions) - 4:
                x_0 = int(positions[i + 0] * self._hires_rate_x)
                y_0 = int(positions[i + 1] * self._hires_rate_y)
                x_1 = int(positions[i + 2] * self._hires_rate_x)
                y_1 = int(positions[i + 3] * self._hires_rate_y)
                color = self._colors[3] if x_0 != x_1 else (self._colors[1] if (x_0 & 0x01) != 0x00 else self._colors[2])
                pyxel.image(self._frame_buffer).line(x_0, y_0, x_1, y_1, color)
                i = i + 2

    # イメージを表示する
    def _view_image(self, basename):

        # .png 名の取得
        path = './' + basename + ".png"

        # ファイルの存在
        exist = os.path.isfile(path)
        if exist:

            # イメージの読み込み
            pyxel.image(self._frame_buffer).load(0, 0, path)

        # 終了
        return exist

    # ログを出力する
    def _log(self, *args, level = 0):
        if level >= self._log_level:
            for value in args:
                print(value, end = '')
            print('')


# Basic の宣言
#
applesoftbasic = None
basicfile = ['./AKA0', './AKA6']
basicstep = 0

# Pyxel の更新を行う
#
def update():

    # グローバル宣言
    global applesoftbasic
    global basicfile
    global basicstep

    # ApplesoftBasic の生成
    if applesoftbasic is None:
        applesoftbasic = ApplesoftBasic()
        applesoftbasic.ready(basicfile[basicstep])

    # ApplesoftBasic の更新
    if applesoftbasic is not None:
        result = applesoftbasic.update()
        if not result:
            applesoftbasic = None
            basicstep = basicstep + 1
            if basicstep >= len(basicfile):
                basicstep = 0

# Pyxel の描画を行う
#
def draw():

    # グローバル宣言
    global applesoftbasic

    # ApplesoftBasic の描画
    if applesoftbasic is not None:
        applesoftbasic.draw()

# アプリケーションのエントリポイント
#
if __name__ == '__main__':

#   # 引数の取得
#   if len(sys.argv) < 2:
#       sys.stderr.write('error - no file.\n')
#       exit()
    
    # Pyxel の初期化
    pyxel.init(240, 192, title = 'Akalabeth: World of Doom')

    # リソースの読み込み
    pyxel.load('./akalabeth.pyxres')

    # 画面のクリア
    pyxel.cls(0)

    # Pyxel の実行
    pyxel.run(update, draw)
