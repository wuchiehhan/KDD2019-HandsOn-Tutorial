# Databricks notebook source
# MAGIC %run "./TutorialClasses"

# COMMAND ----------

# Azure Storage account name
MagAccount = 'kdd2019magstore'

# MAG container name
MagContainer = 'mag-2019-06-07'

# Shared access signature of MAG Container
MagSAS = ''

# COMMAND ----------

mag = MicrosoftAcademicGraph(container=MagContainer, account=MagAccount, sas=MagSAS)
Affiliations = mag.getDataframe('Affiliations')
ConferenceSeries = mag.getDataframe('ConferenceSeries')
FieldsOfStudy = mag.getDataframe('FieldsOfStudy')
Journals = mag.getDataframe('Journals')

# COMMAND ----------

# Affiliation Similarity
ResourcePath = 'ns/AffiliationEmbedding_d100.tsv'
ns = NetworkSimilarity(resource=ResourcePath, container=MagContainer, account=MagAccount, sas=MagSAS)
df = ns.getDataframe()
display(df)

# COMMAND ----------

id1 = 1290206253 # Microsoft
id2 = 136199984 # Harvard University
print(ns.getSimilarity(id1, id2))

# COMMAND ----------

topEntities = ns.getTopEntities(id1)
topEntitiesWithName = topEntities.join(Affiliations, topEntities.EntityId == Affiliations.AffiliationId, 'inner') \
    .select(Affiliations.AffiliationId, Affiliations.DisplayName, topEntities.EntityType, topEntities.Score)
display(topEntitiesWithName)

# COMMAND ----------

# Venues
ResourcePath = 'ns/VenueEmbedding_d100.tsv'
ns = NetworkSimilarity(resource=ResourcePath, container=MagContainer, account=MagAccount, sas=MagSAS)
df = ns.getDataframe()
#display(df)

# COMMAND ----------

id1 = 1130985203 # KDD
id2 = 137773608 # Nature
print(ns.getSimilarity(id1, id2))

# COMMAND ----------

topEntities = ns.getTopEntities(id1)
display(topEntities)

# COMMAND ----------

# Union conferences and journals to get venue dataframe
conf = ConferenceSeries.select(ConferenceSeries.ConferenceSeriesId.alias('VenueId'), ConferenceSeries.NormalizedName, ConferenceSeries.DisplayName)
jour = Journals.select(Journals.JournalId.alias('VenueId'), Journals.NormalizedName, Journals.DisplayName)
venues = conf.union(jour)

# COMMAND ----------

topEntities = ns.getTopEntities(id1)
topEntitiesWithName = topEntities.join(venues, topEntities.EntityId == venues.VenueId, 'inner') \
    .select(venues.VenueId, venues.NormalizedName, venues.DisplayName, topEntities.EntityType, topEntities.Score)
display(topEntitiesWithName)

# COMMAND ----------

# Fields of Study
ResourcePath = 'ns/FosEmbedding_d100.tsv'
ns = NetworkSimilarity(resource=ResourcePath, container=MagContainer, account=MagAccount, sas=MagSAS)
df = ns.getDataframe()

# COMMAND ----------

id1 = 124101348 # Data mining
id2 = 108583219 # Deep learning
print(ns.getSimilarity(id1, id2))

# COMMAND ----------

topEntities = ns.getTopEntities(id1)
topEntitiesWithName = topEntities.join(FieldsOfStudy, topEntities.EntityId == FieldsOfStudy.FieldOfStudyId, 'inner') \
    .select(FieldsOfStudy.FieldOfStudyId, FieldsOfStudy.DisplayName, topEntities.EntityType, topEntities.Score)
display(topEntitiesWithName)
