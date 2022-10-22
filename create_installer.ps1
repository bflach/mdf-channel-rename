# Assemble output name
$git_sha = git rev-parse --short HEAD
$Filename = "mdf-channel-rename_" +  $git_sha

# Configure pyinstaller - create single file, use icon
pyinstaller -F -i gui_rename_icon_157599.ico -n $Filename mdf_channel_rename.py
