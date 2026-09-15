#mimiking the porperty descriptor class
class MyDescriptor:
    def __init__(self,fget=None,fset=None,fdel=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel

    def __get__(self,instance,owner):
        if instance is None:
            return self
        return self.fget(instance)

    def __set__(self, instance, value):
        if self.fset is None:
            return AttributeError(f"No setter function is defind by your instance {instance}")
        return self.fset(instance,value)

    def setter(self,fset): # it's not setter(self.fget)
        return MyDescriptor(self.fget,fset,self.fdel) # Don't call with 'self' as python adds it while calling. if added error.
    

class A:
    def helloA(self):
        print(f"Im at A and my self object is {type(self)} \n")

class B(A):
    def hello(self):
        # super().hello()
        # A.hello(B())
        # A().hello()
        print(f"Im at B and my self object is {type(self)} \n")

class C(B):
    def hello(self):
        print(f"before super: {type(self)} \n")
        # class C(A,B):
        # super().hello()
        # A.hello(B())
        # A().hello()

        # class C(B) class B(A) class A
        # super().hello()
        
        '''
        Important: Although I don't inherit A, I still able to access beacuse A is in the module's namespace.
        Even if B doesn't inheirt A, I still be able to access A here.

        Important: If I super(), then if I access a function thats only at A and if B doesn't ineherit A (or)
        C doesn't inherit A & B, then I can't access A and it's variable & method as __mro__ of this class C won't
        have class A.
        '''
        # B.hello(A()) # It works 
        # A().hello() # It also still works

        # class C(B) class B class A
        # super().helloA() # fail

        # class C(B) class B(A) class A
        super().helloA() # Pass ((<class '__main__.C'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>))

        print(f"after super: {type(self)} \n")
        print("C")

class Income:
    def __init__(self,income):
        self.income = income

    def __str__(self):
        return f"Income is {self.income}"

    def __add__(self, other):
        return Income(self.income+other.income)

def main():
    # alter_list_inside_tuple()
    working_with_class()

def working_with_class():
    # print(type(Family())) # Out - <class '__main__.Family'>
    # print(type(Family)) # Out - <class 'type'>

    # Initializing the contents of object using object
    '''
    Class Family:
        ...
    '''
    # family = Family()
    # family.name = "Jayesh"
    # family.age = 20
    # print(Family.__dict__)
    # print(type(Family.__dict__))
    # print(family)
    # print(f"I'm {family.name} from MSK family and I'm {family.age} years old") # here we won't get age under the auto suggesstion

    # Initializing the contents of object using class (__init__ method)
    '''
    class Family:
        def __str__(self):
            return "Hello there!!! Im Family object"
            
        def __init__(self,name,age):
            # Validating atttrubutes:
            if age > 60:
                raise ValueError("Sorry you entered wrong age. We all are below age 60")
            self.name = name
            self.age = age

        @MyDescriptor
        def name(self):
            return self._name

        @name.setter
        def name(self,name):
            if name not in [
                'Jayesh',
                'Kannan',
                'Latha',
                'Suba'
            ]:
                raise ValueError("Sorry you are not belong to family")
            self._name = name
        
        def fav_food(self):
            match self.name:
                case "Jayesh":
                    print("Dosa with Paruppu Sambar and Chatni")
                case "Kannan" | "Suba":
                    print("Pori")
                case "Latha":
                    print("Badhusa")
                case _:
                    print(":( Who are you?)")
    '''
    # family = Family("Jayesh",20)
    # print(f"Im {family.name} from MSK family and I'm {family.age} years old")
    # family.fav_food()

    #Failing
    # family.name = "Jk"

    #Passing
    # family.name = "Jayesh"
    # print(family.name)

    #Won't crash, but retuns the MyDescriptor instance obj
    # print(Family.name)

    # print(family._name)
    # print(family.__dict__) #{'_name': 'Jayesh', 'age': 20}
    # Imp: __static_attributes__ is metadata Python records about attribute names 
    # that are assigned through self.attribute = ... (ie., its instance). Our class does't have
    # _name in its namespace Family.__dict__["_name"] will fail.
    # print(Family.__dict__["__static_attributes__"]) # ('_name', 'age', 'name')
    # family._name = "Jk"
    # print(Family.name.__dict__)

    # Task - Family that we are trying to create is only one. ie., only one Kannan Family.
    # So creating multiple instances of Family class is wrong. All the family members are also
    # only one. There is only one Jayesh. How to avoid having multiple Jayesh, or multiple family - 
    # *****************Class variables & methods****************
    '''
    class Family:
        members = ["Jayesh","Kannan","Latha","Suba Lakshmi"]
        food = ["Dosa-Samabar","Poori-Masal","Nan-PannerButterMsala","Chapathi-ChannaMsala"]

        @classmethod
        def fav_food(cls,name):
            print(f"{name}'s fav food is {cls.food[3]}") # can be accessed only using "cls." as it's present inside the class obj's namespace
    '''
    # print(Family.members)
    # Family.fav_food("Jayesh")

    # Inhertiance play
    c = C()
    # print(C.__mro__) # (<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class 'object'>)
    # c.hello()

    # Operator overloading
    Jayesh = Income(70000)
    print(f"Jayesh's",Jayesh)

    Kannan = Income(30000)
    print(f"Kannan's", Kannan)

    print(f"Total family's",Jayesh + Kannan)


def alter_list_inside_tuple():
    # if a tuple's value is a list I can alter them.
    family = (["Jayesh","Kannan"],["Latha","Suba"])
    male = family[0]
    temp = male[0]
    male[0] = male[1]
    male[1] = temp
    print(family)

if __name__ == "__main__":
    main()