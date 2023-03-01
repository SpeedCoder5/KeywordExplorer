import re
import pandas as pd
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as message

from keyword_explorer.tkUtils.Buttons import Buttons
from keyword_explorer.tkUtils.TextField import TextField
from keyword_explorer.tkUtils.DataField import DataField
from keyword_explorer.tkUtils.Checkboxes import Checkboxes, Checkbox
from keyword_explorer.tkUtils.TopicComboExt import TopicComboExt
from keyword_explorer.tkUtils.ToolTip import ToolTip
from keyword_explorer.tkUtils.GPT3GeneratorFrame import GPT3GeneratorFrame, GPT3GeneratorSettings
from keyword_explorer.OpenAI.OpenAIEmbeddings import OpenAIEmbeddings

from typing import List, Dict, Callable

class GPTContextSettings:
    prompt: str
    context_prompt:str
    keywords:str
    def __init__(self, prompt = "unset", context_prompt = "unset", keywords = "unset"):
        self.prompt = prompt
        self.context_prompt = context_prompt
        self.keywords = keywords

    def from_dict(self, d:Dict):
        if 'prompt' in d:
            self.prompt = d['prompt']
        if 'context_prompt' in d:
            self.context_prompt = d['context_prompt']
        if 'keywords' in d:
            self.keywords = d['keywords']


    def to_dict(self) -> Dict:
        return {'prompt':self.prompt,
                'context_prompt':self.context_prompt,
                'keywords':self.keywords}


