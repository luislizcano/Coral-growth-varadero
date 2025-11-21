
% dbRDA

% Import the data:
growth         = importdata('coral_growth.xlsx');
lum            = importdata('coral_lumn_yr.xlsx');
env            = importdata('env_yr.xlsx');

envar       = env.data(36:62,3:5);  % ENV Variables (m3/s,°C,SOI,AMO)
envar_txt   = env.textdata(1,3:5);  % Variable LABELS
years       = env.data(36:62,1);  % ENV Variables (m3/s,°C,SOI,AMO)

%% VAR2
den2        = growth.data(70:96,2);        % Density
ext2        = growth.data(70:96,3);        % Extension
cal2        = growth.data(70:96,4);        % Calcification
lum2        = lum.data(70:96,2);           % Luminescence 1980-1954
%% VAR3
den3        = growth.data(135:161,2);        % Density
ext3        = growth.data(135:161,3);        % Extension
cal3        = growth.data(135:161,4);        % Calcification
lum3        = lum.data(132:158,2);           % Luminescence
%% VAR4
den4        = growth.data(209:235,2);        % Density
ext4        = growth.data(209:235,3);        % Extension
cal4        = growth.data(209:235,4);        % Calcification
lum4        = lum.data(197:223,2);           % Luminescence

bio         = [den2,den3,den4,ext2,ext3,ext4,cal2,cal3,cal4,lum2,lum3,lum4];
bio_labels  = {'Den2','Den3','Den4','Ext2','Ext3','Ext4','Cal2','Cal3','Cal4','Lum2','Lum3','Lum4'};


%% Standardize the RESPONSE data:
stda_env    = f_stnd(envar);
stda_bio    = f_stnd(bio);

% Create a Bray-Curtis dissimilarity matrix:
dis         = f_dis(stda_bio,'euc');

% Perform Distance-based RDA:
rdaDB       = f_rdaDB(dis,size(stda_bio,2),stda_env,[],1000,1);


% Create plot:
wascores    = 1;        % <-- Use weighted species scores
scale       = 2;        % <-- [scaleX]
offset      = 0.1;
fmt         = 'none';
iter        = 0;

% Create RDA plot displaying all biplot vectors:
f_rdaPlot(rdaDB,bio,wascores,scale,offset,bio_labels,envar_txt,fmt,iter,years);
