%% Copyright (C) Smart Eye AB 2002-2018
%% THE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
%% ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
%% THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
%% PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
%% OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
%% OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
%% TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
%% WITH THE CODE OR THE USE OR OTHER DEALINGS IN THE CODE.
%%----------------------------------------------------------------------------%%
%% Smart Eye AB
%% Första långgatan 28 B,
%% 413 27 Göteborg, Sweden
%% Contact: support@smarteye.se
%%
%% You are free to modify and use this code together with
%% your purchased Smart Eye system.
%%
%% You MAY NOT distribute this code (modified or unmodified)
%% without prior written consent from Smart Eye AB.
%%----------------------------------------------------------------------------%%


function saccadeAndFixationAnalysis(leftGazeDirection,leftGazeDirectionQ,rightGazeDirection,rightGazeDirectionQ,timeStamps)

% tweaking parameters
lowestQ = 0.10; % samples with lower gaze quality won't be used
filterLength = 13; % median over +/-6 samples forward/backward window (200ms @ 60Hz)
saccadeDetectThreshold = 100; % minimum deg/s for saccade detection
saccadeExtentThreshold = 25; % minimum deg/s for saccade extent
outlierFactor = 1.8; % samples outside a circle of mean error times this factor will be pruned
minimumSamples = 10; % minimum number of samples (sum of eyes)
colours = ['r' 'g' 'b' 'c' 'm' 'y' 'k'];
stdAxis = [-50 50 -20 40];

%all
startIdx = 1;
stopIdx = size(timeStamps,2);

sequence = startIdx:stopIdx;
leftGazeDirection = leftGazeDirection(:,sequence);
leftGazeDirectionQ = leftGazeDirectionQ(:,sequence);
rightGazeDirection = rightGazeDirection(:,sequence);
rightGazeDirectionQ = rightGazeDirectionQ(:,sequence);
timeStamps = timeStamps(:,sequence);

% number of samples
nSamples = size(timeStamps,2);

% relative time in seconds
timeSec = (double(timeStamps)-double(timeStamps(1))) * 100e-9;

% convert gaze to spherical coordinates in degrees
LGaze = toPolarDeg(leftGazeDirection);
RGaze = toPolarDeg(rightGazeDirection);

% threshold on gaze quality
LGazeQ = removeLowQ(LGaze,leftGazeDirectionQ,lowestQ);
RGazeQ = removeLowQ(RGaze,rightGazeDirectionQ,lowestQ);

% apply median filter
LGazeQM = medianFilt(LGazeQ, filterLength);
RGazeQM = medianFilt(RGazeQ, filterLength);

% calculate eye velocities (H,V,combined)
LVelocity = rotationVelocity(LGazeQM,timeSec);
RVelocity = rotationVelocity(RGazeQM,timeSec);

% calculate an "average" velocity from available data in both eyes
LNaN = (LVelocity == NaN);
RNaN = (RVelocity == NaN);
CLVelocity = LVelocity;
CRVelocity = RVelocity;
CLVelocity(LNaN) = RVelocity(LNaN);
CRVelocity(RNaN) = LVelocity(RNaN);
CVelocity = (CLVelocity + CRVelocity) .* 0.5;

% plot eye velocities
figure
subplot(3,1,1);
plot(timeSec',LVelocity');
subplot(3,1,2);
plot(timeSec',RVelocity');
subplot(3,1,3);
plot(timeSec',CVelocity');

% build a histogram of velocities
velocityHistogramMax = 300; % max deg/second
velocityHistogramBinSize = 2.5; % deg/second
velocityHistogramBins = ceil(velocityHistogramMax/velocityHistogramBinSize)+1;
velocityHistogram = zeros(velocityHistogramBins,1);
binIndex = floor(CVelocity(3,:)/velocityHistogramBinSize)+1;
for i = 1:nSamples
    index = binIndex(i);
    if index<=velocityHistogramBins
        velocityHistogram(index) = velocityHistogram(index)+1;
    end
end

% plot velocity histogram
figure;
bar((0:(velocityHistogramBins-1))*velocityHistogramBinSize,velocityHistogram);

