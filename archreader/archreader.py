from reader import make_reader
from rich import print
import argparse
import os
import re


def init(rss_reader):
    rss_reader.add_feed("https://archlinux.org/feeds/news?format=rss")


def message_formater(entry):
    title = entry.title
    time = str(entry.last_updated).split(".")[0]
    sumarry = entry.summary
    sumarry = re.sub("</p>", "\n", sumarry)
    sumarry = re.sub("<p>", "", sumarry)
    sumarry = re.sub("</a>", "[/blue]", sumarry)
    sumarry = re.sub("<a..*>", "[blue]", sumarry)
    sumarry = re.sub("</h..*>", "[/bold]", sumarry)
    sumarry = re.sub("<h..*>", "[bold]", sumarry)
    sumarry = re.sub("<pre><code>", "", sumarry)
    sumarry = re.sub("</code></pre>", "", sumarry)
    message = f"""
last updated at [red]{time}[/red]
[bold]{title}[/bold]
{sumarry}
    """
    return message


def get_latest(rss_reader):
    enteries = list(rss_reader.get_entries())
    num_entries = len(enteries)
    for i in range(1, num_entries):
        rss_reader.mark_as_read(enteries[i])
    entry = enteries[0]
    message = message_formater(entry)
    print(message)


def get_all(rss_reader):
    enteries = list(rss_reader.get_entries())
    num_entries = len(enteries)
    count = 1
    for entry in enteries:
        rss_reader.mark_as_read(entry)
        message = message_formater(entry)
        print(f"{count}/{num_entries}")
        print(message)
        count += 1


def start(all):
    if os.path.exists("db.sqlite") == False:
        rss_reader = make_reader("db.sqlite")
        init(rss_reader)
    else:
        rss_reader = make_reader("db.sqlite")
    rss_reader.update_feeds()
    if all == True:
        get_all(rss_reader)
    else:
        get_latest(rss_reader)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--all",
        action="store_true",
        help="show all of the data stored from the archlinux rss feed",
    )
    args = parser.parse_args()
    start(args.all)
