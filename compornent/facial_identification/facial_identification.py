#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file facial_identification.py
 @brief The facial_identification  component is a component that calculates the degree of similarity with known facial photos stored in the same directory and outputs the file names of similar images. If there are no similar images, outputs No matches found.
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
import face_recognition
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
facial_identification_spec = ["implementation_id", "facial_identification", 
         "type_name",         "facial_identification", 
         "description",       "The facial_identification  component is a component that calculates the degree of similarity with known facial photos stored in the same directory and outputs the file names of similar images. If there are no similar images, outputs No matches found.", 
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
# @class facial_identification
# @brief The facial_identification  component is a component that calculates the degree of similarity with known facial photos stored in the same directory and outputs the file names of similar images. If there are no similar images, outputs No matches found.
# 
# 
# </rtc-template>
class facial_identification(OpenRTM_aist.DataFlowComponentBase):
	
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
        self._d_student_number_out = OpenRTM_aist.instantiateDataType(RTC.TimedWString)
        """
        """
        self._student_number_outOut = OpenRTM_aist.OutPort("student_number_out", self._d_student_number_out)


		


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
        self.addOutPort("student_number_out",self._student_number_outOut)
		
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
        # 複数の既知の顔画像をロード
        self.known_images = ["19001.jpg", "19002.jpg", "19003.jpg", "19004.jpg"]
    
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
            cv2.imwrite("captured_face.jpg", frame)

            known_encodings = []
            # 既知の顔画像のリストからそれぞれの顔の特徴をエンコードし、リストに追加
            for image in self.known_images:
                loaded_image = face_recognition.load_image_file(image)
                encoding = face_recognition.face_encodings(loaded_image)[0]
                known_encodings.append(encoding)

            # 未知の顔画像をロード
            unknown_image = face_recognition.load_image_file("captured_face.jpg")
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        
            # 既知の顔と未知の顔の間の距離を計算
            face_distances = face_recognition.face_distance(known_encodings, unknown_encoding)

            # 一致する顔画像の中で最も似ているものを選択
            if any(face_distances <= 0.6): # 0.6は類似度の閾値、調整可能
                best_match_index = face_distances.argmin()
                best_match_image = self.known_images[best_match_index]
                print(str(best_match_image[:-4]))
                self._d_student_number_out.data = str(best_match_image[:-4])
                self._student_number_outOut.write()

            else:
                print("No matches found.")   
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
	



def facial_identificationInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=facial_identification_spec)
    manager.registerFactory(profile,
                            facial_identification,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    facial_identificationInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("facial_identification" + args)

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

