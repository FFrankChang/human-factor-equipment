// Copyright (C) Smart Eye AB 2002-2018
// THE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
// ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
// THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
// PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
// OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
// OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
// TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
// WITH THE CODE OR THE USE OR OTHER DEALINGS IN THE CODE.
//----------------------------------------------------------------------------//
// Smart Eye AB
// Första långgatan 28 B,
// 413 27 Göteborg, Sweden
// Contact: support@smarteye.se
//
// You are free to modify and use this code together with
// your purchased Smart Eye system.
//
// You MAY NOT distribute this code (modified or unmodified)
// without prior written consent from Smart Eye AB.
//----------------------------------------------------------------------------//


/////////////////////////////////////////////////////////////
// this file contains functions to load smart eye log data in to matrices and to retrieve columns of values from said matrices
//
// used to load smart eye data into a matrix
// 
// in: 
// filename - tab separated smart eye logfile
// out:
// data - matrix of logdata
// headers - vector of column names

function [data, headers] = getDataFromFile(filename)
  [data,header] = fscanfMat(filename);
  
  headers = strsplit(header,strindex(header,ascii(9))); // split where there is a tab
  headers = headers';
endfunction

// used to load smart eye data into a matrix
// pops a dialog box for the logfile
//
// out:
// data - matrix of logdata
// headers - vector of column names

function [data, headers] = getData()
  SEPpath=xgetfile(title ='Smart Eye Pro Logfile');
  [data,headers] = getDataFromFile(SEPpath);
endfunction

// used to get the column vector for the specified name
// 
// in: 
// data - matrix of smart eye data
// headers - the vector of column names
// name - the name of the column
// out:
// col - the column for the value name

function [col] = getColumnByName(data,header,name)

[r,v] = grep(header,name) ;

col=[];
for i=r
  if ( strsubst(sci2exp(header(i)),ascii(9),'')  == sci2exp(name) )
    col = data(:,i);
  end;
end;

if (col == [])
  error ("column: " + name + " is empty!");
end;

endfunction;

// used to get the 3 columns for each component of a vector or point value
// 
// 
// in: 
// data - matrix of smart eye data
// headers - the vector of column names
// name - the name of the column 
// out: 
// cols - the 3 components of the specified value as a column vector of [x,y,z] values

function [cols] = getXYZColumnsByName(data,header,name) 

[cols] = [getColumnByName(data,header,name+".x"),getColumnByName(data,header,name+".y"),getColumnByName(data,header,name+".z")];

endfunction;
