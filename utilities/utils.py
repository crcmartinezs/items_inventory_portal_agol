from pandas import ExcelWriter

def df_to_excel(df, output):
    
    with ExcelWriter(output, engine='xlsxwriter') as writer:     
        df.to_excel(writer, 'result', index=False)
    
