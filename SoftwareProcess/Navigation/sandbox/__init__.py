import Navigation.prod.Angle as Angle

angle1 = Angle.Angle()
angle2 = Angle.Angle()

angle1.setDegreesAndMinutes("24d30")
angle2.setDegreesAndMinutes("24d31")
print(angle2.getDegrees())