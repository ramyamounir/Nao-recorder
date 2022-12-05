
import sys
import motion
import time
import almath
from naoqi import ALProxy

from rocordedPositions import movements
from rocordedPositions import arms

wholeSequence = ['openHand-L',
                 'openHand-R',
                 'movement-initRight',
                 'movement-initLeft',
                 'delay-200',
                 'movementi-grabLeft',
                 'delay-200',
                 'closeHand-L',
                 'speak-Lets add the milk',
                 'delay-200',
                 'movement-pourLeft',
                 'delay-500',
                 'movementi-pourLeft',
                 'speak-Gimme some sugar',
                 'delay-3000',
                 'movement-pourLeft',
                 'delay-500',
                 'movementi-pourLeft',
                 'speak-What about some baking powder, you einstein',
                 'delay-3000',
                 'movement-pourLeft',
                 'delay-500',
                 'movementi-pourLeft',
                 'speak-Do you want some flour on it?',
                 'delay-3000',
                 'movement-pourLeft',
                 'delay-500',
                 'movementi-pourLeft',
                 #copy 4 times the movement
                 'delay-200',
                 'movement-throwLeft',
                 'delay-200',
                 'speak-Sorry about the mess, but I dont need that',
                 'openHand-L',
                 'delay-200',
                 'movement-grabPlate',
                 'closeHand-L',
                 'movement-grabSpoon',
                 'delay-200',
                 'closeHand-R',
                 'delay-200',
                 'movement-moveSpoon',
                 'delay-200',
                 'movement-stir',
                 'movement-stir',
                 'movement-stir',
                 'movement-stir',
                 'movement-stir',
                 'delay-200',
                 'movementi-moveSpoon',
                 'movement-pourPlate',
                 'delay-200',
                 'movementi-pourPlate',
                 'openHand-R',
                 'openHand-L',
                 'movementi-grabSpoon',
                 'movementi-grabPlate',
                 'movementi-initRight',
                 'movement-finishLeft',
                 'speak-Bon Apetee'
                 ]

if not 'movements' in locals():
  movements = {}
  arms={}

  
currentMovement = [] 
movements['current'] = currentMovement 

currentArm = "R"
arms['current'] = currentArm

doubleL = []
doubleR = []
double = {}
double['current']=[doubleL,doubleR]

command = ""

def executeDouble(params):
  dmoves = double[params[0]]
  mLeft = dmoves[0]
  mRight = dmoves[1]
  
  motionProxy.setStiffnesses("RArm", 1.0)
  motionProxy.setStiffnesses("LArm", 1.0)
  stiffnessOn = True
  axisMask = 63 #both angles and positions
  times = [0.5*i+0.5 for i in range(len(mLeft))]
  motionProxy.post.positionInterpolation("LArm", space, mLeft,axisMask,times ,True)
  motionProxy.post.positionInterpolation("RArm", space, mRight,axisMask,times ,True)

def executeMovement(params):
  movement = movements[params[0]]
  arm = arms[params[0]]
  
  global motionProxy
  motionProxy.setStiffnesses(arm + "Arm", 1.0)
  stiffnessOn = True
  
  axisMask = 63 #both angles and positions
  motionProxy.positionInterpolation(arm+"Arm", space, movement,axisMask, [0.5*i+0.5 for i in range(len(movement))],True)

def executeInvertedMovement(params):
  movement = movements[params[0]]
  inverted = []
  for m in movement:
    inverted = [m]+inverted
  arm = arms[params[0]]
  
  global motionProxy
  motionProxy.setStiffnesses(arm + "Arm", 1.0)
  stiffnessOn = True
  
  axisMask = 63 #both angles and positions
  motionProxy.positionInterpolation(arm+"Arm", space, inverted,axisMask, [0.5*i+0.5 for i in range(len(inverted))],True)
  
handStiffness = 1.0

def closeHandInterpolated(params):
  global motionProxy
  motionProxy.angleInterpolation(params[0]+"Hand",[0,50*almath.TO_RAD],[2,3],True)
  print 'done closing'
  

def openHand (params):
  global motionProxy
  motionProxy.openHand(params[0]+"Hand")
  motionProxy.setStiffnesses(params[0]+"Hand",handStiffness)
  
  
def closeHand (params): #params = arm
  global motionProxy
  motionProxy.closeHand(params[0] + "Hand")
  motionProxy.setStiffnesses(params[0] + "Hand",handStiffness)
  
  
def delayFunctions(params): #params = delay
    time.sleep(int(params[0])/1000.0)     
  
def parse(command):
    tokens = command.split("-")
    return tokens[0],tokens[1:]

 
  
def executeSequence(sequence):
  for s in sequence:
    comm,params = parse(s)
    functions[comm](params)
      
      
def speak(params):
  ttsProxy.say(params[0])
    
      
functions = {}
functions['openHand']  = openHand
functions['closeHand'] = closeHand
functions['movement']  = executeMovement
functions['movementi'] = executeInvertedMovement
functions['delay']     = delayFunctions
functions['speak']     = speak
  
def saveRecord(f,name,positions):
    global movements
    f.write('movements[\'')
    f.write(name)
    f.write('\'] = [')
    skipOutter = True  
    for pos in positions:
      if skipOutter:
        skipOutter = False
      else:
        f.write(',')
      f.write('[')
      skip = True
      for p in pos:
        if not skip:
          f.write(',')
        else:
          skip = False
        f.write(str(p))
      f.write(']')
    f.write(']\n')
    
               
