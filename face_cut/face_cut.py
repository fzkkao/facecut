#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file face_cut.py
 @brief ModuleDescription
 @date $Date$


"""
# </rtc-template>

import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

#other-import
import dlib
import cv2
import numpy

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
face_cut_spec = ["implementation_id", "face_cut", 
         "type_name",         "face_cut", 
         "description",       "ModuleDescription", 
         "version",           "1.0.0", 
         "vendor",            "VenderName", 
         "category",          "Category", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class face_cut
# @brief ModuleDescription
# 
# 
# </rtc-template>
class face_cut(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_image_in = OpenRTM_aist.instantiateDataType(RTC.CameraImage)
        """
        """
        self._image_inIn = OpenRTM_aist.InPort("image_in", self._d_image_in)
        self._d_image_out = OpenRTM_aist.instantiateDataType(RTC.CameraImage)
        """
        """
        self._image_outOut = OpenRTM_aist.OutPort("image_out", self._d_image_out)


		


        # initialize of configuration-data.
        # <rtc-template block="init_conf_param">
		
        # </rtc-template>


		 
    ##
    #
    # The initialize action (on CREATED->ALIVE transition)
    # 
    # @return RTC::ReturnCode_t
    # 
    #
    def onInitialize(self):
        # Bind variables and configuration variable
		
        # Set InPort buffers
        self.addInPort("image_in",self._image_inIn)
		
        # Set OutPort buffers
        self.addOutPort("image_out",self._image_outOut)
		
        # Set service provider to Ports
		
        # Set service consumers to Ports
		
        # Set CORBA Service Ports
		
        return RTC.RTC_OK
	
    ###
    ## 
    ## The finalize action (on ALIVE->END transition)
    ## 
    ## @return RTC::ReturnCode_t
    #
    ## 
    #def onFinalize(self):
    #

    #    return RTC.RTC_OK
	
    ###
    ##
    ## The startup action when ExecutionContext startup
    ## 
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onStartup(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The shutdown action when ExecutionContext stop
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onShutdown(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ##
    #
    # The activated action (Active state entry action)
    #
    # @param ec_id target ExecutionContext Id
    # 
    # @return RTC::ReturnCode_t
    #
    #
    def onActivated(self, ec_id):
    
        return RTC.RTC_OK
	
    ###
    ##
    ## The deactivated action (Active state exit action)
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onDeactivated(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ##
    #
    # The execution action that is invoked periodically
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    def crop_faces(self,img, write_path, padding):
        faceDetector = dlib.get_frontal_face_detector()
        faces = faceDetector(img, 0)

        saved_count = 0  # 保存した画像の数を数えるための変数

        if len(faces) > 0:
            for i, face in enumerate(faces):
                img_h, img_w, c = img.shape
                face_h = int(face.bottom() - face.top())
                face_w = int(face.right() - face.left())

                rect_top = int(face.top()) - (face_h * padding)
                rect_top = max(rect_top, 0)
                rect_bottom = int(face.bottom()) + (face_h * padding)
                rect_bottom = min(rect_bottom, img_h)
                rect_left = int(face.left()) - (face_w * padding)
                rect_left = max(rect_left, 0)
                rect_right = int(face.right()) + (face_w * padding)
                rect_right = min(rect_right, img_w)

                face_img = img[int(rect_top):int(rect_bottom),int(rect_left):int(rect_right)]
                face_filename = f"{write_path}_{i}.jpg"
                cv2.imwrite(face_filename, face_img)
                saved_count += 1  # 保存した画像の数を増やす

        return saved_count  # 保存した画像の数を返す

    def onExecute(self, ec_id):
        if self._image_inIn.isNew(): #新しいデータが来たか確認
            self._d_image_in = self._image_inIn.read()
            #最初一回の取得の際にtrueを出力してしまうことを防ぐ変数
            self.first_image_acquisition = False

            frame = numpy.frombuffer(bytes(self._d_image_in.pixels), dtype=numpy.uint8)
            frame = frame.reshape(self._d_image_in.height, self._d_image_in.width, self._d_image_in.bpp//8)    
            frame = cv2.cvtColor(
                frame, cv2.COLOR_BGRA2BGR)
            #画像をファイルに保存
            saved_count = self.crop_faces(frame,"face",0.1)
            print(saved_count)

            #画像送信
            for image_num in range(saved_count):
                frame = cv2.imread("face_" + str(image_num) + ".jpg")

                self._d_image_out.height = frame.shape[0]
                self._d_image_out.width = frame.shape[1]
                if(len(frame.shape)>2):
                    self._d_image_out.bpp = 8*frame.shape[2]
                else:
                    self._d_image_out.bpp = 8
                self._d_image_out.pixels = frame.flatten().tobytes()
                self._image_outOut.write() 
    
        return RTC.RTC_OK
	
    ###
    ##
    ## The aborting action when main logic error occurred.
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onAborting(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The error action in ERROR state
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onError(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The reset action that is invoked resetting
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onReset(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The state update action that is invoked after onExecute() action
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##

    ##
    #def onStateUpdate(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The action that is invoked when execution context's rate is changed
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onRateChanged(self, ec_id):
    #
    #    return RTC.RTC_OK
	



def face_cutInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=face_cut_spec)
    manager.registerFactory(profile,
                            face_cut,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    face_cutInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("face_cut" + args)

def main():
    # remove --instance_name= option
    argv = [i for i in sys.argv if not "--instance_name=" in i]
    # Initialize manager
    mgr = OpenRTM_aist.Manager.init(sys.argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager()

if __name__ == "__main__":
    main()

