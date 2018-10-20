class Employee:

    raise_amount = 1.04
    nums_of_emps = 0

    def __init__(self, name, last, pay):
        self.name = name
        self.last = last
        self.pay = pay
        self.email = name + '' + last + '@company.com'

        Employee.nums_of_emps += 1

    def fullname(self):
        return self.name + ' ' + self.last

    def apply_raises(self):
        self.pay = int(self.pay * Employee.raise_amount)

    @classmethod
    def set_raise_amt(cls, amount):
        cls.raise_amount = amount


Employee.set_raise_amt(1.5)

emp_1 = Employee('Corey', 'Shafrey', 5000)
emp_2 = Employee('John', 'Smith', 3000)
emp_1.raise_amount= 1.6
print(emp_1.fullname())
print(emp_1.email)
print(emp_1.__dict__)
print(emp_2.__dict__)
print(emp_2.raise_amount)
print(Employee.nums_of_emps)