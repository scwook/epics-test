import xml.etree.ElementTree as ET

root = ET.Element("display")
root.set("typeID", "org.csstudio.opibuilder.Display")
root.set("version", "1.0.0")

actions = ET.SubElement(root, "actions")
actions.set("hook", "false")
actions.set("hook_all", "false")

autoScaleWidgets = ET.SubElement(root, "auto_scale_widgets")
auto_scale_widgets = ET.SubElement(autoScaleWidgets, "auto_scale_widgets")
min_width = ET.SubElement(autoScaleWidgets, "min_width")
min_height = ET.SubElement(autoScaleWidgets, "min_height")

auto_scale_widgets.text = "false"
min_width.text = "-1"
min_height.text = "-1"

autoZoomToFitAll = ET.SubElement(root, "auto_zoom_to_fit_all")
autoZoomToFitAll.text = "false"

backgroundColor = ET.SubElement(root, "background_color")
bg_color = ET.SubElement(backgroundColor, "color")
bg_color.set("red", "240")
bg_color.set("green", "240")
bg_color.set("blue", "240")

boyVersion = ET.SubElement(root, "boy_version")
boyVersion.text = "5.1.0.201704241412"

foregroundColor = ET.SubElement(root, "foreground_color")
fg_color = ET.SubElement(foregroundColor, "color")
fg_color.set("red", "192")
fg_color.set("green", "192")
fg_color.set("blue", "192")

gridSpace = ET.SubElement(root, "grid_space")
gridSpace.text = "6"

height = ET.SubElement(root, "height")
height.text = "600"

macros = ET.SubElement(root, "macros")
include_parent_macros = ET.SubElement(macros, "include_parent_macros")
include_parent_macros.text = "true"

name = ET.SubElement(root, "name")
rules = ET.SubElement(root, "rules")
scripts = ET.SubElement(root, "scripts")

showCloseButton = ET.SubElement(root, "show_close_button")
showCloseButton.text = "true"

showEditRange = ET.SubElement(root, "show_edit_range")
showEditRange.text = "true"

showgrid = ET.SubElement(root, "show_grid")
showgrid.text = "true"

showRuler = ET.SubElement(root, "show_ruler")
showRuler.text = "true"

snapToGeometry = ET.SubElement(root, "snap_to_geometry")
snapToGeometry.text = "true"

widgetType = ET.SubElement(root, "widget_type")
widgetType.text = "Display"

width = ET.SubElement(root, "width")
width.text = "800"

wuid = ET.SubElement(root, "wuid")
wuid.text = "529db863:195a66d09c5:-8000"

x = ET.SubElement(root, "x")
x.text = "-1"

y = ET.SubElement(root, "y")
y.text = "-1"

