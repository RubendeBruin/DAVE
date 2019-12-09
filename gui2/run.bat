call conda activate deploy
echo set PATH=%PATH%;"C:\Users\beneden\Miniconda3\pkgs\pyside2-5.13.1-py37hfa7ce6d_2\Library\bin"

echo call pyside2-uic main_form.ui -o "..\src\DAVE\gui2\forms\main_form.py"
echo call pyside2-uic widget_modeshapes.ui -o "..\src\DAVE\gui2\forms\widgetUI_modeshapes.py"
call pyside2-uic widget_ballastconfiguration.ui -o "..\src\DAVE\gui2\forms\widgetUI_ballastconfiguration.py"
call pyside2-uic widget_ballastsolver.ui -o "..\src\DAVE\gui2\forms\widgetUI_ballastsolver.py"

echo call pyside2-rcc resources.qrc -o "..\src\DAVE\forms\resources_rc.py"
