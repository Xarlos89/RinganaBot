from Functions import *


def TEST_Cart_addItem(): # Opens testing, tests products in shopping cart. 
	login_to_test()
	TEST_Cart_Add_ranItem()

def TEST_make_new_customer(): # Creates a new test customer
	login_to_test()
	TEST_new_Customer()


if __name__ == "__main__":

	# TEST_Cart_addItem()
	TEST_make_new_customer()