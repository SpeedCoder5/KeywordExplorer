import random
import time
import tkinter as tk
import tkinter.messagebox as message
from datetime import datetime, timedelta
from tkinter import filedialog

import pandas as pd

from keyword_explorer.Apps.AppBase import AppBase
from keyword_explorer.TwitterV2.TweetKeywords import TweetKeywords
from keyword_explorer.tkUtils.Buttons import Buttons
from keyword_explorer.tkUtils.Checkboxes import Checkboxes, DIR
from keyword_explorer.tkUtils.DataField import DataField
from keyword_explorer.tkUtils.DateEntryField import DateEntryField
from keyword_explorer.tkUtils.ListField import ListField
from keyword_explorer.tkUtils.TextField import TextField

from keyword_explorer.utils.MySqlInterface import MySqlInterface

from typing import Dict, List, Callable

class KeywordData:
    tweets_per_day:int
    name:str
    def __init__(self, name:str, tweets:int):
        self.reset(name, tweets)

    def reset(self, name:str, tweets:int):
        self.name = name
        self.tweets_per_day = tweets

    def to_string(self) -> str:
        return "{}: {:,}".format(self.name, self.tweets_per_day)

class TweetDownloader(AppBase):
    msi:MySqlInterface
    tkey:TweetKeywords
    prompt_text_field:TextField
    response_text_field:TextField
    keyword_text_field:TextField
    start_date_field:DateEntryField
    end_date_field:DateEntryField
    cur_date_field:DateEntryField
    duration_field:DataField
    samples_field:DataField
    corpus_size_field:DataField
    lowest_count_field:DataField
    highest_count_field:DataField
    option_checkboxes:Checkboxes
    keyword_data_list:List
    randomize:bool
    hour_offset:int


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword_data_list = []
        self.randomize = False
        self.hour_offset = 0 # offset from zulu
        print("TweetDownloader.init()")

    def setup_app(self):
        self.app_name = "TweetDownloader"
        self.app_version = "6.22.22"
        self.geom = (900, 530)
        self.console_lines = 10

        self.tkey = TweetKeywords()
        self.msi = MySqlInterface(user_name ="root", db_name ="twitter_v2")
        if not self.tkey.key_exists():
            message.showwarning("Key Error", "Could not find Environment key 'BEARER_TOKEN_2'")

    def build_app_view(self, row:int, main_text_width:int, main_label_width:int) -> int:
        param_text_width = 20
        param_label_width = 15
        row += 1
        lf = tk.LabelFrame(self, text="Twitter")
        lf.grid(row=row, column=0, columnspan = 2, sticky="nsew", padx=5, pady=2)
        self.build_twitter(lf, main_text_width, main_label_width)

        lf = tk.LabelFrame(self, text="Twitter Params")
        lf.grid(row=row, column=2, columnspan = 2, sticky="nsew", padx=5, pady=2)
        self.build_twitter_params(lf, param_text_width, param_label_width)

        self.end_date_field.set_date()
        day_delta = 2
        self.start_date_field.set_date(d = (datetime.utcnow() - timedelta(days=day_delta)))
        self.cur_date_field.set_date(d = (datetime.utcnow() - timedelta(days=day_delta)))
        self.duration_field.set_text(day_delta)

        return row+1

    def build_twitter(self, lf:tk.LabelFrame, text_width:int, label_width:int):
        row = 0
        self.keyword_text_field = TextField(lf, row, 'Test Keyword(s)', text_width, height=10, label_width=label_width)
        row = self.keyword_text_field.get_next_row()
        self.start_date_field = DateEntryField(lf, row, 'Start Date', text_width, label_width=label_width)
        row = self.start_date_field.get_next_row()
        self.end_date_field = DateEntryField(lf, row, 'End Date', text_width, label_width=label_width)
        row = self.end_date_field.get_next_row()
        self.duration_field = DataField(lf, row, 'Duration:', int(text_width/2), label_width=label_width)
        self.duration_field.add_button("set start", self.set_start_callback)
        self.duration_field.add_button("set end", self.set_end_callback)
        row = self.duration_field.get_next_row()
        buttons = Buttons(lf, row, "Actions", label_width=label_width)
        buttons.add_button("Calc rates", self.calc_rates_callback)
        buttons.add_button("Balanced", self.collect_balanced_callback)
        buttons.add_button("Unbalanced", self.implement_me)
        buttons.add_button("Launch Twitter", self.launch_twitter_callback)
        row = buttons.get_next_row()

    def build_twitter_params(self, lf:tk.LabelFrame, text_width:int, label_width:int):
        row = 0
        self.samples_field = DataField(lf, row, 'Samples (10 - 500):', text_width, label_width=label_width)
        self.samples_field.set_text('100')
        row = self.samples_field.get_next_row()

        self.option_checkboxes = Checkboxes(lf, row, "Options", label_width=label_width)
        self.option_checkboxes.add_checkbox("Randomize", self.randomize_callback, dir=DIR.ROW)
        self.option_checkboxes.add_checkbox("Stream to DB", self.implement_me, dir=DIR.ROW)
        self.option_checkboxes.add_checkbox("Stream to CSV", self.implement_me, dir=DIR.ROW)
        row = self.option_checkboxes.get_next_row()

        self.corpus_size_field = DataField(lf, row, 'Corpus Size:', text_width, label_width=label_width)
        self.corpus_size_field.set_text('500000')
        row = self.corpus_size_field.get_next_row()

        self.lowest_count_field = DataField(lf, row, 'Lowest/Day:', text_width, label_width=label_width)
        self.lowest_count_field.set_text('0')
        row = self.lowest_count_field.get_next_row()

        self.highest_count_field = DataField(lf, row, 'Highest/Day:', text_width, label_width=label_width)
        self.highest_count_field.set_text('0')
        row = self.highest_count_field.get_next_row()

        self.cur_date_field = DateEntryField(lf, row, 'Cur Date', text_width, label_width=label_width)
        row = self.cur_date_field.get_next_row()

    def randomize_callback(self):
        self.randomize = not self.randomize
        # print("self.randomize = {}".format(self.randomize))

    def set_start_callback(self):
        duration = int(self.duration_field.get_text())
        end_dt = self.end_date_field.get_date()
        start_dt = end_dt - timedelta(days= duration)
        self.start_date_field.set_date(start_dt)
        self.cur_date_field.set_date(start_dt)

    def set_end_callback(self):
        duration = int(self.duration_field.get_text())
        start_dt = self.start_date_field.get_date()
        end_dt = start_dt + timedelta(days = duration)
        self.end_date_field.set_date(end_dt)

    def collect_balanced_callback(self):
        rand_min = 0
        date_fmt = "%B %d, %Y (%H:%M:%S)"
        num_samples = self.samples_field.get_as_int()

        key_list = self.keyword_text_field.get_list("\n")
        cur_dt = self.start_date_field.get_date()
        end_dt = self.end_date_field.get_date()
        sql = "insert into table_experiment (name, date) values (%s, %s)"
        values = (self.experiment_field.get_text(), datetime.now())
        experiment_id = self.msi.write_sql_values_get_row(sql, values)

        while cur_dt < end_dt:
            max_end = cur_dt + timedelta(days=1)
            print("\n{}".format(cur_dt.strftime(date_fmt)))
            # first, get the counts for each keyword
            self.keyword_data_list = []
            for s in key_list:
                count = self.tkey.get_keywords_per_day(s, cur_dt)
                self.keyword_data_list.append(KeywordData(s, count))
            self.keyword_data_list.sort(key=lambda kd:kd.tweets_per_day)

            time.sleep(1)
            if self.randomize:
                rand_min = random.randint(0, 59)

            #get the tweets based on the lowest counts
            kd:KeywordData
            min_kd:KeywordData = self.keyword_data_list[0]

            if min_kd.tweets_per_day < num_samples: # make a new sample size that's at least 10
                num_samples = max(10, min_kd.tweets_per_day)

            for kd in self.keyword_data_list:
                if kd.tweets_per_day <= num_samples:
                    sample_mult = 1
                    # get the dates we're going to collect
                    cur_start = cur_dt
                    cur_end = max_end

                    #show the date we are collecting for
                    print("{} collecting all {:,} of {:,} tweets".format(kd.name, num_samples*sample_mult, kd.tweets_per_day))
                    print("\tcollecting all from {} to {}".format(cur_start.strftime(date_fmt), cur_end.strftime(date_fmt)))

                else:
                    if self.randomize or num_samples == min_kd.tweets_per_day:
                        # Make one random sample in the day
                        ratio = min_kd.tweets_per_day / kd.tweets_per_day
                        if self.randomize:
                            ratio = num_samples / kd.tweets_per_day
                        day_offset = random.random() * (1.0 - 2*ratio)
                        cur_start = cur_dt + timedelta(days=day_offset)
                        cur_end = cur_start + timedelta(days=ratio)
                        print("{}: Randomly choosing {}/{} from {} to {}".format(kd.name, num_samples, kd.tweets_per_day, cur_start.strftime(date_fmt), cur_end.strftime(date_fmt)))
                    else:
                        # Make several samples across the day
                        day_frac = num_samples / min_kd.tweets_per_day
                        sample_mult = 1/day_frac

                        #show the date we are collecting for
                        print("{} subsampling {:,} of {:,} tweets".format(kd.name, num_samples*sample_mult, kd.tweets_per_day))
                        total_frac = 0
                        count = 0
                        while total_frac < 1.0:
                            # get the dates we're going to collect
                            cur_start = cur_dt + timedelta(days=(count * day_frac))
                            total_frac = min(1.0, (count+1) * day_frac)
                            cur_end = cur_dt + timedelta(days=total_frac)
                            print("\tsubsampling {} from {} to {}".format(num_samples, cur_start.strftime(date_fmt), cur_end.strftime(date_fmt)))
                            count += 1


                #figure out the best spacing of samples across the day

            self.cur_date_field.set_date(cur_dt)
            self.cur_date_field.update()
            # next day
            cur_dt += timedelta(days=1)


        print("collect_individual_callback(): done")


    def calc_rates_callback(self):
        corpus_size = int(self.corpus_size_field.get_text())
        key_list = self.keyword_text_field.get_list("\n")
        start_dt = self.start_date_field.get_date()
        i = 0
        highest = KeywordData("unset", 0)
        lowest = KeywordData("unset", 0)
        self.dp.clear()
        self.keyword_data_list = []
        for s in key_list:
            count = self.tkey.get_keywords_per_day(s, start_dt)
            if count == 0:
                self.dp.dprint("{}: {:,} SKIPPING".format(s, count))
                continue
            self.keyword_data_list.append(KeywordData(s, count))
            if i == 0:
                lowest.reset(s, count)
                highest.reset(s, count)
            else:
                if count < lowest.tweets_per_day:
                    lowest.reset(s, count)
                elif count > highest.tweets_per_day:
                    highest.reset(s, count)
            self.dp.dprint("[{}]: {:,} keywords/day = {:.1f} days for {}k ".format(s, count, corpus_size/count+1, corpus_size/1000))
            i += 1
        self.highest_count_field.set_text(highest.to_string())
        self.lowest_count_field.set_text(lowest.to_string())

        # sort the list from lowest to highest
        kd:KeywordData
        self.keyword_data_list.sort(key=lambda kd:kd.tweets_per_day)
        for kd in self.keyword_data_list:
            print(kd.to_string())

    def launch_twitter_callback(self):
        # single word
        key_list = self.keyword_text_field.get_list("\n")
        start_dt = self.start_date_field.get_date()
        end_dt = self.end_date_field.get_date()
        self.log_action("Launch_twitter", {"twitter_start": start_dt.strftime("%Y-%m-%d"), "twitter_end":end_dt.strftime("%Y-%m-%d"), "terms":" ".join(key_list)})
        self.tkey.launch_twitter(key_list, start_dt, end_dt)
        # webbrowser.open('https://twitter.com/search?q=chinavirus%20until%3A2020-02-01%20since%3A2019-12-01&src=typed_query')
        # webbrowser.open('https://twitter.com/search?q=%22china%20virus%22%20until%3A2020-02-01%20since%3A2019-12-01&src=typed_query')

    def set_time_sample_callback(self, event:tk.Event = None):
        sample_str = self.sample_list.get_selected()
        self.sample_list.set_label("Sample\n({})".format(sample_str))

    def clean_list_text(self, s:str) -> str:
        """
        Convenience method to clean up list-style text. Useful for a good chunk of the GPT-3 responses for
        the style of prompt that I've been using
        :param s: The string to clean up
        :return: The cleaned-up string
        """
        lines = s.split("\n")
        line:str
        par =""
        for line in lines:
            s = line.strip()
            if s != "":
                par = "{}\n{}".format(par, s)
        return par.strip()


def main():
    app = TweetDownloader()
    app.mainloop()

if __name__ == "__main__":
    main()