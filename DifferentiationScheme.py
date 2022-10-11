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
        pass

    def ModifiedApparentX(self):
        maxNode = int(self.t / self.ht)
        x = np.linspace(0, 1, self.I + 1)
        lowerLayer = np.zeros(self.I + 1)
        for i in range(lowerLayer.shape[0]):
            lowerLayer[i] = self.const_u0

        for k in range(1, maxNode):
            upperLayer = np.zeros(self.I + 1)
            for i in range(1, self.I - 1):
                upperLayer[i] = self.calculateNode(i, lowerLayer[i], lowerLayer[i - 1], lowerLayer[i + 1])

            upperLayer[0] = (self.const_alpha / k) * (lowerLayer[0] - self.const_u0) * self.hx + lowerLayer[-1]
            upperLayer[self.I] = -(self.const_alpha / k) * (lowerLayer[self.I] - self.const_u0) * self.hx + lowerLayer[
                self.I - 1]

            lowerLayer = upperLayer

        label = f'Модифицированная явная схема (T={self.T}, t={self.t})'
        return x, lowerLayer, label

    def SimpleImplicitX(self):
        pass

    def ModifiedImplicitX(self):
        pass

    def SimpleApparentT(self):
        pass

    def ModifiedApparentT(self):
        maxNode = int(self.x / self.hx)
        t = np.linspace(0, self.T, self.K + 1)
        lowerLayer = np.zeros(self.I + 1)

        for i in range(lowerLayer.shape[0]):
            lowerLayer[i] = self.const_u0

        U = [lowerLayer[maxNode]]

        for k in range(1, self.K + 1):
            upperLayer = np.zeros(self.I + 1)
            for i in range(1, self.I - 1):
                upperLayer[i] = self.calculateNode(i, lowerLayer[i], lowerLayer[i - 1], lowerLayer[i + 1])

            upperLayer[0] = (self.const_alpha / k) * (lowerLayer[0] - self.const_u0) * self.hx + lowerLayer[-1]
            upperLayer[self.I] = -(self.const_alpha / k) * (lowerLayer[self.I] - self.const_u0) * self.hx + lowerLayer[
                self.I - 1]

            lowerLayer = upperLayer
            U.append(lowerLayer[maxNode])

        label = f'Явная схема (x={self.x})'

        return t, U, label

    def SimpleImplicitT(self):
        pass

    def ModifiedImplicitT(self):
        pass

    def calculateNode(self, i, cur, prev, next):
        node = self.const_k * (next - 2 * cur + prev) / self.hx ** 2 - \
               self.xi * cur + self.phi(i * self.hx, self.l)
        return self.ht * node / self.c + cur