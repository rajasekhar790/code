#####################################################################################
def checkDuplicates(arr):
        
        seen = set()
        dup = []

        for num in arr:
            if num in seen:
                dup.append(num)
            seen.add(num)

        if not dup:
             print("No duplicatea")
        else:
           return(f" There are the duplicate elements {dup}")
#######################################################################################
# another way of finding the duplicates

def find_duplicates(x):
  length = len(x)
  duplicates = []

  for i in range(length):
    n = i + 1
    for a in range(n, length):
        if x[i] == x[a] and x[i] not in duplicates:
          duplicates.append(x[i])
  return duplicates


#########################################################################################

#using direct list 
my_list = ["apple", "banana", "cherry"]
for fruit in my_list:
    print(fruit)  # Prints each fruit, but not its index

#using range 
my_list = ["apple", "banana", "cherry"]
for i in range(len(my_list)):
    print(my_list[i])  # Access value using index i

#Using Enumerate 
my_list = ["apple", "banana", "cherry"]
for index, fruit in enumerate(my_list):
    print(f"Fruit at index {index}: {fruit}")

###########################################################################


## sum of the digits we have to pass the number to the sum_digit function 
def sum_digits(n):
    total = 0
    number = abs(n)  # handle negative numbers if needed
    while number > 0:
        total += number % 10
        number //= 10
    return total


######################################################################################

## Majority Element of the list 
def majority_element(nums):
    majority = None
    count = 0

    # Find a potential candidate using Boyer-Moore Voting Algorithm
    for num in nums:
        if count == 0:
            majority = num
            count = 1
        elif num == majority:
            count += 1
        else:
            count -= 1

####################################################################################
