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