% initial detection ranges
saccadeDetect = CVelocity(3,:) > saccadeDetectThreshold;
saccadeExtent = CVelocity(3,:) > saccadeExtentThreshold;

% extend detections to the right
isSaccade = saccadeDetect;
for i = 2:nSamples
    if (isSaccade(i-1) && saccadeExtent(i))
        isSaccade(i) = 1;
    end
end
% extend detections to the left
for i = nSamples+1-(2:nSamples)
    if (isSaccade(i+1) && saccadeExtent(i))
        isSaccade(i) = 1;
    end
end

% enumerate fixations
nFixations = 0;
fixationNr = zeros(1,nSamples);
fixationFirstIdx = [];
fixationLastIdx  = [];
for i = 1:(nSamples-1)
    if (isSaccade(i) && not(isSaccade(i+1)))
        nFixations = nFixations + 1;
        fixationFirstIdx(nFixations) = i+1;
    elseif (not(isSaccade(i)) && isSaccade(i+1) && nFixations>0)
        fixationLastIdx(nFixations) = i;
    end
    if (not(isSaccade(i)))
        fixationNr(i) = nFixations;
    end
end
if size(fixationLastIdx,2) < nFixations
    fixationLastIdx(nFixations) = nSamples;
end

% determine fixation data
fixationStartTime = zeros(1,nFixations);
fixationEndTime = zeros(1,nFixations);
fixationDuration = zeros(1,nFixations);
fixationPointL = zeros(2,nFixations);
fixationPointLn = zeros(1,nFixations);
fixationPointLd = zeros(1,nFixations);
fixationPointR = zeros(2,nFixations);
fixationPointRn = zeros(1,nFixations);
fixationPointRd = zeros(1,nFixations);
figure;
hold;
for i = 1:nFixations
    fixationStartTime(i) = timeSec(fixationFirstIdx(i));
    fixationEndTime(i) = timeSec(fixationLastIdx(i));
    fixationDuration(i) = fixationEndTime(i) - fixationStartTime(i) + 0.016; % well, almost..

    samples = fixationFirstIdx(i):fixationLastIdx(i);
    Lsamples = LGaze(:,samples);
    Rsamples = RGaze(:,samples);
    
    % prune useless samples
    Lsamples = Lsamples(:,Lsamples(1,:) ~= NaN);
    Rsamples = Rsamples(:,Rsamples(1,:) ~= NaN);

    % plot raw data
    scatter(Lsamples(1,:),Lsamples(2,:),1,'r');
    scatter(Rsamples(1,:),Rsamples(2,:),1,'g');
    
    % determine cluster properties (center, radius)
    while not(isempty(Lsamples))
        fixationPointL(:,i) = mean(Lsamples,2);
        diff = [ Lsamples(1,:)-fixationPointL(1,i); Lsamples(2,:)-fixationPointL(2,i) ];
        dist = sqrt(sum(diff.*diff,1));
        fixationPointLd(i) = mean(dist);

        % prune outliers
        isOutlier = dist > (fixationPointLd(i)*outlierFactor);
        if not(any(isOutlier))
            break;
        end
        Lsamples = Lsamples(:,not(isOutlier));
    end
    fixationPointLn(i) = size(Lsamples,2);
    
    while not(isempty(Rsamples))
        fixationPointR(:,i) = mean(Rsamples,2);
        diff = [ Rsamples(1,:)-fixationPointR(1,i); Rsamples(2,:)-fixationPointR(2,i) ];
        dist = sqrt(sum(diff.*diff,1));
        fixationPointRd(i) = mean(dist);

        % prune outliers
        isOutlier = dist > (fixationPointRd(i)*outlierFactor);
        if not(any(isOutlier))
            break;
        end
        Rsamples = Rsamples(:,not(isOutlier));
    end
    fixationPointRn(i) = size(Rsamples,2);

    % plot moving average for inlier samples (this is just eye-candy and is not being used for real..)
    windowSize = 5;
    Lma = filter(ones(1,windowSize)/windowSize,1,Lsamples')';
    Rma = filter(ones(1,windowSize)/windowSize,1,Rsamples')';
    Lma = Lma(:,windowSize:size(Lma,2));
    Rma = Rma(:,windowSize:size(Rma,2));
    scatter(Lma(1,:),Lma(2,:),4,'r','filled');
    scatter(Rma(1,:),Rma(2,:),4,'g','filled');
end
fixationPointC = (fixationPointL.*[fixationPointLn;fixationPointLn] + fixationPointR.*[fixationPointRn;fixationPointRn])./([1;1]*(fixationPointLn+fixationPointRn));
fixationPointCn = fixationPointLn+fixationPointRn;
axis equal;
axis(stdAxis);

%prune fixations with less than <threshold> samples
enoughSamples = fixationPointCn > minimumSamples;
nFixations = sum(enoughSamples);
fixationFirstIdx = fixationFirstIdx(:,enoughSamples);
fixationLastIdx = fixationLastIdx(:,enoughSamples);
fixationStartTime = fixationStartTime(:,enoughSamples);
fixationEndTime = fixationEndTime(:,enoughSamples);
fixationDuration = fixationDuration(:,enoughSamples);
fixationPointL = fixationPointL(:,enoughSamples);
fixationPointLn = fixationPointLn(:,enoughSamples);
fixationPointLd = fixationPointLd(:,enoughSamples);
fixationPointR = fixationPointR(:,enoughSamples);
fixationPointRn = fixationPointRn(:,enoughSamples);
fixationPointRd = fixationPointRd(:,enoughSamples);
fixationPointC = fixationPointC(:,enoughSamples);
fixationPointCn = fixationPointCn(:,enoughSamples);

% plot 2D raw data
figure;
hold;
plot(LGaze(1,:),LGaze(2,:),'r+');
plot(RGaze(1,:),RGaze(2,:),'g+');
axis equal;
axis(stdAxis);

% plot 2D fixations
figure;
hold;
%scatter((LGazeQM(1,:)+RGazeQM(1,:))*0.5,(LGazeQM(2,:)+RGazeQM(2,:))*0.5,4,'b');
scatter(fixationPointC(1,:),fixationPointC(2,:),fixationDuration*30,'k','filled');
%scatter(fixationPointC(1,:),fixationPointC(2,:),fixationDuration.*sqrt(fixationDuration)*20,'k','filled');
plot(fixationPointC(1,:),fixationPointC(2,:),'k-');
axis equal;
axis(stdAxis);

figure;
hold;
scatter3(fixationPointL(1,:),fixationPointL(2,:),fixationStartTime,fixationDuration*20,'r','filled');
scatter3(fixationPointR(1,:),fixationPointR(2,:),fixationStartTime,fixationDuration*20,'g','filled');
scatter3(fixationPointC(1,:),fixationPointC(2,:),fixationStartTime,fixationDuration*20,'b','filled');
plot3(fixationPointC(1,:),fixationPointC(2,:),fixationStartTime,'b-');

% 3D plot of 2D gaze vs time
figure;
subplot(2,1,1);
hold;
for i = 1:nFixations
    duration = fixationFirstIdx(i):fixationLastIdx(i);
    plot3(timeSec(duration)',LGaze(1,duration)',LGaze(2,duration)','.c');
end
plot3(timeSec(isSaccade)',LGaze(1,isSaccade)',LGaze(2,isSaccade)','.r');
subplot(2,1,2);
hold;
for i = 1:nFixations
    duration = fixationFirstIdx(i):fixationLastIdx(i);
    plot3(timeSec(duration)',RGaze(1,duration)',RGaze(2,duration)','.c');
end
plot3(timeSec(isSaccade)',RGaze(1,isSaccade)',RGaze(2,isSaccade)','.r');

figure;
subplot(2,1,1);
plot(LGaze(1,:),LGaze(2,:),'.',LGaze(1,isSaccade),LGaze(2,isSaccade),'+');
axis equal;
axis(stdAxis);
subplot(2,1,2);
plot(RGaze(1,:),RGaze(2,:),'.',RGaze(1,isSaccade),RGaze(2,isSaccade),'+');
axis equal;
axis(stdAxis);

end

%run e.g. with: saccadeAndFixationAnalysis(LeftGazeDirection,LeftGazeDirectionQ,RightGazeDirection,RightGazeDirectionQ,TimeStamp);