# Widget
widthSize = 100
heightSize = 25
xPosInit = 30
yPosInit = 30
xPosGap = 5
yPosGap = 5
for i in range(0, 810):

    xCount = i % 10
    yCount = int(i / 10)

    widget = ET.SubElement(root, "widget")
    widget.set("typeId", "org.csstudio.opibuilder.widgets.TextInput")
    widget.set("version", "2.0.0")

    actions = ET.SubElement(widget, "actions")
    actions.set("hook", "false")
    actions.set("hook_all", "false")
    alarm_pulsing = ET.SubElement(widget, "alarm_pulsing")
    alarm_pulsing.text = "false"
    auto_size = ET.SubElement(widget, "auto_size")
    auto_size.text = "false"

    backcolor_alarm_sensitive = ET.SubElement(widget, "backcolor_alarm_sensitive")
    backcolor_alarm_sensitive.text = "false"
    background_color = ET.SubElement(widget, "background_color")
    widget_background_color = ET.SubElement(background_color, "color")
    widget_background_color.set("red", "255")
    widget_background_color.set("green", "255")
    widget_background_color.set("blue", "255")

    border_alarm_sensitive = ET.SubElement(widget, "border_alarm_sensitive")
    border_alarm_sensitive.text = "false"
    border_color = ET.SubElement(widget, "border_color")
    widget_border_color = ET.SubElement(border_color, "color")
    widget_border_color.set("red", "0")
    widget_border_color.set("green", "128")
    widget_border_color.set("blue", "255")

    border_style = ET.SubElement(widget, "border_style")
    border_style.text = "3"
    border_width = ET.SubElement(widget, "border_width")
    border_width.text = "1"
    confirm_message = ET.SubElement(widget, "confirm_message")
    enabled = ET.SubElement(widget, "enabled")
    enabled.text = "true"
    font = ET.SubElement(widget, "font")
    opifont_name = ET.SubElement(font, "opifont.name")
    opifont_name.set("fontName", "맑은 고딕")
    opifont_name.set("height", "9")
    opifont_name.set("style", "0")
    opifont_name.set("pixels", "false")
    opifont_name.text = "Default"
    forecolor_alarm_sensitive = ET.SubElement(widget, "forecolor_alarm_sensitive")
    forecolor_alarm_sensitive.text = "false"

    foreground_color = ET.SubElement(widget, "foreground_color")
    widget_foreground_color = ET.SubElement(foreground_color, "color")
    widget_foreground_color.set("red", "0")
    widget_foreground_color.set("green", "0")
    widget_foreground_color.set("blue", "0")

    format_type = ET.SubElement(widget, "format_type")
    format_type.text = "0"
    widget_height = ET.SubElement(widget, "height")
    widget_height.text = f"{heightSize}"
    horizontal_alignment = ET.SubElement(widget, "horizontal_alignment")
    horizontal_alignment.text = "0"
    limits_from_pv = ET.SubElement(widget, "limits_from_pv")
    limits_from_pv.text = "false"
    maximum = ET.SubElement(widget, "maximum")
    maximum.text = "1.7976931348623157E308"
    minimum = ET.SubElement(widget, "minimum")
    minimum.text = "-1.7976931348623157E308"
    multiline_input = ET.SubElement(widget, "multiline_input")
    multiline_input.text = "false"
    name = ET.SubElement(widget, "name")
    name.text = "Text Input"
    precision = ET.SubElement(widget, "precision")
    precision.text = "0"
    precision_from_pv = ET.SubElement(widget, "precision_from_pv")
    precision_from_pv.text = "true"
    pv_name = ET.SubElement(widget, "pv_name")
    pv_name.text = f"KOBRA-OPTICS:BEAM-COE:Total.VAL[{i}]"
    pv_value = ET.SubElement(widget, "pv_value")
    rotation_angle = ET.SubElement(widget, "rotation_angle")
    rotation_angle.text = "0.0"
    rules = ET.SubElement(widget, "rules")

    scale_options = ET.SubElement(widget, "scale_options")
    width_scalable = ET.SubElement(scale_options, "width_scalable")
    width_scalable.text = "true"
    height_scalable = ET.SubElement(scale_options, "height_scalable")
    height_scalable.text = "true"
    keep_wh_ratio = ET.SubElement(scale_options, "keep_wh_ratio")
    keep_wh_ratio.text = "false"

    scripts = ET.SubElement(widget, "scripts")
    selector_type = ET.SubElement(widget, "selector_type")
    selector_type.text = "0"
    show_units = ET.SubElement(widget, "show_units")
    show_units.text = "false"
    style = ET.SubElement(widget, "style")
    style.text = "0"
    text = ET.SubElement(widget, "text")
    tooltip = ET.SubElement(widget, "tooltip")
    tooltip.text = "$(pv_name)$(pv_value)"
    transparent = ET.SubElement(widget, "transparent")
    transparent.text = "false"
    visible = ET.SubElement(widget, "visible")
    visible.text = "true"
    widget_type = ET.SubElement(widget, "widget_type")
    widget_type.text = "Text Input"
    widget_width = ET.SubElement(widget, "width")
    widget_width.text = f"{widthSize}"
    widget_wuid = ET.SubElement(widget, "wuid")
    widget_wuid.text = "529db863:195a66d09c5:-63eb"
    widget_x = ET.SubElement(widget, "x")
    widget_x.text = f"{xPosInit + (widthSize + xPosGap) * xCount}"
    widget_y = ET.SubElement(widget, "y")
    widget_y.text = f"{yPosInit + (heightSize + yPosGap) * yCount}"


# ElementTree 객체 생성
tree = ET.ElementTree(root)

# XML 파일로 저장
tree.write("output.xml", encoding="utf-8", xml_declaration=True)

print("XML 파일이 생성되었습니다.")