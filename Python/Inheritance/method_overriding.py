class Parent(): 
	
	def __init__(self): 
		self.value = "Inside Parent"
		
	def show(self): 
		print(self.value) 
		
class Child(Parent): 
	
	def __init__(self): 
		super().__init__() 
		self.value = "Inside Child"
		

	def show(self): 
		print(self.value) 
		

obj1 = Parent() 
obj2 = Child() 

obj1.show() 
obj2.show()  

class Parent1(): 
		 
	def show(self): 
		print("Inside Parent1") 
		 
class Parent2(): 
		
	def display(self): 
		print("Inside Parent2") 
		
		
class Child(Parent1, Parent2): 
		
	def show(self): 
		print("Inside Child") 
	

obj = Child() 

obj.show() 
obj.display()