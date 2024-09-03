dir=$PWD
dart_path=$PWD
dart_path+="/dart/models.py"
banner_path=$PWD
banner_path+="/gui_interface/banner.png"

pyinstaller ../src/main.py --add-data "/Users/neo/Documents/10ML/directory_traversing/src/dart/models.py:dart" --hidden-import=timm.models.layers.attention_pool2d --add-data "/Users/neo/Documents/10ML/directory_traversing/src/gui_interface/banner.png:gui_interface" --name "DART interface gh-script-t1" --windowed