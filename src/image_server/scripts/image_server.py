#!/usr/bin/env python
# 
# VIPER: Vision Inference Processing (Edge) Endogenous Robot
# Andrew D'Amico
# MSDS 462 Computer Vision
# Northwestern University
# Copyright (c) 2021, Andrew D'Amico. All rights reserved.
# Licenced under BSD Licence.

###################################|####################################
############################ M O D U L E S #############################
############################# ROS MODULES ##############################
import rospy
from viper_toolkit import NameManager, ProcessTimer
from viper_toolkit import Parameter, ParameterManager
from viper_toolkit import Logger

############################# STD MODULES ##############################
import time
######################### IMAGE SERVER MODULES #########################
from sensor_msgs.msg import Image
from std_msgs.msg import Bool

######################### MODEL SERVER MODULES #########################
from model_server.srv import ImageRequest, ImageRequestResponse


class Ticket(object):
    def __init__(self):
        self.raw = Image()
        self.state = Bool()
        self.set_flags()
    
    def set_flags(self):
        self.request = True
        #600x800 = False
        #400x800 = False

class ImageServer(object):
    def __init__(self):
        self.setup_ros()
        self.wait_for_dependencies()
        self.loop()

    def setup_ros(self):
        # This runs all of the preceeding functions.
        rospy.init_node('image_server', log_level=rospy.DEBUG)
        self.setup_parameters()
        self.setup_ticket()
        self.setup_request_nodes()
        self.setup_image_nodes()
        self.setup_publishers()
        self.setup_model_server_proxy()
        rospy.loginfo(f"[{self.name.abv}] ROS Setup")
    
    def setup_parameters(self):
        #Create an instance of the parameters object.
        self.name = NameManager()
        self.logger = Logger(name_manager = self.name) 
        self.img_s_parameters = ParameterManager(
            logger = self.logger, 
            name_manager = self.name)
        
        # Add each of our parameters and indicate the rate we wish
        # for the noze to run
        self.img_s_parameters.add(
            Parameter(
                name="rate", 
                target=f"{self.name.name}/rate", 
                default=50,
                dynamic=True,
                name_manager = self.name,
                logger=self.logger))

        # Indicates that the parameter should be updated dynamically 
        # if it changes after the node has started running.
        self.img_s_parameters.add(
            Parameter(
                name="updates", 
                target=f"{self.name.name}/dynamic", 
                default=True, 
                dynamic=True,
                name_manager=self.name,
                logger=self.logger))

    def setup_ticket(self):
        # Instantiates a ticket object which contain both
        # the flags for the type of image requested, as well
        # as the last image itself
        self.ticket = Ticket()
        rospy.loginfo(f"[{self.name.abv}] Ticket Setup")

    def wait_for_dependencies(self):
        # There is no functionality for the image server unless our 
        # camera module is online. 
        dependencies = [self.camera_node]
        for package in dependencies:
            rospy.loginfo(f"[{self.name.abv}] Waiting for {package} to come online.")
            rospy.wait_for_message(package, Image)
            
        rospy.loginfo(f"[{self.name.abv}] {package} Online.")
        return
        

        
    def setup_request_nodes(self):
        # Subscribe to the image request message from the Pose 
        # Estimation node
        rospy.Subscriber('image_request/POS', 
            Bool, 
            self.image_rqst_callback,
            queue_size = 1
            )
        rospy.loginfo(f"[{self.name.abv}] Pose Detection Node Subscribed")
        
        # Subscribe to the Image request message from the Scene 
        # Segmentation node
        rospy.Subscriber('image_request/SEG', 
            Bool, 
            self.image_rqst_callback,
            queue_size = 1
            )
        rospy.loginfo(f"[{self.name.abv}] Segmentation Node Subscribed")
        
        # Subscribe to the image request message from the depth 
        # perception node
        rospy.Subscriber('image_request/DPT', 
            Bool, 
            self.image_rqst_callback,
            queue_size = 1
            )
        rospy.loginfo(f"[{self.name.abv}] Depth Perception Node Subscribed")
    
    def setup_image_nodes(self):
        # Create the holding container for an incoming image message.
        self.image = Image()
        
        # Subscribe to the camera node.
        self.camera_node = "/inland_ir_cam/image"
        rospy.Subscriber(self.camera_node,
            Image, 
            self.image_callback, 
            queue_size=1
            )
        rospy.loginfo(f"[{self.name.abv}] Camera Subscribed")
    
    def setup_publishers(self):
        # This is the method by which we publish the most recent image
        # Specifically, this is used by the final image augmentation 
        # node as the models receive their image via the service.
        self.pub_image = rospy.Publisher(
            'image_server/image',
            Image,
            queue_size=1
            )
        rospy.loginfo("[IMG] Image Republisher Online")
        
        # This publishes the status of the images delivered to the 
        # Model Server. It announces to all nodes that new images are
        # available at the model server and they may now make a new 
        # request.
        self.pub_status = rospy.Publisher(
            'image_server/status',
            Bool,
            queue_size=1
            )
        rospy.loginfo("[IMG] Image Server Status Online")
            
    def setup_model_server_proxy(self):
        # This is the method API by which the image server requests
        # that the model server accept its image. The request message
        # is the image, and the reply is a bool indicating success.
        self.image_push_rqst = rospy.ServiceProxy(
            'model_server/image_fetching_service',
            ImageRequest
            )

    def image_callback(self, msg):
        # This callback function saves the image message received 
        # from the camera to self.image
        self.image = msg
        rospy.logdebug(f"[{self.name.abv}] Image Received.")
        
    def image_rqst_callback(self, msg):
        # If any message is received from a modeling node indicating a 
        # new image is required, this callback function sets the request
        # ticket flag to True. This ensures that we only deliver images 
        # to the modeling server which will be used by the models.
        node_status = msg.data
        if node_status:
            self.ticket.request = True

    def action_loop(self):
        self.ticket.request = True
        if self.ticket.request:
            self.timer.lap("Negotiate with Model Server")
            # If request is true, then nodes are requesting images. If
            # response is false, then we only need to republish the
            # new image.
            try:
                rospy.loginfo("[IMG] Image Fetching Service Requested.")
                response = self.image_push_rqst(self.image)
            except:
                rospy.logerr("[IMG] Could not send image to Model Server")
                # If we couldn't deliver the image to the model server
                # then we need to keep trying
                return

            if response.status.data:
                # If True, the model server now has the newest image.
                # Note that currently this should always be True,
                # however that will not be the case as we offer
                # different sized images
                try:
                    # We tell all of the listening nodes they can now
                    # use the Model Server.
                    self.ticket.state = True
                    #we clear our request queue
                    self.ticket.request = False
                    rospy.loginfo("[IMG] Images Delivered to Model Server")
                except:
                    rospy.logerr("[IMG] Could not broadcast image available")
                    # If we could not change status, we should still
                    # return the new image for nodes that are not
                    # dependent on the model server
                    return
                self.timer.time(
                    "Negotiate with Model Server", 
                    name = "MOD"
                    )
            else:
                rospy.loginfo("[IMG] Model Server returned False")
                # If the ticket requests are set to false then the 
                # model server doesn't need a new image yet, however
                # the other nodes which are not dependent on the model
                # server do, so we will publish that image.
                self.ticket.state = False
                return

    def loop(self):

        while not rospy.is_shutdown():
            print(self.img_s_parameters.rate)
            print(self.img_s_parameters)
            rate = rospy.Rate(self.img_s_parameters.rate)
            # Update any of our parameters from the parameter server
            if self.img_s_parameters.updates == True:
                self.img_s_parameters.update()
                
            self.timer = ProcessTimer(abv=self.name.abv)
            # See if we need to service the Model Server
            self.action_loop()
            
            # Publish the current state of the image at the Model Server.
            self.pub_status.publish(self.ticket.state)
            
            # Publish the last image we received regardless.
            self.pub_image.publish(self.image)
            rospy.logdebug("[IMG] Image Published")
            self.timer.time("total_runtime")
            rate.sleep()

if __name__ == '__main__':
    ImageServer()
