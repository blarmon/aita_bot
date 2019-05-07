def find132pattern(nums):
    potential = []

    for i in range(len(nums)):
        potential = []

        for i in range(len(nums)):
            potential.append([nums[i]])
            for j in range(len(potential)):

                if len(potential[j]) == 2 and nums[i] < potential[j][1] and nums[i] > potential[j][0]:
                    return True

                if len(potential[j]) == 1 and nums[i] > potential[j][0]:
                    potential[j].append(nums[i])
                    
            print(potential)

        return False

print(find132pattern([-2,1,2,-2,1,2]))