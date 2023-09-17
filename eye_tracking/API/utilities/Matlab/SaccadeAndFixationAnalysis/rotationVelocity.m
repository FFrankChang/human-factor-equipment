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


function vel = rotationVelocity(gazeDirection,timeSec)
% returns [H;V;D] components D=sqrt(H^2+V^2)
length = size(gazeDirection,2);

deltaDir = gazeDirection(:,3:length) - gazeDirection(:,1:(length-2));
deltaTime = timeSec(:,3:length) - timeSec(:,1:(length-2));

vel = [
    0 deltaDir(1,:)./deltaTime 0;
    0 deltaDir(2,:)./deltaTime 0;
    0 sqrt(deltaDir(1,:).^2 + deltaDir(2,:).^2)./deltaTime 0
    ];
    
end