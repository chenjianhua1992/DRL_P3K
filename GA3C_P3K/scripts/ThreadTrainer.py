from threading import Thread
from configure import *
from DDQN_asc import DDQN
import time
import rospy
from GA3C_P3K.srv import *

class ThreadTrainer(Thread):
    def __init__(self, rebuffer):
        super(ThreadTrainer, self).__init__()
        self.setDaemon(True)

        self.trainerbrain = DDQN('DDQN_asc0', configure.actions_dim, rebuffer, True)
        self.Relo_Time = time.time()
        rospy.wait_for_service('/food_relocate_request')
        self.food_relocate_request_service = rospy.ServiceProxy('/food_relocate_request', Data_request)
        self.food_numb = configure.number_of_food

    def run(self):
        while self.trainerbrain.episode < configure.EPISODES:
            self.trainerbrain.Perce_Train()

            self.Curr_Time = time.time()
            if (self.Curr_Time-self.Relo_Time) > 1800 :
                for id in xrange(0, self.food_numb):
                    self.food_relocate_request_service(id)
                    rospy.sleep(0.05)
                self.Relo_Time = self.Curr_Time