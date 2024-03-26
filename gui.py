# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.1.0-0-g733bf3d)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################
import subprocess
import threading
import os

import pathlib
import shutil
import time

import wx
import wx.xrc

def check_process_running(process_name):
    output = subprocess.check_output(['tasklist'], creationflags=0x08000000)
    processes = output.decode("ansi").split('\n')
    for process in processes:
        if process_name.lower() in process.lower():
            return True
    return False

class BackgroundThread(threading.Thread):
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.parent = parent

    def run(self):
        self.parent.do_work()

class MyFrame1 ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Dragon's Dogma 2 AutoSave Manager", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER^wx.MAXIMIZE_BOX)


        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        if os.path.exists("./DD2AutoSave.conf"):
            rt = pathlib.Path("./DD2AutoSave.conf").read_text()
            rts = rt.split("\n")
            self.srcDir = rts[0]
            self.destDir = rts[1]
            self.maxSave = int(rts[2])
            self.itvSave = int(rts[3])
        else:
            self.srcDir = u"Steam Save Directory(i.e. */Steam/userdate/uid/2054970/remote/win64_save)"
            self.destDir = u"File Backup Directory"
            self.maxSave = 3
            self.itvSave = 8

        self.m_dirPickerSrc = wx.DirPickerCtrl( self, wx.ID_ANY, self.srcDir, u"Steam Save Directory", wx.DefaultPosition, wx.Size( 500,-1 ), wx.DIRP_DEFAULT_STYLE )
        bSizer3.Add( self.m_dirPickerSrc, 0, wx.ALL, 5 )

        self.m_dirPickerDes = wx.DirPickerCtrl( self, wx.ID_ANY, self.destDir, u"Select a folder", wx.DefaultPosition, wx.Size( 500,-1 ), wx.DIRP_DEFAULT_STYLE )
        bSizer3.Add( self.m_dirPickerDes, 0, wx.ALL, 5 )

        self.m_listBox_save= []
        self.m_listBox = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 500,100 ), self.m_listBox_save, 0 )
        bSizer3.Add( self.m_listBox, 0, wx.ALL, 5 )

        gSizer1 = wx.GridSizer( 0, 4, 0, 0 )
        # Save Num Slider
        self.m_slider1 = wx.Slider( self, wx.ID_ANY, self.maxSave, 1, 10, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        gSizer1.Add( self.m_slider1, 0, wx.ALL, 5 )
        self.m_slider1.Bind(wx.EVT_SLIDER, self.onSliderChange1)
        self.m_slider1_Text = wx.StaticText( self, wx.ID_ANY, u"存档数量:"+str(self.m_slider1.Value), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_slider1_Text.Wrap( -1 )
        gSizer1.Add( self.m_slider1_Text, 0, wx.ALL, 5 )

        # Save Time Slider
        self.m_slider2 = wx.Slider( self, wx.ID_ANY, self.itvSave, 1, 30, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        gSizer1.Add( self.m_slider2, 0, wx.ALL, 5 )
        self.m_slider2.Bind(wx.EVT_SLIDER, self.onSliderChange2)
        self.m_slider2_Text = wx.StaticText( self, wx.ID_ANY, u"存档间隔:" + str(self.m_slider2.Value) + "min", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_slider2_Text.Wrap( -1 )
        gSizer1.Add( self.m_slider2_Text, 0, wx.ALL, 5 )

        # Start Button
        self.m_buttonStart = wx.Button( self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_buttonStart.Bind(wx.EVT_BUTTON, self.onButtonStart)
        gSizer1.Add( self.m_buttonStart, 0, wx.ALL, 5 )

        # Restore Button
        self.m_buttonRestore = wx.Button( self, wx.ID_ANY, u"Restore", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_buttonRestore, 0, wx.ALL, 5 )
        self.m_buttonRestore.Bind(wx.EVT_BUTTON, self.onButtonRestore)

        bSizer3.Add( gSizer1, 1, wx.EXPAND, 5 )

        self.m_statusText = wx.StaticText( self, wx.ID_ANY, u"Status", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_statusText.Wrap( -1 )

        bSizer3.Add( self.m_statusText, 0, wx.ALL, 5 )

        # self.timer = wx.Timer(self)
        # self.Bind(wx.EVT_TIMER, self.onTimer)

        self.SetSizer( bSizer3 )
        self.Layout()

        self.Centre( wx.BOTH )
    
    def onSliderChange1(self, event):
        self.maxSave = self.m_slider1.Value
        self.m_slider1_Text.SetLabel("存档数量:"+str(self.m_slider1.Value))
        
    def onSliderChange2(self, event):
        self.itvSave = self.m_slider2.Value
        self.m_slider2_Text.SetLabel("存档间隔:"+str(self.m_slider2.Value)+"min")
        

    def onButtonStart(self, event):
        self.srcDir = self.m_dirPickerSrc.Path
        self.destDir = self.m_dirPickerDes.Path
        self.maxSave = self.m_slider1.Value
        self.itvSave = self.m_slider2.Value
        filename ="./DD2AutoSave.conf"
        pathlib.Path(filename).write_text(self.srcDir+"\n" + self.destDir+"\n" + str(self.maxSave)+"\n"+ str(self.itvSave) + "\n")
        self.thread = BackgroundThread(self)
        self.thread.start()

    def do_work(self):
        self.saveDir = []
        process_name = "DD2.exe"
        if(check_process_running(process_name)):
            self.m_statusText.SetForegroundColour((0, 255, 0))
            self.m_statusText.SetLabel("Run")
        else:
            self.m_statusText.SetForegroundColour((255, 0, 0))
            self.m_statusText.SetLabel("Stop")
        while(check_process_running(process_name)):
            
            print(self.saveDir)
            self.saveDir.append(self.destDir+"\\"+str(time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime())) +"\\win64_save")
            if len(self.saveDir) > self.maxSave:
                # filename = "E://ddsave//new_file.txt"
                # pathlib.Path(filename).write_text(dest_folder_list[0][:-12])
                shutil.rmtree(self.saveDir[0][:-11])
                wx.CallAfter(self.popText)
                self.saveDir.pop(0)
            shutil.copytree(self.srcDir, self.saveDir[-1])
            wx.CallAfter(self.addText, self.saveDir[-1][len(self.destDir):-11])
            time.sleep(self.itvSave * 60)
            #time.sleep(3)
        self.m_statusText.SetForegroundColour((255, 0, 0))
        self.m_statusText.SetLabel("Stop")
    
    def addText(self, savemsg):
        self.m_listBox.InsertItems([savemsg], 0)
    
    def popText(self):
        self.m_listBox.Delete(self.maxSave-1)

    def onButtonRestore(self, event):
        select_index = self.m_listBox.GetSelection()
        if select_index != wx.NOT_FOUND:
            nowSelect = self.m_listBox.GetString(select_index)
            warningDialog = wx.MessageDialog(None, "请确定回到这个时间"+nowSelect+"的世界", "Reverse", wx.YES_NO | wx.ICON_QUESTION)
            if warningDialog.ShowModal() == wx.ID_YES:
                warningDialog.Destroy()
                selectTarget = self.destDir + nowSelect + "\\win64_save"
                shutil.copy(selectTarget+"\\data000.bin", self.srcDir+"\\data000.bin")
                shutil.copy(selectTarget+"\\data00-1.bin", self.srcDir+"\\data00-1.bin")
                shutil.copy(selectTarget+"\\data001Slot.bin", self.srcDir+"\\data001Slot.bin")
            else:
                warningDialog.Destroy()
                pass


    def __del__( self ):
        pass

if __name__ == "__main__":
    app = wx.App()
    window = MyFrame1(parent=None)
    window.Show()
    app.MainLoop()