stiffnessOn = True             
if __name__ == "__main__":
  #config, connect to robot and get proxies
  robotIP      = "169.254.252.60"
  motionProxy = ALProxy("ALMotion", robotIP, 9559)
  postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
  ttsProxy = ALProxy("ALTextToSpeech",robotIP,9559)
  space = motion.FRAME_ROBOT
  
  #go to posture
  motionProxy.stiffnessInterpolation("Body", 1.0, 1.0)
  motionProxy.setIdlePostureEnabled("Body",False)
  #motionProxy.setIdlePostureEnabled("Body",False)
  #postureProxy.goToPosture("Crouch", 0.5)
  
  #read input and do task   
  while(True):
    var = raw_input()
    if(var=='h'):
      #display all commands
      print 'e', 'exit'
      print '\\n', 'record new position'
      print 'saver', 'save record'
      print 'play', 'play current record'
      print 'playr', 'play saved record'
      print 'plays', 'play sequence'
      
      print 'erase','erase current record'
      print 'open/close', 'open /  close hand'
      print 'stiff', 'toggle arm stiffness'
      print 'arm' , 'switches arm being recorded'
    elif(var=='e' or var == 'exit'):
      break
    elif(var == 'play' or var == 'playr'):
    
      recordName = 'current'
      if(var=='playr'):
        recordName = raw_input('record name: ')
      
      movement = []
      arm = currentArm
      if(recordName in movements):
        movement = movements[recordName]
        arm = arms[recordName]
      else:
        print 'No movement named', recordName
        continue
      
    
      if(len(movement)==0):
        print 'len(movement)=0'
        continue
        
      executeMovement([recordName])
    elif (var =='playd' or var=='playdr'):
      recordName = 'current'
      if(var=='playdr'):
        recordName = raw_input('record name: ')
      
      if(not recordName in double):
        print 'No movement named', recordName
        continue
      
    
      if(len(double[recordName][0])==0):
        print 'len(movement)=0'
        continue
        
      executeDouble([recordName])
      
    elif(var == 'playi' or var == 'playir'):
    
      recordName = 'current'
      if(var=='playir'):
        recordName = raw_input('record name: ')
      
      movement = []
      arm = currentArm
      if(recordName in movements):
        movement = movements[recordName]
        arm = arms[recordName]
      else:
        print 'No movement named', recordName
        continue
      
    
      if(len(movement)==0):
        print 'len(movement)=0'
        continue
        
      executeInvertedMovement([recordName])
      
      
    elif(var=="erase"):
      currentMovement=[]
      movements['current']=currentMovement
      print 'erased'
    elif (var == 'arm'):
      if(len(currentMovement)>0):
        ans = raw_input('movement will be lost, proceed(y/n)? ')
        if(ans<>'y'):
          continue
          
      if(currentArm=='R'):
        currentArm='L'
      else:
        currentArm='R'
        
      currentMovement=[]
      movements['current']=currentMovement
      arms['current'] = currentArm
      print 'erased, arm=',currentArm  
        
    elif (var=='saver'):
      name = raw_input('movement name: ')
      movements[name]=currentMovement
      arms[name]=currentArm 
      currentMovement=[]
      movements['current']=currentMovement
      print 'saved record'
    elif (var=='savedr'):
      name = raw_input('movement name: ')
      double[name]=[doubleL,doubleR]
      doubleL=[]
      doubelR=[]
      double['current']=[doubleL,doubleR]
      print 'saved double record'
    elif (var=="open"):
      motionProxy.openHand(currentArm + "Hand")
      motionProxy.setStiffnesses(currentArm + "Hand",1.0)
    elif (var =="close"):
      motionProxy.closeHand(currentArm + "Hand")
      motionProxy.setStiffnesses(currentArm + "Hand",1.0)
    elif (var =="new"):
      name = raw_input()
    elif (var=="stiff"):
      stiffnessOn = not stiffnessOn
      print "Stiffness",stiffnessOn
      if(stiffnessOn):
        motionProxy.setStiffnesses(currentArm+"Arm", 1.0)
      else:
        motionProxy.setStiffnesses(currentArm+"Arm", 0.0)
      
    
    elif(var==''):
      pos = motionProxy.getPosition(currentArm+"Arm",space,False)
      currentMovement += [pos]
      print "position recored:"
      print '\t',pos
      print  
    elif(var=='d'):
      posL = motionProxy.getPosition("LArm",space,False)
      posR = motionProxy.getPosition("RArm",space,False)
      doubleL += [posL]
      doubleR += [posR]
      print "position recored:"
      print '\t',posL
      print '\t',posR
      print  
    elif(var=='plays'):
      seq = []
      while(True):
        s = raw_input('action:')
        if(s==''):
          break
        seq+=[s]
      print 'playing sequence: ',seq
      executeSequence(seq)
    elif(var=='closei'):
      closeHandInterpolated(currentArm)
    elif(var=='playa'):
      executeSequence(wholeSequence)
      print 'done with sequence'
    elif(var=='playsub'):
      startPos = int(raw_input('start:'))
      endPos = int(raw_input('end:'))
      executeSequence(wholeSequence[startPos:(endPos-1)])
      print 'done with sequence'
  
  f = open('rocordedPositions.py','w')
  
  
  f.write('movements={}\n\n')
  
  for k,v in movements.items():
    saveRecord(f,k,v)
    f.write('\n')
  
  f.write('\n')
  f.write('\n')
  f.write('arms={}\n\n')
  for k,v in arms.items():
    f.write('arms[\'')
    f.write(k)
    f.write('\']= \'')
    f.write(v)
    f.write('\'\n')
  
  f.close()
  
  
  #
  
  
  
    
  