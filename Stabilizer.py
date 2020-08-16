import numpy as np

class Stabilizer:

    def __init__(self, currentAngle, sampleSize, velocity, maxVelocity, maxDifference):
        self.measurements = np.array([])
        self.currentAngle = currentAngle
        self.sampleSize = sampleSize
        self.velocity = velocity
        self.maxVelocity = maxVelocity
        self.maxDifference = maxDifference

    def measure(self, angle):
        self.measurements = np.append(self.measurements, angle)

        # Deletes oldest sample if too many samples
        if (len(self.measurements) > self.sampleSize):
            self.measurements = self.measurements[1:self.sampleSize]
        
        avg = np.average(self.measurements)

        difference = avg - self.currentAngle

        change = difference * self.velocity
        if abs(change) > self.maxVelocity or abs(difference) > self.maxDifference:
            change = self.maxVelocity * change / abs(change)
        
        self.currentAngle = self.currentAngle + change
        return(self.currentAngle)
