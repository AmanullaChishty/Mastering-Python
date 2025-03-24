# Problem 1: Sum of Array Elements
def sum_array(arr):
    total = 0
    for num in arr:
        total += num
    return total

arr = list(range(1,6))
print("Problem-1 Sum: ", sum_array(arr))

#Problem 2: Reverse an Array
def reverse_array(arr):
    for i in range(len(arr)):
        arr.insert(i,arr.pop())
    return arr

arr1 = list(range(1,6))
arr2 = ['a','b','c','d']
print("Problem-2: ",reverse_array(arr2))

#Problem 2: Reverse an Array approcah-2
def reverse_array2(arr):
    l,r = 0,len(arr)-1
    while l<r:
        arr[l],arr[r]=arr[r],arr[l]
        l+=1
        r-=1
    return arr

arr3 = list(range(1,7))
print("Problem approach-2: ",reverse_array2(arr3))

#Problem 3: Find Maximum and Minimum in an Array
def find_max_min(arr):
    if not arr:
        return None,None
    mn=mx = arr[0]

    for num in arr:
        if num>mx:
            mx=num
        if num < mn:
            mn =num
    return mx,mn

arr5 = [3, 1, 4, 1, 5, 9, 2]
maximum, minimum = find_max_min(arr5)
print("Prob-3 Maximum:", maximum, "Minimum:", minimum)

# Problem 4: Binary Search in a Sorted Array
def binary_search(arr,target):
    l,r=0,len(arr)-1

    while l<=r:
        mid = (l+r)//2
        if arr[mid]==target:
            return mid
        elif arr[mid]<target:
            l = mid+1
        else:
            r = mid-1
    return -1 

sorted_arr = [1, 3, 5, 7, 9, 11]
target = 7
print("Prob-4 Index of", target, ":", binary_search(sorted_arr, target))

#Problem 5: Rotate Array
#Rotate an array to the right by k steps. For example, rotating [1, 2, 3, 4, 5] by 2 steps yields [4, 5, 1, 2, 3].

