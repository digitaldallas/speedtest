import pyspeedtest
import csv
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates, rcParams
from PIL import Image
from time import strftime

def main():
    file_plot='bandwidth.png'
    file_log='speedtest.results.csv'
    try:
        log_test(file_log)
        #plot_file_name = 'bandwidth.png'
        create_plot(file_plot, file_log)
        #os.system('open ' + file_plot)
        image = Image.open(file_plot)
        image.show()
    except Exception as ex:
        log_error(str(ex))

def log_test(log_file_name):
    st = pyspeedtest.SpeedTest()

    results={
            'datetime':strftime("%Y-%m-%d %H:%M:%S"),
            'ping': st.ping(),
            'download': st.download()/1000000,
            'upload': st.upload()/1000000
    }

    #print(results)

    with open(log_file_name, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=results.keys())
        #writer.writeheader()
        writer.writerow(results)

def log_error(error_msg):
    with open('error.log', 'a', newline='') as f:
        f.write(error_msg)

def create_plot(plot_file_name, log_file_name):
    df = load_csv_df(log_file_name)
    make_plot_file(df, plot_file_name)

def load_csv(file_name):
    with open(file_name) as csv_data:
        reader = csv.reader(csv_data)

        # eliminate blank rows if they exist
        rows = [row for row in reader if row]
        headings = rows[0] 

    table=[]
    for row in rows[1:]:
        table_row={}
        for col_header, data_column in zip(headings, row):
            table_row[col_header]=data_column
        table.append(table_row.copy())
    
    return table[-48:]   # return data for last 48 periods (i.e., 24 hours)

def load_csv_df(file_name):
    df = pd.read_csv(
        file_name,
        parse_dates={'timestamp':[0]},
        na_values=['TEST','FAILED'],            
        )
    return df[-46:]

def make_plot_file(last_24, file_plot_name):
    rcParams['xtick.labelsize'] = 'xx-small'

    plt.plot(last_24['timestamp'],last_24['download'], 'b-')
    plt.title('Bandwidth Report (last 24 hours)')
    plt.ylabel('Bandwidth in MBps')
    #plt.yticks(xrange(0,21))
    #plt.ylim(0.0,20.0)

    plt.xlabel('Date/Time')
    plt.xticks(rotation='45')

    plt.grid()

    current_axes = plt.gca()
    current_figure = plt.gcf()

    hfmt = dates.DateFormatter('%m/%d %H:%M')
    current_axes.xaxis.set_major_formatter(hfmt)
    current_figure.subplots_adjust(bottom=.25)

    loc = current_axes.xaxis.get_major_locator()
    loc.maxticks[dates.HOURLY] = 24
    #loc.maxticks[dates.MINUTELY] = 60

    current_figure.savefig(file_plot_name)        

if __name__ == '__main__':
  main()        