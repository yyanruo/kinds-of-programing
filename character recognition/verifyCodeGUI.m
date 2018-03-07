function varargout = verifyCodeGUI(varargin)
% VERIFYCODEGUI MATLAB code for verifyCodeGUI.fig
%      VERIFYCODEGUI, by itself, creates a new VERIFYCODEGUI or raises the existing
%      singleton*.
%
%      H = VERIFYCODEGUI returns the handle to a new VERIFYCODEGUI or the handle to
%      the existing singleton*.
%
%      VERIFYCODEGUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in VERIFYCODEGUI.M with the given input arguments.
%
%      VERIFYCODEGUI('Property','Value',...) creates a new VERIFYCODEGUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before verifyCodeGUI_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to verifyCodeGUI_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help verifyCodeGUI

% Last Modified by GUIDE v2.5 30-Apr-2017 11:28:28

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @verifyCodeGUI_OpeningFcn, ...
                   'gui_OutputFcn',  @verifyCodeGUI_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before verifyCodeGUI is made visible.
function verifyCodeGUI_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to verifyCodeGUI (see VARARGIN)

% Choose default command line output for verifyCodeGUI
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

set(handles.text2,'visible','off');
set(handles.text3,'visible','off');
ha=axes('units','normalized','position',[0 0 1 1]);
uistack(ha,'top');
II=imread('background.jpg');
image(II);
colormap gray
set(ha,'handlevisibility','off','visible','off');

% UIWAIT makes verifyCodeGUI wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = verifyCodeGUI_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on selection change in listbox1.
function listbox1_Callback(hObject, eventdata, handles)
% hObject    handle to listbox1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns listbox1 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from listbox1
selectedIndex = get(hObject,'Value'); 
listBoxString = get(hObject,'String');
imgName = listBoxString(selectedIndex,:);
folder = handles.folder;
fName = strcat(folder,'/',imgName);
I = imread(fName);
axes(handles.axes1);
imshow(I);

codeRecog = handles.codeRecog;
codeStr = codeRecog(selectedIndex,:);
set(handles.text2,'visible','on');
set(handles.text3,'visible','on');
set(handles.text2,'String',codeStr);


% --- Executes during object creation, after setting all properties.
function listbox1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to listbox1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: listbox controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

folder = uigetdir;
filePattern = fullfile(folder, '*.bmp');
bmpFiles = dir(filePattern);
nameMat = cat(1,bmpFiles.name);
set(handles.listbox1, 'string', nameMat);
[codeRecog,meanErrorRate] = verifyCodeRecognition(folder,bmpFiles);
meanErrStr = sprintf('MER:  %4.2f\n',meanErrorRate);
set(handles.text3,'String',meanErrStr);
% Calculate the mean error rate
handles.codeRecog = codeRecog;
handles.folder = folder;
guidata(hObject,handles);


% --- Executes during object creation, after setting all properties.
function axes1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to axes1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: place code in OpeningFcn to populate axes1
set(hObject,'visible','off');
set(get(hObject,'children'),'visible','off') %hide the current axes contents
