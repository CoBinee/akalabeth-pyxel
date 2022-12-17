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

        # フォントの初期化
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
            pyxel.KEY_Z: 0x5a
        }

        # 入力の初期化
        self._input_length = 8

        # ログの初期化
        self._log_level = 2

    # Applesoft Basic を実行する
    def run(self, path):

        # パスの設定
        self._path = path

        # ファイルの読み込み
        if not self._load():
            exit()

        # リストの解析
        if not self._parse():
            exit()

        # プログラムの処理
        if not self._process():
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
                    self._log(f'parse//{number}, {statement}: {self._lists[number][statement]}', level = 1)
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

    # プログラムを処理する
    def _process(self):

        # Transformer の作成
        number = self._start
        statement = 0
        while number >= 0:
            result = [None]
            self._log(f'process//{number}, {statement}: ', level = 1)

            # ステートメントの実行
            try:
                if (number in self._trees) and (statement in self._trees[number]):
                    result = self.transform(self._trees[number][statement])

            # 例外
            except Exception as e:
                sys.stderr.write('{0}\n'.format(e))
                return False

            # 実行の完了
            finally:
                if result[0] == 'else':
                    if number in self._nexts:
                        number = self._nexts[number]
                        statement = 0
                    else:
                        number = -1
                elif result[0] == 'goto':
                    number = result[1]
                    statement = 0
                elif result[0] == 'gosub':
                    number, statement = self._get_next_statement(number, statement)
                    self._gosubs.append([number, statement])
                    number = result[1]
                    statement = 0
                elif result[0] == 'return':
                    params = self._gosubs.pop()
                    number = params[0]
                    statement = params[1]
                elif result[0] == 'for':
                    number, statement = self._get_next_statement(number, statement)
                    self._fors.append([number, statement, result[1][0], result[1][1], result[1][2]])
                elif result[0] == 'next':
                    if result[1] is not None:
                        number = result[1][0]
                        statement = result[1][1]
                    else:
                        number, statement = self._get_next_statement(number, statement)
                elif result[0] == 'stop':
                    number = -1
                else:
                    number, statement = self._get_next_statement(number, statement)

        # 終了
        return True

    # Transformer

    # statement
    def statement(self, tree):
        self._log('statement: ', tree)
        return tree[0]

    # command_clear
    def command_clear(self, tree):
        self._log('command_clear: ', tree)
        self._variables.clear()
        self._arrays.clear()
        return [None, None]

    # command_let
    def command_let(self, tree):
        self._log('command_let: ', tree)
        return [None, None]

    # let
    def let(self, tree):
        self._log('let: ', tree)
        result = self._set_variable(tree[0], tree[1])
        return result

    # command_goto
    def command_goto(self, tree):
        self._log('command_goto: ', tree)
        return ['goto', int(tree[0])]
    
    # command_gosub
    def command_gosub(self, tree):
        self._log('command_gosub: ', tree)
        return ['gosub', int(tree[0])]
    
    # command_return
    def command_return(self, tree):
        self._log('command_return: ', tree)
        return ['return', None]
    
    # command_on_goto
    def command_on_goto(self, tree):
        self._log('command_on_goto: ', tree)
        return ['goto', int(tree[int(tree[0])])]
    
    # command_on_gosub
    def command_on_gosub(self, tree):
        self._log('command_on_gosub: ', tree)
        return ['gosub', int(tree[int(tree[0])])]
    
    # command_for
    def command_for(self, tree):
        self._log('command_for: ', tree)
        self._set_variable(tree[0], tree[1])
        return ['for', [tree[0], tree[2], tree[3] if len(tree) >= 4 else 1]]
    
    # command_next
    def command_next(self, tree):
        self._log('command_next: ', tree)
        i = len(self._fors) - 1
        if len(tree) > 0:
            while i >= 0 and self._fors[i][2] != tree[0]:
                self._fors.pop()
                i = i - 1
        result = None
        if i >= 0:
            name = self._fors[i][2]
            goal = self._fors[i][3]
            step = self._fors[i][4]
            value = self._get_variable(name) + step
            self._set_variable(name, value)
            if (step > 0 and value <= goal) or (step < 0 and value >= goal):
                result = [self._fors[i][0], self._fors[i][1]]
            else:
                self._fors.pop()
        return ['next', result]
    
    # command_if
    def command_if(self, tree):
        self._log('command_if: ', tree)
        return [None, None] if tree[0] != 0 else ['else', None]
    
    # command_if_goto
    def command_if_goto(self, tree):
        self._log('command_if_goto: ', tree)
        return ['goto', int(tree[1])] if tree[0] != 0 else ['else', None]
    
    # command_stop
    def command_stop(self, tree):
        self._log('command_stop: ', tree)
        return ['stop', None]

    # command_print
    def command_print(self, tree):
        self._log('command_print: ', tree)
        cr = True
        for element in tree:
            if type(element) is str:
                bload = re.search(r'(?i)bload\s*(aka\d)', element)
                if bload is not None:
                    self._view_image(bload.group(1))
                else:
                    self._print(element)
                    cr = True
            elif type(element) is int:
                self._print(str(element))
                cr = True
            elif type(element) is float:
                # self._print(f'{element:.1f}')
                self._print(str(int(element)))
                cr = True
            elif element.type == 'SEMICOLON':
                cr = False
            elif element.type == 'COMMA':
                tab = self._tab - self._cursor_x % self._tab
                while tab > 0:
                    self._print(' ')
                    tab = tab - 1
                cr = True
            else:
                pass
        if cr:
            self._newline()
        return [None, None]

    # command_input
    def command_input(self, tree):
        self._log('command_input: ', tree)
        i = 0
        if type(tree[i]) is str:
            self._print(tree[i])
            i = i + 1
        string = self._input()
        self._set_variable(tree[i], string)
        return [None, None]

    # command_get
    def command_get(self, tree):
        self._log('command_get: ', tree)
        string = self._getkey()
        self._set_variable(tree[0], string)
        return [None, None]

    # command_home
    def command_home(self, tree):
        self._log('command_home: ', tree)
        self._cursor_x = self._text_clip_x
        self._cursor_y = self._text_clip_y
        self._clear_text()
        return [None, None]

    # command_htab
    def command_htab(self, tree):
        self._log('command_htab: ', tree)
        self._cursor_x = int(tree[0]) - 1
        return [None, None]

    # command_vtab
    def command_vtab(self, tree):
        self._log('command_vtab: ', tree)
        self._cursor_y = int(tree[0]) - 1
        return [None, None]

    # command_inverse
    def command_inverse(self, tree):
        self._log('command_inverse: ', tree)
        self._text_mode = 'inverse'
        return [None, None]

    # command_normal
    def command_normal(self, tree):
        self._log('command_normal: ', tree)
        self._text_mode = 'normal'
        return [None, None]

    # command_text
    def command_text(self, tree):
        self._log('command_text: ', tree)
        self._text_clip_x = 0
        self._text_clip_y = 0
        self._text_clip_size_x = self._text_size_x
        self._text_clip_size_y = self._text_size_y
        self._screen_mode = 'text'
        return [None, None]

    # command_hgr
    def command_hgr(self, tree):
        self._log('command_hgr: ', tree)
      # self._text_clip_x = 0
        self._text_clip_y = self._text_size_y - self._text_size_hires
      # self._text_clip_size_x = self._text_size_x
        self._text_clip_size_y = self._text_size_hires
        self._screen_mode = 'hires'
        self._clear_hires()
        return [None, None]

    # command_hplot
    def command_hplot(self, tree):
        self._log('command_hplot: ', tree)
        self._plot(tree)
        return [None, None]

    # command_hcolor
    def command_hcolor(self, tree):
        self._log('command_hcolor: ', tree)
        # self._color_hires = self._colors[int(tree[0])]
        return [None, None]

    # command_data
    def command_data(self, tree):
        self._log('command_data: ', tree)
        return [None, None]

    # command_read
    def command_read(self, tree):
        self._log('command_read: ', tree)
        for var in tree:
            self._set_variable(var, self._datas[self._data_index])
            self._data_index = self._data_index + 1
        return [None, None]

    # command_restore
    def command_restore(self, tree):
        self._log('command_restore: ', tree)
        self._data_index = 0
        return [None, None]

    # command_poke
    def command_poke(self, tree):
        self._log('command_poke: ', tree)
        address = int(tree[0])
        value = int(tree[1])
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
        self._log('command_call: ', tree)
        address = int(tree[0])
        if address == -868:
            self._clear_text_line()
        elif address == 62450:
            self._clear_hires()
        return [None, None]

    # function_abs
    def function_abs(self, tree):
        self._log('function_abs: ', tree)
        return abs(tree[0])

    # function_atn
    def function_atn(self, tree):
        self._log('function_atn: ', tree)
        return math.atan(tree[0])

    # function_cos
    def function_cos(self, tree):
        self._log('function_cos: ', tree)
        return math.cos(tree[0])

    # function_exp
    def function_exp(self, tree):
        self._log('function_exp: ', tree)
        return math.exp(tree[0])

    # function_int
    def function_int(self, tree):
        self._log('function_int: ', tree)
        return int(tree[0])

    # function_log
    def function_log(self, tree):
        self._log('function_log: ', tree)
        return math.log(tree[0])

    # function_rnd
    def function_rnd(self, tree):
        self._log('function_rnd: ', tree)
        if tree[0] < 0:
            random.seed(tree[0])
        return random.random()

    # function_sgn
    def function_sgn(self, tree):
        self._log('function_sgn: ', tree)
        return 1 if tree[0] > 0 else (-1 if tree[0] < 0 else 0)

    # function_sin
    def function_sin(self, tree):
        self._log('function_sin: ', tree)
        return math.sin(tree[0])

    # function_sqr
    def function_sqr(self, tree):
        self._log('function_sqr: ', tree)
        return math.sqrt(tree[0])

    # function_tan
    def function_tan(self, tree):
        self._log('function_tan: ', tree)
        return math.tan(tree[0])

    # function_len
    def function_len(self, tree):
        self._log('function_len: ', tree)
        return len(tree[0])

    # function_left
    def function_left(self, tree):
        self._log('function_left: ', tree)
        return tree[0][:int(tree[1])]

    # function_mid
    def function_mid(self, tree):
        self._log('function_mid: ', tree)
        head = int(tree[1])
        tail = int(tree[1]) + int(tree[2]) if len(tree) > 2 else len(tree[0])
        return tree[0][head:tail]

    # function_right
    def function_right(self, tree):
        self._log('function_right: ', tree)
        return tree[0][-int(tree[1]):]

    # function_asc
    def function_asc(self, tree):
        self._log('function_asc: ', tree)
        return ord(tree[0][0])

    # function_chr
    def function_chr(self, tree):
        self._log('function_chr: ', tree)
        return chr(int(tree[0]))

    # function_str
    def function_str(self, tree):
        self._log('function_str: ', tree)
        return str(int(tree[0]))

    # function_val
    def function_val(self, tree):
        self._log('function_val: ', tree)
        result = 0.0
        try:
            result = float(tree[0])
        except:
            pass
        return result

    # function_peek
    def function_peek(self, tree):
        self._log('function_peek: ', tree)
        result = 0
        address = int(tree[0])
        if address == -16384:
            result = self._inkey()
        return result

    # expression
    def expression(self, tree):
        self._log('expression: ', tree)
        return tree[0]

    # logical_or
    def logical_or(self, tree):
        self._log('logical_or: ', tree)
        result = tree[0]
        if len(tree) > 1:
            result = 0
            for value in tree:
                if value != 0:
                    result = 1
        return result

    # logical_and
    def logical_and(self, tree):
        self._log('logical_and: ', tree)
        result = tree[0]
        if len(tree) > 1:
            result = 1
            for value in tree:
                if value == 0:
                    result = 0
        return result

    # compare
    def compare(self, tree):
        self._log('compare: ', tree)
        return tree[0]

    # greater
    def greater(self, tree):
        self._log('greater: ', tree)
        return 1 if tree[0] > tree[1] else 0
        
    # greater_equal
    def greater_equal(self, tree):
        self._log('greater: ', tree)
        return 1 if tree[0] >= tree[1] else 0
        
    # less
    def less(self, tree):
        self._log('less: ', tree)
        return 1 if tree[0] < tree[1] else 0
        
    # less_equal
    def less_equal(self, tree):
        self._log('less_equal: ', tree)
        return 1 if tree[0] <= tree[1] else 0
        
    # equal
    def equal(self, tree):
        self._log('equal: ', tree)
        return 1 if tree[0] == tree[1] else 0
        
    # not_equal
    def not_equal(self, tree):
        self._log('not_equal: ', tree)
        return 1 if tree[0] != tree[1] else 0
        
    # sum
    def sum(self, tree):
        self._log('sum: ', tree)
        return tree[0]

    # addition
    def addition(self, tree):
        self._log('addition: ', tree)
        return tree[0] + tree[1]

    # subtraction
    def subtraction(self, tree):
        self._log('subtraction: ', tree)
        return tree[0] - tree[1]

    # product
    def product(self, tree):
        self._log('product: ', tree)
        return tree[0]

    # multiply
    def multiply(self, tree):
        self._log('multiply: ', tree)
        return tree[0] * tree[1]

    # division
    def division(self, tree):
        self._log('division: ', tree)
        return tree[0] / tree[1]

    # exponent
    def exponent(self, tree):
        self._log('exponent: ', tree)
        return tree[0]

    # power
    def power(self, tree):
        self._log('power: ', tree)
        return tree[0] ** tree[1]

    # atom
    def atom(self, tree):
        self._log('atom: ', tree)
        return tree[0]

    # positive
    def positive(self, tree):
        self._log('positive: ', tree)
        return tree[0]

    # negative
    def negative(self, tree):
        self._log('negative: ', tree)
        return -tree[0]

    # negation
    def negation(self, tree):
        self._log('negation: ', tree)
        return 1 if tree[0] == 0 else 0

    # factor
    def factor(self, tree):
        self._log('factor: ', tree)
        return tree[0] if type(tree[0]) is not list else self._get_variable(tree[0])

    # sentence
    def sentence(self, tree):
        self._log('sentence: ', tree)
        return tree[0]

    # strcat
    def strcat(self, tree):
        self._log('strcat: ', tree)
        return tree[0] + tree[1]

    # term
    def term(self, tree):
        self._log('term: ', tree)
        return tree[0] if type(tree[0]) is not list else self._get_variable(tree[0])

    # variable_number
    def variable_number(self, tree):
        self._log('variable_number: ', tree)
        return tree

    # variable_string
    def variable_string(self, tree):
        self._log('variable_string: ', tree)
        return tree

    # NAME_REAL
    def NAME_REAL(self, tree):
        self._log('NAME_REAL: ', tree)
        tree.value = tree.value.upper()[0:2]
        return tree

    # NAME_INTERER
    def NAME_INTEGER(self, tree):
        self._log('NAME_INTEGER: ', tree)
        tail = 2 if len(tree.value) > 2 else 1
        tree.value = tree.value.upper()[0:tail] + '%'
        return tree

    # NAME_STRING
    def NAME_STRING(self, tree):
        self._log('NAME_STRING: ', tree)
        tail = 2 if len(tree.value) > 2 else 1
        tree.value = tree.value.upper()[0:tail] + '$'
        return tree

    # NUMBER
    def NUMBER(self, tree):
        self._log('NUMBER: ', tree)
        return float(tree.value)

    # STRING
    def STRING(self, tree):
        self._log('STRING: ', tree)
        tail = len(tree.value) - 1
        if tree.value[0] == "\"":
            if tree.value[tail] == "\"":
                tail = tail - 1
        elif tree.value[0] == "'":
            if tree.value[tail] == "'":
                tail = tail - 1
        return tree.value[1:tail + 1]

    # SEMICOLON
    def SEMICOLON(self, tree):
        self._log('SEMICOLON', tree)
        return Token('SEMICOLON', tree.value)

    # COMMA
    def COMMA(self, tree):
        self._log('COMMA', tree)
        return Token('COMMA', tree.value)

    # 変数に値を代入する
    def _set_variable(self, names, value):
        result = None
        if names[0].type == 'NAME_REAL':
            try:
                result = float(value)
            except:
                result = 0.0
        elif names[0].type == 'NAME_INTEGER':
            try:
                result = int(value)
            except:
                result = 0
        else:
            result= str(value)
        key = names[0].value
        length = len(names)
        if length == 1:
            self._variables[key] = result
        elif length == 2:
            if key not in self._arrays:
                self._arrays[key] = dict()
            dim_1 = int(names[1])
            self._arrays[key][dim_1] = result
        elif length == 3:
            if key not in self._arrays:
                self._arrays[key] = dict()
            dim_1 = int(names[1])
            if dim_1 not in self._arrays[key]:
                self._arrays[key][dim_1] = dict()
            dim_2 = int(names[2])
            self._arrays[key][dim_1][dim_2] = result
        return result

    # 変数の値を取得する
    def _get_variable(self, names):
        result = None
        key = names[0].value
        length = len(names)
        if length == 1:
            if key in self._variables:
                result = self._variables[key]
        elif length == 2:
            if key not in self._arrays:
                self._arrays[key] = dict()
            dim_1 = int(names[1])
            if dim_1 in self._arrays[key]:
                result = self._arrays[key][dim_1]
        elif length == 3:
            if key not in self._arrays:
                self._arrays[key] = dict()
            dim_1 = int(names[1])
            if dim_1 not in self._arrays[key]:
                self._arrays[key][dim_1] = dict()
            dim_2 = int(names[2])
            if dim_2 in self._arrays[key][dim_1]:
                result = self._arrays[key][dim_1][dim_2]
        return result if result is not None else (0 if names[0].type != 'NAME_STRING' else '')

    # 次のステートメントを取得する
    def _get_next_statement(self, number, statement):
        statement = statement + 1
        if (number not in self._trees) or (statement not in self._trees[number]):
            if number in self._nexts:
                number = self._nexts[number]
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
        pyxel.image(2).cls(self._color_back)

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
        pyxel.image(2).rect(self._text_clip_x * self._font_size_x, self._text_clip_y * self._font_size_y, self._text_clip_size_x * self._font_size_x, self._text_clip_size_y * self._font_size_y, self._color_back)

    # カーソル位置から右端までのテキストを消去する
    def _clear_text_line(self):

        # クリップ
        # self._clip_text()

        # テキストの消去
        pyxel.image(2).rect(self._cursor_x * self._font_size_x, self._cursor_y * self._font_size_y, (self._text_clip_x + self._text_clip_size_x - self._cursor_x) * self._font_size_x, self._font_size_y, self._color_back)

    # 文字列を出力する
    def _print(self, string, flush = False):

        # クリップ
        # self._clip_text()

        # １文字ずつ出力
        for c in string:
            self._putc(c)

        # 画面の更新
        if flush:
            pyxel.blt(0, 0, 2, 0, 0, self._screen_size_x, self._screen_size_y)
            pyxel.flip()

    # １文字を出力する
    def _putc(self, c, cursor = True, flush = False):

        # 色の取得
        color = 0 if self._text_mode == 'normal' else 128

        # 位置の取得
        x = self._cursor_x * self._font_size_x
        y = self._cursor_y * self._font_size_y

        # １文字の出力
        pyxel.image(2).blt(x, y, 0, ((ord(c) - 0x20) & 0x0f) * 0x08 + color, ((ord(c) - 0x20) >> 4) * 0x08, self._font_size_x, self._font_size_y)

        # カーソルの更新
        if cursor:
            self._cursor_x = self._cursor_x + 1
            if self._cursor_x >= self._text_clip_x + self._text_clip_size_x:
                self._newline()

        # 画面の更新
        if flush:
            pyxel.blt(0, 0, 2, 0, 0, self._screen_size_x, self._screen_size_y)
            pyxel.flip()

    # 改行する
    def _newline(self):
        
        # 改行
        self._cursor_x = self._text_clip_x
        self._cursor_y = self._cursor_y + 1

        # スクロール
        if self._cursor_y >= self._text_clip_y + self._text_clip_size_y:
            pyxel.image(2).blt(self._text_clip_x * self._font_size_x, self._text_clip_y * self._font_size_y, 2, self._text_clip_x * self._font_size_x, (self._text_clip_y + 1) * self._font_size_y, self._text_clip_size_x * self._font_size_x, (self._text_clip_size_y - 1) * self._font_size_y)
            pyxel.image(2).rect(self._text_clip_x * self._font_size_x, (self._text_clip_y + self._text_clip_size_y - 1) * self._font_size_y, self._text_clip_size_x * self._font_size_x, self._font_size_y, self._color_back)
            pyxel.blt(0, 0, 2, 0, 0, self._screen_size_x, self._screen_size_y)
            pyxel.flip()
            self._cursor_y = self._text_clip_y + self._text_clip_size_y - 1

    # 文字列入力を受け付ける
    def _input(self):

        # クリップ
        # self._clip_text()

        # 文字列の初期化
        string = ''

        # 点滅の初期化
        blink = 0

        # ENTER が押されるまで
        enter = False
        while not enter:

            # カーソルの消去
            self._putc(' ', cursor = False)

            # キーの入力
            for key in self._keycodes:
                if pyxel.btnp(key):
                    if len(string) < self._input_length:
                        code = self._keycodes[key]
                        if code == 0x0d:
                            enter = True
                        elif code == 0x7f:
                            if len(string) > 0:
                                string = string[:-1]
                                self._cursor_x = self._cursor_x - 1
                                self._putc(' ', cursor = False)
                                blink = 0
                        elif code >= 0x20:
                            c = chr(code)
                            string = string + c
                            self._putc(c)
                            blink = 0

            # カーソルの描画
            if ((blink & 0x08) == 0) and (not enter):
                self._putc('_', cursor = False)

            # 点滅の更新
            blink = blink + 1

            # 画面の更新
            pyxel.blt(0, 0, 2, 0, 0, self._screen_size_x, self._screen_size_y)
            pyxel.flip()

        # 改行
        self._newline()

        # 終了
        return string

    # 文字入力を受け付ける
    def _getkey(self):

        # 文字列の初期化
        string = ''

        # 点滅の初期化
        blink = 0

        # 文字が押されるまで
        getkey = False
        while not getkey:

            # カーソルの消去
            self._putc(' ', cursor = False)

            # キーの入力
            for key in self._keycodes:
                if pyxel.btnp(key):
                    code = self._keycodes[key]
                    if 0x20 <= code and code < 0x7f:
                        string = chr(code)
                        getkey = True

            # カーソルの描画
            if ((blink & 0x08) == 0) and (not getkey):
                self._putc('_', cursor = False)

            # 点滅の更新
            blink = blink + 1

            # 画面の更新
            pyxel.blt(0, 0, 2, 0, 0, self._screen_size_x, self._screen_size_y)
            pyxel.flip()

        # 終了
        return string

    # キー入力を受け付ける
    def _inkey(self):

        # 文字列の初期化
        code = 0

        # キーの入力
        for key in self._keycodes:
            if pyxel.btnp(key):
                code = self._keycodes[key] | 0x80

        # 画面の更新
        pyxel.blt(0, 0, 2, 0, 0, self._screen_size_x, self._screen_size_y)
        pyxel.flip()

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
            pyxel.image(2).rect(self._hires_clip_x, self._hires_clip_y, self._hires_clip_size_x, self._hires_clip_size_y, self._color_back)

    # 線を引く
    def _plot(self, positions):

        # クリップ
        # self._clip_hires()

        # 点
        if len(positions) == 2:
            pyxel.image(2).pset(positions[0] * self._hires_rate_x, positions[1] * self._hires_rate_y, self._color_hires)

        # 線
        else:
            i = 0
            while i <= len(positions) - 4:
                x_0 = int(positions[i + 0] * self._hires_rate_x)
                y_0 = int(positions[i + 1] * self._hires_rate_y)
                x_1 = int(positions[i + 2] * self._hires_rate_x)
                y_1 = int(positions[i + 3] * self._hires_rate_y)
                color = self._colors[3] if x_0 != x_1 else (self._colors[1] if (x_0 & 0x01) != 0x00 else self._colors[2])
                pyxel.image(2).line(x_0, y_0, x_1, y_1, color)
                i = i + 2

    # イメージを表示する
    def _view_image(self, basename):

        # .png 名の取得
        path = './' + basename + ".png"

        # ファイルの存在
        if os.path.isfile(path):

            # イメージの読み込み
            pyxel.image(2).load(0, 0, path)

            # キー入力待ち
            while self._inkey() < 0x80:
                pass

    # ログを出力する
    def _log(self, *args, level = 0):
        if level >= self._log_level:
            for value in args:
                print(value, end = '')
            print('')

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

    # Applesoft Basic の実行
    ApplesoftBasic().run('./AKA0')

    # Applesoft Basic の実行
    ApplesoftBasic().run('./AKA6')
