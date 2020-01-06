call conda activate deploy


echo call pyside2-uic main_form.ui -o "..\src\DAVE\gui2\forms\main_form.py"
echo call pyside2-uic widget_modeshapes.ui -o "..\src\DAVE\gui2\forms\widgetUI_modeshapes.py"
echo call pyside2-uic widget_ballastconfiguration.ui -o "..\src\DAVE\gui2\forms\widgetUI_ballastconfiguration.py"
echo call pyside2-uic widget_ballastsolver.ui -o "..\src\DAVE\gui2\forms\widgetUI_ballastsolver.py"
echo call pyside2-uic widget_airy.ui -o "..\src\DAVE\gui2\forms\widgetUI_airy.py"
echo call pyside2-uic widget_stability_displ.ui -o "..\src\DAVE\gui2\forms\widget_stability_displUI.py"
call pyside2-uic widget_explore.ui -o "..\src\DAVE\gui2\forms\widgetUI_explore.py"


echo call pyside2-rcc ..\guis\resources.qrc -o "..\src\DAVE\forms\resources_rc.py"
