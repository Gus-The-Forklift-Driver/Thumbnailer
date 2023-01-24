import os
from subprocess import call
import dearpygui.dearpygui as dpg
import os
import thumbnail
import re

dpg.create_context()


def callback(sender, app_data):
    # print('OK was clicked.')
    # print("Sender: ", sender)
    # print("App Data: ", app_data)
    dpg.set_value('folder_path', app_data['file_path_name'])
    file_amount = 0
    for root, dirs, files in os.walk(app_data['file_path_name']):
        for file in files:
            if file.split('.')[-1] == dpg.get_value('input_extention'):
                if use_regex(file) == False:
                    file_amount += 1
    print(file_amount)
    dpg.set_value('progress', 0)
    dpg.set_value('progress_text', f'0/{file_amount}')


def cancel_callback(sender, app_data):
    # print('Cancel was clicked.')
    # print("Sender: ", sender)
    # print("App Data: ", app_data)
    pass


def use_regex(input_text):
    pattern = re.compile(r"^.*_[0-9]+x[0-9]+\..*$", re.IGNORECASE)
    return bool(pattern.match(input_text))


def crawl():
    folder_path = dpg.get_value('folder_path')
    file_amount = 0
    progress = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.split('.')[-1] == dpg.get_value('input_extention'):
                if use_regex(file) == False:
                    file_amount += 1
    print(file_amount)
    dpg.set_value('progress', 0)
    dpg.set_value('progress_text', f'0/{file_amount}')
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.split('.')[-1] == dpg.get_value('input_extention'):
                print(os.path.join(root, file))
                if use_regex(file) == False:
                    thumbnail.resizer(input=os.path.join(root, file),
                                      iterations=dpg.get_value('iterations'),
                                      extention=dpg.get_value('output_extention'),
                                      output_location=root,
                                      )
                    progress += 1
                    dpg.set_value('progress', progress/file_amount)
                    dpg.set_value('progress_text', f'{progress}/{file_amount}')


dpg.add_file_dialog(
    directory_selector=True, show=False, callback=callback, tag="file_dialog_id",
    cancel_callback=cancel_callback)


with dpg.window(label="", tag='main_window'):
    dpg.add_button(label="Directory Selector", callback=lambda: dpg.show_item("file_dialog_id"))
    dpg.add_input_text(default_value='./', tag='folder_path')

    dpg.add_separator()

    dpg.add_input_int(label='iterations', tag='iterations')
    dpg.add_input_text(label='input extention', default_value='png', tag='input_extention')
    dpg.add_input_text(label='output extention', default_value='jpg', tag='output_extention')

    dpg.add_button(label='Generate Mipmaps', callback=crawl)

    dpg.add_separator()
    with dpg.group(horizontal=True):
        dpg.add_progress_bar(tag='progress', default_value=0)
        dpg.add_text(tag='progress_text', default_value='0/0')

    dpg.add_separator()
    with dpg.tree_node(tag='tree_view'):
        pass

dpg.create_viewport(title='Mipmap generator', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('main_window', True)
dpg.start_dearpygui()
dpg.destroy_context()
