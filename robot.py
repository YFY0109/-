import threading
import time
from shanxian.board import makeblockdevices


def motorUp(port):
    makeblockdevices.sxEncoderMotor.Set(port, '角度', 20)


def motorDown(port):
    makeblockdevices.sxEncoderMotor.Set(port, '角度', 0)


def motorStop(port):
    makeblockdevices.sxEncoderMotor.Set(port, '速度', 0)


def setMotor(port, wait):
    motorUp(port)
    time.sleep(wait)
    motorDown(port)
    motorStop(port)


def returnThread(port=1, wait=2):
    func = lambda: setMotor(port, wait)
    thread = threading.Thread(target=func)
    return thread


thread = returnThread

if __name__ == '__main__':
    thr = thread(1, 2)
    thr.start()
