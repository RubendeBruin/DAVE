call conda activate deploy

call pyside2-uic main_form.ui -o "..\src\DAVE\gui\forms\main_form.py"
echo call pyside2-uic widget_modeshapes.ui -o "..\src\DAVE\gui\forms\widgetUI_modeshapes.py"
echo call pyside2-uic widget_ballastconfiguration.ui -o "..\src\DAVE\gui\forms\widgetUI_ballastconfiguration.py"
echo call pyside2-uic widget_ballastsolver.ui -o "..\src\DAVE\gui\forms\widgetUI_ballastsolver.py"
echo call pyside2-uic widget_airy.ui -o "..\src\DAVE\gui\forms\widgetUI_airy.py"
echo echo call pyside2-uic widget_stability_displ.ui -o "..\src\DAVE\gui\forms\widget_stability_displUI.py"
echo call pyside2-uic widget_explore.ui -o "..\src\DAVE\gui\forms\widgetUI_explore.py"
echo call pyside2-uic widget_tank_order.ui -o "..\src\DAVE\gui\forms\widgetUI_tank_order.py"

echo call pyside2-uic widget_waveinteraction.ui -o "..\src\DAVE\gui\forms\widget_waveinteraction.py"
echo call pyside2-uic widget_axis.ui -o "..\src\DAVE\gui\forms\widget_axis.py"
echo call pyside2-uic widget_body.ui -o "..\src\DAVE\gui\forms\widget_body.py"
echo call pyside2-uic widget_poi.ui -o "..\src\DAVE\gui\forms\widget_poi.py"
call pyside2-uic widget_cable.ui -o "..\src\DAVE\gui\forms\widget_cable.py"
echo call pyside2-uic addnode_form.ui -o "..\src\DAVE\gui\forms\addnode_form.py"
echo call pyside2-uic widget_name.ui -o "..\src\DAVE\gui\forms\widget_name.py"
echo call pyside2-uic widget_visual.ui -o "..\src\DAVE\gui\forms\widget_visual.py"
echo call pyside2-uic widget_force.ui -o "..\src\DAVE\gui\forms\widget_force.py"
echo call pyside2-uic widget_sheave.ui -o "..\src\DAVE\gui\forms\widget_sheave.py"
echo call pyside2-uic widget_linhyd.ui -o "..\src\DAVE\gui\forms\widget_linhyd.py"
echo call pyside2-uic widget_lincon6.ui -o "..\src\DAVE\gui\forms\widget_lincon6.py"
echo call pyside2-uic widget_beam.ui -o "..\src\DAVE\gui\forms\widget_beam.py"
echo call pyside2-uic widget_con2d.ui -o "..\src\DAVE\gui\forms\widget_con2d.py"
echo call pyside2-uic frm_standard_assets.ui -o "..\src\DAVE\gui\forms\frm_standard_assets.py"
echo call pyside2-uic dlg_solver.ui -o "..\src\DAVE\gui\forms\dlg_solver.py"
echo call pyside2-uic frm_animation.ui -o "..\src\DAVE\gui\forms\frm_animation.py"
echo call pyside2-uic widget_dynprop.ui -o "..\src\DAVE\gui\forms\widget_dynprop.py"
echo call pyside2-uic widget_contactball.ui -o "..\src\DAVE\gui\forms\widget_contactball.py"
echo call pyside2-uic widget_geometricconnection.ui -o "..\src\DAVE\gui\forms\widget_geometricconnection.py"
echo call pyside2-uic widget_sling.ui -o "..\src\DAVE\gui\forms\widget_sling.py"
echo call pyside2-uic widget_selection_actions.ui -o "..\src\DAVE\gui\forms\widget_selection_actions.py"


echo call pyside2-rcc resources.qrc -o "..\src\DAVE\gui\forms\resources_rc.py"