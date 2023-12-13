﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file tardy_confirmation.py
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


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
tardy_confirmation_spec = ["implementation_id", "tardy_confirmation", 
         "type_name",         "tardy_confirmation", 
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
# @class tardy_confirmation
# @brief ModuleDescription
# 
# 
# </rtc-template>
class tardy_confirmation(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_time_in = OpenRTM_aist.instantiateDataType(RTC.TimedWString)
        """
        """
        self._time_inIn = OpenRTM_aist.InPort("time_in", self._d_time_in)
        self._d_student_name_in = OpenRTM_aist.instantiateDataType(RTC.TimedWString)
        """
        """
        self._student_name_inIn = OpenRTM_aist.InPort("student_name_in", self._d_student_name_in)
        self._d_notification = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        """
        self._notificationOut = OpenRTM_aist.OutPort("notification", self._d_notification)


		


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
        self.addInPort("time_in",self._time_inIn)
        self.addInPort("student_name_in",self._student_name_inIn)
		
        # Set OutPort buffers
        self.addOutPort("notification",self._notificationOut)
		
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
        self.estimated_time = "00:00" #時間:分　のような形で指定

        self.estimated_time = self.estimated_time.split(':')
        self.estimated_time = int(self.estimated_time[0])*60 + int(self.estimated_time[1])

        self.n_time = ""
    
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
        if self._time_inIn.isNew(): #新しいデータが来たか確認
            self._d_time_in = self._time_inIn.read() #値を読み込む
            self.n_time =  self._d_time_in.data 

        if self._student_name_inIn.isNew(): #新しいデータが来たか確認
            if self.n_time :
                self._d_student_name_in = self._student_name_inIn.read() #値を読み込む
                student_name =  self._d_student_name_in.data 
                
                #時間を比較するために分数に変換
                self.n_time = self.n_time.split(':')
                self.n_time = int(self.n_time[0])*60 + int(self.n_time[1])

                if self.n_time > self.estimated_time:
                    out_data = [student_name,"遅刻"]
                else:
                    out_data = [student_name,"なし"]


                self._d_notification.data = out_data
                self._notificationOut.write()
        
            
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
	



def tardy_confirmationInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=tardy_confirmation_spec)
    manager.registerFactory(profile,
                            tardy_confirmation,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    tardy_confirmationInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("tardy_confirmation" + args)

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

