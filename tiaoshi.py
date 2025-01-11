############################################################
import inspect
import pdb
import os

def get_vname():
    frame = inspect.currentframe()  # 当前函数的栈帧
    call_frame = frame.f_back.f_back  # 获取调用 `t` 的上一级栈帧
    call_code = inspect.getframeinfo(call_frame).code_context[0].strip()  # 获取调用代码并去除空白
    arg_str = call_code.split('(')[1].split(')')[0]  # 提取括号中的所有参数
    first_arg = arg_str.split(',')[0].strip()  # 提取第一个参数

    # 如果直接传递的是变量
    if first_arg.isidentifier():
        print(f"Variable name: {first_arg}", end='-'*10)
        print_caller_file_and_line(3)
    else:
        print("No variable name found.", end='-'*10)
        print_caller_file_and_line(3)
 
def print_caller_file_and_line(depth=2):
    # 获取调用栈信息
    stack = inspect.stack()
    # 调用方位于栈的第二层
    caller_frame = stack[depth]
    caller_file = os.path.basename(caller_frame.filename)  # 调用者的文件名
    caller_line = caller_frame.lineno  # 调用者的行号
    print(f"调试文件: {caller_file}, 所在行号: {caller_line}")

def tiaoshi(x=None, exit0=True, details=False, mulp=False, get_name=True, use_debug=True):
    if not use_debug:
        return
    if get_name:
        get_vname()
    print(type(x))
    if isinstance(x,str):
        print(x)
        t = input('continue?(stop or else)')
        if t == 'stop':
            exit(0)
        return
    try:
        x[0]
    except:
        if isinstance(x,dict):
            ks = list(x.keys())
            print(ks)
            t = input('show dict details?(y/n) ')
            while t in ['y','Y']:
                tt = input(f'which key to visit?(input key name or index[0-{len(ks)-1}]) ')
                try:
                    tiaoshi(x[tt],exit0=False)
                except:
                    if tt.isdigit() and int(tt) < len(ks):
                        tt = int(tt)
                        tt = ks[tt]
                        print(f'{"*"*10}visit key "{tt}"{"*"*10}')
                        tiaoshi(x[tt],exit0=False)
                    else:
                        print('no such key in dict!')
                t = input('continue show dict details?(y/n) ')
            return
        else:
            print(x)
            t = input('continue?(stop or else)')
            if t == 'stop':
                exit(0)
            if exit0:
                print_caller_file_and_line(2)
                exit(0)
            else:
                return
    try:
        print(x.shape)
    except:
        try:
            print(len(x))
            if isinstance(x,list):
                if not all(type(y) == type(x[0]) for y in x):
                    if input('Customized Warning: the list has different data types! show them all?(y/n)') in ['y','Y']:
                        for ele in x:
                            print(type(ele))
                printlen = input("print how much elements' shape? (default 0) ")
                if printlen.isdigit():
                    for idx in range(min(len(x),int(printlen))):
                        try:
                            print(x[idx].shape)
                        except:
                            print(f"can't get x[{idx}] shape,  x[{idx}] has type: {type(x[idx])}")
                            t = input('continue?(stop or else)')
                            if t == 'stop':
                                exit(0)
        except:
            print("can't get shape or len")
    if not mulp:
        t = input('show details?(y/n)')
        if t == 'pdb':
            pdb.set_trace()
        elif t == 'stop':
            exit(0)
        elif t in ['y', 'Y']:
            details = True
        if details:
            print(x)
        # 更深入查看
        deep_visit = input('show details for sub elements?(y/n)')
        visit_remember = []
        while deep_visit in ['y', 'Y']:
            idx = input(f'to visit which element?(range[0-{len(x)-1}], default 0)')
            if idx.isdigit() and int(idx) < len(x):
                idx = int(idx)
            else:
                idx = 0
            print(f"{'*'*10}now visit x[{idx}]{'*'*10}")
            tiaoshi(x[idx], exit0=False, get_name=False)
            visit_remember.append(idx)
            print(f"{'*'*10}x{set(visit_remember)} has been visited{'*'*10}")
            deep_visit = input('show details for sub elements?(y/n)')
    if exit0:
        print_caller_file_and_line(2)
        exit(0)
#############################################################
