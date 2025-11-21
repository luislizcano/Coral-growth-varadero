
exec('D:/Box/Box Sync/luislizcanos/USF/Courses/Data Analysis Methods/Labs/Lab_4/fs_spect.sce');
exec('D:/Box/Box Sync/luislizcanos/USF/Courses/Data Analysis Methods/Labs/Lab_4/fourierseries.sce');
exec('D:/Box/Box Sync/luislizcanos/USF/Courses/Data Analysis Methods/Labs/Lab_2/leastsq2.sce');
exec('D:/Box/Box Sync/luislizcanos/USF/Courses/Data Analysis Methods/Labs/Lab_4/cross_spect.sce');
exec('D:/Box/Box Sync/luislizcanos/USF/Courses/Data Analysis Methods/Labs/Lab_1/replace_nodata.sce'); 


[fd,SST,Sheetnames,Sheetpos] = xls_open('E:/Google Drive/Articulos/Pendientes/Varadero growth rates/data/coral_growth_monthly.xls')
//Read first data sheet
[var,TextInd] = xls_read(fd,Sheetpos)
//var = readxls('E:/Google Drive/Articulos/Pendientes/Varadero growth rates/data/coral_growth_monthly.xls');

//VAR1
den1 = var(1:408,5);
ext1 = var(1:408,6);
cal1 = var(1:408,7);
t1 = var(1:408,4);

//VAR2
den2 = var(409:1189,5);
ext2 = var(409:1189,6);
cal2 = var(409:1189,7);
den2 = replace_nodata(den2,-99999.0);
ext2 = replace_nodata(ext2,-99999.0);
cal2 = replace_nodata(cal2,-99999.0);
t2 = var(409:1189,4);

//VAR3
den3 = var(1190:2077,5);
ext3 = var(1190:2077,6);
cal3 = var(1190:2077,7);
den3 = replace_nodata(den3,-99999.0);
ext3 = replace_nodata(ext3,-99999.0);
cal3 = replace_nodata(cal3,-99999.0);
t3 = var(1190:2077,4);

//VAR4
den4 = var(2078:2856,5);
ext4 = var(2078:2856,6);
cal4 = var(2078:2856,7);
den4 = replace_nodata(den4,-99999.0);
ext4 = replace_nodata(ext4,-99999.0);
cal4 = replace_nodata(cal4,-99999.0);
t4 = var(2078:2856,4);

//Compute spectra
//VAR1
[f_var1a,period_var1a,amp_var1a] = fs_spect(t1,den1);
[f_var1b,period_var1b,amp_var1b] = fs_spect(t1,ext1);
[f_var1c,period_var1c,amp_var1c] = fs_spect(t1,cal1);
//VAR2
[f_var2a,period_var2a,amp_var2a] = fs_spect(t2,den2);
[f_var2b,period_var2b,amp_var2b] = fs_spect(t2,ext2);
[f_var2c,period_var2c,amp_var2c] = fs_spect(t2,cal2);
//VAR3
[f_var3a,period_var3a,amp_var3a] = fs_spect(t3,den3);
[f_var3b,period_var3b,amp_var3b] = fs_spect(t3,ext3);
[f_var3c,period_var3c,amp_var3c] = fs_spect(t3,cal3);
//VAR4
[f_var4a,period_var4a,amp_var4a] = fs_spect(t4,den4);
[f_var4b,period_var4b,amp_var4b] = fs_spect(t4,ext4);
[f_var4c,period_var4c,amp_var4c] = fs_spect(t4,cal4);


plot(period_var1a*-1,amp_var1a*5,'r')
plot(f_var1b*-1,amp_var1b,'b')
plot(f_var1c*-1,amp_var1c,'b')


//// ENVIRONMENTAL DATA
[fd2,SST2,Sheetnames2,Sheetpos2] = xls_open('E:/Google Drive/Articulos/Pendientes/Varadero growth rates/data/env_monthly.xls');
//Read first data sheet
[env,TextInd2] = xls_read(fd2,Sheetpos2);

//SOI
soi_y = env(1:756,8);
soi_x = env(1:756,3);
[f_soi,period_soi,amp_soi] = fs_spect(soi_x,soi_y);
plot(period_soi*-1,amp_soi,'b')

//AMO
amo_y = env(1:756,9);
amo_x = env(1:756,3);
[f_amo,period_amo,amp_amo] = fs_spect(amo_x,amo_y);
plot(period_amo*-1,amp_amo,'g')

////Water Level
wl_y = env(1:383,5);
wl_x = env(1:383,3);
[f_wl,period_wl,amp_wl] = fs_spect(wl_x,wl_y);
plot(period_wl*-1,amp_wl/100,'b')

////Water FLOW
wf_y = env(1:420,4);
wf_x = env(1:420,3);
[f_wf,period_wf,amp_wf] = fs_spect(wf_x,wf_y);
plot(period_wf*-1,amp_wf/100,'g')

//Air Temperature
temp_y = env(25:744,7);
temp_x = env(25:744,3);
[f_temp,period_temp,amp_temp] = fs_spect(temp_x,temp_y);
plot(period_temp*-1,amp_temp,'b')