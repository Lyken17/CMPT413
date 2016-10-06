from collections import defaultdict
import types
NumberTypes = (types.IntType,
               types.LongType,
               types.FloatType,
               types.ComplexType)



class FeatureVector(defaultdict):
    def __init__(self):
        super(FeatureVector, self).__init__(float)
        return

    def export(self):
        # Convert to defaultdict, for dumping
        result = defaultdict(float)
        for key in self:
            result[key] = self[key]
        return result

    def dump(self, filename):
        # export to designated file
        result = self.export()
        import pickle
        output = open(filename, 'wb')
        pickle.dump(result, output)
        output.close()
        return

    def __add__(self, otherFeatureVector):
        result = FeatureVector()
        for key in self:
            result[key] += self[key]
        for key in otherFeatureVector:
            result[key] += otherFeatureVector[key]
        return result

    def __iadd__(self, otherFeatureVector):
        for key in otherFeatureVector:
            self[key] += otherFeatureVector[key]
        return self

    def __sub__(self, otherFeatureVector):
        result = FeatureVector()
        for key in self:
            result[key] += self[key]
        for key in otherFeatureVector:
            result[key] -= otherFeatureVector[key]
        return result

    def __isub__(self, otherFeatureVector):
        for key in otherFeatureVector:
            self[key] -= otherFeatureVector[key]
        return self

    def __mul__(self, number):
        if not isinstance(number, NumberTypes):
            raise ValueError("Multiplication requires number!")
        result = FeatureVector()
        for key in self:
            result[key] = self[key] * float(number)
        return self

    def __div__(self, number):
        if not isinstance(number, NumberTypes):
            raise ValueError("Division requires number!")
        result = FeatureVector()
        for key in self:
            result[key] = self[key] / float(number)
        return self

    def __eq__(self, otherFeatureVector):
        if len(self) != len(otherFeatureVector):
            return False
        for key in otherFeatureVector:
            if self[key] != otherFeatureVector[key]:
                return False
        return True
