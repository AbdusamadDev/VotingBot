class Solution(object):
    def rotate(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: None Do not return anything, modify matrix in-place instead.
        """
        new_matrix = [[] for _ in range(len(matrix))]
        # for index, ls in enumerate(matrix):
        index = 0
        while True:
            try:
                new_matrix[index].append(matrix[index][index])
                print(new_matrix)
            except IndexError:
                return new_matrix
            except:
                return new_matrix

print(Solution().rotate([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
