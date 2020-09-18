from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results

# load_credentials(filename="/Users/xuefeiliu/Documents/Github/411github/cs562project/twitterproj/twitter_keys.yaml",
#                  yaml_key="search_tweets_30_day_dev",
#                  env_overwrite=False)



premium_search_args = load_credentials("/Users/xuefeiliu/Documents/Github/411github/cs562project/twitterproj/twitter_keys.yaml",
                                       yaml_key="search_tweets_premium",
                                       env_overwrite=False)

rule = gen_rule_payload("beyonce", results_per_call=100) # testing with a sandbox account
print(rule) 

tweets = collect_results(rule,
                         max_results=100,
                         result_stream_args=premium_search_args)
[print(tweet.all_text, end='\n\n') for tweet in tweets[0:10]];
