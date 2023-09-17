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


function polarGaze = toPolarDeg(aGazeDirection)
% convert 3D gaze direction to polar coordinates in degrees
% forward,upward = -Z,Y
polarGaze = [atan2(aGazeDirection(1,:),-aGazeDirection(3,:));asin(aGazeDirection(2,:))]*180/pi;

end