class GPTContextFrame(GPT3GeneratorFrame):
    keyword_filter:DataField
    context_prompt:DataField
    context_text_field:TextField
    prompt_query_cb:Checkbox
    project_df:pd.DataFrame

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project_df = pd.DataFrame()

    def build_frame(self, frm: ttk.Frame, text_width:int, label_width:int):
        row = 0

        self.keyword_filter = DataField(frm, row, "Keywords:", text_width+20, label_width=label_width)
        self.keyword_filter.set_text("Pequod OR Rachel OR Ahab")
        ToolTip(self.keyword_filter.tk_entry, "Keywords (separated by OR) to filter available data")
        row = self.keyword_filter.get_next_row()

        self.context_prompt = DataField(frm, row, "Context:", text_width+20, label_width=label_width)
        self.context_prompt.set_text("Working on whaling ships")
        ToolTip(self.context_prompt.tk_entry, "The prompt that will provide context")
        row = self.context_prompt.get_next_row()

        self.prompt_text_field = TextField(frm, row, "Prompt:", text_width, height=1, label_width=label_width)
        self.prompt_text_field.set_text("Why is Ahab obsessed with Moby Dick?")
        ToolTip(self.prompt_text_field.tk_text, "The prompt that the GPT will use to generate text from")
        row = self.prompt_text_field.get_next_row()

        cboxes = Checkboxes(frm, row, "Options")
        self.prompt_query_cb = cboxes.add_checkbox("Use Prompt for context", self.handle_checkboxes)
        self.prompt_query_cb.set_val(False)
        row = cboxes.get_next_row()

        # Add the tabs
        tab_control = ttk.Notebook(frm)
        tab_control.grid(column=0, row=row, columnspan=2, sticky="nsew")
        gen_tab = ttk.Frame(tab_control)
        tab_control.add(gen_tab, text='Generated')

        ctx_tab = ttk.Frame(tab_control)
        tab_control.add(ctx_tab, text='Context')

        self.response_text_field = TextField(gen_tab, row, 'Response:', text_width, height=11, label_width=label_width)
        ToolTip(self.response_text_field.tk_text, "The response from the GPT will be displayed here")

        self.context_text_field = TextField(ctx_tab, row, 'Context:', text_width, height=11, label_width=label_width)
        ToolTip(self.context_text_field.tk_text, "The context including the prompt")

        row = self.response_text_field.get_next_row()

        self.buttons = Buttons(frm, row, "Actions")
        b = self.buttons.add_button("Ask Question", self.new_prompt_callback, width=-1)
        ToolTip(b, "Gets answer from the GPT")
        b = self.buttons.add_button("Summarize", self.get_summmary_callback, width=-1)
        ToolTip(b, "Gets Summary from the GPT")
        b = self.buttons.add_button("Narrative", self.get_story_callback, width=-1)
        ToolTip(b, "Gets Story from the GPT")
        b = self.buttons.add_button("Extend", self.extend_callback, width=-1)
        ToolTip(b, "Extends the GPT's response")

    def set_project_dataframe(self, df:DataField):
        self.project_df = df

    def handle_checkboxes(self, event = None):
        print("prompt_query_cb = {}".format(self.prompt_query_cb.get_val()))

    def new_prompt_callback(self):
        if self.project_df.empty:
            tk.messagebox.showwarning("Warning!", "Please import data first")
            return
        oae = OpenAIEmbeddings()
        ctx_question = self.context_prompt.get_text()
        if self.prompt_query_cb.get_val():
            ctx_question = self.prompt_text_field.get_text()
        context = oae.create_context(ctx_question, self.project_df)

        question = self.prompt_text_field.get_text()
        full_question = oae.create_question(question=question, context=context)

        self.context_text_field.clear()
        self.context_text_field.set_text(full_question)

        self.dp.dprint("Submitting Question: {}".format(question))
        answer = oae.get_response(full_question)
        self.response_text_field.set_text(answer)

    def get_summmary_callback(self):
        if self.project_df.empty:
            tk.messagebox.showwarning("Warning!", "Please import data first")
            return
        oae = OpenAIEmbeddings()
        ctx_prompt = self.context_prompt.get_text()
        if self.prompt_query_cb.get_val():
            ctx_prompt = self.prompt_text_field.get_text()
        context = oae.create_context(ctx_prompt, self.project_df)

        question = self.prompt_text_field.get_text()
        full_prompt = oae.create_summary(context=context)

        self.context_text_field.clear()
        self.context_text_field.set_text(full_prompt)

        self.dp.dprint("Submitting summary prompt: {}".format(context))
        answer = oae.get_response(full_prompt, max_tokens=256)
        self.response_text_field.set_text(answer)

    def get_story_callback(self):
        if self.project_df.empty:
            tk.messagebox.showwarning("Warning!", "Please import data first")
            return
        oae = OpenAIEmbeddings()
        ctx_prompt = self.context_prompt.get_text()
        if self.prompt_query_cb.get_val():
            ctx_prompt = self.prompt_text_field.get_text()
        context = oae.create_context(ctx_prompt, self.project_df)

        prompt = self.prompt_text_field.get_text()
        full_prompt = oae.create_narrative(prompt=prompt, context=context)

        self.context_text_field.clear()
        self.context_text_field.set_text(full_prompt)

        self.dp.dprint("Submitting story prompt: {}".format(prompt))
        answer = oae.get_response(full_prompt, max_tokens=256)
        self.response_text_field.set_text(answer)

    def extend_callback(self):
        if self.project_df.empty:
            tk.messagebox.showwarning("Warning!", "Please import data first")
            return
        oae = OpenAIEmbeddings()
        prompt = "{} {}".format(self.prompt_text_field.get_text(), self.response_text_field.get_text())
        self.prompt_text_field.clear()
        self.prompt_text_field.set_text(prompt)
        self.response_text_field.clear()
        self.dp.dprint("Submitting extend prompt:")
        response = oae.get_response(prompt)
        self.response_text_field.set_text(response)

    def set_params(self, settings:GPTContextSettings):
        self.prompt_text_field.clear()
        self.context_prompt.clear()
        self.keyword_filter.clear()

        self.prompt_text_field.set_text(settings.prompt)
        self.context_prompt.set_text(settings.context_prompt)
        self.keyword_filter.set_text(settings.keywords)

    def get_settings(self) -> GPTContextSettings:
        gs = GPTContextSettings()
        gs.prompt = self.prompt_text_field.get_text()
        gs.context_prompt = self.context_prompt.get_text()
        gs.keywords = self.keyword_filter.get_text()
        return gs
