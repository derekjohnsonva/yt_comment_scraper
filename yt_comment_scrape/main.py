#!/usr/bin/env python3
"""
This gets all of the comments from all of the youtube videos on a channel.
Version: 1.0
Python 3.10+
Date created: 2024-01-06 
Date modified: -pip
"""
# import os
import xml.etree.ElementTree as ET

import googleapiclient.discovery
from googleapiclient.errors import HttpError
from secrets import youtube_api_key

CHANNEL_ID = 'UCeQhm8DwHBg_YEYY0KGM1GQ'


def get_video_ids(youtube, channel_id):
    # Use the search endpoint to get video details based on the channel ID
    next_page_token = None
    video_ids = []

    try:
        while True:
            request = youtube.search().list(
                part='id',
                channelId=channel_id,
                type='video',
                maxResults=50,  # Adjust as needed
                pageToken=next_page_token
            )

            response = request.execute()

            for item in response['items']:
                video_ids.append(item['id']['videoId'])

            next_page_token = response.get('nextPageToken')

            if not next_page_token:
                break

    except HttpError as e:
        print(f"An error occurred: {e}")
        return None
    return video_ids


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = youtube_api_key

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    video_ids = get_video_ids(youtube, CHANNEL_ID)
    print(f"Found {len(video_ids)} videos")
    comment_threads = []
    for video_id in video_ids:
        try:
            next_page_token = None
            while True:
                request = youtube.commentThreads().list(
                    part="snippet,replies",
                    videoId=video_id,
                    pageToken=next_page_token
                )

                response = request.execute()
                comment_threads += response['items']
                next_page_token = response.get('nextPageToken')
                # TODO: remove this break statement to get all comments
                if not next_page_token:
                    break

        except HttpError as e:
            print(f"An error occurred: {e}")
            continue
    print(f"Found {len(comment_threads)} comments")
    # write comments to file
    # Create the XML structure
    root = ET.Element("comments")
    for comment_thread in comment_threads:
        comment_element = ET.SubElement(root, "comment")
        video_id = ET.SubElement(comment_element, "videoId")
        video_id.text = comment_thread["snippet"]["videoId"]
        author_id = ET.SubElement(comment_element, "authorChannelId")
        author_id.text = comment_thread["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]["value"]
        text_display = ET.SubElement(comment_element, "textDisplay")
        text_display.text = comment_thread["snippet"]["topLevelComment"]["snippet"]["textDisplay"]

        if "replies" in comment_thread:
            replies_element = ET.SubElement(comment_element, "replies")
            for reply in comment_thread["replies"]["comments"]:
                reply_element = ET.SubElement(replies_element, "reply")
                reply_author_id = ET.SubElement(
                    reply_element, "authorChannelId")
                reply_author_id.text = reply["snippet"]["authorChannelId"]["value"]
                reply_text_display = ET.SubElement(
                    reply_element, "textDisplay")
                reply_text_display.text = reply["snippet"]["textDisplay"]

    # Create an ElementTree object
    tree = ET.ElementTree(root)

    # Write the XML structure to a file
    tree.write("comment_data.xml", encoding="utf-8", xml_declaration=True)
    print("Comment data has been written to 'comment_data.xml' successfully.")


if __name__ == "__main__":
    main()
