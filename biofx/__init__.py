def mccoxph():
    return

def qnorm(df):
    # https://stackoverflow.com/questions/37935920/quantile-normalization-on-pandas-dataframe
    # https://en.wikipedia.org/wiki/Quantile_normalization
    rank_mean = df.stack().groupby(df.rank(method='first').stack().astype(int)).mean()
    return df.rank(method='min').stack().astype(int).map(rank_mean).unstack()

def __cli():
    args = __do_inputs()
    # Now read in the input files for purposes of standardizing inputs
    df = None
    if args.tsv_in:
        df = pd.read_csv(args.input,sep="\t",index_col=0)
    else:
        df = pd.read_csv(args.input,index_col=0)
    gmt = gmt_to_dataframe(args.gmt)
    result = gsva(df,geneset_df=gmt,
                  method=args.method,
                  kcdf=args.kcdf,
                  abs_ranking=args.abs_ranking,
                  min_sz=args.min_sz,
                  max_sz=args.max_sz,
                  parallel_sz=args.parallel_sz,
                  parallel_type=args.parallel_type,
                  mx_diff=args.mx_diff,
                  tau=args.tau,
                  ssgsea_norm=args.ssgsea_norm,
                  verbose=args.verbose,
                  tempdir=args.tempdir
                 )
    sep = ','
    if args.tsv_out: sep = "\t"
    if args.output:
        result.to_csv(args.output,sep=sep)
    else:
        result.to_csv(os.path.join(args.tempdir,'final.csv'),sep=sep)
        with open(os.path.join(args.tempdir,'final.csv')) as inf:
            for line in inf:
                sys.stdout.write(line)

def __do_inputs():
    # Setup command line inputs
    parser=argparse.ArgumentParser(description="Execute R bioconductors GSVA",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    group0 = parser.add_argument_group('Input options')
    group0.add_argument('input',help="Use - for STDIN")
    args = parser.parse_args()
    return args
