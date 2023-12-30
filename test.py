# from contextlib import contextmanager
import numpy as np
# @contextmanager
# def my_context_manager():
#     # 在进入代码块之前执行的操作，相当于 __enter__ 方法
#     print("Entering the context")

#     # yield 之前的代码部分相当于 __enter__ 方法的内容
#     yield "Hello, World!"

#     # 在离开代码块时执行的操作，相当于 __exit__ 方法
#     print("Leaving the context")

# # 使用 with 语句来使用上下文管理器
# with my_context_manager() as value:
#     print("Inside the context")
#     print("Received value:", value)

# # 离开 with 语句后，会执行 __exit__ 方法中的内容
# class MyClass:
#     def __init__(self, value):
#         self.value = value

#     def __add__(self, other):
#         print("Calling __add__")

#     def __radd__(self, other):
#         print("Calling __radd__")

# # 创建两个实例
# obj1 = MyClass(5)
# obj2 = MyClass(10)

# # 调用 __add__ 方法
# result1 = obj1 + obj2  # 输出: Calling __add__

# # 调用 __radd__ 方法
# result2 = 20 + obj1    # 输出: Calling __radd__

# # 调用 __radd__ 方法
# result3 = obj2 + 20    # 输出: Calling __radd__

# X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

# for i in range(X.shape[0])[0::2]:
#     print(i)

# for i in range(X.shape[0])[1::2]:
#     print(i)

import psutil
import time

def memory_usage():
    # 获取当前进程的内存使用情况
    process = psutil.Process()
    memory_info = process.memory_info()

    # 打印内存使用情况
    print(f"Memory used: {memory_info.rss / (1024 ** 2):.2f} MB")

if __name__ == "__main__":
    # 在你的代码逻辑之前调用 memory_usage() 记录初始内存使用情况
    memory_usage()

    # 你的代码逻辑
    a = [1] * 10**6
    b = [2] * 10**7
    del b

    # 在你的代码逻辑之后再次调用 memory_usage() 记录结束时的内存使用情况
    memory_usage()
