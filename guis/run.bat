call pyside2-uic main_form.ui -o "..\src\DAVE\forms\viewer_form.py"
call pyside2-uic widget_axis.ui -o "..\src\DAVE\forms\widget_axis.py"
call pyside2-uic widget_body.ui -o "..\src\DAVE\forms\widget_body.py"
call pyside2-uic widget_poi.ui -o "..\src\DAVE\forms\widget_poi.py"
call pyside2-uic widget_cable.ui -o "..\src\DAVE\forms\widget_cable.py"
call pyside2-uic addnode_form.ui -o "..\src\DAVE\forms\addnode_form.py"
call pyside2-uic widget_name.ui -o "..\src\DAVE\forms\widget_name.py"
call pyside2-uic widget_visual.ui -o "..\src\DAVE\forms\widget_visual.py"
call pyside2-uic widget_force.ui -o "..\src\DAVE\forms\widget_force.py"
call pyside2-uic widget_linhyd.ui -o "..\src\DAVE\forms\widget_linhyd.py"
call pyside2-uic widget_lincon6.ui -o "..\src\DAVE\forms\widget_lincon6.py"
call pyside2-uic widget_beam.ui -o "..\src\DAVE\forms\widget_beam.py"
call pyside2-uic widget_con2d.ui -o "..\src\DAVE\forms\widget_con2d.py"
call pyside2-uic frm_standard_assets.ui -o "..\src\DAVE\forms\frm_standard_assets.py"

call pyside2-rcc resources.qrc -o "..\src\DAVE\forms\resources_rc.py"