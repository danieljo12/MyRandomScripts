import pyautogui, sys
import cv2
import pytesseract
import numpy as np
import keyboard
import pydirectinput as directinput
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
threshhold = 0.7
topCordx = 0
topCordy = 0
bottomCordx = 0
bottomCordy = 0

burgerCordx = 0
burgerCordy = 0 

colaCordx = 0
colaCordy = 0 

friesCordx = 0
friesCordy = 0 

def getMouseCordd():
    x=0
    y=0
    while True:
        if keyboard.is_pressed('u'):
            x, y = pyautogui.position()
            
        elif keyboard.is_pressed('j'):
            print(x, " : " ,y , "\n")
            return x,y
            break

def getCoords():
    global topCordx
    global topCordy
    global bottomCordx
    global bottomCordy
    global burgerCordx
    global burgerCordy
    global colaCordx 
    global colaCordy 
    global friesCordx 
    global friesCordy 
    
    try:
        print("Press u on the top left of text box and press j to complete")
        topCordx,topCordy = getMouseCordd()
        
        time.sleep(1)
        
        print("Press u on the bottom right of text box and press j to complete")
        bottomCordx,bottomCordy = getMouseCordd()
        
        time.sleep(1)
        
        print("Press u on the burger and press j to complete")
        burgerCordx,burgerCordy = getMouseCordd()
        
        time.sleep(1)
        
        print("Press u on the cola and press j to complete")
        colaCordx,colaCordy = getMouseCordd()
        time.sleep(1)
        print("Press u on the fries and press j to complete")
        friesCordx,friesCordy = getMouseCordd()
        
    except:
        print("Error... u probably typed something that aint a number... bad boi\n")
        raise 


def clickBButton(textBox):
    
    if textBox.find("Fries")!= -1:
        print("click fries")
        directinput.click(friesCordx, friesCordy) 
        return True
    elif textBox.find("Burger")!= -1:
        print("click burger")
        directinput.click(burgerCordx, burgerCordy)
        return True
    elif textBox.find("Cola") != -1:
        print("click cola")
        directinput.click(colaCordx, colaCordy)
        return True
    else:
        return False

def findFriesInImage(colorScreenShotImage,grayScreenShotImage, templateFriesLocation):
    try:
        template = cv2.imread(templateFriesLocation,0)
        w,h = template.shape[::-1]
        
        res = cv2.matchTemplate(grayScreenShotImage, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshhold)
        
        if res.max() >= threshhold: # Found it
            for pt in zip(*loc[::-1]):
                cv2.rectangle(colorScreenShotImage,pt,(pt[0]+w, pt[1]+h), (0,255,255),2)
                cv2.imwrite('output.png',colorScreenShotImage)
            return 'Fries'
        return 'NULL'
    except:
        print("invalid file location")
        return 'NULL'

def findColaInImage(colorScreenShotImage,grayScreenShotImage, templateColaLocation):
    try:
        template = cv2.imread(templateColaLocation,0)
        
        w,h = template.shape[::-1]
        
        res = cv2.matchTemplate(grayScreenShotImage, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshhold)
        
        if res.max() >= threshhold: # Found it
            for pt in zip(*loc[::-1]):
                cv2.rectangle(colorScreenShotImage,pt,(pt[0]+w, pt[1]+h), (0,255,255),2)
                cv2.imwrite('output.png',colorScreenShotImage)
            return 'Cola'
        return 'NULL'
    except:
        print("invalid file location")
        return 'NULL'

def findBurgerInImage(colorScreenShotImage,grayScreenShotImage, templateBurgerLocation):
    try:
        template = cv2.imread(templateBurgerLocation,0)
        
        w,h = template.shape[::-1]
        
        res = cv2.matchTemplate(grayScreenShotImage, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshhold)
        
        if res.max() >= threshhold: # Found it
            for pt in zip(*loc[::-1]):
                cv2.rectangle(colorScreenShotImage,pt,(pt[0]+w, pt[1]+h), (0,255,255),2)
                cv2.imwrite('output.png',colorScreenShotImage)
            
            return 'Burger'
        return 'NULL'
    except:
        print("invalid file location")
        return 'NULL'

def findOrderTextInScreenShot(grayScreenShotImage):
    
    text = pytesseract.image_to_string(grayScreenShotImage)
    
    if(text.find("Burger") != -1 or text.find("Fries") != -1 or text.find("Cola") != -1):
        return text
    else:
        return 'NULL'

def findValidOrder(colorScreenShotImage,grayScreenShotImage, templateColaLocation, templateFriesLocation, templateBurgerLocation):
    
    # Checks if it can find the order via extracting text first before trying a other method
    text = findOrderTextInScreenShot(grayScreenShotImage)
    
    if(text != 'NULL'):
        return text
    
    
    if(findFriesInImage(colorScreenShotImage,grayScreenShotImage,templateFriesLocation) != 'NULL'):
        return 'Fries'
    elif(findColaInImage(colorScreenShotImage,grayScreenShotImage,templateColaLocation) != 'NULL'):
        return 'Cola'
    elif(findBurgerInImage(colorScreenShotImage,grayScreenShotImage,templateBurgerLocation) != 'NULL'):
        return 'Burger'
    else:
        return 'NULL'

if __name__ == "__main__":
    getCoords()
    
    num =1
    
    print(topCordx, topCordy)
    
    while True:
        im = pyautogui.screenshot(region=(topCordx,topCordy, bottomCordx - topCordx, bottomCordy - topCordy))
        im.save("pic.png")
        
        img_color = cv2.imread('pic.png')
        img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
        
        text = findValidOrder(img_color,img_gray, 'cola_template.PNG', 'fries_template.PNG', 'burger_template.PNG')
        
        print(text)
        if text == 'NULL':
            num +=1
        
        if num == 25:
            clickBButton("Cola")
            num = 1
        else:
            clickBButton(text)
        
        
        time.sleep(.4)