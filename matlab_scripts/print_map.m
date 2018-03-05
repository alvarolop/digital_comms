function [] = print_map(table, parameter)
map = shaperead('D:\Dropbox\Digital Comms - Mobile\Visualisation\LAD Shapes\LAD_shapes');
cmap = colormap(autumn);
hold on;
% axis off;
set(gca,'xtick',[],'ytick',[])

maximum = max(parameter);
minimum = min(parameter);
range = maximum - minimum + 1;

% ylabel('latitud');
% xlabel('longitud');

for i =1:size(parameter)
    lad_id = map(i).geo_code; %Pick one LAD
    if ~isempty(lad_id)
        lad_position = find(ismember(table.lad_id, lad_id),1);
        if ~isempty(lad_position)
            
            i_value=parameter(lad_position);
            color_intensity = 64 - round((i_value-minimum+1)*64/range);
            
            if (color_intensity == 0)
                color_intensity = 1;
            end
            color_i = cmap(color_intensity,:);

            mapshow(map(i),'FaceColor', color_i, 'EdgeColor','k');
        else
            error('Error. \n %s is not a LAD.',class(n))
        end
    end
end
% colorbar('YTickLabel',
% {'> 2.000 €',
% '< 2.000 €',
% '< 1.000 €',
% '< 500 €',
% '< 200 €',
% '< 100 €',
% '< 40 €',
% '< 20 €',
% '< 10 €',
% '< 5 €',
% '0 €'})



% colorbar('YTickLabel',{'> 2.000 €','< 2.000 €','< 1.000 €','< 500 €', '< 200 €', '< 100 €', '< 40 €', '< 20 €', '< 10 €', '< 5 €', '0 €'})
% saveas(gcf,'mapa2.jpg');
end