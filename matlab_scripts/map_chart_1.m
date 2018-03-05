clear
figure (1);
mapa = shaperead('LAD_shapes');
resultados = xlsread('D:\Dropbox\00TFM\Digital Comms Output\csv\chart_1_pop_static2017_throughput_base_coverage_high.csv',1);


%colores=colormap('copper');
%indicar columna de resultados que se quieran obtener 3 geotipos, 4 ...
test=4;
%total españa
maximo=max(resultados(:,test));
minimo=min(resultados(:,test));
rango=maximo-minimo+1;
faltan=[];
hold on;
ylabel('latitud');
xlabel('longitud');
 
for i =1:174
    %Se obtiene del fichero de formas el código del municipio en formato de
    %5 dígitos
    codigo=mapa(i).PROVMUN;
    if isempty(codigo)
        continue
    end
    %Se calcula la posición del municipio en el fichero de resultados
    posicion=find((str2num(codigo)==resultados(:,1)));
    if isempty(posicion)
        faltan=[faltan,i];
    else
    valor_i=resultados(posicion(1),test);
    
    colormap(copper);
    cmap = colormap;

    aux = round((valor_i-minimo+1)*64/rango);
    aux = 64 - aux;
    if (aux == 0)
        aux = 1;
    end
    color_i = cmap(aux,:);
      
%        switch valor_i
%         case 0
%             color_i='w';
%         case 1
%             color_i='b';
%         case 2
%             color_i='g';
%         case 3
%             color_i='c';
%         case 4
%             color_i='r';
%         otherwise
%             color_i = 'g';
%        end
%         
    
    mapshow(mapa(i),'FaceColor',color_i, 'EdgeColor',color_i)
    end
end

%contourf(peaks)    
%colorbar('YTickLabel',{'0','< 5 €','< 10 €','< 20 €','< 40 €','< 100 €','< 200 €','< 500 €','< 1.000 €','< 2.000 €','> 2.000 €'})
colorbar('YTickLabel',{'> 2.000 €','< 2.000 €','< 1.000 €','< 500 €', '< 200 €', '< 100 €', '< 40 €', '< 20 €', '< 10 €', '< 5 €', '0 €'})

%saveas(gcf,'geotipos.jpg');
%saveas(gcf,'');
%colorbar;
saveas(gcf,'mapa2.jpg');