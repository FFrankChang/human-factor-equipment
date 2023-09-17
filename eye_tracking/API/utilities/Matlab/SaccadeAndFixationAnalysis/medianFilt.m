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


function vecOut = medianFilt(vecIn, length)
% apply a median filter of size length, NaN doesn't count
firstOfs = -floor(length/2);
lastOfs = firstOfs + length -1;
vecOut=NaN(size(vecIn));
for i = 1:size(vecIn,2)
    first = max(1,i+firstOfs);
    last = min(size(vecIn,2),i+lastOfs);
    tmp = vecIn(:,first:last);
    sel = isfinite(tmp(1,:)); % assuming NaN same for all rows
    tmp = tmp(:,sel);
    if not(isempty(tmp))
        vecOut(:,i) = median(tmp,2);
    end
end

end