#!/usr/bin/env python
from datetime import datetime
from youtube_yapper_trapper.crew import YoutubeCommentsCrew
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
import sys

load_dotenv()

# def extract_video_id(url):
#     """ Extracts video ID using URL parsing for reliability. """
#     query = urlparse(url).query
#     video_id = parse_qs(query).get('v')
#     if video_id:
#         return video_id[0]
#     return None

def extract_video_id(url):
    """
    Extracts the video ID from any form of YouTube URL (normal, shortened, embedded).
    """
    parsed_url = urlparse(url)
    
    if "youtu.be" in parsed_url.netloc:
        # Handles shortened URLs, e.g., https://youtu.be/tqcm8qByMp8
        video_id = parsed_url.path.split('/')[1]
    elif "youtube.com" in parsed_url.netloc and "/embed/" in parsed_url.path:
        # Handles embed URLs, e.g., https://www.youtube.com/embed/tqcm8qByMp8
        video_id = parsed_url.path.split('/')[2]
    else:
        # Handles normal YouTube URLs
        video_id = parse_qs(parsed_url.query).get('v')
        if video_id:
            video_id = video_id[0]
    
    return video_id

def get_formatted_datetime():
    """ Returns the current date and time formatted as a string. """
    return datetime.now().strftime("%Y-%m-%d_%H-%M")

def write_results_to_file(filename, content):
    """ Writes analysis results to a Markdown file. """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
        file.flush()

def run_analysis(video_id, url):
    """ Runs the crew for analyzing YouTube comments. """
    inputs = {"video_id": video_id, "url": url}
    crew = YoutubeCommentsCrew()
    result = crew.crew().kickoff(inputs=inputs)
    print("Analysis Result:")
    print(result)
    return result

def run():
    url = input("🚀 Enter YouTube URL: ")
    video_id = extract_video_id(url)
    if not video_id:
        print("🚨 Invalid YouTube URL provided.")
        return

    result = run_analysis(video_id, url)
    filename = f"Report_{get_formatted_datetime()}.md"
    write_results_to_file(filename, result)

if __name__ == "__main__":
    run()
