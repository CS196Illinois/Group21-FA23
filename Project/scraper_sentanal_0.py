#!/usr/bin/env python
# coding: utf-8

#chatgpt told me to do this...
from pydantic_settings import BaseSettings

import streamlit as st

st.text('hello')
# In[ ]:


from distutils.sysconfig import get_python_inc
from sysconfig import get_python_version


#get_python_version().run_line_magic('pip', 'install obsei[all]')
#get_python_inc().run_line_magic('pip', 'install transformers')


# In[ ]:


import logging
import sys


# In[ ]:


from obsei.source.youtube_scrapper import YoutubeScrapperSource, YoutubeScrapperConfig
from obsei.analyzer.classification_analyzer import (
    ClassificationAnalyzerConfig,
    ZeroShotClassificationAnalyzer
)


# # PUT IN YOUTUBE VIDEO LINKS IN THE video_url VARIABLE BELOW

# In[ ]:


video_url = 'https://www.youtube.com/watch?v=IZXxSmbdsrw'


# In[ ]:


source_config = YoutubeScrapperConfig(
    video_url= video_url,
    fetch_replies=False,
    max_comments=50,
    lookup_period="1Y",
)

source = YoutubeScrapperSource()
source_response_list = source.lookup(source_config)
print(len(source_response_list))
print(type(source_response_list))

for idx, source_response in enumerate(source_response_list):
    print(f"source_response#'{idx}'='{source_response.__dict__}'")


# In[ ]:


text_analyzer = ZeroShotClassificationAnalyzer(
    model_name_or_path="typeform/mobilebert-uncased-mnli", device="auto"
)

analyzer_response_list = text_analyzer.analyze_input(
    source_response_list=source_response_list,
    analyzer_config=ClassificationAnalyzerConfig(
        labels=["positive", "negative"],
    ),
)

for idx, an_response in enumerate(analyzer_response_list):
    print(f"analyzer_response#'{idx}'='{an_response.__dict__}'")


# In[ ]:


from pandas import DataFrame
from obsei.sink.pandas_sink import PandasSink, PandasSinkConfig

sink_config = PandasSinkConfig(
   dataframe=DataFrame()
)
sink = PandasSink()
dataframe = sink.send_data(analyzer_response_list, sink_config)
dataframe


# In[ ]:


dataframe.loc[dataframe['segmented_data_classifier_data_negative'].astype('float')>0.5] #prints out all negative comments


# In[ ]:


dataframe[['segmented_data_classifier_data_negative']].astype('float').plot.bar() #plot of no of negative comments


# In[ ]:


dataframe.loc[dataframe['segmented_data_classifier_data_positive'].astype('float')>0.5] #prints out all positive comments


# In[ ]:


dataframe[['segmented_data_classifier_data_positive']].astype('float').plot.bar() #plot of positive comments


# In[ ]:




