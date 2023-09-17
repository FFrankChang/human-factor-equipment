%% Initialization
clear all
close all

%% Streaming Definitions

% Definition of the Streaming Parameters (change these to reflect your own settings)
port = 9763;        % port number as defined in the Network Streamer in MVN
timeout = 3000;     % maximum time to wait to receive a package in miliseconds
segmentId = 1;      % Segment ID (for example Pelvis is 1)

% Parameters to run the code
lastReceived = NaN;
counter = 1;
maxPacketLength = 2000;

%% Create Figure to plot position
hfig = figure;
xlabel('position in x-direction (m)')
ylabel('position in y-direction (m)')
title(['Position in space segment ' num2str(segmentId)])
ButtonHandle = uicontrol('Parent',hfig,'Style', 'PushButton','String', 'Stop Loop','Callback', 'delete(gcbf)');
hold all

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
    [pos, ori, lastReceived, timeCode, newPacketFlag] = parse_position_packet(message, lastReceived);
    
    % Skip unknown packets
    if newPacketFlag ~=0
        
        % Plot of segment position
        plot(pos(segmentId,1),pos(segmentId,2),'k*');
    end
    drawnow    
    
end


