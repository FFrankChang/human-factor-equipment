%% Initialization
clear all 
close all

%% Streaming Definitions

% Definition of the Streaming Parameters (change these to reflect your own settings)
port = 9763;        % port number as defined in the Network Streamer in MVN
timeout = 3000;     % maximum time to wait to receive a package in miliseconds
jointIndex = 16;    % Segment ID (for example RightKnee = 16)

% Parameters to run the code
lastReceived = NaN; 
counter = 1;
maxPacketLength = 2000;

%% Create a Feedback color graph
hfig = figure('Name',(['Feedback on the angle of joint ' num2str(jointIndex)]));
hold all;
rect = rectangle('Position',[1 2 5 6]);
cmap = colormap([1 1 0; 1 0.75 0; 1 0.5 0; 1 0.25 0; 1 0 0]);
rect.FaceColor = [1 1 1];
set(gca,'visible','off')
title(['Feedback on the angle of joint ' num2str(jointIndex)])
ButtonHandle = uicontrol('Parent',hfig,'Style', 'PushButton','String', 'Stop Loop','Callback', 'delete(gcbf)');

newPacketFlag = 1;

%% Streaming Loop
while 1
    if ~ishandle(ButtonHandle)
        disp('Loop stopped by user');
        break;
    end
    
    try
        % Kevin Bartlett (2020). A simple UDP communications application (https://www.mathworks.com/matlabcentral/fileexchange/24525-a-simple-udp-communications-application), MATLAB Central File Exchange. Retrieved May 1, 2020.
        message = judp('receive', port, 8*maxPacketLength, timeout);
    catch e
        disp(e.message)
        continue
    end
    
    % conversion of the UDP messages into parameters
    [Ids, angles, lastReceived, timeCode, newPacketFlag] = parse_jointangle_packet(message, lastReceived);
    
    if newPacketFlag ~= 0
        
        % conversion from quaternions to euler angle
        yAngle = angles(jointIndex,3);
        
        condition = abs(round(yAngle*5/90));
        
        if condition > 5
            rect.FaceColor = cmap(5,:);
        elseif condition < 1
            rect.FaceColor = cmap(1,:);
        else
            rect.FaceColor = cmap(condition,:);
        end
    end
    drawnow
    
end
