# YouTube Comment Scrape

Running `main.py` will get all of the comments from the Tunadorable youtube channel and put them in a file called
`comment_data.xml`

running the cells in `explore.ipynb` will filter the comment threads to only threads in which the account owner
commented. The filtered data will be put in `filtered_comments.xml`.

The format for the xml is as follows

```xml
<comments>
    <comment>
        <videoId> The id of the video the comment was left under
        <authorChannelId> the id of the channel that left the top level comment
        <textDisplay> the text of the top level comment
        <replies> This is a optional field
            <reply> There can be many replies
                <authorChannelId> the id of the channel that left the reply
                <textDisplay> the text of the reply
            </reply>
        </replies>
    </comment>
</comments>
```

## Getting ChannelIDs

If you want to run this on other channels, you will need to find their specific channel ID.

[This](https://www.youtube.com/watch?v=0oDy2sWPF38) video seems to do the best job explaining how to find it
