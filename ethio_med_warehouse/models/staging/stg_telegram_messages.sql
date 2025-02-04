-- models/staging/stg_telegram_messages.sql
SELECT
    message_id,
    channel_title,
    channel_username,
    message,
    message_date,
    media_path,
    emoji_used,
    youtube_links
FROM {{ source('telegram_data', 'telegram_messages') }} WHERE message_date IS NOT NULL
