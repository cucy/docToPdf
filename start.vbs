Set shell = Wscript.createobject("wscript.shell")

a = shell.run ("bin\startweb1.bat",0)
a = shell.run ("bin\startweb2.bat",0)
a = shell.run ("bin\startwork.bat",0)
a = shell.run ("nginx\start.bat",0)