function [] = plot_chart_2(data_path, scenario)
%% GET TABLE INFORMATION
Table=readtable(data_path);
% summary(Table) % Print info of the Table

title_prefix = pad('Chart_2_');

step_100 = Table.population_sum(length(Table.population_sum));

step_25_x = find(Table.population_sum>step_100/4,1);
step_50_x = find(Table.population_sum>step_100/2,1);
step_75_x = find(Table.population_sum>step_100*3/4,1);

step_25_text = '\times 25%';
step_50_text = '\times 50%';
step_75_text = '\times 75%';

%% PRINT TABLE 3: Capacity margin comparison per year
figure2 = figure('Name',strcat(title_prefix, pad('year_all_'),scenario),'NumberTitle','off');
% set(figure2, 'Visible', 'off');
for year = 2020:2030
    subplot(6,2,year-2019);
    column = strcat('cap_margin_year_', num2str(year));
    bar([Table{:,column}]);
    set(gca,'xticklabel',Table.postcode);
end  
filepath = join(['D:\Dropbox\00TFM\Digital Comms Output\matlab_figures\',title_prefix,'year_all_', scenario],'');
saveas(figure2,filepath);


%% PRINT TABLES N: Capacity margin per year
for year = 2020:2030
    figure3 = figure('Name',strcat(title_prefix, pad('year_'), num2str(year), '_', scenario),'NumberTitle','off');
%     set(figure3, 'Visible', 'off');
    column = strcat('cap_margin_year_', num2str(year));
    plot([Table{:,column}]);
    set(gca,'xticklabel',Table.postcode);
    filepath = join(['D:\Dropbox\00TFM\Digital Comms Output\matlab_figures\detail_per_year\',title_prefix,'year_', num2str(year), '_', scenario],'');
    saveas(figure3,filepath);
end
end

% Add text annotations inside the graph
% https://es.mathworks.com/help/matlab/creating_plots/add-text-to-specific-points-on-graph.html

