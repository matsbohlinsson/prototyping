import pickle
import dill



def foo2():
    print("hej")

pickled = pickle.dumps(foo2)
print(pickled)
print(foo2.__repr__())
