from picamera import PiCamera

camera = PiCamera()

defaultImageName = "image.png"

def takePic(imageName=defaultImageName):
    location = "/home/pi/Desktop/ROBOT/" + imageName
    camera.capture(location)
    print("Image captured.")
    return imageName
