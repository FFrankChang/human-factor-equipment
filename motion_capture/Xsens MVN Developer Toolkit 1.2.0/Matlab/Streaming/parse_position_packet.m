function [pos,ori,sampleCounter,timeCode,newPacketFlag] = parse_position_packet(message,lastReceived)

%% Parse the headers
messageId = char(message(1:6))';                                     % ID string
messageType = hex2dec(char(message(5:6))');                          % Message Type
sampleCounter = double(typecast(flipud(message(7:10)),'uint32'))+1;  % Counts number of sent samples
datagramCounter = dec2bin(typecast(message(11),'uint8'));            % Counts number of sent datagrams
numSegments = double(typecast(message(12),'uint8'));                 % number of segments in the avatar
timeCode = double(typecast(flipud(message(13:16)),'uint32'));        % time code of the sample

% Parameters to run the code
packetSize = 32; 

%% Analyze if new packages have been received
pos = [];
ori = [];
if sampleCounter == lastReceived
    newPacketFlag = 0;
    return
else
    newPacketFlag = 1;
end


%% Conversion to position and orientation parameters
if messageType == 2 
    
    % Initialization of position and orientation variables
    pos = zeros(numSegments, 3);
    ori = zeros(numSegments, 4);
    
    for s = 1:numSegments
        offset = (s-1)*packetSize;
        segmentId = double(typecast(flipud(message(offset + [25:28])),'uint32'));
        pos(s,1) = double(typecast(flipud(message(offset + 4 + [25:28])),'single'));
        pos(s,2) = double(typecast(flipud(message(offset + 8 + [25:28])),'single'));
        pos(s,3) = double(typecast(flipud(message(offset + 12 + [25:28])),'single'));
        ori(s,1) = double(typecast(flipud(message(offset + 16 + [25:28])),'single'));
        ori(s,2) = double(typecast(flipud(message(offset + 20 + [25:28])),'single'));
        ori(s,3) = double(typecast(flipud(message(offset + 24 + [25:28])),'single'));
        ori(s,4) = double(typecast(flipud(message(offset + 28 + [25:28])),'single'));
    end
    
else
    newPacketFlag = 0;
    return
end


