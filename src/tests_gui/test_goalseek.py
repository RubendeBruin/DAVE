from DAVE import *
from DAVE.gui import Gui

s = Scene()
s.new_frame('frame1')

g = Gui(s, workspace="EXPLORE", block=False)
dock = g.guiWidgets['Explore 1-to-1']
dock.ui.editEvaluate.setPlainText("s['frame1'].x")
dock.ui.editSet.setText("s['frame1'].x")

dock.ui.btnGoalSeek.click()

g.app.exec()  #<-- verify that the button is added to the history