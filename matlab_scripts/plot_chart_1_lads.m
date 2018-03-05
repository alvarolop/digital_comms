function [] = plot_chart_1_lads(data_path, scenario)
%% GET TABLE INFORMATION
Table=readtable(data_path);
% summary(Table) % Print info of the Table

title_prefix = pad('Chart_1_lads_');

step_100 = Table.population_sum(length(Table.population_sum));

step_25_x = find(Table.population_sum>step_100/4,1);
step_50_x = find(Table.population_sum>step_100/2,1);
step_75_x = find(Table.population_sum>step_100*3/4,1);

step_25_text = '\times 25%';
step_50_text = '\times 50%';
step_75_text = '\times 75%';
% https://artofproblemsolving.com/wiki/index.php/LaTeX:Symbols


%% PRINT TABLE 1: Cost summed of all years
figure1 = figure('Name',strcat(title_prefix, scenario),'NumberTitle','off');
% set(figure1, 'Visible', 'off');

%Plot population plot
s=subplot(2,1,1);
% title(figure1,'Population')
bar([Table.population])
set(gca,'xticklabel',Table.name)

text(step_25_x,max(Table.population)*3/4,step_25_text);
text(step_50_x,max(Table.population)*3/4,step_50_text);
text(step_75_x,max(Table.population)*3/4,step_75_text);

% Plot cost plot
s(2)=subplot(2,1,2);
% title(s(2),'Cost')
bar([Table.cost])
set(gca,'xticklabel',Table.name)

text(step_25_x,max(Table.cost)*3/4,step_25_text);
text(step_50_x,max(Table.cost)*3/4,step_50_text);
text(step_75_x,max(Table.cost)*3/4,step_75_text);

% Save figure
filepath = join(['D:\Dropbox\00TFM\Digital Comms Output\matlab_figures\',title_prefix, scenario],'');
saveas(figure1,filepath);


%% PRINT TABLE 2: Cost aggregated and summed of all years 
figure1 = figure('Name',strcat(title_prefix, pad('aggregated_'), scenario),'NumberTitle','off');
% set(figure1, 'Visible', 'off');

%Plot population plot
s(1)=subplot(2,1,1);
% title(s(1),'Population')
bar([Table.population_sum]);
set(gca,'xticklabel',Table.name);

text(step_25_x,Table.population_sum(step_25_x),step_25_text)
text(step_50_x,Table.population_sum(step_50_x),step_50_text)
text(step_75_x,Table.population_sum(step_75_x),step_75_text)

% Plot cost plot
s(2)=subplot(2,1,2);
% title(s(2),'Cost')
bar([Table.cost_sum]);
set(gca,'xticklabel',Table.name);

text(step_25_x,Table.cost_sum(step_25_x),step_25_text)
text(step_50_x,Table.cost_sum(step_50_x),step_50_text)
text(step_75_x,Table.cost_sum(step_75_x),step_75_text)

% Save figure
filepath = join(['D:\Dropbox\00TFM\Digital Comms Output\matlab_figures\',title_prefix, 'aggregated_', scenario],'');
saveas(figure1,filepath)


%% PRINT TABLE 3: Cost comparison per year
figure2 = figure('Name',strcat(title_prefix, pad('year_all_'),scenario),'NumberTitle','off');
% set(figure2, 'Visible', 'off');
for year = 2020:2030
    subplot(6,2,year-2019);
    column = strcat('cost_year_', num2str(year));
    bar([Table{:,column}]);
    set(gca,'xticklabel',Table.name);
end  
filepath = join(['D:\Dropbox\00TFM\Digital Comms Output\matlab_figures\', title_prefix, 'year_all_', scenario],'');
saveas(figure2,filepath);


%% PRINT TABLES N: Cost per year
for year = 2020:2030
    figure3 = figure('Name',strcat(title_prefix, pad('year_'), num2str(year), '_', scenario),'NumberTitle','off');
%     set(figure3, 'Visible', 'off');
    column = strcat('cost_year_', num2str(year));
    bar([Table{:,column}]);
    set(gca,'xticklabel',Table.name);
    filepath = join(['D:\Dropbox\00TFM\Digital Comms Output\matlab_figures\detail_per_year\', title_prefix, 'year_', num2str(year), '_', scenario],'');
    saveas(figure3,filepath);
end

%% PRINT MAP 1: Cost summed of all years
% figure4 = figure('Name',strcat(title_prefix, scenario),'NumberTitle','off');
% 
% print_map(Table,Table.cost)
% 
% % Save figure
% filepath = join(['D:\Dropbox\00TFM\Digital Comms Output\matlab_maps\',title_prefix, scenario],'');
% saveas(figure4,filepath);

%% PRINT MAP 2: Cost comparison per year
% figure5 = figure('Name',strcat(title_prefix, pad('year_all_'),scenario),'NumberTitle','off');
% 
% for year = 2020:2030
%     subplot(4,3,year-2019);
%     column = strcat('cost_year_', num2str(year));
%     print_map(Table,[Table{:,column}])
% end 
% subplot(4,3,12);
% colorbar('YTickLabel',{'> 2.000 €','< 2.000 €','< 1.000 €','< 500 €', '< 200 €', '< 100 €', '< 40 €', '< 20 €', '< 10 €', '< 5 €', '0 €'})
% 
% % Save figure
% filepath = join(['D:\Dropbox\00TFM\Digital Comms Output\matlab_maps\', title_prefix, 'year_all_', scenario],'');
% saveas(figure5,filepath);

%% PRINT MAP N: Cost per year
% for year = 2020:2030
%     figure5 = figure('Name',strcat(title_prefix, pad('year_'), num2str(year), '_', scenario),'NumberTitle','off');
%     set(figure5, 'Visible', 'off');
%     column = strcat('cost_year_', num2str(year));
%     print_map(Table,[Table{:,column}])
%     colorbar('YTickLabel',{'> 2.000 €','< 2.000 €','< 1.000 €','< 500 €', '< 200 €', '< 100 €', '< 40 €', '< 20 €', '< 10 €', '< 5 €', '0 €'})
% 
%     % Save figure
%     filepath = join(['D:\Dropbox\00TFM\Digital Comms Output\matlab_maps\detail_per_year\', title_prefix, 'year_', num2str(year), '_', scenario],'');
%     saveas(figure5,filepath);
% end 
end

% Add text annotations inside the graph
% https://es.mathworks.com/help/matlab/creating_plots/add-text-to-specific-points-on-graph.html

