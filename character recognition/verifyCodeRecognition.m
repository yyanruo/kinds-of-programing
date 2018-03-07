% verifyCode recognition
function [codeRecog,meanErrorRate] = verifyCodeRecognition(openPath,img_path_list)
count = 4; % 4 characters in the image
%savePath = uigetdir('D:\','Which folder to save results');
%openPath =  uigetdir('D:\Nutstore\Education\Courses\Computer Vision\project1\Project1','Which folder to save results');
%img_path_list = dir(strcat(openPath,'\','*.bmp'));

errorCount = 0;
codeRecog = [];
numImg = length(img_path_list);
for k=1:numImg
    
    FileName = img_path_list(k).name;
    fName = strcat(openPath,'/',FileName);

    rgbIm = imread(fName);%read the original image
    Ibw = rgb_2_bw(rgbIm);
    Icomp = imcomplement(Ibw); % white to black
    centralImg = imEraseBound(Icomp,3); % 2nd argument is the boundary width
    % split the characters
    [splittedImgs,isSucceed] = split_img(centralImg,count);
    if isSucceed
        % recognition
        str = '';% to save recognized result
        for i = 1:count
            str(i) = single_char_recognize(splittedImgs{i,1});    
            if ~strcmp(FileName(i),str(i))
                errorCount = errorCount + 1;
            end
        end
        codeRecog = cat(1,codeRecog,str);
        %disp(str);
        
    end
    
end
meanErrorRate = errorCount/(numImg*count);

end

function c = single_char_recognize(imgMat)
    % single char recognize by neural network classifier
    input = reshape(imgMat,[numel(imgMat),1]);
    res = classifier(input);
    [~,classIdx] = max(res);
    c = classIdx2char(classIdx); 
    
end

function [splittedImgs,isSucceed] = split_img(I,count)
    % split characters in the image by connected components, since no
    % overlap in the image
    width = 5;
    splittedImgs = cell(count,1);
    L = bwlabel(I); % label the connected component with 8-connectivity
    for i = 1:count
    if max(L(:)) ~= count
        isSucceed = 0; % not successful
        disp('Splitting not successful!\n');
    else
        isSucceed = 1;
        Itemp = zeros(size(I));
        idx = find(L == i);
        Itemp(idx) = 1;
        % Crop the image and resize as 32x32
        P = regionprops(Itemp,'BoundingBox');
        P.BoundingBox = P.BoundingBox + [-width/2,-width/2,width,width];
        Icrop = imcrop(Itemp,P.BoundingBox);
        Iresize = imresize(Icrop,[32,32]);% resize the image to the same size
        splittedImgs{i,1} = Iresize;
    end
    end
       
end

function outputImg = imEraseBound(I,boundaryWidth)
% eliminate the thin boundary around the image
    outputImg = I;
    outputImg(1:boundaryWidth,:) = 0;
    outputImg(end-boundaryWidth:end,:) = 0;
    outputImg(:,1:boundaryWidth) = 0;
    outputImg(:,end-boundaryWidth:end) = 0;
end


function aTarget = char2ClassIdx(c)
    % convert 0-9 and alphabeta to corresponding class index for training
    % in neural network
    numClass = 36; %
    aTarget = zeros(numClass,1);
    ascii = abs(c); % get the ascii code
    if (ascii >= 48) && (ascii <= 57) % 0-9
        idx = ascii - 47; % the index of '0' is 1 and so on
    elseif (ascii >= 97) && (ascii <= 122) % a-z
        idx = ascii - 86; % the index of 'a' is 11
    elseif (ascii >= 65) && (ascii <= 90)
        idx = ascii - 54; % the index of 'A' is 11
    else
        error('Unrecognizable Character\n');
    end
    aTarget(idx) = 1;
end

function c = classIdx2char(classIdx)
    % convert the classIdx to corresponding index
    if classIdx <= 10
        c = num2str(classIdx - 1);
    else
        c = char(classIdx + 54);
    end
end

function BW = rgb_2_bw(rgbIm)
thre = 180; % for foreground, the lowest channel value should below this threshold
BW = zeros(size(rgbIm,1),size(rgbIm,2));
for row = 1:size(rgbIm,1)
    for col = 1:size(rgbIm,2)
        minValue = min(rgbIm(row,col,:));
        if minValue > thre
            BW(row,col) = 1;
        end
    end
end
end

