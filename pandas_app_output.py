import pandas as pd
import numpy as np


def cal_to_output(inputFile: str, outputFile: str) -> None:
    # input
    df = pd.DataFrame(pd.read_csv(inputFile, names=['time', 'sym', 'qty', 'prc']))

    # sort df by sym,time, groupby sym
    df_groupby = df.sort_values(by=['sym', 'time']).groupby('sym')

    # apply/lambda: to get wavg
    wavg = lambda x: np.average(x.iloc[0], weights=x.iloc[1], axis=0)
    get_wavg = df_groupby[['prc', 'qty']].apply(wavg).astype('int')

    # apply/lambda: to get timegap
    timegap = lambda x: max(x.diff(1).fillna(0).astype('int'))
    get_timegap = df_groupby['time'].apply(timegap)

    # agg: to get sum qty
    get_sum_qty = df_groupby['qty'].agg(sum).astype('int')

    # agg: to get max prc
    get_max_prc = df_groupby['prc'].agg(max).astype('int')

    # output
    output = pd.concat((get_timegap, get_sum_qty, get_wavg, get_max_prc), axis=1)
    output.to_csv(outputFile, header=0)


if __name__ == '__main__':
    input_File = "input.csv"
    output_File = "out.csv"
    cal_to_output(input_File, output_File)
