import pandas as pd
from datetime import datetime, timedelta
import jqdatasdk as jq
import os



class FuturesInfo:
    data_exist = []
    empty = []

    def __init__(self, f_start, f_end, f_kind, the_path):
        self.f_start = f_start
        self.f_end = f_end
        self.f_kind = f_kind
        self.path = the_path

    def get_large_data(self):
        """
        Get the futures data and download the datasets to local

        Parameters
        ----------
        f_start : time string, the time you start collecting the data
          A string
        f_end : time string, the time you end collecting the data
          A string
        f_kind: the substring of the futures ticker. Category of futures types
          A string
        the_path: the location you want to download data to
          A string

        Returns
        -------
        print out all the futures data downloaded. Return one of the future's dataframe. Downloaded all specified futures to specified location

        Examples
        --------
        >>> from magic_futures_data_acquisition_pkg import magic_futures_data_acquisition_pk
        >>> get_large = FuturesInfo('2020-01-01','2020-03-01','AP','/Users/tylerwang/Desktop/get_futures_data/')
        >>> get_large.get_large_data()
        ['', 'AP1805.XZCE', 'AP1807.XZCE', 'AP1810.XZCE', 'AP1811.XZCE', 'AP1812.XZCE', 'AP1901.XZCE', 'AP1903.XZCE', 'AP1905.XZCE', 'AP1907.XZCE', 'AP1910.XZCE', 'AP1911.XZCE', 'AP1912.XZCE', 'AP2001.XZCE', 'AP2003.XZCE', 'AP2005.XZCE', 'AP2007.XZCE', 'AP2010.XZCE', 'AP2011.XZCE', 'AP2012.XZCE', 'AP2101.XZCE', 'AP2103.XZCE', 'AP2105.XZCE', 'AP2110.XZCE', 'AP2111.XZCE', 'AP2112.XZCE', 'AP2201.XZCE', 'AP2203.XZCE', 'AP2204.XZCE', 'AP2205.XZCE', 'AP2210.XZCE', 'AP2211.XZCE', 'AP2212.XZCE', 'AP2301.XZCE', 'AP2303.XZCE', 'AP2304.XZCE', 'AP2305.XZCE', 'AP2310.XZCE', 'AP2311.XZCE', 'AP8888.XZCE', 'AP9999.XZCE']
        	time	open	close	high	low	volume	money
        0	2020-01-02	7740.0	7741.0	7791.0	7706.0	93362.0	7.237311e+09
        1	2020-01-03	7736.0	7589.0	7767.0	7580.0	149249.0	1.148803e+10
        2	2020-01-06	7560.0	7474.0	7577.0	7428.0	168525.0	1.261648e+10
        3	2020-01-07	7474.0	7501.0	7528.0	7443.0	107722.0	8.070493e+09
        4	2020-01-08	7505.0	7497.0	7556.0	7424.0	128109.0	9.595661e+09
        5	2020-01-09	7497.0	7360.0	7545.0	7358.0	145093.0	1.083167e+10
        """
        global data_exist
        global empty
        f = open("futures_list.txt", "w+")
        lis = f.read()
        data_exist = lis.split(" ")
        # log in the  JQ account
        jq.auth(acc, pas)
        all_futures = jq.get_all_securities(['futures'])
        # name the index of the DataFrame
        all_futures.index.name = 'id'
        # convert index column to list
        futures_idx = all_futures.index.values.tolist()
        substring = self.f_kind
        empty = []
        for idx in futures_idx:
            if substring in idx:
                empty.append(idx)
        count = 0
        for item in empty:
            future_info_yearly = jq.get_price(security=item, start_date=datetime.strptime(self.f_start, '%Y-%m-%d'),
                                              end_date=datetime.strptime(self.f_end, '%Y-%m-%d'), frequency='1d')
            str = item + '.csv'
            future_info_yearly.index.name = 'time'
            future_info_yearly.dropna(inplace=True)
            future_info_yearly.to_csv(os.path.join(self.path, str), mode='a')
            if item not in data_exist:
                data_exist.append(item)

            count += 1
            print(count)
        f = open("futures_list.txt", "w")
        f.write(" ".join(empty))
        f.close()
        for item in data_exist:
            if item == "":
                continue
            str = item + '.csv'
            df = pd.read_csv(self.path + str)
            df.drop_duplicates(subset=['time'], inplace=True)
            df.sort_values(by='time', inplace=True)
            df = df[df.time.str.contains('time') == False]
            df.to_csv(os.path.join(self.path, str), index=False, index_label='time')
        print(data_exist)
        return df


    def get_missing_data(self):
        """
        Find the missing date in existing datasets and download the missing data to local

        Parameters
        ----------
        f_start : time string, the time you start collecting the data
          A string
        f_end : time string, the time you end collecting the data
          A string
        f_kind: the substring of the futures ticker. Category of futures types
          A string
        the_path: the location you want to download data to
          A string

        Returns
        -------
        print out the missing date for all existing futures and search for the missing date in API and download the datasets to local
        return the new dataframe contains missing data
        Examples
        --------
        >>> from magic_futures_data_acquisition_pkg import magic_futures_data_acquisition_pk
        >>> get_miss = FuturesInfo('2020-01-01', '2020-02-01', 'AP','/Users/tylerwang/Desktop/get_futures_data/')
        >>> get_miss.get_missing_data()
        AP1805.XZCE:['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-06', '2020-01-07', '2020-01-08', '2020-01-09', '2020-01-10', '2020-01-13', '2020-01-14', '2020-01-15', '2020-01-16', '2020-01-17', '2020-01-20', '2020-01-21', '2020-01-22', '2020-01-23', '2020-01-24', '2020-01-27', '2020-01-28', '2020-01-29', '2020-01-30', '2020-01-31']
        	time	open	close	high	low	volume	money
        0	2020-01-02	7740.0	7741.0	7791.0	7706.0	93362.0	7.237311e+09
        1	2020-01-03	7736.0	7589.0	7767.0	7580.0	149249.0	1.148803e+10
        2	2020-01-06	7560.0	7474.0	7577.0	7428.0	168525.0	1.261648e+10
        3	2020-01-07	7474.0	7501.0	7528.0	7443.0	107722.0	8.070493e+09
        4	2020-01-08	7505.0	7497.0	7556.0	7424.0	128109.0	9.595661e+09
        5	2020-01-09	7497.0	7360.0	7545.0	7358.0	145093.0	1.083167e+10
        """
        global data_exist
        global path
        f = open("futures_list.txt", "r+")
        lis = f.read()
        data_exist = lis.split(" ")
        futures_dict = {}
        substring = self.f_kind
        for item in data_exist:
            if item == "":
                continue
            if substring in item:
                str = item + '.csv'
                future_info = pd.read_csv(self.path + str)
                # groupby datetime and get the size of futures of that day
                date_with_data = future_info.groupby(['time']).size()
                all_date = pd.date_range(start=datetime.strptime(self.f_start, '%Y-%m-%d'),
                                     end=datetime.strptime(self.f_end, '%Y-%m-%d'))
                date_with_data.index = pd.DatetimeIndex(date_with_data.index)
                # set new index to data series, if its NaN then 0
                date_with_data = date_with_data.reindex(all_date, fill_value=0)
                # get the date of missing data
                date_with_data = date_with_data[date_with_data.index.dayofweek < 5]
                miss_date_list = []
                for index, value in date_with_data.items():
                    if value == 0:
                        miss_date_list.append(index.strftime('%Y-%m-%d'))
                        futures_dict[item] = miss_date_list
        for key, value in futures_dict.items():
            print(key, end=":")
            print(value)
        jq.auth(acc, pas)
        count = 0
        for item in futures_dict:
            date_list = []
            for time in futures_dict[item]:
                date_list.append(datetime.strptime(time, '%Y-%m-%d'))
            max_date = max(date_list)
            min_date = min(date_list)
            future_info = jq.get_price(security=item,
                                           start_date=min_date,
                                           end_date=max_date, frequency='1d')
            str = item + '.csv'
            future_info.to_csv(os.path.join(self.path, str), mode='a')
            count += 1
            print(count)
        for item in data_exist:
            if item == "":
                continue
            str = item + '.csv'
            df = pd.read_csv(self.path + str)
            df.drop_duplicates(subset=['time'], inplace=True)
            df.sort_values(by='time', inplace=True)
            df.dropna(inplace = True)
            df.to_csv(os.path.join(self.path, str), index=False, index_label='time')
        return df
