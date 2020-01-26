% Stephen Weinreich
% Murmann Mixed-Signal Group, Stanford University
% Jan 2020

%% Create some data
x = linspace(0,2,200);
sq = -sign(x-1);
sq1 = 4/pi*1/1*sin(1*pi*x);
sq3 = sq1 + 4/pi*1/3*sin(3*pi*x);
sq5 = sq3 + 4/pi*1/5*sin(5*pi*x);

%% Save to CSV file
% Create cell array to hold our data. Set it to the maximum size you might
% want: in this case, I need 5 columns (x, sq, sq1, sq3, sq5) and am 
% allowing for up to 1000 data points.
data = cell(1000, 5);
% Set the header row
data(1,:) = {'x', 'sq', 'sq1', 'sq3', 'sq5'};
% Set the data
data(2:1+length(x),1) = num2cell(x);
data(2:1+length(sq),2) = num2cell(sq);
data(2:1+length(sq1),3) = num2cell(sq1);
data(2:1+length(sq3),4) = num2cell(sq3);
data(2:1+length(sq5),5) = num2cell(sq5);
% Get rid of extra empty rows (in this case, it reduces to 201 rows)
data=data(~all(cellfun(@isempty,data),2),:);
% Save to CSV file
T = cell2table(data(2:end,:),'VariableNames',data(1,:));
writetable(T,'cadwiki_example.csv')