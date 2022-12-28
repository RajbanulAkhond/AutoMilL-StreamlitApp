% Get the Current Directory
%directory = pwd();
directory = 'E:\ML Project\Project Phases\PHASE II (Data)\Data_cleaning_profiling\EAF_data_four_months';
% FILE SELECTION MODULE
% file_list = uigetfile('*.xls', 'Grab the files you want to process', 'MultiSelect', 'on');
% if iscell(file_list) == 0
%     file_list = {file_list};
% end

%FULLY ATOMATED FILE SELECTION
fileinfo = dir('..\EAF_data_four_months\*.xls');
file_list = sort({fileinfo.name});
excel = actxserver('Excel.Application');  %invisible by default
excel.DisplayAlerts = false; 

%EAF DATA SPECIFIC
data1_start_row = 6;
data1_cols = [1 14 23 26 28 32 34 36 38 41 43 45];
data2_cols = [4 6 8 10 14 16 21 24 27 30 33 35 37 39 42];
data1 = [];
data2 =  [];
total_data = 0;


%Loop through all files
for i = 1:length(file_list)
   
    tmp_data1 = [];
    tmp_data2 =  [];
   
    filename = append(directory, '\', file_list{i});
    
    workbook = excel.Workbooks.Open(filename);
    worksheet = workbook.Sheets.Item(1);  %no need for get
    cmp_range = worksheet.Range('A1:A100').value;  %no need to go through activesheet, or get
    idx = find(strcmp(cmp_range,'GENERAL'),1,'last');

%     [~,~,data_in] = xlsread(filename);
    
    data_in_file = idx - 10;
    total_data = total_data + data_in_file;
    data1_end_row = idx - 5;
    data2_start_row = data1_end_row + 8;
    data2_end_row = data2_start_row + data_in_file - 1;
    
    range = sprintf('A1:AS%i',data2_end_row);
    data_in = worksheet.Range(range).value;
    
    for j = 1:12
       tmp_data1 = [tmp_data1,data_in(data1_start_row:data1_end_row,data1_cols(j))]; 
    end
    data1 = [data1;tmp_data1];
    for j = 1:15
       tmp_data2 = [tmp_data2, data_in(data2_start_row:data2_end_row,data2_cols(j))]; 
    end
    data2 = [data2;tmp_data2];
end

raw_data = [data1,data2];
xlswrite('raw_data.xlsx',raw_data);
 
