import time
import csv

import logging

import os
import boto3
from urllib.parse import urlparse

'''
inputs: the name of a NAMED QUERY
outputs: the details of the NAMED QUERY, including the query string and database
'''


def get_named_query_details(named_query_name):
    client = boto3.client('athena')
    first = True

    # there can be more than 50 named queries, and the max results is 50.  we need to page through the results until we find what we need
    nqList = client.list_named_queries(MaxResults=50)
    while first or 'NextToken' in nqList:
        nqListWithDetails = client.batch_get_named_query(NamedQueryIds=nqList['NamedQueryIds'])
        for nqDetail in nqListWithDetails['NamedQueries']:
            first = False
            # found it!
            if nqDetail['Name'] == named_query_name:
                nqDetail['QueryString'] = nqDetail['QueryString'].strip()
                if nqDetail['QueryString'][-1:] == ';':
                    nqDetail['QueryString'] = nqDetail['QueryString'][:-1]
                return nqDetail
        nqList = client.list_named_queries(MaxResults=50, NextToken=nqList['NextToken'])
        if len(nqList) > 0:
            first = True

    return []


'''
inputs: the NAMED QUERY name and the string to APPEND TO NAMED QUERY, so that the result is an Athena executable SQL statement
outputs: the results file after the query has completed execution, in JSON format
'''


def get_athena_named_query_results_json(named_query_name):
    # print( "I am in the JSON ")
    nqDetail = get_named_query_details(named_query_name)
    query_string = nqDetail['QueryString']
    results_file = get_athena_query_results_file_location(query_string, 'datamart',
                                                          'valkyrie-usaid-' + account_id + '-us-east-1', 'otd/json/')
    return get_athena_query_results_json(results_file)


'''
STUFF I USE 
'''


def get_athena_query_string_results_json(query_string):
    results_file = get_athena_query_results_file_location(query_string, 'datamart',
                                                          'valkyrie-usaid-' + boto3.client('sts').get_caller_identity()[
                                                              'Account'] + '-us-east-1', 'otd/json')
    # print ( "results File: " , results_file )
    return get_athena_query_results_json(results_file)


'''
inputs: an S3 RESULTS FILE created by Athena 
outputs:  JSON format results, nice and neat for an API even
'''


