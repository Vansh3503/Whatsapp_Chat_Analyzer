from urlextract import URLExtract
import pandas as pd
import re
from collections import Counter
from wordcloud import WordCloud
import emoji

extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

        # fetch no of messages
    num_messages = df.shape[0]
    # number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch no  of media
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    # FETCH NO OF LINK
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    def count_emojis(text):
        # Use a regular expression to match all emoji characters
        emojis = re.findall(r'[\U0001f600-\U0001f650]', text)
        return len(emojis)

    # Count the total number of emojis in all chats
    df['Emoji Count'] = df['message'].apply(count_emojis)
    total_emojis = df['Emoji Count'].sum()

    return num_messages, len(words), num_media_messages, len(links), total_emojis


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=""))
    return df_wc


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []
    for message in temp['message']:
        words.extend(message.split())

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


from collections import Counter

import emoji
from collections import Counter
import pandas as pd
from collections import Counter
import emoji

def emoji_helper(selected_user, df):
    try:
        if df is None:
            print("Input DataFrame is None.")
            return None

        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]

        emojis = []
        for message in df['message']:
            emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

        emoji_counts = Counter(emojis)
        emoji_df = pd.DataFrame(emoji_counts.most_common(len(emoji_counts)))

        # Debugging prints
        print("emoji_df:")
        print(emoji_df)

        return emoji_df
    except Exception as e:
        # Handle the specific exception or log the error for debugging
        print(f"Error in emoji_helper: {e}")
        return None



def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap= df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap





