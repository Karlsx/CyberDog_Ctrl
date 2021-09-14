#!/usr/bin/python3
#
# Copyright (c) 2021 Karlsx All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os import system
import grpc
import cyberdog_app_pb2
import cyberdog_app_pb2_grpc
import keyboard


class Vector3:
    x: float = 0
    y: float = 0
    z: float = 0

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z
        pass


MAX_SPEED = 16

stub = None
cyberdog_ip = None  # Write Your Cyberdog IP Here or Input while running
speed_lv = 1
linear = Vector3(0, 0, 0)
angular = Vector3(0, 0, 0)


# Send Order Cmd to Cyberdog
def RunOrderCMD():
    # Open grpc channel
    global cyberdog_ip
    if (cyberdog_ip is None):
        cyberdog_ip = input('Cyberdog Ip:')
    with grpc.insecure_channel(str(cyberdog_ip) + ':50051') as channel:
        print("Wait connect")
        try:
            grpc.channel_ready_future(channel).result(timeout=10)
        except grpc.FutureTimeoutError:
            print("Connect error, Timeout")
            return
        # Get stub from channel
        stub = cyberdog_app_pb2_grpc.CyberdogAppStub(channel)

        # Stand up
        response = stub.setMode(
            cyberdog_app_pb2.CheckoutMode_request(
                next_mode=cyberdog_app_pb2.ModeStamped(
                    header=cyberdog_app_pb2.Header(
                        stamp=cyberdog_app_pb2.Timestamp(
                            sec=0,      # seem not need
                            nanosec=0   # seem not need
                        ),
                        frame_id=""     # seem not need
                    ),
                    mode=cyberdog_app_pb2.Mode(
                        control_mode=cyberdog_app_pb2.CheckoutMode_request.MANUAL,
                        mode_type=0     # seem not need
                    )),
                timeout=10))
        succeed_state = False
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Stand up, result:' + str(succeed_state))

        # Execute HI_FIVE order
        if (succeed_state == False):
            return
        response = stub.setExtmonOrder(
            cyberdog_app_pb2.ExtMonOrder_Request(
                order=cyberdog_app_pb2.MonOrder(
                    id=cyberdog_app_pb2.MonOrder.MONO_ORDER_HI_FIVE,
                    para=0      # seem not need
                ),
                timeout=50))
        for resp in response:
            succeed_state = resp.succeed
            print('Execute HI_FIVE order, result:' + str(succeed_state))

        # Get down
        if (succeed_state == False):
            return
        response = stub.setMode(
            cyberdog_app_pb2.CheckoutMode_request(
                next_mode=cyberdog_app_pb2.ModeStamped(
                    header=cyberdog_app_pb2.Header(
                        stamp=cyberdog_app_pb2.Timestamp(
                            sec=0,      # seem not need
                            nanosec=0   # seem not need
                        ),
                        frame_id=""     # seem not need
                    ),
                    mode=cyberdog_app_pb2.Mode(
                        control_mode=cyberdog_app_pb2.CheckoutMode_request.DEFAULT,
                        mode_type=0     # seem not need
                    )),
                timeout=10))
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Get down, result:' + str(succeed_state))

def PrintState():
    print('Now speed:%.1fm/s' % float(speed_lv*0.1))
    print('W:GoFront')
    print('S:GoBack')
    print('A:GoLeft')
    print('D:GoRight')
    print('Q:TurnLeft')
    print('E:TurnRight')
    print('U:SpeedUp')
    print('I:SpeedDown')
    print('ESC:Exit Control')

def SendData():
    global stub
    system('clear')
    PrintState()
    stub.sendAppDecision(
        cyberdog_app_pb2.Decissage(
            twist=cyberdog_app_pb2.Twist(
                linear=cyberdog_app_pb2.Vector3(
                    x=linear.x,
                    y=linear.y,
                    z=linear.z
                ),
                angular=cyberdog_app_pb2.Vector3(
                    x=angular.x,
                    y=angular.y,
                    z=angular.z
                )
            )
        )
    )


def GoForward(Event):
    linear.x = 0.1 * speed_lv
    linear.y = 0
    angular.z = 0
    SendData()


def GoBack(Event):
    linear.x = -0.1 * speed_lv
    linear.y = 0
    angular.z = 0
    SendData()


def GoLeft(Event):
    linear.x = 0
    linear.y = 0.1 * speed_lv
    angular.z = 0
    SendData()


