# akar.py - Applesoft Basic Runner
#


# 参照
#
import sys
import os
import re
import math
import random
import argparse
import json
import pyxel


# Applesoft Basic クラス
#
class ApplesoftBasic:

    # コンストラクタ
    def __init__(self):

        # Applesoft Basic の初期化

        # パスの初期化
        self._path = None

        # リストの初期化
        ## self._lines = dict()
        ## self._lists = dict()
        self._start = -1

        # 変数宣言の初期化
        self._dims = dict()

        ### ツリーの初期化
        ##self._trees = dict()

        # 中間コードの初期化
        self._codes = dict()
        self._code_number = -1
        self._code_statement = 0
        self._code_step = 0
        self._code_mode = None
        self._code_speed = 1

        # スタック
        self._stacks = list()

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
        self._key_string = ''
        self._key_length = 8
        self._key_blink = 0

        # ログの初期化
        self._log_level = 2

    # Applesoft Basic を準備する
    def ready(self, path, speed = 1000):

        # パスの設定
        self._path = path

        # ファイルの読み込み
        if not self._import():
            exit()

        # 中間コードの実行
        if not self._execute(speed):
            exit()

    # .json ファイルを読み込む
    def _import(self):

        # .json ファイルの操作
        try:

            # .json ファイルを開く
            json_file = open(self._path, mode='r', encoding='utf8')

            # .json ファイルを読み込む
            json_text = json_file.read()
            json_data = json.loads(json_text)
            for number_key, number_value in json_data['code'].items():
                number = int(number_key)
                if number not in self._codes:
                    self._codes[number] = dict()
                for statement_key, statement_value in number_value.items():
                    statement = int(statement_key)
                    self._codes[number][statement] = statement_value
            self._datas = json_data['data']
            self._start = 0

            # .json ファイルを閉じる
            json_file.close()

        # エラー
        except Exception as e:
            print('import error:\n' + str(e), file=sys.stderr)
            return False

        # 終了
        return True

    # 中間コードの実行する
    def _execute(self, speed):

        # 実行の初期化
        self._code_number = self._get_goto_number(self._start)
        self._code_statement = 0
        self._code_step = 0
        self._code_mode = None
        self._code_speed = speed

        # 終了
        return True

    # 1 フレームの更新を行う
    def update(self):

        # コードの処理
        if self._code_mode is None:
            cycle = 0
            while self._code_number >= 0 and cycle < self._code_speed and self._code_mode is None:
                self._code_mode = self._process()
                if self._code_mode is None:
                    self._code_number, self._code_statement, self._code_step = self._get_next_code(self._code_number, self._code_statement, self._code_step)
                elif self._code_mode == 'goto':
                    self._code_mode = None
                elif self._code_mode == 'input':
                    self._key_string = ''
                    self._key_blink = 0
                elif self._code_mode == 'get':
                    self._key_string = ''
                    self._key_blink = 0
                elif self._code_mode == 'inkey':
                    self._key_string = ''
                    self._key_blink = 0

        # キー入力待ち
        elif self._code_mode == 'input':
            if self._input():
                vars = self._pop_vars()
                self._set_variable(vars, self._key_string)
                self._code_number, self._code_statement, self._code_step = self._get_next_code(self._code_number, self._code_statement, self._code_step)
                self._code_mode = None
        elif self._code_mode == 'get':
            if self._getkey():
                vars = self._pop_vars()
                self._set_variable(vars, self._key_string)
                self._code_number, self._code_statement, self._code_step = self._get_next_code(self._code_number, self._code_statement, self._code_step)
                self._code_mode = None
        elif self._code_mode == 'inkey':
            keycode = self._inkey()
            if keycode != 0:
                self._stacks.append(['NUMBER', keycode])
                self._code_number, self._code_statement, self._code_step = self._get_next_code(self._code_number, self._code_statement, self._code_step)
                self._code_mode = None
        elif self._code_mode == 'wait':
            if self._getkey():
                self._code_number, self._code_statement, self._code_step = self._get_next_code(self._code_number, self._code_statement, self._code_step)
                self._code_mode = None

        # プログラムの終了
        return True if self._code_number >= 0 else False

    # 1 フレームの描画を行う
    def draw(self):

        # 画面の更新
        pyxel.blt(0, 0, self._frame_buffer, 0, 0, self._screen_size_x, self._screen_size_y)

    # プログラムを処理する
    def _process(self):

        # コードの実行
        code = self._codes[self._code_number][self._code_statement][self._code_step]
        self._log(f'process//{self._code_number}, {self._code_statement}, {self._code_step}: {code[0]}, {code[1]}', level=1)
        result = getattr(self, '_execute_' + code[0].lower())(code[1])

        # 終了
        return result

    # Transformer

    # statement
    def statement(self, tree):
        return None
        """
        self._log(f'statement: {tree}')
        return tree[0]
        """

    # command_clear
    def command_clear(self, tree):
        code = 'CLEAR'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_clear(self, value):
        self._variables.clear()
        self._arrays.clear()
        self._gosubs.clear()
        self._fors.clear()
        self._data_index = 0
        return None
        """
        self._log(f'command_clear: {tree}')
        self._variables.clear()
        self._arrays.clear()
        self._gosubs.clear()
        self._fors.clear()
        self._data_index = 0
        return [None, None]
        """

    # command_let
    def command_let(self, tree):
        return None
        """
        self._log(f'command_let: {tree}')
        return [None, None]
        """

    # let
    def let(self, tree):
        code = 'LET'
        value = len(tree)
        self._add_code(code, value)
        return None
    def _execute_let(self, value):
        p = self._stacks.pop()
        vars = self._pop_vars()
        self._set_variable(vars, p[1])
        return None
        """
        self._log(f'let: {tree}')
        result = self._set_variable(tree[0], tree[1][1])
        return ['NUMBER', result]
        """

    # command_dim
    def command_dim(self, tree):
        code = 'DIM'
        value = len(tree)
        self._add_code(code, value)
        return None
    def _execute_dim(self, value):
        p_ = []
        for i in range(value):
            p_.append(self._pop_vars())
        p_.reverse()
        return None

    # command_goto
    def command_goto(self, tree):
        code = 'GOTO'
        self._add_code(code, 0)
        return None
    def _execute_goto(self, value):
        p = self._stacks.pop()
        self._code_number = self._get_goto_number(int(p[1]))
        self._code_statement = 0
        self._code_step = 0
        return 'goto'
        """
        self._log(f'command_goto: {tree}')
        return ['goto', int(tree[0][1])]
        """
    
    # command_gosub
    def command_gosub(self, tree):
        code = 'GOSUB'
        self._add_code(code, 0)
        return None
    def _execute_gosub(self, value):
        number, statement = self._get_next_statement(self._code_number, self._code_statement)
        self._gosubs.append([number, statement])
        p = self._stacks.pop()
        self._code_number = self._get_goto_number(int(p[1]))
        self._code_statement = 0
        self._code_step = 0
        return 'goto'
        """
        self._log(f'command_gosub: {tree}')
        return ['gosub', int(tree[0][1])]
        """
    
    # command_return
    def command_return(self, tree):
        code = 'RETURN'
        self._add_code(code, 0)
        return None
    def _execute_return(self, value):
        p = self._gosubs.pop()
        self._code_number = p[0]
        self._code_statement = p[1]
        self._code_step = 0
        return 'goto'
        """
        self._log(f'command_return: {tree}')
        return ['return', None]
        """
    
    # command_on_goto
    def command_on_goto(self, tree):
        code = 'ON_GOTO'
        value = len(tree)
        self._add_code(code, value)
        return None
    def _execute_on_goto(self, value):
        p_ = []
        for i in range(value):
            p_.append(self._stacks.pop())
        p_.reverse()
        self._code_number = self._get_goto_number(int(p_[int(p_[0][1])][1]))
        self._code_statement = 0
        self._code_step = 0
        return 'goto'
        """
        self._log(f'command_on_goto: {tree}')
        return ['goto', int(tree[int(tree[0][1])][1])]
        """
    
    # command_on_gosub
    def command_on_gosub(self, tree):
        code = 'ON_GOSUB'
        value = len(tree)
        self._add_code(code, value)
        return None
    def _execute_on_gosub(self, value):
        p_ = []
        for i in range(value):
            p_.append(self._stacks.pop())
        p_.reverse()
        number, statement = self._get_next_statement(self._code_number, self._code_statement)
        self._gosubs.append([number, statement])
        self._code_number = self._get_goto_number(int(p_[int(p_[0][1])][1]))
        self._code_statement = 0
        self._code_step = 0
        return 'goto'
        """
        self._log(f'command_on_gosub: {tree}')
        return ['gosub', int(tree[int(tree[0][1])][1])]
        """
    
    # command_for
    def command_for(self, tree):
        code = 'FOR'
        value = len(tree)
        self._add_code(code, value)
        return None
    def _execute_for(self, value):
        p3 = self._stacks.pop() if value > 3 else [None, 1]
        p2 = self._stacks.pop()
        p1 = self._stacks.pop()
        v0 = self._pop_vars()
        self._set_variable(v0, p1[1])
        number, statement = self._get_next_statement(self._code_number, self._code_statement)
        self._fors.append([number, statement, v0[1], p2[1], p3[1]])
        return None
        """
        self._log(f'command_for: {tree}')
        # 配列は非対応
        self._set_variable(tree[0], tree[1][1])
        return ['for', tree[0][1], tree[2][1], tree[3][1] if len(tree) >= 4 else 1]
        """
    
    # command_next
    def command_next(self, tree):
        code = 'NEXT'
        value = len(tree)
        self._add_code(code, value)
        return None
    def _execute_next(self, value):
        result = None
        i = len(self._fors) - 1
        if value > 0:
            vars = self._pop_vars()
            while i >= 0 and self._fors[i][2] != vars[1]:
                self._fors.pop()
                i = i - 1
        if i >= 0:
            name = self._fors[i][2]
            kind = 'VARIABLE_STRING' if name[-1] == '$' else ('VARIABLE_INTEGER' if name[-1] == '%' else 'VARIABLE_REAL')
            goal = self._fors[i][3]
            step = self._fors[i][4]
            vars = [kind, name]
            v = self._get_variable(vars) + step
            self._set_variable(vars, v)
            if (step > 0 and v <= goal) or (step < 0 and v >= goal):
                self._code_number = self._fors[i][0]
                self._code_statement = self._fors[i][1]
                self._code_step = 0
                result = 'goto'
            else:
                self._fors.pop()
        return result
        """
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
        """
    
    # command_if
    def command_if(self, tree):
        code = 'IF'
        value = len(tree)
        self._add_code(code, value)
        return None
    def _execute_if(self, value):
        result = None
        p = self._stacks.pop()
        if p[1] == 0:
            self._code_number = self._get_goto_number(self._code_number + 1)
            self._code_statement = 0
            self._code_step = 0
            result = 'goto'
        return result
        """
        self._log(f'command_if: {tree}')
        return [None, None] if tree[0][1] != 0 else ['else', None]
        """
    
    # command_if_goto
    def command_if_goto(self, tree):
        code = 'GOTO'
        self._add_code(code, 0)
        return None
    def _execute_goto(self, value):
        p = self._stacks.pop()
        self._code_number = self._get_goto_number(p[1])
        self._code_statement = 0
        self._code_step = 0
        return 'goto'
        """
        self._log(f'command_if_goto: {tree}')
        return ['goto', int(tree[1][1])] if tree[0][1] != 0 else ['else', None]
        """
    
    # command_stop
    def command_stop(self, tree):
        code = 'STOP'
        self._add_code(code, 0)
        return None
    def _execute_stop(self, value):
        self._code_number = -1
        return None
        """
        self._log(f'command_stop: {tree}')
        return ['stop', None]
        """

    # command_print
    def command_print(self, tree):
        code = 'PRINT'
        value = len(tree)
        self._add_code(code, value)
        return None
    def _execute_print(self, value):
        result = None
        cr = True
        p_ = []
        for i in range(value):
            p_.append(self._stacks.pop())
        p_.reverse()
        for p in p_:
            if p[0] == 'STRING':
                bload = re.search(r'(?i)bload\s*(aka\d)', p[1])
                if bload is not None:
                    if self._view_image(bload.group(1)):
                        result = 'wait'
                else:
                    self._print(p[1])
                    cr = True
            elif p[0] == 'NUMBER':
                self._print(str(int(p[1])))
                cr = True
            elif p[0] == 'SEMICOLON':
                cr = False
            elif p[0] == 'COMMA':
                tab = self._tab - self._cursor_x % self._tab
                while tab > 0:
                    self._print(' ')
                    tab = tab - 1
                cr = True
            else:
                pass
        if cr:
            self._newline()
        return result
        """
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
        """

    # command_input
    def command_input(self, tree):
        code = 'INPUT'
        value = len(tree)
        self._add_code(code, value)
        return None
    def _execute_input(self, value):
        vars = self._pop_vars()
        if value > 1:
            self._execute_semicolon(0)
            self._execute_print(value)
        self._push_vars(vars)
        return 'input'
        """
        self._log(f'command_input: {tree}')
        i = 0
        if tree[i][0] == 'STRING':
            self._print(tree[i][1])
            i = i + 1
        return ['input', tree[i][1]]
        """

    # command_get
    def command_get(self, tree):
        code = 'GET'
        self._add_code(code, 0)
        return None
    def _execute_get(self, value):
        return 'get'
        """
        self._log(f'command_get: {tree}')
        return ['get', tree[0][1]]
        """

    # command_home
    def command_home(self, tree):
        code = 'HOME'
        self._add_code(code, 0)
        return None
    def _execute_home(self, value):
        self._cursor_x = self._text_clip_x
        self._cursor_y = self._text_clip_y
        self._clear_text()
        return None
        """
        self._log(f'command_home: {tree}')
        self._cursor_x = self._text_clip_x
        self._cursor_y = self._text_clip_y
        self._clear_text()
        return [None, None]
        """

    # command_htab
    def command_htab(self, tree):
        code = 'HTAB'
        self._add_code(code, 0)
        return None
    def _execute_htab(self, value):
        p = self._stacks.pop()
        self._cursor_x = int(p[1]) - 1
        return None
        """
        self._log(f'command_htab: {tree}')
        self._cursor_x = int(tree[0][1]) - 1
        return [None, None]
        """

    # command_vtab
    def command_vtab(self, tree):
        code = 'VTAB'
        self._add_code(code, 0)
        return None
    def _execute_vtab(self, value):
        p = self._stacks.pop()
        self._cursor_y = int(p[1]) - 1
        return None
        """
        self._log(f'command_vtab: {tree}')
        self._cursor_y = int(tree[0][1]) - 1
        return [None, None]
        """

    # command_inverse
    def command_inverse(self, tree):
        code = 'INVERSE'
        self._add_code(code, 0)
        return None
    def _execute_inverse(self, value):
        self._text_mode = 'inverse'
        return None
        """
        self._log(f'command_inverse: {tree}')
        self._text_mode = 'inverse'
        return [None, None]
        """

    # command_normal
    def command_normal(self, tree):
        code = 'NORMAL'
        self._add_code(code, 0)
        return None
    def _execute_normal(self, value):
        self._text_mode = 'normal'
        return None
        """
        self._log(f'command_normal: {tree}')
        self._text_mode = 'normal'
        return [None, None]
        """

    # command_text
    def command_text(self, tree):
        code = 'TEXT'
        self._add_code(code, 0)
        return None
    def _execute_text(self, value):
        self._text_clip_x = 0
        self._text_clip_y = 0
        self._text_clip_size_x = self._text_size_x
        self._text_clip_size_y = self._text_size_y
        self._screen_mode = 'text'
        return None
        """
        self._log(f'command_text: {tree}')
        self._text_clip_x = 0
        self._text_clip_y = 0
        self._text_clip_size_x = self._text_size_x
        self._text_clip_size_y = self._text_size_y
        self._screen_mode = 'text'
        return [None, None]
        """

    # command_hgr
    def command_hgr(self, tree):
        code = 'HGR'
        self._add_code(code, 0)
        return None
    def _execute_hgr(self, value):
      # self._text_clip_x = 0
        self._text_clip_y = self._text_size_y - self._text_size_hires
      # self._text_clip_size_x = self._text_size_x
        self._text_clip_size_y = self._text_size_hires
        self._screen_mode = 'hires'
        self._clear_hires()
        return None
        """
        self._log(f'command_hgr: {tree}')
      # self._text_clip_x = 0
        self._text_clip_y = self._text_size_y - self._text_size_hires
      # self._text_clip_size_x = self._text_size_x
        self._text_clip_size_y = self._text_size_hires
        self._screen_mode = 'hires'
        self._clear_hires()
        return [None, None]
        """

    # command_hplot
    def command_hplot(self, tree):
        code = 'HPLOT'
        value = len(tree)
        self._add_code(code, value)
        return None
    def _execute_hplot(self, value):
        positions = []
        for i in range(value):
            p = self._stacks.pop()
            positions.append(p[1])
        positions.reverse()
        self._plot(positions)
        return None
        """
        self._log(f'command_hplot: {tree}')
        positions = []
        for value in tree:
            positions.append(int(value[1]))
        self._plot(positions)
        return [None, None]
        """

    # command_hcolor
    def command_hcolor(self, tree):
        code = 'HCOLOR'
        self._add_code(code, 0)
        return None
    def _execute_hcolor(self, value):
        p = self._stacks.pop()
        # self._color_hires = self._colors[int(p[1])]
        return None
        """
        self._log(f'command_hcolor: {tree}')
        # self._color_hires = self._colors[int(tree[0])]
        return [None, None]
        """

    # command_data
    def command_data(self, tree):
        code = 'DATA'
        self._add_code(code, 0)
        return None
    def _execute_data(self, value):
        return None
        """
        self._log(f'command_data: {tree}')
        return [None, None]
        """

    # command_read
    def command_read(self, tree):
        code = 'READ'
        value = len(tree)
        self._add_code(code, value)
        return None
    def _execute_read(self, value):
        varslist = []
        for i in range(value):
            vars = self._pop_vars()
            varslist.append(vars)
        varslist.reverse()
        for vars in varslist:
            self._set_variable(vars, self._datas[self._data_index])
            self._data_index = self._data_index + 1
        return None
        """
        self._log(f'command_read: {tree}')
        for var in tree:
            self._set_variable(var, self._datas[self._data_index])
            self._data_index = self._data_index + 1
        return [None, None]
        """

    # command_restore
    def command_restore(self, tree):
        code = 'RESTORE'
        self._add_code(code, 0)
        return None
    def _execute_restore(self, value):
        self._data_index = 0
        return None
        """
        self._log(f'command_restore: {tree}')
        self._data_index = 0
        return [None, None]
        """

    # command_poke
    def command_poke(self, tree):
        code = 'POKE'
        self._add_code(code, 0)
        return None
    def _execute_poke(self, value):
        p1 = self._stacks.pop()
        p0 = self._stacks.pop()
        address = int(p0[1])
        param = int(p1[1])
        if address == 32:
            self._text_clip_x = param
        elif address == 33:
            self._text_clip_size_x = param
        elif address == 34:
            bottom = self._text_clip_y + self._text_clip_size_y
            self._text_clip_y = param
            self._text_clip_size_y = bottom - param
        elif address == 35:
            self._text_clip_size_y = param - self._text_clip_y
        elif address == 36:
            self._cursor_x = param
        elif address == 37:
            self._cursor_y = param
        elif address == -16368:
            pass
        return None
        """
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
        """

    # command_call
    def command_call(self, tree):
        code = 'CALL'
        self._add_code(code, 0)
        return None
    def _execute_call(self, value):
        p = self._stacks.pop()
        address = int(p[1])
        if address == -868:
            self._clear_text_line()
        elif address == 62450:
            self._clear_hires()
        return None
        """
        self._log(f'command_call: {tree}')
        address = int(tree[0][1])
        if address == -868:
            self._clear_text_line()
        elif address == 62450:
            self._clear_hires()
        return [None, None]
        """

    # function_abs
    def function_abs(self, tree):
        code = 'ABS'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_abs(self, value):
        p = self._stacks.pop()
        param = abs(p[1])
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'function_abs: {tree}')
        return ['NUMBER', abs(tree[0][1])]
        """

    # function_atn
    def function_atn(self, tree):
        code = 'ATN'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_atn(self, value):
        p = self._stacks.pop()
        param = math.atan(p[1])
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'function_atn: {tree}')
        return ['NUMBER', math.atan(tree[0][1])]
        """

    # function_cos
    def function_cos(self, tree):
        code = 'COS'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_cos(self, value):
        p = self._stacks.pop()
        param = math.cos(p[1])
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'function_cos: {tree}')
        return ['NUMBER', math.cos(tree[0][1])]
        """

    # function_exp
    def function_exp(self, tree):
        code = 'EXP'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_exp(self, value):
        p = self._stacks.pop()
        param = math.exp(p[1])
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'function_exp: {tree}')
        return ['NUMBER', math.exp(tree[0][1])]
        """

    # function_int
    def function_int(self, tree):
        code = 'INT'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_int(self, value):
        p = self._stacks.pop()
        param = int(p[1])
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'function_int: {tree}')
        return ['NUMBER', int(tree[0][1])]
        """

    # function_log
    def function_log(self, tree):
        code = 'LOG'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_log(self, value):
        p = self._stacks.pop()
        param = math.log(p[1])
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'function_log: {tree}')
        return ['NUMBER', math.log(tree[0][1])]
        """

    # function_rnd
    def function_rnd(self, tree):
        code = 'RND'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_rnd(self, value):
        p = self._stacks.pop()
        if p[1] < 0:
            random.seed(p[1])
        param = random.random()
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'function_rnd: {tree}')
        if tree[0][1] < 0:
            random.seed(tree[0][1])
        return ['NUMBER', random.random()]
        """

    # function_sgn
    def function_sgn(self, tree):
        code = 'SGN'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_sgn(self, value):
        p = self._stacks.pop()
        param = 1 if p[1] > 0 else (-1 if p[1] < 0 else 0)
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'function_sgn: {tree}')
        return ['NUMBER', 1 if tree[0][1] > 0 else (-1 if tree[0][1] < 0 else 0)]
        """

    # function_sin
    def function_sin(self, tree):
        code = 'SIN'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_sin(self, value):
        p = self._stacks.pop()
        param = math.sin(p[1])
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'function_sin: {tree}')
        return ['NUMBER', math.sin(tree[0][1])]
        """

    # function_sqr
    def function_sqr(self, tree):
        code = 'SQR'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_sqr(self, value):
        p = self._stacks.pop()
        param = math.sqrt(p[1])
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'function_sqr: {tree}')
        return ['NUMBER', math.sqrt(tree[0][1])]
        """

    # function_tan
    def function_tan(self, tree):
        code = 'TAN'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_tan(self, value):
        p = self._stacks.pop()
        param = math.tan(p[1])
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'function_tan: {tree}')
        return ['NUMBER', math.tan(tree[0][1])]
        """

    # function_len
    def function_len(self, tree):
        code = 'LEN'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_len(self, value):
        p = self._stacks.pop()
        param = len(p[1])
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'function_len: {tree}')
        return ['NUMBER', len(tree[0][1])]
        """

    # function_left
    def function_left(self, tree):
        code = 'LEFT'
        self._add_code(code, 0)
        return 'STRING'
    def _execute_left(self, value):
        p1 = self._stacks.pop()
        p0 = self._stacks.pop()
        param = p0[1][:int(p1[1])]
        self._stacks.append(['STRING', param])
        return None
        """
        self._log(f'function_left: {tree}')
        return ['STRING', tree[0][1][:int(tree[1])]]
        """

    # function_mid
    def function_mid(self, tree):
        code = 'MID'
        value = len(tree)
        self._add_code(code, value)
        return 'STRING'
    def _execute_mid(self, value):
        p2 = self._stacks.pop() if value > 2 else None
        p1 = self._stacks.pop()
        p0 = self._stacks.pop()
        head = int(p1[1])
        tail = int(p1[1]) + (int(p2[1]) if value > 2 else len(p0[1]))
        param = p0[1][head:tail]
        self._stacks.append(['STRING', param])
        return None
        """
        self._log(f'function_mid: {tree}')
        head = int(tree[1][1])
        tail = int(tree[1][1]) + int(tree[2][1]) if len(tree) > 2 else len(tree[0][1])
        return ['STRING', tree[0][1][head:tail]]
        """

    # function_right
    def function_right(self, tree):
        code = 'RIGHT'
        self._add_code(code, 0)
        return 'STRING'
    def _execute_right(self, value):
        p1 = self._stacks.pop()
        p0 = self._stacks.pop()
        param = p0[1][-int(p1[1]):]
        self._stacks.append(['STRING', param])
        return None
        """
        self._log(f'function_right: {tree}')
        return ['STRING', tree[0][1][-int(tree[1]):]]
        """

    # function_asc
    def function_asc(self, tree):
        code = 'ASC'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_asc(self, value):
        p = self._stacks.pop()
        param = ord(p[1][0])
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'function_asc: {tree}')
        return ['NUMBER', ord(tree[0][1][0])]
        """

    # function_chr
    def function_chr(self, tree):
        code = 'CHR'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_chr(self, value):
        p = self._stacks.pop()
        param = chr(int(p[1]))
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'function_chr: {tree}')
        return ['NUMBER', chr(int(tree[0][1]))]
        """

    # function_str
    def function_str(self, tree):
        code = 'STR'
        self._add_code(code, 0)
        return 'STRING'
    def _execute_str(self, value):
        p = self._stacks.pop()
        param = str(int(p[1]))
        self._stacks.append(['STRING', param])
        return None
        """
        self._log(f'function_str: {tree}')
        return ['STRING', str(int(tree[0][1]))]
        """

    # function_val
    def function_val(self, tree):
        code = 'VAL'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_val(self, value):
        p = self._stacks.pop()
        param = 0.0
        try:
            param = float(p[1])
        except:
            pass
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'function_val: {tree}')
        result = 0.0
        try:
            result = float(tree[0][1])
        except:
            pass
        return ['NUMBER', result]
        """

    # function_peek
    def function_peek(self, tree):
        code = 'PEEK'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_peek(self, value):
        p = self._stacks.pop()
        result = None
        if p[1] == -16384:
            result = 'inkey'
        return result
        """
        self._log(f'function_peek: {tree}')
        result = 0
        address = int(tree[0][1])
        if address == -16384:
            result = self._inkey()
            self._key_peek_16384 = True
        return ['NUMBER', result]
        """

    # expression
    def expression(self, tree):
        return 'NUMBER'
        """
        self._log(f'expression: {tree}')
        return tree[0]
        """

    # logical_or
    def logical_or(self, tree):
        value = len(tree)
        if value > 1:
            code = 'OR'
            self._add_code(code, value)
        return 'NUMBER'
    def _execute_or(self, value):
        param = 0
        for i in range(value):
            p = self._stacks.pop()
            if p[1] != 0:
                param = 1
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'logical_or: {tree}')
        result = tree[0][1]
        if len(tree) > 1:
            result = 0
            for value in tree:
                if value[1] != 0:
                    result = 1
        return ['NUMBER', result]
        """

    # logical_and
    def logical_and(self, tree):
        value = len(tree)
        if value > 1:
            code = 'AND'
            self._add_code(code, value)
        return 'NUMBER'
    def _execute_and(self, value):
        param = 1
        for i in range(value):
            p = self._stacks.pop()
            if p[1] == 0:
                param = 0
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'logical_and: {tree}')
        result = tree[0][1]
        if len(tree) > 1:
            result = 1
            for value in tree:
                if value[1] == 0:
                    result = 0
        return ['NUMBER', result]
        """

    # compare
    def compare(self, tree):
        return 'NUMBER'
        """
        self._log(f'compare: {tree}')
        return tree[0]
        """

    # greater
    def greater(self, tree):
        code = 'GREATER'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_greater(self, value):
        p1 = self._stacks.pop()
        p0 = self._stacks.pop()
        param = 1 if p0[1] > p1[1] else 0
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'greater: {tree}')
        return ['NUMBER', 1 if tree[0][1] > tree[1][1] else 0]
        """
        
    # greater_equal
    def greater_equal(self, tree):
        code = 'GREATER_EQUAL'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_greater_equal(self, value):
        p1 = self._stacks.pop()
        p0 = self._stacks.pop()
        param = 1 if p0[1] >= p1[1] else 0
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'greater: {tree}')
        return ['NUMBER', 1 if tree[0][1] >= tree[1][1] else 0]
        """
        
    # less
    def less(self, tree):
        code = 'LESS'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_less(self, value):
        p1 = self._stacks.pop()
        p0 = self._stacks.pop()
        param = 1 if p0[1] < p1[1] else 0
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'less: {tree}')
        return ['NUMBER', 1 if tree[0][1] < tree[1][1] else 0]
        """
        
    # less_equal
    def less_equal(self, tree):
        code = 'LESS_EQUAL'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_less_equal(self, value):
        p1 = self._stacks.pop()
        p0 = self._stacks.pop()
        param = 1 if p0[1] <= p1[1] else 0
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'less_equal: {tree}')
        return ['NUMBER', 1 if tree[0][1] <= tree[1][1] else 0]
        """
        
    # equal
    def equal(self, tree):
        code = 'EQUAL'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_equal(self, value):
        p1 = self._stacks.pop()
        p0 = self._stacks.pop()
        param = 1 if p0[1] == p1[1] else 0
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'equal: {tree}')
        return ['NUMBER', 1 if tree[0][1] == tree[1][1] else 0]
        """
        
    # not_equal
    def not_equal(self, tree):
        code = 'NOT_EQUAL'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_not_equal(self, value):
        p1 = self._stacks.pop()
        p0 = self._stacks.pop()
        param = 1 if p0[1] != p1[1] else 0
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'not_equal: {tree}')
        return ['NUMBER', 1 if tree[0][1] != tree[1][1] else 0]
        """
        
    # sum
    def sum(self, tree):
        return 'NUMBER'
        """
        self._log(f'sum: {tree}')
        return tree[0]
        """

    # addition
    def addition(self, tree):
        code = 'ADDITION'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_addition(self, value):
        p1 = self._stacks.pop()
        p0 = self._stacks.pop()
        param = p0[1] + p1[1]
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'addition: {tree}')
        return ['NUMBER', tree[0][1] + tree[1][1]]
        """

    # subtraction
    def subtraction(self, tree):
        code = 'SUBTRACTION'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_subtraction(self, value):
        p1 = self._stacks.pop()
        p0 = self._stacks.pop()
        param = p0[1] - p1[1]
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'subtraction: {tree}')
        return ['NUMBER', tree[0][1] - tree[1][1]]
        """

    # product
    def product(self, tree):
        return 'NUMBER'
        """
        self._log(f'product: {tree}')
        return tree[0]
        """

    # multiply
    def multiply(self, tree):
        code = 'MULTIPLY'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_multiply(self, value):
        p1 = self._stacks.pop()
        p0 = self._stacks.pop()
        param = p0[1] * p1[1]
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'multiply: {tree}')
        return ['NUMBER', tree[0][1] * tree[1][1]]
        """

    # division
    def division(self, tree):
        code = 'DIVISION'
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_division(self, value):
        p1 = self._stacks.pop()
        p0 = self._stacks.pop()
        param = p0[1] / p1[1]
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'division: {tree}')
        return ['NUMBER', tree[0][1] / tree[1][1]]
        """

    # exponent
    def exponent(self, tree):
        return 'NUMBER'
        """
        self._log(f'exponent: {tree}')
        return tree[0]
        """

    # power
    def power(self, tree):
        code = "POWER"
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_power(self, value):
        p1 = self._stacks.pop()
        p0 = self._stacks.pop()
        param = p0[1] ** p1[1]
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'power: {tree}')
        return ['NUMBER', tree[0][1] ** tree[1][1]]
        """

    # atom
    def atom(self, tree):
        return 'NUMBER'
        """
        self._log(f'atom: {tree}')
        return tree[0]
        """

    # positive
    def positive(self, tree):
        return 'NUMBER'
        """
        self._log(f'positive: {tree}')
        return tree[0]
        """

    # negative
    def negative(self, tree):
        code = "NEGATIVE"
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_negative(self, value):
        p = self._stacks.pop()
        param = -p[1]
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'negative: {tree}')
        return ['NUMBER', -tree[0][1]]
        """

    # negation
    def negation(self, tree):
        code = "NEGATION"
        self._add_code(code, 0)
        return 'NUMBER'
    def _execute_negation(self, value):
        p = self._stacks.pop()
        param = 1 if p[1] == 0 else 0
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'negation: {tree}')
        return ['NUMBER', 1 if tree[0][1] == 0 else 0]
        """

    # factor
    def factor(self, tree):
        if tree[0] == 'VARIABLE_REAL' or tree[0] == 'VARIABLE_INTEGER':
            code = 'FACTOR'
            self._add_code(code, 0)
        return 'NUMBER'
    def _execute_factor(self, value):
        vars = self._pop_vars()
        param = self._get_variable(vars)
        self._stacks.append(['NUMBER', param])
        return None
        """
        self._log(f'factor: {tree}')
        result = tree[0][1] if tree[0][0] != 'VARIABLE_REAL' and tree[0][0] != 'VARIABLE_INTEGER' else self._get_variable(tree[0])
        return ['NUMBER', result]
        """

    # sentence
    def sentence(self, tree):
        return 'STRING'
        """
        self._log(f'sentence: {tree}')
        return tree[0]
        """

    # strcat
    def strcat(self, tree):
        code = 'STRCAT'
        self._add_code(code, 0)
        return 'STRING'
    def _execute_strcat(self, value):
        p1 = self._stacks.pop()
        p0 = self._stacks.pop()
        param = p0[1] + p1[1]
        self._stacks.append(['STRING', param])
        return None
        """
        self._log(f'strcat: {tree}')
        return ['STRING', tree[0][1] + tree[1][1]]
        """

    # term
    def term(self, tree):
        if tree[0] == 'VARIABLE_STRING':
            code = 'TERM'
            self._add_code(code, 0)
        return 'STRING'
    def _execute_term(self, value):
        vars = self._pop_vars()
        param = self._get_variable(vars)
        self._stacks.append(['STRING', param])
        return None
        """
        self._log(f'term: {tree}')
        result = tree[0][1] if tree[0][0] != 'VARIABLE_STRING' else self._get_variable(tree[0])
        return ['STRING', result]
        """

    # variable_number
    def variable_number(self, tree):
        code = 'VARIABLE_REAL' if tree[0] == 'NAME_REAL' else 'VARIABLE_INTEGER'
        value = len(tree)
        self._add_code(code, value)
        return code
    def _execute_variable_real(self, value):
        self._stacks.append(['VARIABLE_REAL', value])
        return None
    def _execute_variable_integer(self, value):
        self._stacks.append(['VARIABLE_INTEGER', value])
        return None
        """
        self._log(f'variable_number: {tree}')
        result = ['VARIABLE_REAL' if tree[0][0] == 'NAME_REAL' else 'VARIABLE_INTEGER']
        for i in range(len(tree)):
            result.append(tree[i][1])
        return result
        """

    # variable_string
    def variable_string(self, tree):
        code = 'VARIABLE_STRING'
        value = len(tree)
        self._add_code(code, value)
        return 'VARIABLE_STRING'
    def _execute_variable_string(self, value):
        self._stacks.append(['VARIABLE_STRING', value])
        return None
        """
        self._log(f'variable_string: {tree}')
        result = ['VARIABLE_STRING']
        for i in range(len(tree)):
            result.append(tree[i][1])
        return result
        """

    # NAME_REAL
    def NAME_REAL(self, tree):
        code = 'NAME_REAL'
        value = tree.value.upper()[0:2]
        self._add_code(code, value)
        return code
    def _execute_name_real(self, value):
        self._stacks.append(['NAME_REAL', value])
        return None
        """
        self._log(f'NAME_REAL: {tree}')
        return ['NAME_REAL', tree.value.upper()[0:2]]
        """

    # NAME_INTERER
    def NAME_INTEGER(self, tree):
        code = 'NAME_INTEGER'
        tail = 2 if len(tree.value) > 2 else 1
        value = tree.value.upper()[0:tail] + '%'
        self._add_code(code, value)
        return code
    def _execute_name_integer(self, value):
        self._stacks.append(['NAME_INTEGER', value])
        return None
        """
        self._log(f'NAME_INTEGER: {tree}')
        tail = 2 if len(tree.value) > 2 else 1
        return ['NAME_INTEGER', tree.value.upper()[0:tail] + '%']
        """

    # NAME_STRING
    def NAME_STRING(self, tree):
        code = 'NAME_STRING'
        tail = 2 if len(tree.value) > 2 else 1
        value = tree.value.upper()[0:tail] + '$'
        self._add_code(code, value)
        return code
    def _execute_name_string(self, value):
        self._stacks.append(['NAME_STRING', value])
        return None
        """
        self._log(f'NAME_STRING: {tree}')
        tail = 2 if len(tree.value) > 2 else 1
        return ['NAME_STRING', tree.value.upper()[0:tail] + '$']
        """

    # NUMBER
    def NUMBER(self, tree):
        code = 'NUMBER'
        value = tree.value
        self._add_code(code, value)
        return code
    def _execute_number(self, value):
        self._stacks.append(['NUMBER', float(value)])
        return None
        """
        self._log(f'NUMBER: {tree}')
        return ['NUMBER', float(tree.value)]
        """

    # STRING
    def STRING(self, tree):
        code = 'STRING'
        tail = len(tree.value) - 1
        if tree.value[0] == "\"":
            if tree.value[tail] == "\"":
                tail = tail - 1
        elif tree.value[0] == "'":
            if tree.value[tail] == "'":
                tail = tail - 1
        value = tree.value[1:tail + 1]
        self._add_code(code, value)
        return code
    def _execute_string(self, value):
        self._stacks.append(['STRING', value])
        return None
        """
        self._log(f'STRING: {tree}')
        tail = len(tree.value) - 1
        if tree.value[0] == "\"":
            if tree.value[tail] == "\"":
                tail = tail - 1
        elif tree.value[0] == "'":
            if tree.value[tail] == "'":
                tail = tail - 1
        return ['STRING', tree.value[1:tail + 1]]
        """

    # SEMICOLON
    def SEMICOLON(self, tree):
        code = 'SEMICOLON'
        self._add_code(code, 0)
        return code
    def _execute_semicolon(self, value):
        self._stacks.append(['SEMICOLON'])
        return None
        """
        self._log(f'SEMICOLON: {tree}')
        return ['SEMICOLON', 0]
        """

    # COMMA
    def COMMA(self, tree):
        code = 'COMMA'
        self._add_code(code, 0)
        return code
    def _execute_comma(self, value):
        self._stacks.append(['COMMA'])
        return None
        """
        self._log(f'COMMA: {tree}')
        return ['COMMA', 0]
        """

    # スタックへ変数を設定する
    def _push_vars(self, vars):
        length = len(vars)
        i = length - 1
        while i > 2:
            self._stacks.append('NUMBER', vars[i])
            i = i - 1
        kind = 'NAME_STRING' if vars[1][-1] == '$' else ('NAME_INTEGER' if vars[1][-1] == '%' else 'NAME_REAL')
        self._stacks.append([kind, vars[1]])
        self._stacks.append([vars[0], length - 1])

    # スタックから変数を取得する
    def _pop_vars(self):
        p0 = self._stacks.pop()
        vars = []
        for i in range(p0[1]):
            p1 = self._stacks.pop()
            vars.append(p1[1])
        vars.append(p0[0])
        vars.reverse()
        return vars

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
        maximum = max(self._codes)
        while (number <= maximum) and (not number in self._codes):
            number = number + 1
        return int(number if number <= maximum else -1)

    # 次のコードを取得する
    def _get_next_code(self, number, statement, step):
        step = step + 1
        if step >= len(self._codes[number][statement]):
            number, statement = self._get_next_statement(number, statement)
            step = 0
        return number, statement, step

    # 次のステートメントを取得する
    def _get_next_statement(self, number, statement):
        statement = statement + 1
        if statement >= len(self._codes[number]):
            number = self._get_goto_number(number + 1)
            statement = 0
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
jsonfile = ['./AKA0.json', './AKA6.json']
jsonstep = 0

# Pyxel の更新を行う
#
def update():

    # グローバル宣言
    global applesoftbasic
    global jsonfile
    global jsonstep

    # ApplesoftBasic の生成
    if applesoftbasic is None:
        applesoftbasic = ApplesoftBasic()
        applesoftbasic.ready(jsonfile[jsonstep])

    # ApplesoftBasic の更新
    if applesoftbasic is not None:
        result = applesoftbasic.update()
        if not result:
            applesoftbasic = None
            jsonstep = jsonstep + 1
            if jsonstep >= len(jsonfile):
                jsonstep = 0

# Pyxel の描画を行う
#
def draw():

    # グローバル宣言
    global applesoftbasic

    # ApplesoftBasic の描画
    if applesoftbasic is not None:
        applesoftbasic.draw()

# Pyxel を実行する
#
def run():

    # Pyxel の初期化
    pyxel.init(240, 192, title = 'Akalabeth: World of Doom')

    # リソースの読み込み
    pyxel.load('./akalabeth.pyxres')

    # 画面のクリア
    pyxel.cls(0)

    # Pyxel の実行
    pyxel.run(update, draw)

# アプリケーションのエントリポイント
#
if __name__ == '__main__':

    # ゲームの実行
    run()
