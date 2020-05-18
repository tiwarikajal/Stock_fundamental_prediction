import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import glob
from time import sleep

def extract_xml_link(link):
    tables = pd.read_html(link)
    try:
        temp_df = pd.DataFrame(tables[1])
        temp_df2 = temp_df[temp_df['Description'].str.contains("INS")]
    #     print(temp_df2)
        final_link = link.rsplit("/", 1)[0] + '/'+temp_df2['Document'].values[0]
        #print('Extracting data for:',temp_df2['Document'].values[0])
        return final_link
    except Exception:
        #print('xml table not found on index page')
        pass

def print_filing_data(link):
    try:
        xml_link = extract_xml_link(link)
        r = get(xml_link)
        r_text = r.text
        soup_object = BeautifulSoup(r_text,'lxml')
        tags = soup_object.find_all()
        df = pd.DataFrame(columns=['cik','variable','time_period','value_usd'])
        all_tags=['us-gaap:netincomelossavailabletocommonstockholdersbasic','us-gaap:revenues','us-gaap:revenues','us-gaap:salesrevenuegoodsnet','us-gaap:salesrevenuenet','us-gaap:netincomeloss','us-gaap:paymentstoacquirepropertyplantandequipment','us-gaap:proceedsfromsaleofpropertyplantandequipment','us-gaap:researchanddevelopmentexpense','us-gaap:costofrevenue']
        for tag in tags :
            if ('us-gaap:' in tag.name) and tag.name in all_tags:
                name = tag.name.split('gaap:')[1]
    #             cref = tag['contextref'][-10:]
                cref = tag['contextref']
                value = tag.text
    #         
                if ('STD_364' in cref and 'x' not in cref ) or ('YTD' in cref and 'D_' not in cref):
                    df = df.append({'cik':xml_link.rsplit("/", 1)[1],'variable': tag.name, 'time_period': cref, 'value_usd': value}, ignore_index=True)
#         return df[df['time_period'].str.endswith("4YTD")] #to filter out quarterly values and only consider yearly.
        return df.drop_duplicates('value_usd')
    except Exception:
        #print('cant find data from given xml url')
        return None
def main():
    rev_dest_dir = '/mnt/nfs/scratch1/dpariyani/xml_data/input_links/CompanyWiseData_revenue2/'
    netincome_dest_dir = '/mnt/nfs/scratch1/dpariyani/xml_data/input_links/CompanyWiseData_netincome2/'
    payment_dest_dir = '/mnt/nfs/scratch1/dpariyani/xml_data/input_links/CompanyWiseData_payment2/'
    path = '/mnt/nfs/scratch1/dpariyani/xml_data/input_links/CompanyWiseFiles/*.csv' 
    for filepath in glob.iglob(path):
        link_list = pd.read_csv(filepath)
        df = pd.DataFrame(columns=['cik','variable','time_period','value_usd'])
        for row in link_list.iterrows():
            link = row[1]['IndexLink']
            df2 = print_filing_data(link)
            df = df.append(df2,ignore_index=True)
            sleep(0.1)
        df_revenue = df[(df['variable']=='us-gaap:revenues') | (df['variable']=='us-gaap:salesrevenuegoodsnet') | (df['variable'] == 'us-gaap:salesrevenuenet') | (df['variable'] == 'us-gaap:costofrevenue')].drop_duplicates(subset='time_period', keep="first")
        df_revenue.sort_values(by=['time_period'],inplace=True)
        df_revenue.to_csv(rev_dest_dir+filepath.split('/')[-1])
        
        df_netincome = df[(df['variable']=='us-gaap:netincomelossavailabletocommonstockholdersbasic') | (df['variable']=='us-gaap:netincomeloss')].drop_duplicates(subset='time_period', keep="first")
        df_netincome.sort_values(by=['time_period'],inplace=True)
        df_netincome.to_csv(netincome_dest_dir+filepath.split('/')[-1])
        
        
        df_payment = df[(df['variable']=='us-gaap:paymentstoacquirepropertyplantandequipment') | (df['variable']=='us-gaap:proceedsfromsaleofpropertyplantandequipment')].drop_duplicates(subset='time_period', keep="first")
        df_payment.sort_values(by=['time_period'],inplace=True)
        df_payment.to_csv(payment_dest_dir+filepath.split('/')[-1])
        
        
        del(df)
if __name__ == '__main__':
    main()



