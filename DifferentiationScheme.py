import numpy as np


class DifferentiationScheme:
    def __init__(self, params):
        self.l = params["l"]
        self.s = params["s"]
        self.const_alpha = params["alpha"]
        self.const_k = params["k"]
        self.c = params["c"]
        self.T = params["T"]
        self.x = params["x"]
        self.t = params["t"]
        self.I = int(params["I"])
        self.K = int(params["K"])
        self.const_u0 = params["U_0"]
        self.hx = self.l / self.I
        self.ht = self.T / self.K
        self.xi = 4 * self.const_alpha / np.sqrt(self.s)

    @staticmethod
    def phi(x, l):
        return np.sin(np.pi * x / l) ** 4

    def setNewParams(self, params):
        self.l = params["l"]
        self.s = params["s"]
        self.const_alpha = params["alpha"]
        self.const_k = params["k"]
        self.c = params["c"]
        self.T = params["T"]
        self.x = params["x"]
        self.t = params["t"]
        self.I = int(params["I"])
        self.K = int(params["K"])
        self.const_u0 = params["U_0"]
        self.hx = self.l / self.I
        self.ht = self.T / self.K
        self.xi = 4 * self.const_alpha / np.sqrt(self.s)

    def SimpleApparentX(self):
        iteration = int(self.t / self.ht)
        x = np.linspace(0, self.l, self.I + 1)
        A_low = np.zeros(self.I + 1)
        gamma = 4 * self.const_alpha / np.sqrt(self.s)
        for i in range(0, self.I + 1):
            A_low[i] = self.const_u0
        for k in range(1, iteration):
            A_top = np.zeros(self.I + 1)
            for i in range(1, self.I):
                temp = self.const_k * (A_low[i + 1] - 2 * A_low[i] + A_low[i - 1]) / self.hx ** 2 - gamma * (
                            A_low[i] - self.const_u0) + self.phi(
                    i * self.hx, self.l)
                A_top[i] = self.ht * temp / self.c + A_low[i]
            A_top[0] = A_top[1] / ((self.const_alpha * self.hx / self.const_k) + 1)
            A_top[self.I] = A_top[self.I - 1] / ((self.const_alpha * self.hx / self.const_k) + 1)
            A_low = A_top

        label = f'Простейшая явная схема (T={self.T}, t={self.t}'
        return x, A_low, label

    def ModifiedApparentX(self):
        maxNode = int(self.t / self.ht)
        x = np.linspace(0, 1, self.I + 1)
        lowerLayer = np.zeros(self.I + 1)
        for i in range(lowerLayer.shape[0]):
            lowerLayer[i] = self.const_u0

        for k in range(1, maxNode):
            upperLayer = np.zeros(self.I + 1)
            for i in range(1, self.I):
                node = self.const_k * (lowerLayer[i + 1] - 2 * lowerLayer[i] + lowerLayer[i - 1]) / self.hx ** 2 - \
                       self.xi * lowerLayer[i] + self.phi(i * self.hx, self.l)
                upperLayer[i] = self.ht * node / self.c + lowerLayer[i]

            node0 = 2 * self.const_k * (lowerLayer[1] - lowerLayer[0] - self.const_alpha
                                        * self.hx * (lowerLayer[0] - self.const_u0) / self.const_k) / self.hx ** 2 - self.xi * lowerLayer[0] + self.const_u0 + self.phi(0, self.l)
            upperLayer[0] = self.ht * node0 / self.c + lowerLayer[0]
            nodeI = 2 * self.const_k * (lowerLayer[self.I - 1] - lowerLayer[self.I] - self.const_alpha
                                        * self.hx * (lowerLayer[self.I] - self.const_u0) / self.const_k) / self.hx ** 2 - self.xi * \
                    lowerLayer[self.I] + self.const_u0 + self.phi(self.I * self.hx, self.l)
            upperLayer[self.I] = self.ht * nodeI / self.c + lowerLayer[self.I]
            lowerLayer = upperLayer

        label = f'Модифицированная явная схема (T={self.T}, t={self.t})'
        return x, lowerLayer, label

    def SimpleImplicitX(self):
        pass

    def ModifiedImplicitX(self):
        pass

    def SimpleApparentT(self):
        gamma = 4 * self.const_alpha / np.sqrt(self.s)
        iteration = int(self.x / self.hx)
        t = np.linspace(0, self.T, self.K + 1)
        A_low = np.zeros(self.I + 1)
        for i in range(0, self.I + 1):
            A_low[i] = self.const_u0
        U = [A_low[iteration]]
        for k in range(1, self.K + 1):
            A_top = np.zeros(self.I + 1)
            for i in range(1, self.I):
                temp = self.const_k * (A_low[i + 1] - 2 * A_low[i] + A_low[i - 1]) / self.hx ** 2 - gamma * (A_low[i] - self.const_u0) + self.phi(
                    i * self.hx, self.l)
                A_top[i] = self.ht * temp / self.c + A_low[i]

            A_top[0] = A_top[1] / ((self.const_alpha * self.hx / self.const_k) + 1)
            A_top[self.I] = A_top[self.I - 1] / ((self.const_alpha * self.hx / self.const_k) + 1)
            A_low = A_top

            U.append(A_low[iteration])

        label = f'Простейшая явная схема (x={self.x})'
        return t, U, label

    def ModifiedApparentT(self):
        maxNode = int(self.x / self.hx)
        t = np.linspace(0, self.T, self.K + 1)
        lowerLayer = np.zeros(self.I + 1)

        for i in range(lowerLayer.shape[0]):
            lowerLayer[i] = self.const_u0

        U = [lowerLayer[maxNode]]

        for k in range(1, self.K + 1):
            upperLayer = np.zeros(self.I + 1)
            for i in range(1, self.I):
                node = self.const_k * (lowerLayer[i + 1] - 2 * lowerLayer[i] + lowerLayer[i - 1]) / self.hx ** 2 - \
                       self.xi * lowerLayer[i] + self.phi(i * self.hx, self.l)
                upperLayer[i] = self.ht * node / self.c + lowerLayer[i]

            node0 = 2 * self.const_k * (lowerLayer[1] - lowerLayer[0] - self.const_alpha
                                        * self.hx * (lowerLayer[
                                                         0] - self.const_u0) / self.const_k) / self.hx ** 2 - self.xi * \
                    lowerLayer[0] + self.const_u0 + self.phi(0, self.l)
            upperLayer[0] = self.ht * node0 / self.c + lowerLayer[0]
            nodeI = 2 * self.const_k * (lowerLayer[self.I - 1] - lowerLayer[self.I] - self.const_alpha
                                        * self.hx * (lowerLayer[
                                                         self.I] - self.const_u0) / self.const_k) / self.hx ** 2 - self.xi * \
                    lowerLayer[self.I] + self.const_u0 + self.phi(self.I * self.hx, self.l)
            upperLayer[self.I] = self.ht * nodeI / self.c + lowerLayer[self.I]
            lowerLayer = upperLayer

            U.append(lowerLayer[maxNode])

        label = f'Модифицированная явная схема (x={self.x})'

        return t, U, label

    def SimpleImplicitT(self):
        pass

    def ModifiedImplicitT(self):
        pass
