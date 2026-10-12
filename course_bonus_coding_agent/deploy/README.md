---
title: "Desk Coder"
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: "6.30.0"
python_version: "3.12.12"
app_file: app.py
pinned: false
short_description: A small coding agent built in a notebook
---

# Desk Coder

A coding agent with three tools: it lists, reads, and edits files in its own workspace folder and nothing outside it. No tool runs code. It runs on an OpenAI model (`gpt-6.1-sol` unless the Space's OPENAI_MODEL variable names another); the key is a Space secret, never in these files. Every issuer, bond, and price in its workspace is fictional.

Built 2026-10-12 in the Bonus course of Python for Fixed Income, a course series. The idea comes from Thorsten Ball, "How to Build an Agent" (https://ampcode.com/notes/how-to-build-an-agent, April 15, 2025).

This course is educational content created in a personal capacity. Nothing here is investment advice or a recommendation to buy or sell any security. All portfolio data is synthetic.