def GoRight(Event):
    linear.x = 0
    linear.y = -0.1 * speed_lv
    angular.z = 0
    SendData()


def TurnLeft(Event):
    linear.x = 0
    linear.y = 0
    angular.z = 0.1 * speed_lv
    SendData()


def TurnRight(Event):
    linear.x = 0
    linear.y = 0
    angular.z = -0.1 * speed_lv
    SendData()


def Stop(Event):
    linear.x = 0
    linear.y = 0
    angular.z = 0
    SendData()


def SpeedUp(Event):
    global speed_lv
    speed_lv += 1
    speed_lv = min(speed_lv, MAX_SPEED)


def SpeedDown(Event):
    global speed_lv
    speed_lv -= 1
    speed_lv = max(speed_lv, 1)


# Send Move Cmd to Cyberdog
def RunMoveCMD():
    global stub
    global cyberdog_ip
    if (cyberdog_ip is None):
        cyberdog_ip = input('Cyberdog Ip:')
    with grpc.insecure_channel(str(cyberdog_ip) + ':50051') as channel:
        print("Wait connect")
        try:
            grpc.channel_ready_future(channel).result(timeout=10)
        except grpc.FutureTimeoutError:
            print("Connect error, Timeout")
            return
        stub = cyberdog_app_pb2_grpc.CyberdogAppStub(channel)

        # Stand up
        response = stub.setMode(
            cyberdog_app_pb2.CheckoutMode_request(
                next_mode=cyberdog_app_pb2.ModeStamped(
                    header=cyberdog_app_pb2.Header(
                        stamp=cyberdog_app_pb2.Timestamp(
                            sec=0,      # seem not need
                            nanosec=0   # seem not need
                        ),
                        frame_id=""     # seem not need
                    ),
                    mode=cyberdog_app_pb2.Mode(
                        control_mode=cyberdog_app_pb2.CheckoutMode_request.MANUAL,
                        mode_type=0     # seem not need
                    )),
                timeout=10))
        succeed_state = False
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Stand up, result:' + str(succeed_state))

        # Change gait to walk
        response = stub.setPattern(
            cyberdog_app_pb2.CheckoutPattern_request(
                patternstamped=cyberdog_app_pb2.PatternStamped(
                    header=cyberdog_app_pb2.Header(
                        stamp=cyberdog_app_pb2.Timestamp(
                            sec=0,      # seem not need
                            nanosec=0   # seem not need
                        ),
                        frame_id=""     # seem not need
                    ),
                    pattern=cyberdog_app_pb2.Pattern(
                        gait_pattern=cyberdog_app_pb2.Pattern.GAIT_TROT
                    )
                ),
                timeout=10
            )
        )
        for resp in response:
            succeed_state = resp.succeed
            print('Change gait to walk, result:' + str(succeed_state))

        # Send Move Cmd
        if (succeed_state == False):
            return
        PrintState()
        keyboard.on_press_key('w', GoForward)
        keyboard.on_press_key('s', GoBack)
        keyboard.on_press_key('a', GoLeft)
        keyboard.on_press_key('d', GoRight)
        keyboard.on_press_key('q', TurnLeft)
        keyboard.on_press_key('e', TurnRight)
        keyboard.on_press_key('u', SpeedUp)
        keyboard.on_press_key('i', SpeedDown)
        keyboard.on_release(Stop)
        keyboard.wait('esc')
        system('clear')

        # Get down
        if (succeed_state == False):
            return
        response = stub.setMode(
            cyberdog_app_pb2.CheckoutMode_request(
                next_mode=cyberdog_app_pb2.ModeStamped(
                    header=cyberdog_app_pb2.Header(
                        stamp=cyberdog_app_pb2.Timestamp(
                            sec=0,      # seem not need
                            nanosec=0   # seem not need
                        ),
                        frame_id=""     # seem not need
                    ),
                    mode=cyberdog_app_pb2.Mode(
                        control_mode=cyberdog_app_pb2.CheckoutMode_request.DEFAULT,
                        mode_type=0     # seem not need
                    )),
                timeout=10))
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Get down, result:' + str(succeed_state))


if __name__ == '__main__':
    while True:
        mod = input('Choose mode [1:RunOrderCMD, 2:RunMoveCMD, else:Exit]:')
        print(mod)
        if (mod == '1'):
            RunOrderCMD()
        elif (mod == '2'):
            RunMoveCMD()
        else:
            break
