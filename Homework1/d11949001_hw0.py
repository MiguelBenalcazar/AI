"""
Author: Miguel Benalcazar  <migangben@gmail.com>
Date: 2023=02-24
Purpose: Homework No 1 for AI NTU class.
"""
import sys

class Solution:
    def __init__(self):
        self.N = 0
        self.M = 0
        self.graph = {}
        self.out = []
        self.flag = True


    def validateInput(self):
        """
        This function reads inputs separated by space
        Input Validation
            Verify if the input has 2 digits separated by q space
        return the input entered as follows x
        x[0], x[1]
        """
        try:
            x = input()
            x = x.split(' ')
            if len(x) != 2:
                raise ValueError("ERROR ENTERING THE INFORMATION, PLEASE TRY AGAIN! ")
                # x = self.validateInput()
            for i in x:
                if i == '':
                    raise ValueError("ERROR ENTERING THE INFORMATION, PLEASE TRY AGAIN! ")
                    # x = self.validateInput()
                elif not i.isdigit():
                    raise ValueError("ERROR ENTERING THE INFORMATION, PLEASE TRY AGAIN! ")
                    # x = self.validateInput()
            if type(x) is None:
                raise ValueError("ERROR ENTERING THE INFORMATION, PLEASE TRY AGAIN! ")
            else:
                return x
        except ValueError as e:
            print(e)
            sys.exit(1)
        except EOFError:
            print("ERROR ENTERING THE INFORMATION, PLEASE TRY AGAIN! ")
            sys.exit(1)

    def validateNM(self):
        """
        This function calculate conditions for N and M
        for N : 1 <= N <= 30
        for M : 0 <= M <= N(N-1)/2

        Returns:
            n: Number of Islands
            m: Number of the bridges
            n_aux: N(N-1)/2
            n_condition: Bool => 1 <= N <= 30
            m_condition: Bool =? 0 <= M <= n_aux
        """

        nm = self.validateInput()
        n, m = nm[0], nm[1]
        n_aux = int(n) * (int(n) - 1) / 2
        n_condition = int(n) < 1 or int(n) > 30
        m_condition = int(m) < 0 or int(m) > n_aux
        return n, m, n_aux, n_condition,m_condition

    def enterNM(self):
        """
        Main function to enter data N and M
        """
        try:
            n, m, n_aux, n_condition, m_condition = self.validateNM()
            if n_condition or m_condition:
                if n_condition and not m_condition:
                    raise ValueError("N IS A NUMBER BETWEEN 1 AND 30")
                elif not n_condition and m_condition:
                    raise ValueError(f"M IS A NUMBER BETWEEN 0 AND {int(n_aux)}")
                else:
                    raise ValueError("N AND M ARE OUT OF RANGE")
                self.enterNM()

            self.N = int(n)
            self.M = int(m)
        except ValueError as e:
            print(e)
            sys.exit(1)

    def uv_validateInput(self):
        """
        Function to validate info u, v
        1 <= u,v <= N
        u != v
        """
        uv = self.validateInput()
        u, v = uv[0], uv[1]
        u_condition = int(u) < 1 or int(u) > self.N
        v_condition = int(v) < 1 or int(v) > self.N
        uv = int(u) == int(v)
        return u, v, u_condition or v_condition, uv

    def enterUV(self):
        """
        Main function to enter data u,v
        Returns:
        :return u: Island
        :return v: island
        :return u,v bridge connection
        """
        try:
            u, v, uv_condition, uv_similar = self.uv_validateInput()
            if uv_condition or uv_similar:
                if uv_condition and not uv_similar:
                    raise ValueError(f"uv MUST BE A NUMBER LESS OR EQUAL THAN {self.N}")
                elif not uv_condition and uv_similar:
                    raise ValueError("u MUST BE DIFFERENT FROM v")
                u, v = self.enterUV()
            return u, v
        except ValueError as e:
            print(e)
            sys.exit(1)

    def verifyDataInArray(self, u, v):
        """
        Function to verify if u or v are included in graph
        :param u: island start
        :param v: island end
        :return: flag False if not
        """
        flag = False
        for i in self.graph[u]:
            if i == v:
                flag = True
        for i in self.graph[v]:
            if i == u:
                flag = True
        return flag

    def enterMainUV(self):
        """
        Main function to control the u,v data
        """
        try:
            for i in range(self.N):
                self.graph[f'{i+1}'] = []

            for i in range(self.M):
                u, v = self.enterUV()

                while self.verifyDataInArray(u,v):
                    raise ValueError("THE BRIDGE CANNOT BE DUPLICATED")
                    u, v = self.enterUV()
                self.graph[u].append(v)
                self.graph[v].append(u)
        except ValueError as e:
            print(e)
            sys.exit(1)

    def sortGraphArray(self):
        """
        Function to sort graph Array
        """
        for i in self.graph.keys():
            aux = [int(j) for j in self.graph.get(i)]
            aux.sort()
            original = [f'{j}' for j in aux]
            self.graph[i] = []
            self.graph[i] = original


    def deepFirstSearch(self, visited, island):
        """
        Function to control deep first search
        :param visited: Array to control if Island was already visited
        :param island: Starting Island or Island number
        """
        if island not in visited:
            visited.append(island)
            count = 0
            for neighbour in self.graph[island]:
                # print(f'island {island} inside {neighbour}  array {self.graph[island]} count {count}')
                if island not in self.out and self.flag:
                    self.out.append(island)
                self.deepFirstSearch(visited, neighbour)
                count += 1
                if count == len(self.graph[island]):
                    self.flag = False

    def printResult(self):
        """
        Function to show results
        """
        text = ''
        count = 0
        for i in self.out:
            if count == 0:
                text = f'{i}'
                count += 1
            elif count == len(self.out)-1:
                text = f'{text} {i}'
            else:
                text = f'{text} {i}'
                count += 1

        # print(f'Islands and bridges: \n {self.graph} ')
        # print(f'Order to visit: \n {text}')
        print(text)

    def solve(self):
        """
        Main Function to control Capibara
        """
        self.enterNM()
        self.enterMainUV()
        visited = []
        self.sortGraphArray()
        self.deepFirstSearch(visited, "1")
        self.printResult()


if __name__ == '__main__':
    ans = Solution()
    ans.solve()