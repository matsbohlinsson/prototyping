
def setname(self, name):
    print(f'setname() called {name}')
def getname(self):
    print(f'getname() called')
    return 'din mamma'


class In:
    name=property(getname, setname)



p1=In()
p1.name="Steve"

p2=In()
p2.name="Steve2"
