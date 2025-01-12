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
