



def decorate_event(method):
    """ setup a method as an event """
    setattr(method, "__is_event", True )
    print("decorate_event", method)
    return method

def decorate_set_on_listener(prototype):
    """ Private decorator for use in the editor.
        Allows the Editor to create listener methods.

        Args:
            params (str): The list of parameters for the listener
                method (es. "(self, new_value)")
    """
    # noinspection PyDictCreation,PyProtectedMember
    def add_annotation(method):
        method._event_info = {'name':method.__name__, 'prototype':prototype}
        print("qq", method.__name__, method)
        return method

    return add_annotation


@decorate_event
def myfunc():
    print("YOO")

#@decorate_set_on_listener(lambda x: print(f'YOO2:{x}'))
def myfunc2():
    print("YOO2")

class MyClass:

    def __init__(self):
        pass

    @decorate_set_on_listener(lambda x: print(f'YOO2:{x}'))
    @decorate_event
    def mycallback(self):
        print("callback2")



print(myfunc.__is_event)

myclass=MyClass()

print(myclass.mycallback.__is_event)
#print(myfunc2._event_info)
#myfunc2._event_info['prototype']("hej")

myclass.mycallback._event_info['prototype']("hej2")