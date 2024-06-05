from typing import List

import yagooglesearch
from pydantic import BaseModel


class OutreachSearchResult(BaseModel):
    rank: int
    title: str
    description: str
    url: str


async def get_google_search(query: str, max_search: int = 5):
    client = yagooglesearch.SearchClient(
        query,
        tbs="li:1",
        max_search_result_urls_to_return=max_search,
        http_429_cool_off_time_in_minutes=5,
        http_429_cool_off_factor=1.5,
        # proxy="socks5h://127.0.0.1:9050",
        verbosity=5,
        verbose_output=True,  # False (only URLs) or True (rank, title, description, and URL)
    )
    client.assign_random_user_agent()
    urls = client.search()

    search_response: List[OutreachSearchResult] = []
    for u in urls:
        search_response.append(OutreachSearchResult.model_validate(u))
    return search_response


async def get_search_template(query: str, max_search: int = 5):
    urls = [
        {
            "rank": 1,
            "title": "How to Vlog: A Beginner’s Guide to Vlogging",
            "description": "Vlogging is the new normal. Toddlers are doing it, teenagers are doing it, moms are doing it, industry experts are doing it… It’s kind of like kung-fu fighting back in 1974, according to Carl Douglas. But what exactly does it take to learn how to vlog? Is there a school of vlogging you should attend",
            "url": "https://www.wix.com/blog/photography/how-to-vlog",
        },
        {
            "rank": 2,
            "title": "How to start a vlog: everything you need to know",
            "description": "What makes a good video vlog? · Develop a niche. · Identify and speak to your target audience. · Deliver value. · Maintain pro video quality. · Be distinctive.",
            "url": "https://www.adobe.com/express/learn/blog/how-to-start-a-vlog",
        },
        {
            "rank": 3,
            "title": "How to Make a Vlog in 5 Easy Steps",
            "description": "JA great first vlog to create is a video telling your followers all about you. Explain who you are and where you came from, share your likes and",
            "url": "https://animoto.com/blog/video-tips/how-to-make-a-vlog",
        },
        {
            "rank": 4,
            "description": "The ultimate guide to vlog editing for beginners",
            "title": "How to edit a vlog with Clipchamp · Step 1. Upload your video clips · Step 2. Trim and enhance your video clips · Step 3. Edit the audio of your",
            "url": "https://clipchamp.com/en/blog/ultimate-guide-vlog-editing/",
        },
    ]
    search_response: List[OutreachSearchResult] = []
    for u in urls[0 : min(len(urls), max_search)]:
        search_response.append(OutreachSearchResult.model_validate(u))

    return search_response
