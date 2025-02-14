# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""
import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')  # Cambia el backend a uno que no use Tkinter
import matplotlib.pyplot as plt

def createHtml():
    html_content = """
    <!DOCTYPE html>
    <html>
        <body>
            <h1>Shippping dashboard example</h1>
            <div style="width:45%:float:left">
                <img src="shipping_per_warehouse.png" alt="Fig 1">
                <img src="mode_of_shipment.png" alt="Fig 2">
            </div>
            <div style="width:45%:float:left">
                <img src="average_customer_rating.png" alt="Fig 3">
                <img src="weight_distribution.png" alt="Fig 1">
            </div>  
        </body>
    </html>
    """

    with open('docs/index.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

def pregunta_01():

    if not os.path.exists('docs'):
        os.makedirs('docs')
    
    dforiginal = pd.read_csv('files/input/shipping-data.csv')
    
    df = dforiginal.copy()
    #Grafica
    plt.figure

    
    envios = df.Warehouse_block.value_counts()

    # Transformamos los datos en una grafica de barras
    envios.plot.bar(
        title = 'Shipping per Warehouse',
        xlabel = 'Warehouse block',
        ylabel = ' Record count',
        color = 'tab:blue',
        fontsize = 8,
    )

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.savefig('docs/shipping_per_warehouse.png')


    #Grafica 2
    plt.figure()
    counts = df.Mode_of_Shipment.value_counts()
    counts.plot.pie(
        title = 'Mode of shipment',
        wedgeprops = dict(width=0.35),
        ylabel = '',
        colors = ['tab:blue', 'tab:orange', 'tab:green'],
    )

    # Se guarda la figura
    plt.savefig('docs/mode_of_shipment.png')


    #Grafica 3
    plt.figure()

    df = dforiginal.copy()

    df = (df[['Mode_of_Shipment', 'Customer_rating']].groupby('Mode_of_Shipment').describe())
    df.columns = df.columns.droplevel()
    df = df[['mean', 'min', 'max']]

    # grafico de barras 
    plt.barh(
        y = df.index.values,
        width = df['max'].values - 1,
        left = df['min'].values,
        height = 0.9,
        color = 'lightgray',
        alpha = 0.8,
    )

    colors = ['tab:green' if value > 3.0 else 'tab:orange' for value in df['mean'].values]
    plt.barh(
        y = df.index.values,
        width = df['mean'].values - 1,
        left = df['min'].values,
        color = colors,
        height = 0.5,
        alpha = 1.0,
    )

    
    plt.title('Average Customer Rating')
    plt.gca().spines['left'].set_color('gray')
    plt.gca().spines['bottom'].set_color('gray')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    
    # Se guarda la figura
    plt.savefig('docs/average_customer_rating.png')

    #grafica 4
    plt.figure()
    df = dforiginal.copy()
    # histograma
    df.Weight_in_gms.plot.hist(
        title = ' Shipped Weight Distribution',
        color = 'tab:orange',
        edgecolor = 'white',
    )

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # Se guarda la imagen
    plt.savefig('docs/weight_distribution.png')

    #Ejecucion html
    createHtml()

pregunta_01()
