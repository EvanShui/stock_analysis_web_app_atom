#import libraries
from bokeh.io import curdoc
from bokeh.models.widgets import TextInput, Button, Paragraph, CheckboxButtonGroup
from bokeh.layouts import layout, row, column

#create widgets
text_input=TextInput(value="word")
button=Button(label="Generate Text")
output=Paragraph()
output2=Paragraph()
boolean = True
lst = []
checkbox_button_group = CheckboxButtonGroup(labels=lst)

def update():
    output.text += text_input.value
    lst.append(text_input.value)
    for num, val in enumerate(lst):
        output2.text += str(num) + ", " + val
    checkbox_button_group.labels=lst


button.on_click(update)
#lay_out = layout(column(row(text_input, button),row(output, output2)))
widgets = row(text_input, button)
output_row = row(output, output2)
lay_out = column(widgets, output_row, checkbox_button_group)
curdoc().add_root(lay_out)
