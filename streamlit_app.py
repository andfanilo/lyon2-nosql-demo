import streamlit as st
import redis

r = redis.Redis(host='localhost', port=6379)

r.set('foo', 'bar')
value = r.get('foo')