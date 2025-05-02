import streamlit as st
import locale
import time
import re


def remove_chars(string):
    result = re.sub(r'\D', '', string)
    return result

def format_brl(raw: str) -> str:
        digits = remove_chars(raw)
        if not digits:
            return ""
        value = float(digits) / 100
        return locale.currency(value, grouping=True)


def make_on_change(key):
        def callback():
            st.session_state[key] = format_brl(st.session_state[key])
        return callback


def coalesce(first, second):
      if first is not None and first != '' and first != 0 :
          return first
      else:
          return second 

def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.01)

def build_string(text, value):
     string = text + ' ' + value
     yield stream_data(string)