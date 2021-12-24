"""
A convinient class of objects to communicate with Machina Bridge
by Ardavan Bidgoli
Robotics Fellow at CMU
WIP
"""
import websockets
import asyncio

class MachinaRobot (object):

    def __init__(self, address = "ws://127.0.0.1:6999/Bridge", debug = True):
        # init 
        self.commands = []
        self.address = address
        self.debug = debug

        # error messages
        self.floatError = " must be a float."
        self.stringError = " must be a string."
        self.listError = " must be a list of strings."
        self.intError = " must be an integer."
        self.externalAxisError = " must be between 1 and 6."


    async def sendToBridge(self,address= "", command=""):
        # generic fucntion to communicate with web
        print (command)
        print (type(command))
        if not isinstance(command, str) :
            raise ValueError("command must be an string object.")
            
        if not isinstance(address, str) :
            raise ValueError("address must be an string object i.e.: \"ws://127.0.0.1:6999/Bridge\"")

        if address == "": 
            address = self.address

        print("sending to bridge...")

        async with websockets.connect(address) as websocket:
            # it waits until the ws sends the message
            await websocket.send(command)
            print("Message sent:{}".format(command))
            # then waits Bridge sends the feedback
            feedback = await websocket.recv()
            # then it prints the feedback
            print("Message Recieved:{}".format(feedback))


    def runCommands(self,cmds = ""):
        if cmds == "":
            cmds = self.commands

        if not isinstance(cmds, list) : 
            if isinstance(cmds, str) :
                cmds = [cmds]
            else:
                raise ValueError("command {}".format(self.listError))

        for cmd in cmds:
             
            if not isinstance(cmd, str) :
                raise ValueError("each command {}".format(self.stringError))
            #asyncio.get_event_loop().run_until_complete(self.sendToBridge(self.address,cmd))
            try:
                print("sending {} to ws".format(cmd))
                asyncio.get_event_loop().run_until_complete(self.sendToBridge(self.address,cmd))
            except:
                
                print ("FAIL: {}".format(cmd))
        return 


    ##  ███████╗███████╗████████╗████████╗██╗███╗   ██╗ ██████╗ ███████╗
    ##  ██╔════╝██╔════╝╚══██╔══╝╚══██╔══╝██║████╗  ██║██╔════╝ ██╔════╝
    ##  ███████╗█████╗     ██║      ██║   ██║██╔██╗ ██║██║  ███╗███████╗
    ##  ╚════██║██╔══╝     ██║      ██║   ██║██║╚██╗██║██║   ██║╚════██║
    ##  ███████║███████╗   ██║      ██║   ██║██║ ╚████║╚██████╔╝███████║
    ##  ╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝

    def Speed(self,speedInc):
        self.commands = "Speed({});".format(speedInc) 
        self.runCommands()
        return  

    def SpeedTo(self,speedVal):
        self.commands = "SpeedTo({});".format(speedVal) 
        self.runCommands()
        return  

    def Acceleration(self,accelerationInc):
        self.commands = "Acceleration({});".format(accelerationInc) 
        self.runCommands()
        return  

    def AccelerationTo(self,accelerationVal):
        self.commands = "AccelerationTo({});".format(accelerationVal) 
        self.runCommands()
        return    


    # def rotationSpeed(self,rotationSpeedInc):
    #     self.commands = "RotationSpeed({});".format(rotationSpeedInc) 
    #     self.runCommands()
    #     return  

    # def rotationSpeedTo(self,rotationSpeedVal):
    #     self.commands = "RotationSpeedTo({});".format(rotationSpeedVal) 
    #     self.runCommands()
    #     return  

    # def jointSpeed(self,jointSpeedInc):
    #     self.commands = "JointSpeed({});".format(jointSpeedInc) 
    #     self.runCommands()
    #     return  

    # def jointSpeedTo(self,jointSpeedVal):
    #     self.commands = "JointSpeedTo({});".format(jointSpeedVal) 
    #     self.runCommands()
    #     return  

    # def jointAcceleration(self,jointAccelerationInc):
    #     self.commands = "JointAcceleration({});".format(jointAccelerationInc) 
    #     self.runCommands()
    #     return  

    # def jointAccelerationTo(self,jointAccelerationVal):
    #     self.commands = "JointAccelerationTo({});".format(jointAccelerationVal) 
    #     self.runCommands()
    #     return  

    def Precision(self,precisionInc):
        self.commands = "Precision({});".format(PrecisionInc) 
        self.runCommands()
        return  

    def PrecisionTo(self,precisionVal):
        self.commands = "PrecisionTo({});".format(precisionVal) 
        self.runCommands()
        return  

    def MotionMode(self,mode):
        # motion type should be "linear" or "joint" as string
        if self.debug:
            if not isinstance(motionType, string):
                raise ValueError("motionType {}".format(stringError))  

        self.commands = "MotionMode(\"{}\");".format(mode) 
        self.runCommands()
        return  

    def PushSettings(self):
        self.commands = "PushSettings();" 
        self.runCommands()
        return  

    def PopSettings(self):
        self.commands = "PopSettings();" 
        self.runCommands()
        return 

    ##   █████╗  ██████╗████████╗██╗ ██████╗ ███╗   ██╗███████╗
    ##  ██╔══██╗██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
    ##  ███████║██║        ██║   ██║██║   ██║██╔██╗ ██║███████╗
    ##  ██╔══██║██║        ██║   ██║██║   ██║██║╚██╗██║╚════██║
    ##  ██║  ██║╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║███████║
    ##  ╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
        
    def Move(self, xInc, yInc, zInc = 0):
        if self.debug:
            if not isinstance(xInc, float):
                raise ValueError("xInc {}".format(floatError))
            if not isinstance(yInc, float):
                raise ValueError("yInc {}".format(floatError))
            if not isinstance(zInc, float):
                raise ValueError("zInc {}".format(floatError))

        self.commands = "Move({},{},{});".format(xInc, yInc, zInc) 
        self.runCommands()
        return
        
    def MoveTo (self,x,y,z):
        if self.debug:
            if not isinstance(x, float):
                raise ValueError("x {}".format(floatError))
            if not isinstance(y, float):
                raise ValueError("y {}".format(floatError))
            if not isinstance(z, float):
                raise ValueError("z {}".format(floatError))
        self.commands = "MoveTo({},{},{});".format(x, y, z) 
        self.runCommands()
        return


    def ExternalAxis(self,axisNumber,increment):
        if self.debug:
            if not isinstance(axisNumber, int):
                raise ValueError("axisNumber {}".format(intError))

            if 1> axisNumber or axisNumber >6 :
                raise ValueError("axisNumber {}".format(externalAxisError))

            if not isinstance(increment, float):
                raise ValueError("increment {}".format(floatError))

        self.commands = "ExternalAxis({},{});".format(axisNumber, increment) 
        self.runCommands()
        return

    def ExternalAxisTo(self,axisNumber, val):
        if self.debug:
            if not isinstance(axisNumber, int):
                raise ValueError("axisNumber {}".format(intError))

            if 1> axisNumber or axisNumber >6 :
                raise ValueError("axisNumber {}".format(externalAxisError))

            if not isinstance(val, float):
                raise ValueError("val {}".format(floatError))

        self.commands = "ExternalAxisTo({},{});".format(axisNumber, val) 
        self.runCommands()
        return

    def TransformTo(self,x,y,z,x0,x1,x2,y0,y1,y2):
        self.commands = "TransformTo({},{},{},{},{},{},{},{},{});".format(x,y,z,x0,x1,x2,y0,y1,y2) 
        self.runCommands()
        return

    def Rotate(self,x,y,z,angleInc):
        self.commands = "Rotate({},{},{},{});".format(x,y,z,angleInc) 
        self.runCommands()
        return

    def RotateTo(self,x0,x1,x2,y0,y1,y2):
        self.commands = "RotateTo({},{},{},{},{},{});".format(x0,x1,x2,y0,y1,y2) 
        self.runCommands()
        return

    def Axes (self,j1,j2,j3,j4,j5,j6):
        self.commands = "Axes({},{},{},{},{},{});".format(j1,j2,j3,j4,j5,j6) 
        self.runCommands()
        return

    def AxesTo (self,j1,j2,j3,j4,j5,j6):
        self.commands = "AxesTo({},{},{},{},{},{});".format(j1,j2,j3,j4,j5,j6) 
        self.runCommands()
        return  

    

    def Message(self,msg):
        self.commands = "Message(\"{}\");".format(msg) 
        self.runCommands()
        return  

    def Wait(self,millis):
        self.commands = "Wait({});".format(millis) 
        self.runCommands()
        return  

    # ████████╗ ██████╗  ██████╗ ██╗     
    # ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
    #    ██║   ██║   ██║██║   ██║██║     
    #    ██║   ██║   ██║██║   ██║██║     
    #    ██║   ╚██████╔╝╚██████╔╝███████╗
    #    ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
    #                                    

    def ToolCreate(self,name, x, y, z, x0, x1, x2, y0, y1, y2, weight, cogX, cogY, cogZ):
        self.commands =   "Tool.create(\"{}\",{},{},{},{},{},{},{},{},{},{},{},{},{},);".format(name,
                                                                                                weight, 
                                                                                                cogX, cogY, cogZ)
        self.runCommands()
        return


    def Attach(self,name):
        self.commands = "Attach(\"{}\");".format(name) 
        self.runCommands()
        return  

    def Detach(self):
        self.commands = "Detach();" 
        self.runCommands()
        return 

    def WriteDigital(self,pin,on):
        self.commands = "WriteDigital({},{});".format(pin,on) 
        self.runCommands()
        return 

    def WriteAnalog(self,pin,value):
        self.commands = "WriteAnalog({},{});".format(pin,value) 
        self.runCommands()
        return