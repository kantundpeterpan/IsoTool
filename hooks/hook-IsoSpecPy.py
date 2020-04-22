import platform

if platform.system() == 'Linux':
	binaries = [('/home/kantundpeterpan/anaconda3/envs/ms/lib/python3.8/site-packages/IsoSpecCppPy.cpython-38-x86_64-linux-gnu.so', 'IsoSpecPy')]
if platform.system() == 'Windows':
	binaries = [('C:\\ProgramData\\Miniconda3\\Lib\\site-packages\\IsoSpecPy\\prebuilt-libIsoSpec++2.0.1-x32.dll', 'IsoSpecPy')]
