
CREATE_TABLES = '''

DROP TABLE IF EXISTS FACT_Search_Terms CASCADE;

CREATE TABLE FACT_Search_Terms AS
SELECT concat(ad_group_id, '_', campaign_id) AS search_term_key,
date,
ad_group_id,
campaign_id,
search_term,
SUM(clicks) AS clicks,
SUM(cost) AS cost,
SUM(conversion_value) AS conversion_value,
SUM(conversions) AS conversions,
COUNT(index) AS Records
FROM public.search_terms
GROUP BY date,
ad_group_id,
campaign_id,
search_term;
 
DROP TABLE IF EXISTS DIM_Campaigns CASCADE;

CREATE TABLE DIM_Campaigns AS
SELECT DISTINCT
Campaign_Id,
Structure_Value,
Status
FROM public.campaigns;

DROP TABLE IF EXISTS DIM_adgroups CASCADE;

CREATE TABLE DIM_adgroups AS
SELECT DISTINCT
concat(ad_group_id, '_', campaign_id) AS search_term_key,
ad_group_id,
Campaign_id,
status,
country,
priority,
_campaign_structure_value
FROM adgroups;


'''

CREATE_VIEWS = '''
DROP VIEW IF EXISTS ROAS_by_country_and_priority;

CREATE VIEW public.ROAS_by_country_and_priority
AS
SELECT 
dag.country,
dag.priority,
dca.structure_value,
SUM(fst.clicks) AS clicks,
SUM(fst.cost) AS cost,
SUM(fst.conversion_value) AS conversion_value,
SUM(fst.conversions) AS conversions,
SUM(fst.conversion_value)/NULLIF(SUM(fst.cost),0) AS ROAS
FROM public.fact_search_terms AS fst
INNER JOIN public.dim_adgroups AS dag
ON fst.search_term_key = dag.search_term_key
INNER JOIN public.dim_campaigns as dca
ON fst.campaign_id = dca.campaign_id
GROUP BY
dag.country,
dag.priority,
dca.structure_value;

DROP VIEW IF EXISTS ROAS_by_country;

CREATE VIEW public.ROAS_by_country
AS
SELECT 
dag.country,
dca.structure_value,
SUM(fst.clicks) AS clicks,
SUM(fst.cost) AS cost,
SUM(fst.conversion_value) AS conversion_value,
SUM(fst.conversions) AS conversions,
SUM(fst.conversion_value)/NULLIF(SUM(fst.cost),0) AS ROAS
FROM public.fact_search_terms AS fst
INNER JOIN public.dim_adgroups AS dag
ON fst.search_term_key = dag.search_term_key
INNER JOIN public.dim_campaigns as dca
ON fst.campaign_id = dca.campaign_id
GROUP BY
dag.country,
dca.structure_value;

DROP VIEW IF EXISTS ROAS_by_priority;

CREATE VIEW public.ROAS_by_priority
AS
SELECT 
dag.priority,
dca.structure_value,
SUM(fst.clicks) AS clicks,
SUM(fst.cost) AS cost,
SUM(fst.conversion_value) AS conversion_value,
SUM(fst.conversions) AS conversions,
SUM(fst.conversion_value)/NULLIF(SUM(fst.cost),0) AS ROAS
FROM public.fact_search_terms AS fst
INNER JOIN public.dim_adgroups AS dag
ON fst.search_term_key = dag.search_term_key
INNER JOIN public.dim_campaigns as dca
ON fst.campaign_id = dca.campaign_id
GROUP BY
dag.priority,
dca.structure_value;
'''
