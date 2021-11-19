#!/usr/bin/env python3


class Limiter:
    def __init__(self, min=0.1, max=1.0):
        self.min = min
        self.max = max
        self.value = max

    def __get__(self, obj, objtype):
        return self.value

    def __set__(self, obj, value):
        if value < self.min:
            self.value = self.min

        elif value > self.max:
            self.value = self.max

        else:
            self.value = value
        print('limiter: ', self.value)

#
# def limiter(min=0.1, max=1.0):
#     def wrapper(value):
#         if value < min:
#             value = min
#         elif value > max:
#             value = max
#         else:
#             value = value
#     return wrapper
