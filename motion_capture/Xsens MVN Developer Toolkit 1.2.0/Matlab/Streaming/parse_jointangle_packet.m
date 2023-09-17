function [Ids,angles,sampleCounter,timeCode,newPacketFlag] = parse_jointangle_packet(message,lastReceived)

%% Parse the headers
messageId = char(message(1:6))';                                     % ID string
messageType = hex2dec(char(message(5:6))');                          % Message Type
sampleCounter = double(typecast(flipud(message(7:10)),'uint32'))+1;  % Counts number of sent samples
datagramCounter = dec2bin(typecast(message(11),'uint8'));            % Counts number of sent datagrams
numJoints = double(typecast(message(12),'uint8'));                   % number of segments in the avatar
timeCode = double(typecast(flipud(message(13:16)),'uint32'));        % time code of the sample

% Parameters to run the code
packetSize = 20; 

%% Analyze if new packages have been received
Ids = [];
angles = [];
if sampleCounter == lastReceived
    newPacketFlag = 0;
    return
else
    newPacketFlag = 1;
end


%% Conversion to euler angles
if messageType == 32 
    
    % Initialization of position and orientation variables
    Ids = zeros(numJoints, 2);
    angles = zeros(numJoints, 3);
    
    for s = 1:numJoints
        offset = (s-1)*packetSize;
        Ids(s,1) = double(typecast(flipud(message(offset + [25:28])),'uint32'));
        Ids(s,2) = double(typecast(flipud(message(offset + 4 + [25:28])),'uint32'));
        angles(s,1) = double(typecast(flipud(message(offset + 8 + [25:28])),'single'));
        angles(s,2) = double(typecast(flipud(message(offset + 12 + [25:28])),'single'));
        angles(s,3) = double(typecast(flipud(message(offset + 16 + [25:28])),'single'));
    end
    
else
    newPacketFlag = 0;
    return
end