def get_athena_query_results_json(results_file):
    # parse the s3 URL and find the bucket name and key name
    s3_client = boto3.client('s3')
    s3url = urlparse(results_file)
    s3_bucket = s3url.netloc
    s3_key = s3url.path
    # download the result from s3
    # Lambda gives you access to /tmp as a directory, no more than 500MB
    s3_client.download_file(s3_bucket, s3_key[1:], "/tmp/results.csv")
    # Parse file.
    results = []
    with open("/tmp/results.csv", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(row)
    os.remove("/tmp/results.csv")

    '''
    remove the original parsed csv and metadata
    '''
    s3_client.delete_object(Bucket=s3_bucket, Key=s3_key[1:])
    s3_client.delete_object(Bucket=s3_bucket, Key=s3_key[1:] + ".metadata")

    return results


'''
inputs: the QUERY STRING to execute against the DATABASE, putting the results in the DESTINATION_BUCKET with a path specified by DESTINATION_KEY_BASE (must end in a "/")
outputs: the results file after the query has completed execution
'''


def get_athena_query_results_file_location(query_string, database, destination_bucket, destination_key_base):
    # Kickoff the Athena query
    athena_client = boto3.client('athena')
    response = athena_client.start_query_execution(
        QueryString=query_string,
        QueryExecutionContext={
            'Database': database
        },
        ResultConfiguration={
            'OutputLocation': 's3://' + destination_bucket + '/' + destination_key_base
        }
    )

    queryrunning = 0
    # Setup logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # Log the query execution id
    logger.info('Execution ID: ' + response['QueryExecutionId'])
    # wait for query to finish.
    while queryrunning == 0:
        time.sleep(2)
        status = athena_client.get_query_execution(QueryExecutionId=response['QueryExecutionId'])
        results_file = status["QueryExecution"]["ResultConfiguration"]["OutputLocation"]
        if status["QueryExecution"]["Status"]["State"] != "RUNNING":
            queryrunning = 1
    # print ( "The Results File is" , results_file)
    print(status)
    if status["QueryExecution"]["Status"]['State'] == 'FAILED':
        return status["QueryExecution"]["Status"]['State']
    else:
        return results_file


"""
New Functions 
"""


def summarize_otd(date_level, source_system, year="ALL", by_country="No", rank="No"):
    if date_level == 'year':
        summary_date_column = 'fy'
        source_date_column = 'planned_delivery_fiscal_year'
        sort_date_column = 'fy'
        sort_column_calc = 'planned_delivery_fiscal_year'
    elif date_level == 'month':
        summary_date_column = 'month'
        _temp_list = ["case ",
                      "when planned_in_country_date is not NULL and planned_in_country_date <> ''",
                      "then",
                      "concat( substr(date_format(try_cast(planned_in_country_date  as DATE ) , '%M' ) ,1,3) ,",
                      "'-', ",
                      "cast(year( try_cast(planned_in_country_date  as DATE ) ) as varchar(4) )",
                      ")",
                      "else NULL",
                      "end "
                      ]
        source_date_column = " ".join(_temp_list)
        sort_date_column = 'date_for_sorting'
        _temp_list = ["case ",
                      "when planned_in_country_date is not NULL and planned_in_country_date <> ''",
                      "then ",
                      "date_trunc('month', try_cast(planned_in_country_date  as DATE )) ",
                      "else NULL",
                      "end"
                      ]
        sort_column_calc = " ".join(_temp_list)
    elif date_level == 'quarter':
        summary_date_column = 'fq'
        source_date_column = "concat(substr(planned_delivery_fiscal_quarter,1,4),'-Q',substr(planned_delivery_fiscal_quarter,6,2))"
        sort_date_column = 'fq'
        sort_column_calc = "concat(substr(planned_delivery_fiscal_quarter,1,4),'-Q',substr(planned_delivery_fiscal_quarter,6,2))"
    elif date_level == 'none':
        summary_date_column = 'fq'
        source_date_column = "concat(substr(planned_delivery_fiscal_quarter,1,4),'-Q',substr(planned_delivery_fiscal_quarter,6,2))"
        sort_date_column = 'fq'
        sort_column_calc = "concat(substr(planned_delivery_fiscal_quarter,1,4),'-Q',substr(planned_delivery_fiscal_quarter,6,2))"
    else:
        print("invalid date_level value of " + date_level)


    if by_country == "Yes":
        country_column_with_comma = "country_name,"
        country_column_no_comma = "country_name"
        group_by_intial = source_date_column + ", " + sort_column_calc + ",  " + "country_name "
        group_by = summary_date_column + ", date_for_sorting" + ", " + "country_name "
    else:
        country_column_with_comma = ''
        country_column_no_comma = ''
        group_by_intial = source_date_column + ", " + sort_column_calc
        group_by = summary_date_column + ", date_for_sorting"

    where_clause = " and source_system = '{}'".format(source_system)
    if year != 'ALL':
        where_clause = where_clause + " and planned_delivery_fiscal_year = '{}'".format(year)

    print("GROUP BY INITIAL " + group_by_intial)

    initial_summary_query_list = [
        "with",
        "INITIAL_SUMMARY ",
        "as",
        "(",
        "SELECT {} as {},".format(source_date_column, summary_date_column),
        "{} as date_for_sorting,".format(sort_column_calc),
        "{}".format(country_column_with_comma),
        "sum(cast(otd as decimal(12,2) ) )  as otd ,",
        "sum (cast(otd_lines as integer ) ) as otd_lines ,",
        "round(sum(cast(value_ordered as decimal(14,2)) ),2) as value ",
        "FROM datamart.order_line",
        "where otd_lines = '1' {}".format(where_clause),
        "group by ",
        "{}".format(group_by_intial),
        ")"
    ]

    otd_summmary_query_list = [
        ",",
        "OTD_SUMMARY",
        "as",
        "(  select ",
        "round( 100 * ( sum(cast(otd as decimal(12,2))) / sum(cast(otd_lines as decimal(12,2) )) ) ) as otd_pct , ",
        "sum(otd_lines) as otd_lines ,",
        "round(sum(value)) as value ,",
        "{}".format(country_column_with_comma),
        "{},".format(summary_date_column),
        "date_for_sorting",
        "from INITIAL_SUMMARY ",
        "group by ",
        "{}".format(group_by),
        ")"
    ]

    if rank == "No":

        rank_summmary_query_list = [
            "select {},".format(summary_date_column),
            "{}".format(country_column_with_comma),
            "otd_pct ,",
            "otd_lines ,",
            "value ,",
            "ROW_NUMBER ( ) ",
            "OVER ( PARTITION BY ",
            "{}".format(summary_date_column),
            "ORDER BY ",
            "{} , ".format(summary_date_column),
            "{}".format(country_column_with_comma),
            "otd_pct , ",
            "otd_lines  desc , ",
            "value desc",
            ") as otd_rank_order ",
            "from OTD_SUMMARY ",
            "order by  ",
            "date_for_sorting  , ",
            "otd_rank_order"
        ]

    else:

        rank_summmary_query_list = [" select * from OTD_SUMMARY"]

    print(" ".join(initial_summary_query_list) + " ".join(otd_summmary_query_list) + " ".join(rank_summmary_query_list))
    return " ".join(initial_summary_query_list) + " ".join(otd_summmary_query_list) + " ".join(rank_summmary_query_list)


def lambda_handler(event, context):
    print(event)
    account_id = boto3.client('sts').get_caller_identity()['Account']
    print("executing under account id ", account_id)

    account_id = boto3.client('sts').get_caller_identity()['Account']
    print("Running on Account", account_id)

    # results = get_athena_query_string_results_json ( build_country_by_query("GHSC-PSM-ARTMIS","2018")    )

    s3 = boto3.resource('s3')

    ghsc_psm_results = {};

    ghsc_psm_country_by_year = {};
    ghsc_psm_country_by_year['2015'] = get_athena_query_string_results_json(
        summarize_otd("year", "GHSC-PSM-ARTMIS", year="2015"))

    # ghsc_psm_country_by_year['2016']   = get_athena_query_string_results_json ( summarize_otd ( "year" , "GHSC-PSM-ARTMIS",  year = "2016" )  )
    # ghsc_psm_country_by_year['2017']   = get_athena_query_string_results_json ( summarize_otd ( "year" , "GHSC-PSM-ARTMIS",  year = "2017" )  )
    # ghsc_psm_country_by_year['2018']   = get_athena_query_string_results_json ( summarize_otd ( "year" , "GHSC-PSM-ARTMIS",  year = "2018" )  )
    # ghsc_psm_country_by_year['2019']   = get_athena_query_string_results_json ( summarize_otd ( "year" , "GHSC-PSM-ARTMIS",  year = "2019" )  )

    ghsc_psm_results['country_by_year'] = ghsc_psm_country_by_year

    ghsc_psm_results['country_by_month'] = get_athena_query_string_results_json(
        summarize_otd("month", "GHSC-PSM-ARTMIS", by_country="Yes", rank="Yes"))
    # ghsc_psm_results['country_by_fiscal_quarter']   = get_athena_query_string_results_json(summarize_otd ( "quarter" , "GHSC-PSM-ARTMIS", by_country = "Yes", rank = "Yes"  ) )
    # ghsc_psm_results['fiscal_quarter']   = get_athena_query_string_results_json(summarize_otd ( "quarter" , "GHSC-PSM-ARTMIS"  ) )
    # ghsc_psm_results['month']            = get_athena_query_string_results_json( summarize_otd( "month" , "GHSC-PSM-ARTMIS"  ) )
    # ghsc_psm_results['year']             = get_athena_query_string_results_json( summarize_otd ( "year" , "GHSC-PSM-ARTMIS"  ) )

    '''
    ghsc_psm_country_by_year['2015'] = get_athena_query_string_results_json ( build_country_by_year("GHSC-PSM-ARTMIS","2015")    ) 
    ghsc_psm_country_by_year['2016'] = get_athena_query_string_results_json ( build_country_by_year("GHSC-PSM-ARTMIS","2016")    ) 
    ghsc_psm_country_by_year['2017'] = get_athena_query_string_results_json ( build_country_by_year("GHSC-PSM-ARTMIS","2017")    ) 
    ghsc_psm_country_by_year['2018'] = get_athena_query_string_results_json ( build_country_by_year("GHSC-PSM-ARTMIS","2018")    ) 
    ghsc_psm_country_by_year['2019'] = get_athena_query_string_results_json ( build_country_by_year("GHSC-PSM-ARTMIS","2019")    ) 

    ghsc_psm_results['country_by_year'] = ghsc_psm_country_by_year 
    ghsc_psm_results['fiscal_quarter']  = get_athena_named_query_results_json('datamart_otd_quarter_ghsc_psm' )  
    ghsc_psm_results['month']           = get_athena_named_query_results_json('datamart_otd_month_ghsc_psm' )  
    ghsc_psm_results['year']            = get_athena_named_query_results_json('datamart_otd_year_ghsc_psm' )  


    #print ( get_athena_named_query_results_json('datamart_otd_year' )   )
    '''

    '''
    Save to JSON file to S3 Bucket 
    '''

    print("The reuslts are: ", ghsc_psm_results)
    # s3object = s3.Object('valkyrie-usaid-'+account_id+'-us-east-1', 'datamart/otd/json/ghsc_psm_otd.json')

    # print ( "THE JSON IS",  json.dumps(ghsc_psm_results,indent=4).encode('UTF-8') )

    # print ( "S3 PuT" , s3object.put(
    # Body=(bytes(json.dumps(ghsc_psm_results,indent=4).encode('UTF-8')))
    #       )   )

    # s3object.put(
    # Body=(bytes(json.dumps(ghsc_psm_results,indent=4).encode('UTF-8')))
    # )