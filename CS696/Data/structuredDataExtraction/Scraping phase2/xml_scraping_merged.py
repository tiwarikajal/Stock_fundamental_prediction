import pandas as pd
from bs4 import BeautifulSoup
from requests import get
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
    #     return df[df['time_period'].str.endswith("YTD")] #to filter out quarterly values and only consider yearly.
        return df.drop_duplicates('value_usd')
    except Exception:
        #print('cant find data from given xml url')
        return None
def main():
    count_nf=0
    count_total = 30001
    link_list = pd.read_csv('10k_links.csv',header=None,names=['CIK','link'])
    link_list.drop(link_list.head(30000).index, inplace=True)
    print(link_list.shape)
    df = pd.DataFrame(columns=['cik','variable','time_period','value_usd'])
    print('starting execution')
    for row in link_list.iterrows():
       if (count_total % 1000 ==0) :
           df.to_csv('/mnt/nfs/scratch1/dpariyani/xml_data/data/data_'+str(count_total)+'.csv')
           print('Rows Done: ',count_total)
           del df
           df = pd.DataFrame(columns=['cik','variable','time_period','value_usd'])
       link = row[1]['link']
       df2 = print_filing_data(link)
       if df2 is None:
           count_nf+=1
       else:
           df = df.append(df2,ignore_index=True)
       count_total+=1
       sleep(0.1)
    df.to_csv('/mnt/nfs/scratch1/dpariyani/xml_data/data/data'+str(count_total)+'.csv')
    print('Extraction Complete.')
    print('No of links not found: ',count_nf)
    print('Total Links tested: ',count_total)
if __name__ == '__main__':
    main()


