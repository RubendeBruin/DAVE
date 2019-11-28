call conda activate deploy
echo set PATH=%PATH%;"C:\Users\beneden\Miniconda3\pkgs\pyside2-5.13.1-py37hfa7ce6d_2\Library\bin"

echo call pyside2-uic widget_axis.ui -o "..\src\DAVE\forms\widget_axis.py"
echo call pyside2-uic widget_body.ui -o "..\src\DAVE\forms\widget_body.py"
echo call pyside2-uic widget_poi.ui -o "..\src\DAVE\forms\widget_poi.py"
echo call pyside2-uic widget_cable.ui -o "..\src\DAVE\forms\widget_cable.py"
echo call pyside2-uic addnode_form.ui -o "..\src\DAVE\forms\addnode_form.py"
echo call pyside2-uic widget_name.ui -o "..\src\DAVE\forms\widget_name.py"
echo call pyside2-uic widget_visual.ui -o "..\src\DAVE\forms\widget_visual.py"
echo call pyside2-uic widget_force.ui -o "..\src\DAVE\forms\widget_force.py"
echo call pyside2-uic main_form.ui -o "..\src\DAVE\forms\viewer_form.py"
echo call pyside2-uic widget_force.ui -o "..\src\DAVE\forms\widget_force.py"
echo call pyside2-uic widget_sheave.ui -o "..\src\DAVE\forms\widget_sheave.py"
echo call pyside2-uic widget_linhyd.ui -o "..\src\DAVE\forms\widget_linhyd.py"
echo call pyside2-uic widget_lincon6.ui -o "..\src\DAVE\forms\widget_lincon6.py"
echo call pyside2-uic widget_beam.ui -o "..\src\DAVE\forms\widget_beam.py"
echo call pyside2-uic widget_con2d.ui -o "..\src\DAVE\forms\widget_con2d.py"
echo call pyside2-uic frm_standard_assets.ui -o "..\src\DAVE\forms\frm_standard_assets.py"
echo call pyside2-uic dlg_solver.ui -o "..\src\DAVE\forms\dlg_solver.py"
call pyside2-uic frm_animation.ui -o "..\src\DAVE\forms\frm_animation.py"


echo call pyside2-rcc resources.qrc -o "..\src\DAVE\forms\resources_rc.py"
