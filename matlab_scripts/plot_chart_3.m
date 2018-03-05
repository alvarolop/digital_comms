function [] = plot_chart_2(data_path, scenario)
%% GET TABLE INFORMATION
Table=readtable(data_path);
% summary(Table) % Print info of the Table

title_prefix = pad('Chart_3_');

step_100 = Table.population_sum(length(Table.population_sum));

step_25_x = find(Table.population_sum>step_100/4,1);
step_50_x = find(Table.population_sum>step_100/2,1);
step_75_x = find(Table.population_sum>step_100*3/4,1);

step_25_text = '\times 25%';
step_50_text = '\times 50%';
step_75_text = '\times 75%';

% Set the 'visible' property 'off'
% ax = gca
% ax.Visible = 'off'
% https://artofproblemsolving.com/wiki/index.php/LaTeX:Symbols


%% PRINT TABLE 1: Capacity Margin summed of all years 
% figure1 = figure('Name',strcat(title_prefix, scenario),'NumberTitle','off');
% 
% %Plot population plot
% s=subplot(2,1,1);
% % title(figure1,'Population')
% bar([Table.population])
% set(gca,'xticklabel',Table.postcode)
% 
% text(step_25_x,max(Table.population)*3/4,step_25_text);
% text(step_50_x,max(Table.population)*3/4,step_50_text);
% text(step_75_x,max(Table.population)*3/4,step_75_text);
% 
% % Plot cost plot
% s(2)=subplot(2,1,2);
% % title(s(2),'Cost')
% bar([Table.cap_margin_year_2020])
% set(gca,'xticklabel',Table.postcode)
% 
% text(step_25_x,max(Table.cost)*3/4,step_25_text);
% text(step_50_x,max(Table.cost)*3/4,step_50_text);
% text(step_75_x,max(Table.cost)*3/4,step_75_text);
% 
% % Save figure
% filepath = join(['D:\Dropbox\00TFM\Digital Comms Output\matlab_figures\',title_prefix, scenario],'');
% saveas(figure1,filepath);


%% PRINT TABLE 2: Cost aggregated and summed of all years 
% figure1 = figure('Name',strcat(title_prefix, pad('aggregated_'), scenario),'NumberTitle','off');
% 
% %Plot population plot
% s(1)=subplot(2,1,1);
% % title(s(1),'Population')
% bar([Table.population_sum]);
% set(gca,'xticklabel',Table.postcode);
% 
% text(step_25_x,Table.population_sum(step_25_x),step_25_text)
% text(step_50_x,Table.population_sum(step_50_x),step_50_text)
% text(step_75_x,Table.population_sum(step_75_x),step_75_text)
% 
% % Plot cost plot
% s(2)=subplot(2,1,2);
% % title(s(2),'Cost')
% bar([Table.cost_sum]);
% set(gca,'xticklabel',Table.postcode);
% 
% text(step_25_x,Table.cost_sum(step_25_x),step_25_text)
% text(step_50_x,Table.cost_sum(step_50_x),step_50_text)
% text(step_75_x,Table.cost_sum(step_75_x),step_75_text)
% 
% % Save figure
% filepath = join(['D:\Dropbox\00TFM\Digital Comms Output\matlab_figures\',title_prefix, 'aggregated_', scenario],'');
% saveas(figure1,filepath)


%% PRINT TABLE 3: Cost comparison per year
figure2 = figure('Name',strcat(title_prefix, pad('year_all_'),scenario),'NumberTitle','off');
set(figure2, 'Visible', 'off');
for year = 2020:2030
    subplot(6,2,year-2019);
    column1 = strcat('Upg_LTE_year_', num2str(year));
    column2 = strcat('Upg_700_year_', num2str(year));
    b = bar([Table{:,column1};Table{:,column2}]);
%     b(2).FaceColor = 'g'
    set(gca,'xticklabel',Table.postcode);
end  
filepath = join(['D:\Dropbox\00TFM\Digital Comms Output\matlab_figures\',title_prefix,'year_all_', scenario],'');
saveas(figure2,filepath);


%% PRINT TABLES N: Cost per year
for year = 2020:2030
    figure3 = figure('Name',strcat(title_prefix, pad('year_'), num2str(year), '_', scenario),'NumberTitle','off');
    set(figure3, 'Visible', 'off');
    column1 = strcat('Upg_LTE_year_', num2str(year));
    column2 = strcat('Upg_700_year_', num2str(year));
    bar([Table{:,column1};Table{:,column2}]);
    set(gca,'xticklabel',Table.postcode);
    filepath = join(['D:\Dropbox\00TFM\Digital Comms Output\matlab_figures\detail_per_year\',title_prefix,'year_', num2str(year), '_', scenario],'');
    saveas(figure3,filepath);
end
end

% Add text annotations inside the graph
% https://es.mathworks.com/help/matlab/creating_plots/add-text-to-specific-points-on-graph.html

