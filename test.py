import socket
import win32serviceutil

import servicemanager
import win32event
import win32service

import random
import pathlib
import shutil
import time

import subprocess

class SMWinservice(win32serviceutil.ServiceFramework):
    '''Base class to create winservice in Python'''
  
    _svc_name_ = 'DDAutoSave'
    _svc_display_name_ = 'DragonsDogemaAutoSave'
    _svc_description_ = 'Dragons Dogema Auto Save Service'

    @classmethod
    def parse_command_line(cls):
        '''
        ClassMethod to parse the command line
        '''
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        '''
        Constructor of the winservice
        '''
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        '''
        Called when the service is asked to stop
        '''
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        '''
        Called when the service is asked to start
        '''
        self.start()
        # servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
        #                       servicemanager.PYS_SERVICE_STARTED,
        #                       (self._svc_name_, ''))
        while(True):
            self.main()

        pass

    def start(self):
        '''
        Override to add logic before the start
        eg. running condition
        '''
        pass

    def stop(self):
        '''
        Override to add logic before the stop
        eg. invalidating running condition
        '''
        pass

    def main(self):
        '''
        Main class to be ovverridden to add logic
        '''
        #src_folder = "path/to/source/folder"
        dest_folder_list = []
        process_name = 'DD2.exe'
        #flag
        while(check_process_running(process_name)):
            src_path = "./win64_save"
            dest_folder_list.append("./ddsave//"+str(time.strftime("%Y-%m-%d-%H-%M-%S",time.gmtime())) +"//win64_save")
            if len(dest_folder_list) > 3:
                filename = "./ddsave//new_file.txt"
                pathlib.Path(filename).write_text(dest_folder_list[0][:-12])
                shutil.rmtree(dest_folder_list[0][:-12])
                dest_folder_list.pop(0)
            shutil.copytree(src_path, dest_folder_list[-1])
            time.sleep(60*8)

      # def runself(self):
      #     while self.isRunning:
      #         time.sleep(5)

def check_process_running(process_name):
    output = subprocess.check_output(['tasklist'])
    processes = output.decode("ansi").split('\n')
    for process in processes:
        if process_name.lower() in process.lower():
            return True
    return False

# entry point of the module: copy and paste into the new module
# ensuring you are calling the "parse_command_line" of the new created class
if __name__ == '__main__':
    SMWinservice.parse_command_line()
