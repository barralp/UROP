import threading;
import time

class ThreadTesting :
    def threading1(self) :
        self.variable = True
        while self.variable :
            time.sleep(0.5)
            print('running')

    def startThread(self) :
        checkForDataThread = threading.Thread(target=self.threading1)
        checkForDataThread.start()
        time.sleep(3)
        self.variable = False
        print('joining')
        checkForDataThread.join()
        print('joined')

if __name__ == '__main__':
    threadTest = ThreadTesting()
    threadTest.startThread()