import threading
 
num = 10

def print_cube():
    global num
    while num < 17:
        print("Cube: {}" .format(num * num * num))
 
 
def print_square():
    global num
    while num < 15:
        print("Square: {}" .format(num * num))

def print_num():
    for i in range(20):
        global num
        num += i
        print("Number: {}" .format(num))

def modify_boolean(my_bool):
    # Modifying the boolean value
    my_bool[0] = not my_bool[0]


 
 
if __name__ =="__main__":
    # t1 = threading.Thread(target=print_square)
    # t2 = threading.Thread(target=print_cube)
    # t3 = threading.Thread(target=print_num)
 
    # t1.start()
    # t2.start()
    # t3.start()
    
    # t1.join()
    # t2.join()
    # t3.join()
 
    # print("Done!")
    # Creating a boolean variable
    original_boolean = [True]

    # Passing a reference to the boolean to the function
    modify_boolean(original_boolean)

    # The original boolean remains unchanged
    print(original_boolean)  # Output: True